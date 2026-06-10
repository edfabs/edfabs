import uuid
import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

import mundial.models.user


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(
                    default=False,
                    help_text='Designates that this user has all permissions without explicitly assigning them.',
                    verbose_name='superuser status',
                )),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('full_name', models.CharField(max_length=200)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='mundial/avatars/')),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('role', models.CharField(
                    choices=[('ADMIN', 'Administrador'), ('USER', 'Usuario')],
                    default='USER',
                    max_length=10,
                )),
                ('groups', models.ManyToManyField(
                    blank=True,
                    help_text='The groups this user belongs to.',
                    related_name='user_set',
                    related_query_name='user',
                    to='auth.Group',
                    verbose_name='groups',
                )),
                ('user_permissions', models.ManyToManyField(
                    blank=True,
                    help_text='Specific permissions for this user.',
                    related_name='user_set',
                    related_query_name='user',
                    to='auth.Permission',
                    verbose_name='user permissions',
                )),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', mundial.models.user.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PointConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phase', models.CharField(
                    choices=[
                        ('GROUPS', 'Fase de Grupos'),
                        ('ROUND_OF_32', 'Ronda de 32'),
                        ('ROUND_OF_16', 'Octavos de Final'),
                        ('QUARTERFINAL', 'Cuartos de Final'),
                        ('SEMIFINAL', 'Semifinal'),
                        ('THIRD_PLACE', 'Tercer Lugar'),
                        ('FINAL', 'Final'),
                    ],
                    max_length=20,
                    unique=True,
                )),
                ('points', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('fifa_code', models.CharField(max_length=3, unique=True)),
                ('group', models.CharField(blank=True, max_length=1, null=True)),
                ('flag_url', models.URLField(blank=True)),
            ],
            options={
                'ordering': ['group', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phase', models.CharField(
                    choices=[
                        ('GROUPS', 'Fase de Grupos'),
                        ('ROUND_OF_32', 'Ronda de 32'),
                        ('ROUND_OF_16', 'Octavos de Final'),
                        ('QUARTERFINAL', 'Cuartos de Final'),
                        ('SEMIFINAL', 'Semifinal'),
                        ('THIRD_PLACE', 'Tercer Lugar'),
                        ('FINAL', 'Final'),
                    ],
                    max_length=20,
                )),
                ('group', models.CharField(blank=True, max_length=1, null=True)),
                ('match_date', models.DateTimeField()),
                ('stadium', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=100)),
                ('status', models.CharField(
                    choices=[('SCHEDULED', 'Programado'), ('IN_PLAY', 'En Juego'), ('FINISHED', 'Finalizado')],
                    default='SCHEDULED',
                    max_length=20,
                )),
                ('home_goals', models.IntegerField(blank=True, null=True)),
                ('away_goals', models.IntegerField(blank=True, null=True)),
                ('winner', models.CharField(
                    blank=True,
                    choices=[('HOME', 'Local'), ('DRAW', 'Empate'), ('AWAY', 'Visitante')],
                    max_length=10,
                    null=True,
                )),
                ('match_number', models.PositiveIntegerField(default=0)),
                ('home_team', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='home_matches',
                    to='mundial.Team',
                )),
                ('away_team', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='away_matches',
                    to='mundial.Team',
                )),
            ],
            options={
                'ordering': ['match_date', 'match_number'],
            },
        ),
        migrations.CreateModel(
            name='LoginAttempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('success', models.BooleanField(default=False)),
                ('user', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='login_attempts',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='AdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=100)),
                ('entity', models.CharField(max_length=100)),
                ('entity_id', models.CharField(blank=True, max_length=100)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('detail', models.TextField(blank=True)),
                ('admin', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='admin_logs',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='UserScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_points', models.IntegerField(default=0)),
                ('correct_predictions', models.IntegerField(default=0)),
                ('incorrect_predictions', models.IntegerField(default=0)),
                ('null_predictions', models.IntegerField(default=0)),
                ('playoff_correct', models.IntegerField(default=0)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='mundial_score',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('choice', models.CharField(
                    choices=[('HOME_WIN', 'Victoria Local'), ('DRAW', 'Empate'), ('AWAY_WIN', 'Victoria Visitante')],
                    max_length=10,
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_locked', models.BooleanField(default=False)),
                ('result', models.CharField(
                    choices=[('PENDING', 'Pendiente'), ('CORRECT', 'Correcta'), ('INCORRECT', 'Incorrecta'), ('NULL', 'Nula')],
                    default='PENDING',
                    max_length=10,
                )),
                ('match', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='predictions',
                    to='mundial.Match',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='predictions',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'unique_together': {('user', 'match')},
            },
        ),
    ]
