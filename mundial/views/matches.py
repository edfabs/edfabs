from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.timezone import now

from ..decorators import verified_required
from ..models import Match, Prediction, PointConfig


@verified_required
def match_list_view(request):
    matches = (
        Match.objects
        .select_related('home_team', 'away_team')
        .order_by('match_date', 'match_number')
    )

    user_preds = {}
    preds_qs = Prediction.objects.filter(user=request.user).values('match_id', 'choice', 'result')
    for p in preds_qs:
        # Key como string para compatibilidad con templatetag dict_get
        user_preds[str(p['match_id'])] = {'choice': p['choice'], 'result': p['result']}

    phases = []
    seen = []
    for match in matches:
        if match.phase not in seen:
            seen.append(match.phase)

    for phase in seen:
        phase_matches = [m for m in matches if m.phase == phase]
        phases.append({
            'phase': phase,
            'label': dict(Match.PHASE_CHOICES).get(phase, phase),
            'matches': phase_matches,
        })

    return render(request, 'mundial/matches/match_list.html', {
        'phases': phases,
        'user_preds': user_preds,
        'now': now(),
        'CHOICE_LABELS': {
            'HOME_WIN': 'Local',
            'DRAW': 'Empate',
            'AWAY_WIN': 'Visitante',
        },
    })


@verified_required
@require_POST
def predict_view(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if not match.is_open_for_predictions:
        if is_ajax:
            return JsonResponse({'success': False, 'error': 'El plazo para predecir ha cerrado.'}, status=400)
        messages.error(request, 'El plazo para predecir ha cerrado.')
        return redirect('mundial:matches')

    choice = request.POST.get('choice', '')
    valid_choices = {c[0] for c in Prediction.CHOICE_CHOICES}
    if choice not in valid_choices:
        if is_ajax:
            return JsonResponse({'success': False, 'error': 'Opción inválida.'}, status=400)
        messages.error(request, 'Opción inválida.')
        return redirect('mundial:matches')

    pred, created = Prediction.objects.get_or_create(
        user=request.user,
        match=match,
        defaults={'choice': choice},
    )
    if not created:
        pred.choice = choice
        pred.save(update_fields=['choice', 'updated_at'])

    if is_ajax:
        return JsonResponse({
            'success': True,
            'choice': choice,
            'created': created,
            'choice_label': dict(Prediction.CHOICE_CHOICES).get(choice, choice),
        })

    messages.success(request, 'Predicción guardada.')
    return redirect('mundial:matches')


@verified_required
def my_predictions_view(request):
    predictions = (
        Prediction.objects
        .filter(user=request.user)
        .select_related('match__home_team', 'match__away_team')
        .order_by('match__match_date')
    )

    point_configs = {pc.phase: pc.points for pc in PointConfig.objects.all()}

    by_phase = {}
    for pred in predictions:
        phase = pred.match.phase
        if phase not in by_phase:
            by_phase[phase] = {
                'label': dict(Match.PHASE_CHOICES).get(phase, phase),
                'preds': [],
                'correct': 0, 'incorrect': 0, 'null': 0, 'pending': 0, 'points': 0,
            }
        data = by_phase[phase]
        data['preds'].append(pred)
        if pred.result == Prediction.CORRECT:
            data['correct'] += 1
            data['points'] += point_configs.get(phase, 0)
        elif pred.result == Prediction.INCORRECT:
            data['incorrect'] += 1
        elif pred.result == Prediction.NULL:
            data['null'] += 1
        else:
            data['pending'] += 1

    ordered_phases = [p for p in Match.PHASE_ORDER if p in by_phase]
    ordered = [(ph, by_phase[ph]) for ph in ordered_phases]

    totals = {
        'correct': sum(d['correct'] for _, d in ordered),
        'incorrect': sum(d['incorrect'] for _, d in ordered),
        'null': sum(d['null'] for _, d in ordered),
        'pending': sum(d['pending'] for _, d in ordered),
        'points': sum(d['points'] for _, d in ordered),
    }

    return render(request, 'mundial/matches/my_predictions.html', {
        'by_phase': ordered,
        'totals': totals,
        'now': now(),
    })
