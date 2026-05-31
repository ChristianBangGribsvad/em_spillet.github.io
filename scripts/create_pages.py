import os
import pandas as pd


# ── Point-level helpers ───────────────────────────────────────────────────────

def _pts_class(result, pts):
    if str(result).strip() == '-':
        return 'pts-unplayed'
    try:
        p = float(pts)
    except (TypeError, ValueError):
        return 'pts-unplayed'
    if p >= 15: return 'pts-15'
    if p >= 10: return 'pts-10'
    if p >= 7:  return 'pts-7'   # covers 7.5
    if p >= 5:  return 'pts-5'
    if p >= 2:  return 'pts-2'
    return 'pts-0'


def _badge(result, pts):
    if str(result).strip() == '-':
        label = '&mdash;'
    else:
        try:
            p = float(pts)
            label = str(int(p)) if p == int(p) else str(p)
        except (TypeError, ValueError):
            label = '&mdash;'
    return f'<span class="pts-badge">{label}</span>'


def _pred_row(match_name, pred, result, pts):
    cls   = _pts_class(result, pts)
    p_str = str(pred)   if str(pred)   not in ('nan', 'None', '')  else '&mdash;'
    r_str = str(result) if str(result) not in ('nan', 'None', '-', '') else '&mdash;'
    return (
        f'<div class="pred-row {cls}">'
        f'<span class="pred-match">{match_name}</span>'
        f'<span class="pred-guess">{p_str}</span>'
        f'<span class="pred-result">{r_str}</span>'
        f'{_badge(result, pts)}'
        f'</div>\n'
    )


def _special_label(col):
    c = col.lower()
    if 'final winner' in c:                    return 'Final winner'
    if 'final loser'  in c:                    return 'Final loser'
    if 'top scorer'   in c and 'goals' not in c: return 'Top scorer'
    if 'goals'        in c:                    return 'Scorer goals'
    return col[:40]


# ── Main HTML builder ─────────────────────────────────────────────────────────

def _predictions_html(user_df):
    """
    Build a full HTML predictions table from a scored user_df.
    Row 0 = predictions, row 1 = results ('-' if unplayed), row 2 = points.
    Organised by group (A-L) then special predictions, with a totals footer.
    """
    GROUPS   = [f'Group {c}' for c in 'ABCDEFGHIJKL']
    all_cols = list(user_df.columns[4:-2])   # skip metadata and f/d_name
    sections = []

    for grp in GROUPS:
        grp_cols   = [c for c in all_cols if c.startswith(grp + ' ')]
        match_cols = [c for c in grp_cols if 'Predictions [' in c]
        win_cols   = [c for c in grp_cols if 'place' in c]
        if not grp_cols:
            continue

        rows = []
        for col in match_cols:
            try:
                name = col.split('[', 1)[1].rstrip(']').replace(' - ', ' vs ')
            except IndexError:
                name = col
            rows.append(_pred_row(name,
                                  user_df.at[0, col],
                                  user_df.at[1, col],
                                  user_df.at[2, col]))

        if win_cols:
            rows.append('<div class="pred-divider">Group winners</div>\n')
            for col in win_cols:
                name = col[len(grp):].strip()   # "1st place" / "2nd place"
                rows.append(_pred_row(name,
                                      user_df.at[0, col],
                                      user_df.at[1, col],
                                      user_df.at[2, col]))

        sections.append(
            f'<div class="pred-section">\n'
            f'<div class="pred-section-header">{grp}</div>\n'
            + ''.join(rows)
            + '</div>\n'
        )

    # Special predictions (anything not part of a named group)
    special_cols = [c for c in all_cols
                    if not any(c.startswith(g + ' ') for g in GROUPS)]
    if special_cols:
        rows = [
            _pred_row(_special_label(col),
                      user_df.at[0, col],
                      user_df.at[1, col],
                      user_df.at[2, col])
            for col in special_cols
        ]
        sections.append(
            '<div class="pred-section">\n'
            '<div class="pred-section-header">Special Predictions</div>\n'
            + ''.join(rows)
            + '</div>\n'
        )

    try:
        total = int(round(pd.to_numeric(user_df.loc[2], errors='coerce').sum()))
    except Exception:
        total = 0

    col_header = (
        '<div class="pred-col-header">'
        '<span>Match</span>'
        '<span>Your pick</span>'
        '<span>Result</span>'
        '<span>Pts</span>'
        '</div>\n'
    )
    total_row = (
        '<div class="pred-total">'
        f'Total &nbsp;<span class="pred-total-pts">{total} pts</span>'
        '</div>\n'
    )

    return (
        '<div class="pred-table">\n'
        + col_header
        + ''.join(sections)
        + total_row
        + '</div>\n'
    )


# ── Public function ───────────────────────────────────────────────────────────

def create_pages(predictions_df):
    output_directory = './pages/'

    for _, row in predictions_df.iterrows():
        name     = row['d_name']
        savename = row['f_name']
        group    = row['Which team(s) do you belong to?'].replace(';', ' and ')

        # Load scored user_df if available; fall back to a placeholder
        pickle_path = os.path.join('data', 'user_dfs', savename)
        if os.path.isfile(pickle_path):
            try:
                user_df           = pd.read_pickle(pickle_path)
                predictions_block = _predictions_html(user_df)
            except Exception:
                predictions_block = '<p><em>Could not load predictions data.</em></p>\n'
        else:
            predictions_block = (
                '<p class="pred-placeholder">'
                '<em>Predictions will appear here once matches are scored.</em>'
                '</p>\n'
            )

        markdown_content = (
            '---\nlayout: default\n---\n\n'
            f'# Results of {name} ({group})\n\n'
            f'{predictions_block}\n'
            '[Back](https://christianbanggribsvad.github.io/wc-predictions.github.io/)'
        )

        with open(output_directory + f'{savename}.md', 'w', encoding='UTF-8') as f:
            f.write(markdown_content)

    print("Markdown pages have been created successfully.")
