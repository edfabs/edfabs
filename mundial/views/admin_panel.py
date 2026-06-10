import csv

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ..decorators import role_required, verified_required
from ..forms.admin import MatchEditForm, MatchResultForm
from ..models import AdminLog, Match, Prediction, PointConfig, UserScore
from ..models.user import CustomUser
from ..services import log_admin_action, qualify_predictions, recalculate_all_scores

User = get_user_model()


@verified_required
def dashboard_view(request):
    """Dashboard para usuarios verificados (y admins redirigen al admin)."""
    if request.user.role == CustomUser.ADMIN:
        return redirect('mundial:admin_dashboard')

    try:
        score = request.user.mundial_score
        user_points = score.total_points
    except Exception:
        user_points = 0

    upcoming = (
        Match.objects
        .filter(status=Match.SCHEDULED)
        .select_related('home_team', 'away_team')
        .order_by('match_date')[:5]
    )
    top_scores = (
        UserScore.objects
        .select_related('user')
        .order_by('-total_points', '-playoff_correct')[:5]
    )
    recent_preds = (
        Prediction.objects
        .filter(user=request.user)
        .select_related('match__home_team', 'match__away_team')
        .order_by('-created_at')[:5]
    )

    return render(request, 'mundial/dashboard.html', {
        'user_points': user_points,
        'upcoming': upcoming,
        'top_scores': top_scores,
        'recent_preds': recent_preds,
    })


@role_required('ADMIN')
def admin_dashboard_view(request):
    total_users = User.objects.filter(role=CustomUser.USER).count()
    verified_users = User.objects.filter(role=CustomUser.USER, is_verified=True).count()
    finished_matches = Match.objects.filter(status=Match.FINISHED).count()
    scheduled_matches = Match.objects.filter(status=Match.SCHEDULED).count()
    inplay_matches = Match.objects.filter(status=Match.IN_PLAY).count()
    leader = (
        UserScore.objects
        .select_related('user')
        .order_by('-total_points', '-playoff_correct')
        .first()
    )
    recent_logs = AdminLog.objects.select_related('admin').order_by('-timestamp')[:15]

    return render(request, 'mundial/admin/dashboard.html', {
        'total_users': total_users,
        'verified_users': verified_users,
        'finished_matches': finished_matches,
        'scheduled_matches': scheduled_matches,
        'inplay_matches': inplay_matches,
        'leader': leader,
        'recent_logs': recent_logs,
    })


@role_required('ADMIN')
def admin_matches_view(request):
    matches = (
        Match.objects
        .select_related('home_team', 'away_team')
        .order_by('match_date', 'match_number')
    )
    return render(request, 'mundial/admin/matches.html', {'matches': matches})


