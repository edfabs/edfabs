from django.urls import path
from django.contrib.auth import views as django_auth_views

from .views import auth as auth_views
from .views import matches as match_views
from .views import leaderboard as lb_views
from .views import admin_panel as admin_views

app_name = 'mundial'

urlpatterns = [
    # ── Dashboard ──────────────────────────────────────────────────────────
    path('', admin_views.dashboard_view, name='dashboard'),

    # ── Auth ───────────────────────────────────────────────────────────────
    path('registro/', auth_views.register_view, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    path('verify-email/<str:token>/', auth_views.verify_email_view, name='verify_email'),
    path('verify-email-notice/', auth_views.verify_email_notice_view, name='verify_email_notice'),
    path('reenviar-verificacion/', auth_views.resend_verification_view, name='resend_verification'),
    path('perfil/', auth_views.profile_view, name='profile'),
    path('perfil/cambiar-email/', auth_views.change_email_view, name='change_email'),

    # Password reset (flujo nativo Django)
    path('password-reset/',
         django_auth_views.PasswordResetView.as_view(
             template_name='mundial/auth/password_reset.html',
             email_template_name='mundial/auth/password_reset_email.txt',
             subject_template_name='mundial/auth/password_reset_subject.txt',
             success_url='/mundial/password-reset/done/',
         ),
         name='password_reset'),
    path('password-reset/done/',
         django_auth_views.PasswordResetDoneView.as_view(
             template_name='mundial/auth/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         django_auth_views.PasswordResetConfirmView.as_view(
             template_name='mundial/auth/password_reset_confirm.html',
             success_url='/mundial/password-reset/complete/',
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         django_auth_views.PasswordResetCompleteView.as_view(
             template_name='mundial/auth/password_reset_complete.html',
         ),
         name='password_reset_complete'),

    # ── Partidos y predicciones ────────────────────────────────────────────
    path('partidos/', match_views.match_list_view, name='matches'),
    path('predecir/<uuid:match_id>/', match_views.predict_view, name='predict'),
    path('mis-predicciones/', match_views.my_predictions_view, name='my_predictions'),

    # ── Tabla de posiciones ────────────────────────────────────────────────
    path('tabla/', lb_views.leaderboard_route_blocked_view, name='leaderboard'),
    path('historial/', lb_views.score_history_view, name='score_history'),

    # ── Panel Admin (/mundial/admin-quiniela/) ─────────────────────────────
    path('admin-quiniela/', admin_views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-quiniela/partidos/', admin_views.admin_matches_view, name='admin_matches'),
    path('admin-quiniela/partidos/<uuid:match_id>/editar/', admin_views.admin_match_edit_view, name='admin_match_edit'),
    path('admin-quiniela/partidos/<uuid:match_id>/resultado/', admin_views.admin_match_result_view, name='admin_match_result'),
    path('admin-quiniela/partidos/<uuid:match_id>/en-juego/', admin_views.admin_match_inplay_view, name='admin_match_inplay'),
    path('admin-quiniela/usuarios/', admin_views.admin_users_view, name='admin_users'),
    path('admin-quiniela/usuarios/<uuid:user_id>/', admin_views.admin_user_detail_view, name='admin_user_detail'),
    path('admin-quiniela/usuarios/<uuid:user_id>/toggle-activo/', admin_views.admin_user_toggle_active_view, name='admin_user_toggle_active'),
    path('admin-quiniela/usuarios/<uuid:user_id>/verificar/', admin_views.admin_user_verify_view, name='admin_user_verify'),
    path('admin-quiniela/puntos/', admin_views.admin_point_config_view, name='admin_point_config'),
    path('admin-quiniela/puntos/recalcular/', admin_views.admin_recalculate_scores_view, name='admin_recalculate'),
    path('admin-quiniela/exportar/tabla/', admin_views.export_leaderboard_csv, name='export_leaderboard'),
    path('admin-quiniela/exportar/predicciones/', admin_views.export_predictions_csv, name='export_predictions'),
]
