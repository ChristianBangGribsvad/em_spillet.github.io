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


def update_pages(predictions_df, todays_schmeichel):
    """Write index.md with today's Schmeichel section only.
    Group data lives on the dedicated per-group pages; the front page is kept clean."""

    pages_loc = "./pages"

    with open("index_template.md", "r", encoding="UTF-8") as f:
        content = f.readlines()

    s_lines = []
    for name in todays_schmeichel.keys():
        link = f"[see their predictions]({pages_loc}/{todays_schmeichel[name]['fname']}.html)"
        s_lines.append(
            f"- {name} with {todays_schmeichel[name]['value']} points"
            f" part of {todays_schmeichel[name]['group']} {link}\n"
        )

    for i, line in enumerate(content):
        if "# Today's Schmeichel(s):" in line:
            content = content[:i + 1] + s_lines + content[i + 1:]
            break

    with open("index.md", "w", encoding="UTF-8") as f:
        f.writelines(content)
