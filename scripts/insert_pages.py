import os
import pandas as pd

_MEDALS     = {1: '🥇', 2: '🥈', 3: '🥉'}
_CLASSES    = {1: 'lb-gold',  2: 'lb-silver',  3: 'lb-bronze'}
_TS_CLASSES = {1: 'ts-gold',  2: 'ts-silver',  3: 'ts-bronze'}


def _standings_html(team, members):
    """
    Load data/group_dfs/{team} and return an HTML standings block.
    members: the predictions_df subset for this team (has d_name + f_name).
    Returns a placeholder if no scores exist yet.
    """
    pickle_path = os.path.join("data", "group_dfs", team)
    placeholder = (
        '<div class="team-standings">\n'
        '<p class="ts-empty"><em>Standings will appear once the first matches are scored.</em></p>\n'
        '</div>\n'
    )
    if not os.path.isfile(pickle_path):
        return placeholder
    try:
        df     = pd.read_pickle(pickle_path)
        latest = df.iloc[-1].sort_values(ascending=False)
    except Exception:
        return placeholder

    fname_map = {row['d_name']: row['f_name'] for _, row in members.iterrows()}
    rows = []
    for rank, (name, score) in enumerate(latest.items(), start=1):
        try:
            pts = int(round(float(score)))
        except (ValueError, TypeError):
            continue
        css   = _TS_CLASSES.get(rank, '')
        icon  = _MEDALS.get(rank, str(rank))
        fname = fname_map.get(name)
        name_html = f'<a href="./{fname}.html">{name}</a>' if fname else name
        rows.append(
            f'<div class="ts-row {css}">'
            f'<span class="ts-pos">{icon}</span>'
            f'<span class="ts-name">{name_html}</span>'
            f'<span class="ts-pts">{pts} pts</span>'
            f'</div>\n'
        )
    if not rows:
        return placeholder
    return '<div class="team-standings">\n' + ''.join(rows) + '</div>\n'

def get_team_colors(all_teams):
    """
    Generate one distinct color per team by spacing hues evenly around the
    HSL wheel (360 / N degrees apart).  With N teams there are always exactly
    N unique colors — no cycling, no repetition, regardless of group count.

    S=0.80 L=0.27 keeps every color dark enough for WCAG AA white-text
    contrast while staying vivid enough to be readable in line plots.
    """
    import colorsys
    teams = sorted(all_teams)
    n = len(teams)
    if n == 0:
        return {}
    result = {}
    for i, team in enumerate(teams):
        h = i / n
        r, g, b = colorsys.hls_to_rgb(h, 0.27, 0.80)
        result[team] = '#{:02x}{:02x}{:02x}'.format(
            int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
        )
    return result


def compute_leaderboard(n=10):
    """
    Read every user_df pickle from data/user_dfs/ and return the top-n
    participants sorted by total points as (rank, name, group, score) tuples.
    """
    entries = []
    user_dir = "data/user_dfs"
    if not os.path.isdir(user_dir):
        return []
    for fname in os.listdir(user_dir):
        try:
            df    = pd.read_pickle(os.path.join(user_dir, fname))
            name  = df.at[0, 'd_name']
            f_name = df.at[0, 'f_name']
            group = str(df.at[0, 'Which team(s) do you belong to?']).replace(';', ' &amp; ')
            score = int(round(pd.to_numeric(df.loc[2], errors='coerce').sum()))
            entries.append((name, f_name, group, score))
        except Exception:
            continue
    entries.sort(key=lambda x: x[3], reverse=True)
    return [(i + 1, name, f_name, group, score)
            for i, (name, f_name, group, score) in enumerate(entries[:n])]


def _leaderboard_block(entries):
    if not entries:
        return ['<div class="leaderboard"><p class="lb-empty"><em>No scores yet.</em></p></div>\n']
    rows = []
    for rank, name, f_name, group, score in entries:
        css  = _CLASSES.get(rank, '')
        icon = _MEDALS.get(rank, str(rank))
        link = f'<a href="./pages/{f_name}.html">{name}</a>'
        rows.append(
            f'<div class="lb-row {css}">'
            f'<span class="lb-pos">{icon}</span>'
            f'<span class="lb-info">{link} <small>({group})</small></span>'
            f'<span class="lb-pts">{score} pts</span>'
            f'</div>\n'
        )
    return ['<div class="leaderboard">\n'] + rows + ['</div>\n']


