"""
Seed command: carga los 48 equipos y 104 partidos del Mundial FIFA 2026.
Grupos oficiales del sorteo FIFA del 5 de diciembre de 2025.
Calendario oficial fase de grupos (72 partidos). Tiempos en hora de Ciudad de México (CDT).
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

import pytz

from mundial.models import Match, PointConfig, Team

MEX_TZ = pytz.timezone('America/Mexico_City')


def mdt(year, month, day, hour, minute=0):
    return MEX_TZ.localize(timezone.datetime(year, month, day, hour, minute))


# ---------------------------------------------------------------------------
# EQUIPOS CLASIFICADOS — grupos oficiales FIFA 2026
# (name, fifa_code, group)
# ---------------------------------------------------------------------------
TEAMS = [
    # Grupo A
    ('México',        'MEX', 'A'), ('Corea del Sur',   'KOR', 'A'),
    ('Chequia',       'CZE', 'A'), ('Sudáfrica',       'RSA', 'A'),
    # Grupo B
    ('Canadá',        'CAN', 'B'), ('Bosnia-Herzegovina', 'BIH', 'B'),
    ('Qatar',         'QAT', 'B'), ('Suiza',           'SUI', 'B'),
    # Grupo C
    ('Brasil',        'BRA', 'C'), ('Marruecos',       'MAR', 'C'),
    ('Haití',         'HAI', 'C'), ('Escocia',         'SCO', 'C'),
    # Grupo D
    ('Estados Unidos','USA', 'D'), ('Paraguay',        'PAR', 'D'),
    ('Australia',     'AUS', 'D'), ('Türkiye',         'TUR', 'D'),
    # Grupo E
    ('Alemania',      'GER', 'E'), ('Costa de Marfil', 'CIV', 'E'),
    ('Ecuador',       'ECU', 'E'), ('Curaçao',         'CUW', 'E'),
    # Grupo F
    ('Países Bajos',  'NED', 'F'), ('Japón',           'JPN', 'F'),
    ('Suecia',        'SWE', 'F'), ('Túnez',           'TUN', 'F'),
    # Grupo G
    ('Bélgica',       'BEL', 'G'), ('Egipto',          'EGY', 'G'),
    ('Irán',          'IRN', 'G'), ('Nueva Zelanda',   'NZL', 'G'),
    # Grupo H
    ('España',        'ESP', 'H'), ('Arabia Saudita',  'KSA', 'H'),
    ('Uruguay',       'URU', 'H'), ('Cabo Verde',      'CPV', 'H'),
    # Grupo I
    ('Francia',       'FRA', 'I'), ('Senegal',         'SEN', 'I'),
    ('Iraq',          'IRQ', 'I'), ('Noruega',         'NOR', 'I'),
    # Grupo J
    ('Argentina',     'ARG', 'J'), ('Argelia',         'ALG', 'J'),
    ('Austria',       'AUT', 'J'), ('Jordania',        'JOR', 'J'),
    # Grupo K
    ('Portugal',      'POR', 'K'), ('Congo DR',        'COD', 'K'),
    ('Uzbekistán',    'UZB', 'K'), ('Colombia',        'COL', 'K'),
    # Grupo L
    ('Inglaterra',    'ENG', 'L'), ('Croacia',         'CRO', 'L'),
    ('Ghana',         'GHA', 'L'), ('Panamá',          'PAN', 'L'),
]

# ---------------------------------------------------------------------------
# PARTIDOS FASE DE GRUPOS — calendario oficial FIFA 2026
# (num, local, visitante, año, mes, día, hora_mex, min, estadio, ciudad, grupo)
# Tiempos convertidos de ET → CDT (México = ET − 1 h)
# ---------------------------------------------------------------------------
GROUP_MATCHES = [
    # ── Grupo A ──────────────────────────────────────────────────────────────
    ( 1, 'MEX','RSA', 2026,6,11,14, 0, 'Estadio Azteca',          'Ciudad de México', 'A'),
    ( 2, 'KOR','CZE', 2026,6,11,21, 0, 'Estadio Akron',           'Guadalajara',      'A'),
    (25, 'CZE','RSA', 2026,6,18,11, 0, 'Mercedes-Benz Stadium',   'Atlanta',          'A'),
    (28, 'MEX','KOR', 2026,6,18,22, 0, 'Estadio Akron',           'Guadalajara',      'A'),
    (53, 'CZE','MEX', 2026,6,24,20, 0, 'Estadio Azteca',          'Ciudad de México', 'A'),
    (54, 'RSA','KOR', 2026,6,24,20, 0, 'Estadio BBVA',            'Monterrey',        'A'),
    # ── Grupo B ──────────────────────────────────────────────────────────────
    ( 3, 'CAN','BIH', 2026,6,12,14, 0, 'BMO Field',               'Toronto',          'B'),
    ( 5, 'QAT','SUI', 2026,6,13,14, 0, "Levi's Stadium",          'Santa Clara',      'B'),
    (26, 'SUI','BIH', 2026,6,18,14, 0, 'SoFi Stadium',            'Inglewood',        'B'),
    (27, 'CAN','QAT', 2026,6,18,17, 0, 'BC Place',                'Vancouver',        'B'),
    (51, 'SUI','CAN', 2026,6,24,14, 0, 'BC Place',                'Vancouver',        'B'),
    (52, 'BIH','QAT', 2026,6,24,14, 0, 'Lumen Field',             'Seattle',          'B'),
    # ── Grupo C ──────────────────────────────────────────────────────────────
    ( 6, 'BRA','MAR', 2026,6,13,17, 0, 'MetLife Stadium',         'East Rutherford',  'C'),
    ( 7, 'HAI','SCO', 2026,6,13,20, 0, 'Gillette Stadium',        'Foxborough',       'C'),
    (30, 'SCO','MAR', 2026,6,19,17, 0, 'Gillette Stadium',        'Foxborough',       'C'),
    (31, 'BRA','HAI', 2026,6,19,20, 0, 'Lincoln Financial Field', 'Philadelphia',     'C'),
    (49, 'SCO','BRA', 2026,6,24,17, 0, 'Hard Rock Stadium',       'Miami Gardens',    'C'),
    (50, 'MAR','HAI', 2026,6,24,17, 0, 'Mercedes-Benz Stadium',   'Atlanta',          'C'),
    # ── Grupo D ──────────────────────────────────────────────────────────────
    ( 4, 'USA','PAR', 2026,6,12,20, 0, 'SoFi Stadium',            'Inglewood',        'D'),
    ( 8, 'AUS','TUR', 2026,6,12,23, 0, 'BC Place',                'Vancouver',        'D'),
    (29, 'USA','AUS', 2026,6,19,14, 0, 'Lumen Field',             'Seattle',          'D'),
    (32, 'TUR','PAR', 2026,6,19,23, 0, "Levi's Stadium",          'Santa Clara',      'D'),
    (59, 'TUR','USA', 2026,6,25,21, 0, 'SoFi Stadium',            'Inglewood',        'D'),
    (60, 'PAR','AUS', 2026,6,25,21, 0, "Levi's Stadium",          'Santa Clara',      'D'),
    # ── Grupo E ──────────────────────────────────────────────────────────────
    ( 9, 'GER','CUW', 2026,6,14,12, 0, 'NRG Stadium',             'Houston',          'E'),
    (11, 'CIV','ECU', 2026,6,14,18, 0, 'Lincoln Financial Field', 'Philadelphia',     'E'),
    (34, 'GER','CIV', 2026,6,20,15, 0, 'BMO Field',               'Toronto',          'E'),
    (35, 'ECU','CUW', 2026,6,20,19, 0, 'Arrowhead Stadium',       'Kansas City',      'E'),
    (55, 'CUW','CIV', 2026,6,25,15, 0, 'Lincoln Financial Field', 'Philadelphia',     'E'),
    (56, 'ECU','GER', 2026,6,25,15, 0, 'MetLife Stadium',         'East Rutherford',  'E'),
    # ── Grupo F ──────────────────────────────────────────────────────────────
    (10, 'NED','JPN', 2026,6,14,15, 0, 'AT&T Stadium',            'Arlington',        'F'),
    (12, 'SWE','TUN', 2026,6,14,21, 0, 'Estadio BBVA',            'Monterrey',        'F'),
    (36, 'TUN','JPN', 2026,6,19,23, 0, 'Estadio BBVA',            'Monterrey',        'F'),
    (33, 'NED','SWE', 2026,6,20,12, 0, 'NRG Stadium',             'Houston',          'F'),
    (57, 'JPN','SWE', 2026,6,25,18, 0, 'AT&T Stadium',            'Arlington',        'F'),
    (58, 'TUN','NED', 2026,6,25,18, 0, 'Arrowhead Stadium',       'Kansas City',      'F'),
    # ── Grupo G ──────────────────────────────────────────────────────────────
    (16, 'IRN','NZL', 2026,6,14,23, 0, 'SoFi Stadium',            'Inglewood',        'G'),
    (14, 'BEL','EGY', 2026,6,15,17, 0, 'Lumen Field',             'Seattle',          'G'),
    (38, 'BEL','IRN', 2026,6,21,14, 0, 'SoFi Stadium',            'Inglewood',        'G'),
    (40, 'NZL','EGY', 2026,6,21,20, 0, 'BC Place',                'Vancouver',        'G'),
    (61, 'BEL','NZL', 2026,6,26,22, 0, 'Lumen Field',             'Seattle',          'G'),
    (62, 'IRN','EGY', 2026,6,26,22, 0, 'BC Place',                'Vancouver',        'G'),
    # ── Grupo H ──────────────────────────────────────────────────────────────
    (13, 'ESP','CPV', 2026,6,15,12, 0, 'Mercedes-Benz Stadium',   'Atlanta',          'H'),
    (15, 'KSA','URU', 2026,6,15,17, 0, 'Hard Rock Stadium',       'Miami Gardens',    'H'),
    (37, 'ESP','KSA', 2026,6,21,11, 0, 'Mercedes-Benz Stadium',   'Atlanta',          'H'),
    (39, 'URU','CPV', 2026,6,21,17, 0, 'Hard Rock Stadium',       'Miami Gardens',    'H'),
    (63, 'ESP','URU', 2026,6,26,19, 0, 'Estadio Azteca',          'Ciudad de México', 'H'),
    (64, 'CPV','KSA', 2026,6,26,19, 0, 'Estadio Akron',           'Guadalajara',      'H'),
    # ── Grupo I ──────────────────────────────────────────────────────────────
    (17, 'FRA','SEN', 2026,6,16,14, 0, 'MetLife Stadium',         'East Rutherford',  'I'),
    (18, 'IRQ','NOR', 2026,6,16,17, 0, 'Gillette Stadium',        'Foxborough',       'I'),
    (41, 'NOR','SEN', 2026,6,22,19, 0, 'MetLife Stadium',         'East Rutherford',  'I'),
    (42, 'FRA','IRQ', 2026,6,22,16, 0, 'Lincoln Financial Field', 'Philadelphia',     'I'),
    (65, 'NOR','FRA', 2026,6,26,14, 0, 'Gillette Stadium',        'Foxborough',       'I'),
    (66, 'SEN','IRQ', 2026,6,26,14, 0, 'Hard Rock Stadium',       'Miami Gardens',    'I'),
    # ── Grupo J ──────────────────────────────────────────────────────────────
    (20, 'AUT','JOR', 2026,6,15,23, 0, "Levi's Stadium",          'Santa Clara',      'J'),
    (19, 'ARG','ALG', 2026,6,16,20, 0, 'Arrowhead Stadium',       'Kansas City',      'J'),
    (43, 'ARG','AUT', 2026,6,22,12, 0, 'AT&T Stadium',            'Arlington',        'J'),
    (44, 'JOR','ALG', 2026,6,22,22, 0, "Levi's Stadium",          'Santa Clara',      'J'),
    (69, 'JOR','ARG', 2026,6,27,21, 0, 'AT&T Stadium',            'Arlington',        'J'),
    (70, 'ALG','AUT', 2026,6,27,21, 0, 'Arrowhead Stadium',       'Kansas City',      'J'),
    # ── Grupo K ──────────────────────────────────────────────────────────────
    (21, 'POR','COD', 2026,6,17,12, 0, 'NRG Stadium',             'Houston',          'K'),
    (24, 'UZB','COL', 2026,6,17,21, 0, 'Estadio Azteca',          'Ciudad de México', 'K'),
    (47, 'POR','UZB', 2026,6,23,12, 0, 'NRG Stadium',             'Houston',          'K'),
    (48, 'COL','COD', 2026,6,23,18, 0, 'Estadio Akron',           'Guadalajara',      'K'),
    (71, 'COL','POR', 2026,6,27,18,30, 'Hard Rock Stadium',       'Miami Gardens',    'K'),
    (72, 'COD','UZB', 2026,6,27,18,30, 'Mercedes-Benz Stadium',   'Atlanta',          'K'),
    # ── Grupo L ──────────────────────────────────────────────────────────────
    (22, 'ENG','CRO', 2026,6,17,15, 0, 'AT&T Stadium',            'Arlington',        'L'),
    (23, 'GHA','PAN', 2026,6,17,18, 0, 'BMO Field',               'Toronto',          'L'),
    (45, 'ENG','GHA', 2026,6,23,15, 0, 'Gillette Stadium',        'Foxborough',       'L'),
    (46, 'PAN','CRO', 2026,6,23,18, 0, 'BMO Field',               'Toronto',          'L'),
    (67, 'PAN','ENG', 2026,6,27,16, 0, 'MetLife Stadium',         'East Rutherford',  'L'),
    (68, 'CRO','GHA', 2026,6,27,16, 0, 'Lincoln Financial Field', 'Philadelphia',     'L'),
]

# Estadios para fase eliminatoria (TBD equipos)
_KNOCKOUT_VENUES = [
    ('MetLife Stadium',         'East Rutherford'),
    ('AT&T Stadium',            'Arlington'),
    ('SoFi Stadium',            'Inglewood'),
    ('Hard Rock Stadium',       'Miami Gardens'),
    ('Lumen Field',             'Seattle'),
    ('Gillette Stadium',        'Foxborough'),
    ('Lincoln Financial Field', 'Philadelphia'),
    ('Arrowhead Stadium',       'Kansas City'),
    ('NRG Stadium',             'Houston'),
    ('Rose Bowl',               'Pasadena'),
    ("Levi's Stadium",          'Santa Clara'),
    ('Mercedes-Benz Stadium',   'Atlanta'),
    ('BC Place',                'Vancouver'),
    ('BMO Field',               'Toronto'),
    ('Estadio Azteca',          'Ciudad de México'),
    ('Estadio Akron',           'Guadalajara'),
    ('Estadio BBVA',            'Monterrey'),
]


class Command(BaseCommand):
    help = 'Carga equipos y 104 partidos del Mundial FIFA 2026 (datos oficiales).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Borrar todos los partidos y equipos antes de cargar.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            Match.objects.all().delete()
            Team.objects.all().delete()
            PointConfig.objects.all().delete()
            self.stdout.write(self.style.WARNING('Datos previos eliminados.'))

        self._seed_teams()
        self._seed_point_configs()
        self._seed_group_stage()
        self._seed_knockout_stage()

        self.stdout.write(self.style.SUCCESS(
            f'✓ Seed completado: {Team.objects.count()} equipos, '
            f'{Match.objects.count()} partidos.'
        ))

    def _seed_teams(self):
        created = 0
        for name, code, group in TEAMS:
            _, is_new = Team.objects.get_or_create(
                fifa_code=code,
                defaults={'name': name, 'group': group},
            )
            if is_new:
                created += 1
        self.stdout.write(f'  Equipos creados: {created}')

    def _seed_point_configs(self):
        defaults = {
            Match.GROUPS:       1,
            Match.ROUND_OF_32:  2,
            Match.ROUND_OF_16:  3,
            Match.QUARTERFINAL: 4,
            Match.SEMIFINAL:    6,
            Match.THIRD_PLACE:  4,
            Match.FINAL:       10,
        }
        for phase, pts in defaults.items():
            PointConfig.objects.get_or_create(phase=phase, defaults={'points': pts})
        self.stdout.write('  PointConfig cargado.')

    def _seed_group_stage(self):
        if Match.objects.filter(phase=Match.GROUPS).exists():
            self.stdout.write('  Fase de grupos ya cargada, omitiendo.')
            return

        team_map = {t.fifa_code: t for t in Team.objects.all()}
        created = 0

        for row in GROUP_MATCHES:
            num, home_code, away_code, y, mo, d, h, mi, stadium, city, group = row
            Match.objects.create(
                match_number=num,
                home_team=team_map[home_code],
                away_team=team_map[away_code],
                phase=Match.GROUPS,
                group=group,
                match_date=mdt(y, mo, d, h, mi),
                stadium=stadium,
                city=city,
            )
            created += 1

        self.stdout.write(f'  Partidos de grupos creados: {created}')

    def _seed_knockout_stage(self):
        knockout_phases = [
            (Match.ROUND_OF_32,  16, mdt(2026, 6, 29, 14, 0)),
            (Match.ROUND_OF_16,   8, mdt(2026, 7,  5, 14, 0)),
            (Match.QUARTERFINAL,  4, mdt(2026, 7, 10, 14, 0)),
            (Match.SEMIFINAL,     2, mdt(2026, 7, 14, 14, 0)),
            (Match.THIRD_PLACE,   1, mdt(2026, 7, 18, 15, 0)),
            (Match.FINAL,         1, mdt(2026, 7, 19, 17, 0)),
        ]

        match_number = 73
        venue_idx = 0
        for phase, count, base_date in knockout_phases:
            if Match.objects.filter(phase=phase).exists():
                self.stdout.write(f'  {phase} ya cargada, omitiendo.')
                match_number += count
                continue
            for i in range(count):
                day_offset = i // 2
                hour_offset = 4 if i % 2 else 0
                match_date = base_date + timedelta(days=day_offset, hours=hour_offset)
                venue = _KNOCKOUT_VENUES[venue_idx % len(_KNOCKOUT_VENUES)]
                Match.objects.create(
                    home_team=None,
                    away_team=None,
                    phase=phase,
                    match_date=match_date,
                    stadium=venue[0],
                    city=venue[1],
                    match_number=match_number,
                )
                match_number += 1
                venue_idx += 1

        created_ko = Match.objects.exclude(phase=Match.GROUPS).count()
        self.stdout.write(f'  Partidos eliminatorias creados: {created_ko}')
