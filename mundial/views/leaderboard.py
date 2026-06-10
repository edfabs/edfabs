from django.shortcuts import render

from ..decorators import verified_required
from ..models import UserScore, Prediction, Match, PointConfig


@verified_required
def leaderboard_view(request):
    scores = (
        UserScore.objects
        .select_related('user')
        .order_by('-total_points', '-playoff_correct', '-correct_predictions')
    )

    user_rank = None
    for i, score in enumerate(scores, 1):
        if score.user_id == request.user.pk:
            user_rank = i
            break

    return render(request, 'mundial/leaderboard/table.html', {
        'scores': scores,
        'user_rank': user_rank,
    })


@verified_required
def score_history_view(request):
    predictions = (
        Prediction.objects
        .filter(user=request.user)
        .select_related('match__home_team', 'match__away_team')
        .order_by('match__match_date')
    )

    point_configs = {pc.phase: pc.points for pc in PointConfig.objects.all()}

    history = []
    total_points = 0
    for pred in predictions:
        pts = 0
        if pred.result == Prediction.CORRECT:
            pts = point_configs.get(pred.match.phase, 0)
            total_points += pts
        history.append({'prediction': pred, 'points': pts})

    return render(request, 'mundial/leaderboard/history.html', {
        'history': history,
        'total_points': total_points,
    })
