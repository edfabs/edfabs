from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, LoginAttempt, Team, Match, PointConfig, Prediction, UserScore, AdminLog


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('full_name', 'avatar')}),
        ('Permisos', {'fields': ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role'),
        }),
    )
    readonly_fields = ('date_joined', 'last_login')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'fifa_code', 'group')
    list_filter = ('group',)
    search_fields = ('name', 'fifa_code')


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phase', 'match_date', 'status', 'winner')
    list_filter = ('phase', 'status', 'group')
    search_fields = ('home_team__name', 'away_team__name', 'stadium', 'city')
    ordering = ('match_date',)


@admin.register(PointConfig)
class PointConfigAdmin(admin.ModelAdmin):
    list_display = ('phase', 'points')


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'choice', 'result', 'is_locked')
    list_filter = ('result', 'choice', 'is_locked')
    search_fields = ('user__email',)


@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points', 'correct_predictions', 'incorrect_predictions', 'null_predictions')
    ordering = ('-total_points',)


@admin.register(AdminLog)
class AdminLogAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action', 'entity', 'entity_id', 'timestamp')
    list_filter = ('action', 'entity')
    ordering = ('-timestamp',)
    readonly_fields = ('admin', 'action', 'entity', 'entity_id', 'timestamp', 'detail')


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('ip', 'user', 'success', 'timestamp')
    list_filter = ('success',)
    ordering = ('-timestamp',)
