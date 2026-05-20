"""Helper script — run once to regenerate test/test_data.csv."""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

groups = {
    'A': [('Mexico','South Africa'),('South Korea','Czechia'),('Czechia','South Africa'),('Mexico','South Korea'),('Czechia','Mexico'),('South Africa','South Korea')],
    'B': [('Canada','Bosnia-Herzegovina'),('Qatar','Switzerland'),('Switzerland','Bosnia-Herzegovina'),('Canada','Qatar'),('Switzerland','Canada'),('Bosnia-Herzegovina','Qatar')],
    'C': [('Brazil','Morocco'),('Haiti','Scotland'),('Scotland','Morocco'),('Brazil','Haiti'),('Morocco','Haiti'),('Scotland','Brazil')],
    'D': [('United States','Paraguay'),('Australia','Turkey'),('United States','Australia'),('Turkey','Paraguay'),('Turkey','United States'),('Paraguay','Australia')],
    'E': [('Germany','Curaçao'),('Ivory Coast','Ecuador'),('Germany','Ivory Coast'),('Ecuador','Curaçao'),('Ecuador','Germany'),('Curaçao','Ivory Coast')],
    'F': [('Netherlands','Japan'),('Sweden','Tunisia'),('Netherlands','Sweden'),('Tunisia','Japan'),('Tunisia','Netherlands'),('Japan','Sweden')],
    'G': [('Belgium','Egypt'),('Iran','New Zealand'),('Belgium','Iran'),('New Zealand','Egypt'),('New Zealand','Belgium'),('Egypt','Iran')],
    'H': [('Spain','Cape Verde Islands'),('Saudi Arabia','Uruguay'),('Spain','Saudi Arabia'),('Uruguay','Cape Verde Islands'),('Uruguay','Spain'),('Cape Verde Islands','Saudi Arabia')],
    'I': [('France','Senegal'),('Iraq','Norway'),('France','Iraq'),('Norway','Senegal'),('Norway','France'),('Senegal','Iraq')],
    'J': [('Argentina','Algeria'),('Austria','Jordan'),('Argentina','Austria'),('Jordan','Algeria'),('Jordan','Argentina'),('Algeria','Austria')],
    'K': [('Portugal','Congo DR'),('Uzbekistan','Colombia'),('Portugal','Uzbekistan'),('Colombia','Congo DR'),('Colombia','Portugal'),('Congo DR','Uzbekistan')],
    'L': [('England','Croatia'),('Ghana','Panama'),('England','Ghana'),('Panama','Croatia'),('Panama','England'),('Croatia','Ghana')],
}

headers = ['Timestamp', 'First name', 'Last name', 'Which team(s) do you belong to?']
for letter, fixtures in groups.items():
    for home, away in fixtures:
        headers.append(f'Group {letter} Predictions [{home} - {away}]')
for letter in groups.keys():
    headers.append(f'Group {letter} 1st place')
    headers.append(f'Group {letter} 2nd place')
headers += [
    'FIFA World Cup 2026 final winner',
    'FIFA World Cup 2026 final loser',
    'Who is going to be the top scorer throughout FIFA World Cup 2026? (20 points)',
    'How many goals does the top scorer score? (10 points)',
]

