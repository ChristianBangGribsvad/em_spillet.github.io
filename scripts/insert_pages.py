import os
import pandas as pd


def create_group_pages(predictions_df):
    """
    Write one markdown page per team group at pages/{Slug}.md and
    regenerate _data/groups.yml so the Jekyll nav renders from data.
    """
    all_teams = (predictions_df["Which team(s) do you belong to?"]
                 .str.split(";").explode().str.strip().unique())

    # _data/groups.yml — consumed by the layout to render the sticky nav
    os.makedirs("_data", exist_ok=True)
    with open("_data/groups.yml", "w", encoding="UTF-8") as f:
        for team in all_teams:
            slug = team.replace(" ", "_")
            f.write(f'- name: "{team}"\n  slug: "{slug}"\n')

    # One page per group
    for team in all_teams:
        slug = team.replace(" ", "_")
        members = predictions_df[
            predictions_df["Which team(s) do you belong to?"].str.contains(team, regex=False)
        ]
        member_lines = "\n".join(
            f"- [{row['d_name']}](./{row['f_name']}.html)"
            for _, row in members.iterrows()
        )
        page = (
            "---\nlayout: default\n---\n\n"
            f"# {team}\n\n"
            f"![{team}](./group_plots/bars_{slug}.svg?raw=true)\n \n"
            f"![{team}](./group_plots/lines_{slug}.svg?raw=true)\n \n"
            f"![{team}](./group_plots/standing_{slug}.svg?raw=true)\n\n"
            f"## {team} participants:\n"
            f"{member_lines}\n\n"
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

    # ── Insert into template ──────────────────────────────────────────────────
    for i, line in enumerate(content):
        if "# Today's Schmeichel(s):" in line:
            content = content[:i + 1] + s_lines + content[i + 1:]
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