@role_required('ADMIN')
def admin_match_edit_view(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    if request.method == 'POST':
        form = MatchEditForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            log_admin_action(request.user, 'EDIT_MATCH', 'Match', match_id, str(match))
            messages.success(request, 'Partido actualizado correctamente.')
            return redirect('mundial:admin_matches')
    else:
        form = MatchEditForm(instance=match)

    return render(request, 'mundial/admin/match_edit.html', {'form': form, 'match': match})


@role_required('ADMIN')
def admin_match_result_view(request, match_id):
    match = get_object_or_404(Match, pk=match_id)

    if request.method == 'POST':
        form = MatchResultForm(request.POST)
        if form.is_valid():
            hg = form.cleaned_data['home_goals']
            ag = form.cleaned_data['away_goals']
            match.home_goals = hg
            match.away_goals = ag
            if hg > ag:
                match.winner = Match.HOME
            elif hg == ag:
                match.winner = Match.DRAW
            else:
                match.winner = Match.AWAY
            match.status = Match.FINISHED
            match.save()
            qualify_predictions(match)
            log_admin_action(
                request.user, 'REGISTER_RESULT', 'Match', match_id,
                f'{match} → {hg}-{ag} (ganador: {match.winner})'
            )
            messages.success(request, f'Resultado registrado: {hg} - {ag}')
            return redirect('mundial:admin_matches')
    else:
        form = MatchResultForm(
            initial={
                'home_goals': match.home_goals or 0,
                'away_goals': match.away_goals or 0,
            }
        )

    return render(request, 'mundial/admin/match_result.html', {'form': form, 'match': match})


@role_required('ADMIN')
@require_POST
def admin_match_inplay_view(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match.status = Match.IN_PLAY
    match.save(update_fields=['status'])
    log_admin_action(request.user, 'MATCH_IN_PLAY', 'Match', match_id, str(match))
    messages.success(request, 'Partido marcado como En Juego.')
    return redirect('mundial:admin_matches')


@role_required('ADMIN')
def admin_users_view(request):
    users = (
        User.objects
        .filter(role=CustomUser.USER)
        .select_related('mundial_score')
        .order_by('-date_joined')
    )
    return render(request, 'mundial/admin/users.html', {'users': users})


@role_required('ADMIN')
def admin_user_detail_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    predictions = (
        Prediction.objects
        .filter(user=user)
        .select_related('match__home_team', 'match__away_team')
        .order_by('match__match_date')
    )
    return render(request, 'mundial/admin/user_detail.html', {
        'target_user': user,
        'predictions': predictions,
    })


@role_required('ADMIN')
@require_POST
def admin_user_toggle_active_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = not user.is_active
    user.save(update_fields=['is_active'])
    action = 'ACTIVATE_USER' if user.is_active else 'DEACTIVATE_USER'
    log_admin_action(request.user, action, 'User', user_id, user.email)
    status = 'activado' if user.is_active else 'desactivado'
    messages.success(request, f'Usuario {user.email} {status}.')
    return redirect('mundial:admin_users')


@role_required('ADMIN')
@require_POST
def admin_user_verify_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_verified = True
    user.save(update_fields=['is_verified'])
    log_admin_action(request.user, 'VERIFY_USER', 'User', user_id, user.email)
    messages.success(request, f'Usuario {user.email} verificado manualmente.')
    return redirect('mundial:admin_users')


@role_required('ADMIN')
def admin_point_config_view(request):
    configs = list(PointConfig.objects.order_by('phase'))
    finished_count = Match.objects.filter(status=Match.FINISHED).count()

    if request.method == 'POST':
        updated = False
        for config in configs:
            key = f'points_{config.phase}'
            if key in request.POST:
                try:
                    new_pts = int(request.POST[key])
                    if new_pts != config.points:
                        config.points = new_pts
                        config.save()
                        log_admin_action(
                            request.user, 'UPDATE_POINTS', 'PointConfig',
                            config.phase, f'{config.phase}: {new_pts} pts'
                        )
                        updated = True
                except (ValueError, TypeError):
                    pass
        if updated:
            messages.success(request, 'Configuración de puntos actualizada.')
        return redirect('mundial:admin_point_config')

    return render(request, 'mundial/admin/point_config.html', {
        'configs': configs,
        'finished_count': finished_count,
    })


@role_required('ADMIN')
@require_POST
def admin_recalculate_scores_view(request):
    recalculate_all_scores()
    log_admin_action(request.user, 'RECALCULATE_SCORES', 'System', '', 'Recálculo total de puntos')
    messages.success(request, 'Puntajes recalculados correctamente.')
    return redirect('mundial:admin_point_config')


# ---- CSV exports ----

class _EchoBuffer:
    def write(self, value):
        return value


@role_required('ADMIN')
def export_leaderboard_csv(request):
    scores = (
        UserScore.objects
        .select_related('user')
        .order_by('-total_points', '-playoff_correct', '-correct_predictions')
    )

    def _rows():
        buf = _EchoBuffer()
        writer = csv.writer(buf)
        yield writer.writerow(['#', 'Nombre', 'Email', 'Puntos', 'Correctas',
                                'Incorrectas', 'Nulas', 'Aciertos Eliminatorias'])
        for i, s in enumerate(scores, 1):
            yield writer.writerow([
                i, s.user.full_name, s.user.email,
                s.total_points, s.correct_predictions,
                s.incorrect_predictions, s.null_predictions,
                s.playoff_correct,
            ])

    response = StreamingHttpResponse(_rows(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="tabla_posiciones.csv"'
    return response


@role_required('ADMIN')
def export_predictions_csv(request):
    predictions = (
        Prediction.objects
        .select_related('user', 'match__home_team', 'match__away_team')
        .order_by('user__email', 'match__match_date')
    )

    def _rows():
        buf = _EchoBuffer()
        writer = csv.writer(buf)
        yield writer.writerow(['Email', 'Nombre', 'Partido', 'Fase',
                                'Predicción', 'Resultado Real', 'Estado'])
        for pred in predictions:
            home = pred.match.home_team.name if pred.match.home_team else 'TBD'
            away = pred.match.away_team.name if pred.match.away_team else 'TBD'
            yield writer.writerow([
                pred.user.email,
                pred.user.full_name,
                f'{home} vs {away}',
                pred.match.get_phase_display(),
                pred.get_choice_display(),
                pred.match.winner or '-',
                pred.get_result_display(),
            ])

    response = StreamingHttpResponse(_rows(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="predicciones.csv"'
    return response
