from django.db import transaction
from .models import Prediction, UserScore, PointConfig, Match, AdminLog


# Mapa de resultado del partido → elección correcta del usuario
_WINNER_TO_CHOICE = {
    Match.HOME: Prediction.HOME_WIN,
    Match.DRAW: Prediction.DRAW,
    Match.AWAY: Prediction.AWAY_WIN,
}

_PLAYOFF_PHASES = {
    Match.ROUND_OF_32, Match.ROUND_OF_16, Match.QUARTERFINAL,
    Match.SEMIFINAL, Match.THIRD_PLACE, Match.FINAL,
}


def qualify_predictions(match):
    """Califica todas las predicciones de un partido FINISHED dentro de una transacción."""
    if not match.winner:
        return

    correct_choice = _WINNER_TO_CHOICE.get(match.winner)
    is_playoff = match.phase in _PLAYOFF_PHASES

    try:
        points_for_phase = PointConfig.objects.get(phase=match.phase).points
    except PointConfig.DoesNotExist:
        points_for_phase = 0

    with transaction.atomic():
        predictions = list(
            Prediction.objects.filter(match=match).select_related('user')
        )
        to_update = []

        for pred in predictions:
            if pred.is_locked and pred.result == Prediction.PENDING:
                pred.result = Prediction.NULL
            elif pred.choice == correct_choice:
                pred.result = Prediction.CORRECT
            else:
                pred.result = Prediction.INCORRECT
            to_update.append(pred)

        Prediction.objects.bulk_update(to_update, ['result'])

        # Actualizar UserScore por usuario
        for pred in to_update:
            score, _ = UserScore.objects.get_or_create(user=pred.user)
            if pred.result == Prediction.CORRECT:
                score.total_points += points_for_phase
                score.correct_predictions += 1
                if is_playoff:
                    score.playoff_correct += 1
            elif pred.result == Prediction.INCORRECT:
                score.incorrect_predictions += 1
            elif pred.result == Prediction.NULL:
                score.null_predictions += 1
            score.save()


def recalculate_all_scores():
    """Recalcula todos los puntajes desde cero."""
    with transaction.atomic():
        UserScore.objects.all().delete()
        Prediction.objects.filter(
            match__status=Match.FINISHED
        ).update(result=Prediction.PENDING, is_locked=False)

        finished = Match.objects.filter(status=Match.FINISHED).order_by('match_date')
        for match in finished:
            qualify_predictions(match)


def log_admin_action(admin, action, entity, entity_id='', detail=''):
    AdminLog.objects.create(
        admin=admin,
        action=action,
        entity=entity,
        entity_id=str(entity_id),
        detail=detail,
    )
