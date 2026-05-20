# FIFA World Cup 2026 Prediction Game

A football prediction game where friends compete by predicting match results.
Scores update automatically every hour during the tournament and are published as a website.

**Live site:** https://christianbanggribsvad.github.io/em_spillet.github.io/

---

## How it works

1. Participants fill out a **Google Form** before the tournament starts
2. Every hour, a **GitHub Action** fetches the latest match results from an API
3. Predictions are **scored automatically** and the website is updated

---

## Repository structure

```
main.py                 # Main script — runs every hour via GitHub Actions
get_results.py          # Fetches live match results from football-data.org
eval_funcs.py           # Calculates scores for each participant
plot_funcs.py           # Generates SVG charts for the website
create_pages.py         # Creates one page per participant
insert_pages.py         # Builds the homepage (index.md)

data/
  user_dfs/             # One file per participant with their scores over time
  group_dfs/            # One file per team group with group standings over time

pages/
  *.md                  # One page per participant
  user_plots/           # Score charts per participant
  group_plots/          # Standings charts per team group

results/
  data_N.pickle         # Cached API responses (used to detect new results)

test/
  test_pipeline.py      # Integration test — run this to verify everything works
  test_data.csv         # Dummy data for testing (3 participants, all groups)

.github/workflows/
  daily.yaml            # Hourly cron job that runs main.py and commits results
  ci.yaml               # Builds and validates the Jekyll site on every push

index_template.md       # Template for the homepage — edited by insert_pages.py
index.md                # Generated homepage — do not edit manually
WC spillet 2026.csv     # Participant predictions from Google Form
```

---

## Scoring

| Prediction | Points |
|---|---|
| Exact score | 15 |
| Correct result + one team's exact score | 10 |
| Correct result only | 5 |
| One team's exact score only | 2 |
| Group 1st and 2nd place both correct | 7.5 each |
| Group 1st/2nd swapped, or one correct | 5 |
| Tournament top scorer (correct player) | 20 |
| Top scorer goals (exact) | 10 |
| Final winner | 25 |
| Final loser | 15 |
| Final winner/loser swapped | 10 / 5 |

---

## Running locally

```bash
pip install -r requirements.txt
python main.py
```

## Running the test

```bash
python test/test_pipeline.py
```

---

## Data source

Match results from [football-data.org](https://www.football-data.org/) (free tier).