# Match predictions per group: (alice_6, bob_6, carol_6)
preds = {
    'A': (['2-1','1-1','2-0','1-1','0-1','1-2'], ['1-0','2-1','0-1','0-0','1-1','2-1'], ['2-0','0-1','2-0','1-1','0-2','1-2']),
    'B': (['3-0','0-2','2-1','1-0','1-1','1-2'], ['2-1','1-1','1-0','2-0','0-1','0-1'], ['3-0','1-2','2-1','1-1','0-1','2-1']),
    'C': (['2-0','0-2','1-1','3-0','2-0','0-2'], ['1-0','0-3','0-1','4-0','1-0','0-2'], ['2-1','0-1','1-2','2-0','2-1','1-2']),
    'D': (['2-1','1-1','2-0','1-1','1-2','2-0'], ['1-0','0-1','3-1','2-1','0-2','2-1'], ['2-0','1-2','2-1','1-0','1-1','1-1']),
    'E': (['4-0','1-1','2-0','3-0','0-2','0-2'], ['3-0','2-1','2-1','2-0','1-2','0-1'], ['5-0','1-0','3-1','2-1','0-1','1-1']),
    'F': (['2-0','2-0','2-1','1-1','0-2','1-1'], ['2-1','1-0','1-0','0-1','1-2','0-1'], ['1-0','2-1','2-0','1-0','0-1','1-2']),
    'G': (['3-0','2-0','2-0','1-1','0-2','1-1'], ['2-0','1-0','3-1','0-1','0-3','0-1'], ['2-1','1-1','2-1','1-0','1-2','1-2']),
    'H': (['3-0','0-2','3-1','2-0','1-2','0-1'], ['4-0','1-2','2-0','3-0','0-2','1-2'], ['3-1','0-1','2-1','2-1','0-1','0-2']),
    'I': (['2-0','1-2','3-0','2-1','1-2','2-0'], ['3-1','0-2','2-0','2-0','0-2','2-1'], ['2-1','1-1','3-1','1-0','1-1','1-0']),
    'J': (['3-0','2-1','2-0','1-2','0-2','1-2'], ['2-0','2-0','2-1','0-1','0-3','0-1'], ['3-1','1-0','2-0','1-1','1-3','1-1']),
    'K': (['3-0','1-2','3-0','2-0','0-1','1-1'], ['4-0','0-2','2-0','3-1','1-2','0-1'], ['3-1','1-1','3-0','2-1','0-2','1-0']),
    'L': (['2-1','1-1','2-0','1-2','0-2','2-1'], ['2-0','2-1','3-0','0-2','0-1','1-0'], ['3-1','1-0','2-1','0-1','0-2','2-0']),
}

# Group winner predictions: (alice_1st, alice_2nd, bob_1st, bob_2nd, carol_1st, carol_2nd)
winners = {
    'A': ('Mexico','South Korea',   'Czechia','South Korea',      'Mexico','Czechia'),
    'B': ('Canada','Switzerland',   'Switzerland','Canada',        'Canada','Qatar'),
    'C': ('Brazil','Scotland',      'Brazil','Morocco',            'Brazil','Scotland'),
    'D': ('United States','Turkey', 'United States','Paraguay',    'United States','Australia'),
    'E': ('Germany','Ivory Coast',  'Germany','Ecuador',           'Germany','Ivory Coast'),
    'F': ('Netherlands','Sweden',   'Netherlands','Japan',         'Netherlands','Sweden'),
    'G': ('Belgium','Iran',         'Belgium','New Zealand',       'Belgium','Iran'),
    'H': ('Spain','Uruguay',        'Spain','Uruguay',             'Spain','Uruguay'),
    'I': ('France','Norway',        'France','Norway',             'France','Senegal'),
    'J': ('Argentina','Austria',    'Argentina','Austria',         'Argentina','Algeria'),
    'K': ('Portugal','Colombia',    'Portugal','Colombia',         'Portugal','Colombia'),
    'L': ('England','Croatia',      'England','Croatia',           'England','Croatia'),
}

def build_row(p_idx, ts, first, last, teams, fin_w, fin_l, scorer, goals):
    # p_idx: 0=alice, 1=bob, 2=carol
    r = [ts, first, last, teams]
    for letter in groups.keys():
        r += preds[letter][p_idx]
    for letter in groups.keys():
        w = winners[letter]
        r += [w[p_idx * 2], w[p_idx * 2 + 1]]
    r += [fin_w, fin_l, scorer, goals]
    return r

rows = [
    build_row(0, '2026/06/01 10:00:00', 'Alice', 'Smith',  'Team Alpha',
              'Spain',  'England',   'Harry Kane',      '5'),
    build_row(1, '2026/06/01 10:30:00', 'Bob',   'Johnson','Team Beta',
              'Brazil', 'France',    'Kylian Mbappe',   '6'),
    build_row(2, '2026/06/01 11:00:00', 'Carol', 'Davis',  'Team Alpha;Team Beta',
              'Mexico', 'Argentina', 'Lionel Messi',    '4'),
]

out = os.path.join(ROOT, 'test', 'test_data.csv')
with open(out, 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f, quoting=csv.QUOTE_ALL)
    w.writerow(headers)
    for r in rows:
        w.writerow(r)

print(f'Written {out}')
print(f'Columns: {len(headers)}, Rows: {len(rows)}, Row-length check: {len(rows[0])==len(headers)}')
