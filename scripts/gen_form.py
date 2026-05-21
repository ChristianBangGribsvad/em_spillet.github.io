"""
Generates a Google Apps Script (.gs) file that creates the WC 2026 predictions form.

Usage:
    python scripts/gen_form.py

Then:
    1. Go to https://script.google.com and create a new project
    2. Paste the contents of the generated  wc2026_form.gs  into the editor
    3. Click Run → createForm()
    4. The completed form will appear in your Google Drive
"""

import os
import sys
import requests

# ── Config ────────────────────────────────────────────────────────────────────

# Social groups participants can belong to (edit as needed)
SOCIAL_GROUPS = [
    "Danica Ejendomme",
    "European Sperm Bank",
    "Frederiksborg Gymnasium",
    "Friends and Family",
    "GeH Fys",
    "Quantum and Laser Photonics DTU",
]

TOP_SCORER_GOALS = [str(i) for i in range(1, 16)]  # 1–15 goals

# Top scorer candidates (sorted alphabetically for easy navigation)
TOP_SCORER_CANDIDATES = sorted([
    "Aleksandar Mitrovic",
    "Antoine Griezmann",
    "Alvaro Morata",
    "Bukayo Saka",
    "Christian Pulisic",
    "Cody Gakpo",
    "Darwin Nunez",
    "Dusan Vlahovic",
    "Erling Haaland",
    "Ferran Torres",
    "Florian Wirtz",
    "Folarin Balogun",
    "Harry Kane",
    "Julian Alvarez",
    "Jude Bellingham",
    "Karim Benzema",
    "Kylian Mbappe",
    "Lamine Yamal",
    "Lionel Messi",
    "Mohamed Salah",
    "Ollie Watkins",
    "Pedri",
    "Phil Foden",
    "Raphinha",
    "Richarlison",
    "Robert Lewandowski",
    "Romelu Lukaku",
    "Serhou Guirassy",
    "Victor Osimhen",
    "Vinicius Junior",
])

OUTPUT_FILE = "wc2026_form.gs"

# ── API ───────────────────────────────────────────────────────────────────────

def fetch_matches():
    uri = "https://api.football-data.org/v4/competitions/WC/matches"
    headers = {"X-Auth-Token": os.environ.get("FOOTBALL_API_TOKEN", "242e02ff31ea497fbe4b85978fe70b81")}
    response = requests.get(uri, headers=headers)
    response.raise_for_status()
    return response.json()["matches"]

# ── Data extraction ───────────────────────────────────────────────────────────

def extract_groups(matches):
    """Return OrderedDict: group_name → {matches: [(home, away)], teams: [sorted list]}"""
    groups = {}
    for m in matches:
        if m["stage"] != "GROUP_STAGE":
            continue
        letter = m["group"][-1]
        name = f"Group {letter}"
        if name not in groups:
            groups[name] = {"matches": [], "teams": set()}
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]
        groups[name]["matches"].append((home, away))
        groups[name]["teams"].update([home, away])

    # Sort teams within each group alphabetically
    for g in groups.values():
        g["teams"] = sorted(g["teams"])

    return dict(sorted(groups.items()))

# ── Code generation ───────────────────────────────────────────────────────────

def js_str(s):
    return f"'{s.replace(chr(39), chr(92) + chr(39))}'"

def js_choices_from_list(var, items):
    """Return JS expression: [var.createChoice('a'), var.createChoice('b'), ...]"""
    choices = ", ".join(f"{var}.createChoice({js_str(i)})" for i in items)
    return f"[{choices}]"