def create_group_pages(predictions_df):
    """
    Write one markdown page per team group at pages/{Slug}.md and
    regenerate _data/groups.yml (includes team color for nav + h1 styling).
    Participant list appears immediately below the section header.
    """
    all_teams = (predictions_df["Which team(s) do you belong to?"]
                 .str.split(";").explode().str.strip().unique())

    colors = get_team_colors(all_teams)

    # _data/groups.yml — consumed by the layout to render the styled nav
    os.makedirs("_data", exist_ok=True)
    with open("_data/groups.yml", "w", encoding="UTF-8") as f:
        for team in sorted(all_teams):
            slug  = team.replace(" ", "_")
            color = colors[team]
            f.write(f'- name: "{team}"\n  slug: "{slug}"\n  color: "{color}"\n')

    # One page per group
    for team in all_teams:
        slug  = team.replace(" ", "_")
        color = colors[team]
        members = predictions_df[
            predictions_df["Which team(s) do you belong to?"].str.contains(team, regex=False)
        ]
        member_lines = "\n".join(
            f"- [{row['d_name']}](./{row['f_name']}.html)"
            for _, row in members.iterrows()
        )
        standings = _standings_html(team, members)
        page = (
            "---\n"
            "layout: default\n"
            f'team_color: "{color}"\n'
            "---\n\n"
            f"# {team}\n\n"
            f"## {team} participants:\n"
            f"{member_lines}\n\n"
            f"{standings}\n"
            f"![{team}](./group_plots/bars_{slug}.svg?raw=true)\n \n"
            f"![{team}](./group_plots/lines_{slug}.svg?raw=true)\n \n"
            "[← Back to standings](../)\n"
        )
        with open(f"pages/{slug}.md", "w", encoding="UTF-8") as f:
            f.write(page)

    print(f"Group pages written: {list(all_teams)}")


def _div_block(css_class, items, empty_msg):
    """Build a <div> block from a list of strings, one <p> per item."""
    if items:
        inner = "".join(f"<p>{item}</p>\n" for item in items)
    else:
        inner = f"<p><em>{empty_msg}</em></p>\n"
    return [f'<div class="{css_class}">\n', inner, '</div>\n']


def update_next_matches_only():
    """
    Refresh both the Next Matches and Yesterday's Results sections in
    index.md on every pipeline run, even when no game results have changed.
    """
    try:
        from get_results import get_upcoming_matches, get_recent_results
        upcoming = get_upcoming_matches()
        recent   = get_recent_results()
    except Exception:
        return  # API unavailable — leave file untouched

    next_block      = _div_block("next-matches",      upcoming,
                                 "No matches scheduled in the next 24 hours.")
    yesterday_block = _div_block("yesterdays-results", recent,
                                 "No results yet.")

    try:
        with open("index.md", "r", encoding="UTF-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return

    new_lines, in_div = [], False
    for line in lines:
        if '<div class="next-matches">' in line:
            in_div = True
            new_lines += next_block
        elif '<div class="yesterdays-results">' in line:
            in_div = True
            new_lines += yesterday_block
        elif '</div>' in line and in_div:
            in_div = False
        elif not in_div:
            new_lines.append(line)

    with open("index.md", "w", encoding="UTF-8") as f:
        f.writelines(new_lines)


def update_pages(predictions_df, todays_schmeichel,
                 upcoming_matches=None, recent_results=None):
    """Write index.md from the template.
    Pass upcoming_matches=[] / recent_results=[] to skip API calls (e.g. tests)."""

    if upcoming_matches is None:
        try:
            from get_results import get_upcoming_matches
            upcoming_matches = get_upcoming_matches()
        except Exception:
            upcoming_matches = []

    if recent_results is None:
        try:
            from get_results import get_recent_results
            recent_results = get_recent_results()
        except Exception:
            recent_results = []

    pages_loc = "./pages"

    with open("index_template.md", "r", encoding="UTF-8") as f:
        content = f.readlines()

    # ── Schmeichel lines ──────────────────────────────────────────────────────
    s_lines = []
    for name in todays_schmeichel.keys():
        link = f"[see their predictions]({pages_loc}/{todays_schmeichel[name]['fname']}.html)"
        pts = int(round(todays_schmeichel[name]['value']))
        s_lines.append(
            f"- {name} with {pts} points"
            f" part of {todays_schmeichel[name]['group']} {link}\n"
        )

    next_block      = _div_block("next-matches",      upcoming_matches,
                                 "No matches scheduled in the next 24 hours.")
    yesterday_block = _div_block("yesterdays-results", recent_results,
                                 "No results yet.")
    lb_block        = _leaderboard_block(compute_leaderboard())

    # ── Insert into template ──────────────────────────────────────────────────
    for i, line in enumerate(content):
        if "# Today's Schmeichel(s):" in line:
            content = content[:i + 1] + s_lines + content[i + 1:]
            break

    for i, line in enumerate(content):
        if "LEADERBOARD" in line:
            content = content[:i] + lb_block + content[i + 1:]
            break

    for i, line in enumerate(content):
        if "NEXT_MATCHES" in line:
            content = content[:i] + next_block + content[i + 1:]
            break

    for i, line in enumerate(content):
        if "YESTERDAY_RESULTS" in line:
            content = content[:i] + yesterday_block + content[i + 1:]
            break

    with open("index.md", "w", encoding="UTF-8") as f:
        f.writelines(content)