def generate_gs(groups):
    all_teams = sorted({t for g in groups.values() for t in g["teams"]})
    lines = []

    def w(line=""):
        lines.append(line)

    w("function createForm() {")
    w("  var form = FormApp.create('FIFA World Cup 2026 - Forudsigelser');")
    w("  form.setDescription('Udfyld dine forudsigelser inden turneringen starter den 11. juni 2026.');")
    w()

    # Regex validation — enforces "number - number" format, defined once and reused
    w("  var scoreValidation = FormApp.createTextValidation()")
    w("    .requireTextMatchesPattern('^\\\\d+\\\\s*-\\\\s*\\\\d+$')")
    w("    .build();")
    w()

    # Helper: single text field per match with format validation
    w("  function addMatch(title, homeTeam, awayTeam) {")
    w("    form.addTextItem()")
    w("        .setTitle(title)")
    w("        .setHelpText(homeTeam + ' goals - ' + awayTeam + ' goals  (e.g. 2 - 1)')")
    w("        .setValidation(scoreValidation)")
    w("        .setRequired(true);")
    w("  }")
    w()

    # ── Personal info ──────────────────────────────────────────────────────────
    w("  // ── Personal info ──────────────────────────────────────────────────")
    w("  form.addTextItem().setTitle('First name').setRequired(true);")
    w("  form.addTextItem().setTitle('Last name').setRequired(true);")
    w()

    # ── Social group membership ────────────────────────────────────────────────
    w("  // ── Which team do you belong to? ───────────────────────────────────")
    w("  var tq = form.addCheckboxItem();")
    w("  tq.setTitle('Which team(s) do you belong to?')")
    w("    .setChoices([")
    for sg in SOCIAL_GROUPS:
        w(f"      tq.createChoice({js_str(sg)}),")
    w("    ])")
    w("    .setRequired(true);")
    w()

    # ── Group stage match predictions ──────────────────────────────────────────
    w("  // ── Group stage predictions ─────────────────────────────────────────")
    for group_name, data in groups.items():
        w(f"  form.addSectionHeaderItem().setTitle({js_str(group_name)});")
        for home, away in data["matches"]:
            title = f"{group_name} Predictions [{home} - {away}]"
            w(f"  addMatch({js_str(title)}, {js_str(home)}, {js_str(away)});")
        w()

    # ── Group winner predictions ───────────────────────────────────────────────
    w("  // ── Group winners ───────────────────────────────────────────────────")
    w("  form.addSectionHeaderItem().setTitle('Group winners');")
    for group_name, data in groups.items():
        teams_js = ", ".join(f"q.createChoice({js_str(t)})" for t in data["teams"])
        w(f"  var q = form.addListItem();")
        w(f"  q.setTitle({js_str(group_name + ' 1st place')}).setChoices([{teams_js}]).setRequired(true);")
        w(f"  var q = form.addListItem();")
        w(f"  q.setTitle({js_str(group_name + ' 2nd place')}).setChoices([{teams_js}]).setRequired(true);")
    w()

    # ── Special predictions ────────────────────────────────────────────────────
    w("  // ── Special predictions ─────────────────────────────────────────────")
    w("  form.addSectionHeaderItem().setTitle('Special predictions');")

    all_teams_js = lambda var: ", ".join(f"{var}.createChoice({js_str(t)})" for t in all_teams)

    w(f"  var q = form.addListItem();")
    w(f"  q.setTitle('FIFA World Cup 2026 final winner').setChoices([{all_teams_js('q')}]).setRequired(true);")
    w(f"  var q = form.addListItem();")
    w(f"  q.setTitle('FIFA World Cup 2026 final loser').setChoices([{all_teams_js('q')}]).setRequired(true);")
    w()
    scorer_candidates_js = lambda var: ", ".join(f"{var}.createChoice({js_str(p)})" for p in TOP_SCORER_CANDIDATES)
    w(f"  var q = form.addListItem();")
    w(f"  q.setTitle('Who is going to be the top scorer throughout FIFA World Cup 2026? (20 points)')")
    w(f"   .setChoices([{scorer_candidates_js('q')}])")
    w(f"   .setRequired(true);")
    w()
    scorer_goals_js = lambda var: ", ".join(f"{var}.createChoice({js_str(g)})" for g in TOP_SCORER_GOALS)
    w(f"  var q = form.addListItem();")
    w(f"  q.setTitle('How many goals does the top scorer score? (10 points)')")
    w(f"   .setChoices([{scorer_goals_js('q')}])")
    w(f"   .setRequired(true);")
    w()

    w("  Logger.log('Form created: ' + form.getPublishedUrl());")
    w("  Logger.log('Edit URL:     ' + form.getEditUrl());")
    w("}")

    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("Fetching WC 2026 match schedule from API...")
    matches = fetch_matches()

    groups = extract_groups(matches)
    if not groups:
        print("ERROR: No group stage matches found in API response.")
        print("The tournament schedule may not be published yet.")
        sys.exit(1)

    total_matches = sum(len(g["matches"]) for g in groups.values())
    print(f"Found {len(groups)} groups, {total_matches} group stage matches.")

    gs_code = generate_gs(groups)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(gs_code)

    print(f"\nGenerated: {OUTPUT_FILE}")
    print("\nNext steps:")
    print("  1. Go to https://script.google.com and create a new project")
    print("  2. Delete any existing code and paste the contents of wc2026_form.gs")
    print("  3. Click Run → createForm()")
    print("  4. Grant permissions when prompted (needed to create Forms in your Drive)")
    print("  5. Check the Logs (View → Logs) for the form URL once it finishes")

if __name__ == "__main__":
    main()
