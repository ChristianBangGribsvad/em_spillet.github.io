import os
import json
import pandas as pd
from loguru import logger


# ── Chart.js template (no rank toggle — used for 3-line personal chart) ───────
_SIMPLE_CHART_TMPL = """\
<div class="chart-wrapper">
<canvas id="CHART_ID"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("CHART_ID");
var data=CHART_DATA;
var hl=null;
data.datasets.forEach(function(ds){ds._c=ds.borderColor;ds._b=ds.backgroundColor;ds._w=ds.borderWidth||2;});
new Chart(el,{
  type:"line",data:data,
  options:{
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:"index",intersect:false},
    plugins:{
      legend:{
        position:"right",labels:{boxWidth:12,padding:12,usePointStyle:true},
        onClick:function(e,item,legend){
          var chart=legend.chart;var idx=item.datasetIndex;
          if(hl===idx){
            data.datasets.forEach(function(ds){ds.borderWidth=ds._w;ds.borderColor=ds._c;ds.backgroundColor=ds._b;});
            hl=null;
          } else {
            data.datasets.forEach(function(ds,i){
              if(i===idx){ds.borderWidth=ds._w+1;ds.borderColor=ds._c;ds.backgroundColor=ds._b;}
              else{ds.borderWidth=1;ds.borderColor="rgba(0,0,0,0.1)";ds.backgroundColor="rgba(0,0,0,0.02)";}
            });
            hl=idx;
          }
          chart.update();
        }
      },
      tooltip:{callbacks:{label:function(c){return c.dataset.label+": "+Math.round(c.raw)+" pts";}}}
    },
    scales:{
      x:{grid:{color:"rgba(0,0,0,0.05)"},ticks:{maxTicksLimit:10}},
      y:{beginAtZero:true,title:{display:true,text:"Points"},grid:{color:"rgba(0,0,0,0.05)"}}
    }
  }
});
})()
</script>
"""


# ── Context data helpers ──────────────────────────────────────────────────────

def _ordinal(n):
    """Return e.g. '1st', '2nd', '3rd', '4th'."""
    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10 if n % 100 not in (11, 12, 13) else 0, 'th')
    return f'{n}{suffix}'


def _load_all_group_combined():
    """
    Load every group_df and return a deduplicated DataFrame:
    index = dates, columns = unique participant names.
    If a participant appears in multiple teams their score is identical — first wins.
    """
    gdir = os.path.join('data', 'group_dfs')
    if not os.path.isdir(gdir):
        return None
    all_series = {}
    for fname in os.listdir(gdir):
        try:
            df = pd.read_pickle(os.path.join(gdir, fname))
            for col in df.columns:
                if col not in all_series:
                    all_series[col] = df[col]
        except Exception:
            continue
    if not all_series:
        return None
    # ffill: participants who scored 0 in a round have no new row — fill forward
    # so all participants share the same date index and comparisons are consistent.
    return pd.DataFrame(all_series).ffill()


def _participant_context(f_name, d_name, group_name):
    """
    Return a dict of all stats needed for the three personal-section features,
    or None when there is not enough data yet (pre-tournament).
    """
    # ── Global totals + rank ──────────────────────────────────────────────────
    udir = os.path.join('data', 'user_dfs')
    if not os.path.isdir(udir):
        return None
    totals = []
    for fname in os.listdir(udir):
        try:
            df    = pd.read_pickle(os.path.join(udir, fname))
            name  = df.at[0, 'd_name']
            fn    = df.at[0, 'f_name']
            score = int(round(pd.to_numeric(df.loc[2], errors='coerce').sum()))
            totals.append((name, fn, score))
        except Exception:
            continue
    if not totals:
        return None
    totals.sort(key=lambda x: x[2], reverse=True)
    n_total  = len(totals)
    rank     = next((i + 1 for i, (_, fn, _) in enumerate(totals) if fn == f_name), None)
    if rank is None:
        return None
    my_total = next((s for _, fn, s in totals if fn == f_name), 0)
    beat_pct = round((n_total - rank) / n_total * 100)

    # ── Per-round combined data ───────────────────────────────────────────────
    combined = _load_all_group_combined()
    if combined is None or d_name not in combined.columns or combined.empty:
        return {
            'rank': rank, 'n_total': n_total, 'beat_pct': beat_pct,
            'my_total': my_total, 'has_rounds': False,
        }

    dates      = [str(d) for d in combined.index.tolist()]
    my_vals    = [round(float(v), 1) for v in combined[d_name].values]
    global_avg = combined.mean(axis=1)
    global_vals = [round(float(v), 1) for v in global_avg.values]

    # Team average from group_avg pickle
    first_team = group_name.split(';')[0].strip()
    team_vals  = None
    avg_path   = os.path.join('data', 'group_avg')
    if os.path.isfile(avg_path):
        try:
            df_avg = pd.read_pickle(avg_path)
            if first_team in df_avg.columns:
                team_vals = [round(float(v), 1) for v in df_avg[first_team].values]
        except Exception:
            pass

    # ── Last-round stats (need ≥ 2 scoring runs) ─────────────────────────────
    last_round_pts = global_avg_last = rank_movement = None
    # Team average for last round and team-pool rank
    team_avg_last = None
    if team_vals and len(team_vals) >= 2:
        team_avg_last = round(team_vals[-1] - team_vals[-2], 1)

    # Build the pool of unique participants across ALL teams this person belongs to
    team_names_list = [t.strip() for t in group_name.split(';')]
    gdir = os.path.join('data', 'group_dfs')
    team_pool_names = set()
    if os.path.isdir(gdir):
        for team in team_names_list:
            try:
                df_t = pd.read_pickle(os.path.join(gdir, team))
                team_pool_names.update(df_t.columns.tolist())
            except Exception:
                pass
    team_pool = sorted(team_pool_names)
    n_team    = len(team_pool)

    last_round_pts = global_avg_last = rank_movement = None
    curr_rank = rank   # fallback: use global rank from user_dfs totals
    curr_team_rank = team_rank_movement = None

    if len(combined) >= 2:
        my_last         = float(combined[d_name].iloc[-1] - combined[d_name].iloc[-2])
        deltas          = combined.iloc[-1] - combined.iloc[-2]
        last_round_pts  = round(my_last, 1)
        global_avg_last = round(float(deltas.mean()), 1)

        prev_rank = int(combined.iloc[-2].rank(ascending=False, method='min')[d_name])
        curr_rank = int(combined.iloc[-1].rank(ascending=False, method='min')[d_name])
        rank_movement = prev_rank - curr_rank   # positive = moved up

        # Team-pool rank
        team_pool_cols = [p for p in team_pool if p in combined.columns]
        if d_name in team_pool_cols:
            prev_team_rank = int(combined[team_pool_cols].iloc[-2]
                                 .rank(ascending=False, method='min')[d_name])
            curr_team_rank = int(combined[team_pool_cols].iloc[-1]
                                 .rank(ascending=False, method='min')[d_name])
            team_rank_movement = prev_team_rank - curr_team_rank
        else:
            curr_team_rank = team_rank_movement = None

    return {
        'rank': rank, 'n_total': n_total, 'beat_pct': beat_pct,
        'my_total': my_total, 'has_rounds': True,
        'dates': dates, 'my_vals': my_vals,
        'global_vals': global_vals, 'team_vals': team_vals,
        'last_round_pts': last_round_pts,
        'global_avg_last': global_avg_last,
        'team_avg_last': team_avg_last,
        'rank_movement': rank_movement,
        'curr_rank': curr_rank,
        'team_names_list': team_names_list,
        'n_team': n_team,
        'curr_team_rank': curr_team_rank,
        'team_rank_movement': team_rank_movement,
    }


# ── HTML/JS generators ────────────────────────────────────────────────────────

def _stat_cards_html(ctx):
    """Two stat cards: global rank + last-round comparison."""
    rank     = ctx['rank']
    n_total  = ctx['n_total']
    beat_pct = ctx['beat_pct']

    card1 = (
        '<div class="stat-card">'
        '<span class="stat-icon">🏆</span>'
        '<div class="stat-body">'
        f'<span class="stat-main">#{_ordinal(rank)} out of {n_total} players across the game</span>'
        f'<span class="stat-sub">You beat {beat_pct}% of all players</span>'
        '</div></div>\n'
    )

    if ctx.get('last_round_pts') is not None:
        my_pts       = ctx['last_round_pts']
        global_avg   = ctx['global_avg_last']
        team_avg     = ctx.get('team_avg_last')
        diff_global  = round(my_pts - global_avg, 1)
        move         = ctx['rank_movement']

        if diff_global > 0:
            arrow, arrow_cls = '↑', 'stat-up'
        elif diff_global < 0:
            arrow, arrow_cls = '↓', 'stat-down'
        else:
            arrow, arrow_cls = '→', ''

        def _fmt(diff):
            return f'+{int(diff)}' if diff > 0 else str(int(diff))

        if move and move > 0:
            move_str = f'Moved up {move} place{"s" if move > 1 else ""}'
        elif move and move < 0:
            move_str = f'Moved down {abs(move)} place{"s" if abs(move) > 1 else ""}'
        else:
            move_str = 'Position unchanged'

        curr_rank      = ctx.get('curr_rank', rank)
        n_total_ctx    = ctx['n_total']
        line1 = (f'{_fmt(diff_global)} pts vs global avg ({int(global_avg)} pts)'
                 f' &middot; {move_str}'
                 f' &middot; {_ordinal(curr_rank)} out of {n_total_ctx} total players')

        if False:  # team avg line removed — too verbose with multiple team names
            pass
        else:
            sub = line1

        card2 = (
            '<div class="stat-card">'
            f'<span class="stat-icon {arrow_cls}">{arrow}</span>'
            '<div class="stat-body">'
            f'<span class="stat-main">{int(my_pts)} pts last round</span>'
            f'<span class="stat-sub">{sub}</span>'
            '</div></div>\n'
        )
    else:
        card2 = (
            '<div class="stat-card">'
            '<span class="stat-icon">⏳</span>'
            '<div class="stat-body">'
            '<span class="stat-main">Last round</span>'
            '<span class="stat-sub">Available after two scoring updates</span>'
            '</div></div>\n'
        )

    return '<div class="stat-cards">\n' + card1 + card2 + '</div>\n'


def _personal_chart_js(slug, ctx, team_color):
    """Chart.js line chart: your score vs global and team averages."""
    if not ctx.get('has_rounds') or not ctx.get('dates'):
        return ''

    YOU_COLOR = '#1e40af'   # deep blue — instantly reads as "me"
    r, g, b   = int(team_color[1:3], 16), int(team_color[3:5], 16), int(team_color[5:7], 16)

    datasets = [
        {
            'label': 'Your score',
            'data': ctx['my_vals'],
            'borderColor': YOU_COLOR,
            'backgroundColor': 'rgba(30,64,175,0.08)',
            'borderWidth': 3,
            'tension': 0.3,
            'pointRadius': 6,
            'pointHoverRadius': 9,
            'fill': True,
            'order': 1,
        },
        {
            'label': 'Global average',
            'data': ctx['global_vals'],
            'borderColor': 'rgba(0,0,0,0.28)',
            'backgroundColor': 'rgba(0,0,0,0.02)',
            'borderWidth': 1.5,
            'borderDash': [5, 5],
            'tension': 0.3,
            'pointRadius': 3,
            'pointHoverRadius': 5,
            'fill': False,
            'order': 3,
        },
    ]

    if ctx.get('team_vals'):
        datasets.insert(1, {
            'label': 'Team average',
            'data': ctx['team_vals'],
            'borderColor': team_color,
            'backgroundColor': f'rgba({r},{g},{b},0.04)',
            'borderWidth': 1.5,
            'borderDash': [3, 3],
            'tension': 0.3,
            'pointRadius': 3,
            'pointHoverRadius': 5,
            'fill': False,
            'order': 2,
        })

    chart_data = json.dumps({'labels': ctx['dates'], 'datasets': datasets})
    return _SIMPLE_CHART_TMPL.replace('CHART_ID', f'personal-{slug}').replace('CHART_DATA', chart_data)


# ── Per-match badge helpers ───────────────────────────────────────────────────

_BADGE_DEFS = {
    'gem':     ('💎', 'Hidden Gem',            'mb-gem'),
    'crystal': ('🔮', 'Crystal Ball',          'mb-crystal'),
    'rarem':   ('😬', 'Rare Miss',             'mb-rarem'),
    'nobody':  ('💀', 'Nobody Saw That Coming','mb-nobody'),
}


def _compute_match_stats():
    """
    Load all user_dfs and return per-match outcome/exact-score counts.
    Returns {col_name: {'n': total_participants, 'outcome': int, 'exact': int}}
    Only includes columns where the match has been played.
    """
    udir = os.path.join('data', 'user_dfs')
    if not os.path.isdir(udir):
        return {}

    all_dfs = []
    for fname in os.listdir(udir):
        if fname.startswith('.'):
            continue
        try:
            all_dfs.append(pd.read_pickle(os.path.join(udir, fname)))
        except Exception:
            continue

    if not all_dfs:
        return {}

    n_total = len(all_dfs)
    stats = {}

    match_cols = {col for df in all_dfs for col in df.columns if 'Predictions [' in col}

    def _outcome(h, a):
        return 'H' if h > a else ('A' if h < a else 'D')

    for col in match_cols:
        # Determine actual result from first df that has a real result
        rh = ra = None
        for df in all_dfs:
            if col not in df.columns:
                continue
            res = str(df.at[1, col]).strip()
            if res in ('-', 'nan', 'None', ''):
                continue
            try:
                parts = res.replace(' ', '').split('-')
                rh, ra = int(parts[0]), int(parts[1])
                break
            except (ValueError, IndexError):
                continue
        if rh is None:
            continue  # unplayed

        real_out = _outcome(rh, ra)
        outcome_n = exact_n = 0

        for df in all_dfs:
            if col not in df.columns:
                continue
            pred = str(df.at[0, col]).strip()
            if pred in ('nan', 'None', '-', ''):
                continue
            try:
                pp = pred.replace(' ', '').split('-')
                ph, pa = int(pp[0]), int(pp[1])
            except (ValueError, IndexError):
                continue
            if _outcome(ph, pa) == real_out:
                outcome_n += 1
            if ph == rh and pa == ra:
                exact_n += 1

        stats[col] = {'n': n_total, 'outcome': outcome_n, 'exact': exact_n}

    return stats


def _match_badge_html(col, my_pred, my_result, match_stats):
    """Return a badge anchor element for this match, or empty string."""
    s = match_stats.get(col)
    if not s:
        return ''
    n = s['n']
    if n == 0:
        return ''

    res_str  = str(my_result).strip()
    pred_str = str(my_pred).strip()
    if res_str  in ('-', 'nan', 'None', ''):
        return ''
    if pred_str in ('nan', 'None', '-', ''):
        return ''

    try:
        rh, ra = [int(x) for x in res_str.replace(' ', '').split('-')]
        ph, pa = [int(x) for x in pred_str.replace(' ', '').split('-')]
    except (ValueError, IndexError):
        return ''

    def _out(h, a):
        return 'H' if h > a else ('A' if h < a else 'D')

    i_exact   = (ph == rh and pa == ra)
    i_correct = (_out(ph, pa) == _out(rh, ra))
    pct_ok    = s['outcome'] / n

    badge_key = None
    if i_exact and s['exact'] / n <= 0.10:
        badge_key = 'gem'
    elif i_correct and pct_ok <= 0.25:
        badge_key = 'crystal'
    elif not i_correct and pct_ok >= 0.80:
        badge_key = 'rarem'
    elif not i_correct and pct_ok <= 0.10:
        badge_key = 'nobody'

    if badge_key is None:
        return ''

    emoji, label, css_cls = _BADGE_DEFS[badge_key]
    return (
        f'<a href="./rules.html#match-badges" class="match-badge {css_cls}" '
        f'target="_blank" rel="noopener">{emoji} {label}</a>\n'
    )


# ── Predictions table helpers ─────────────────────────────────────────────────

def _pts_class(result, pts):
    if str(result).strip() == '-':
        return 'pts-unplayed'
    try:
        p = float(pts)
    except (TypeError, ValueError):
        return 'pts-unplayed'
    if p >= 15: return 'pts-15'
    if p >= 10: return 'pts-10'
    if p >= 7:  return 'pts-7'
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
    p_str = str(pred)   if str(pred)   not in ('nan', 'None', '')      else '&mdash;'
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
    if 'final winner' in c:                       return 'Final winner'
    if 'final loser'  in c:                       return 'Final loser'
    if 'top scorer'   in c and 'goals' not in c:  return 'Top scorer'
    if 'goals'        in c:                       return 'Scorer goals'
    return col[:40]


def _predictions_html(user_df, match_stats=None):
    GROUPS   = [f'Group {c}' for c in 'ABCDEFGHIJKL']
    all_cols = list(user_df.columns[4:-2])
    sections = []

    badge_counts = {k: 0 for k in _BADGE_DEFS}

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
            rows.append(_pred_row(name, user_df.at[0,col], user_df.at[1,col], user_df.at[2,col]))
            if match_stats is not None:
                badge = _match_badge_html(col, user_df.at[0,col], user_df.at[1,col], match_stats)
                if badge:
                    for key, (_, _, css_cls) in _BADGE_DEFS.items():
                        if css_cls in badge:
                            badge_counts[key] += 1
                            break
                    rows.append(badge)
        if win_cols:
            rows.append('<div class="pred-divider">Group winners</div>\n')
            # Combine 1st and 2nd into one row showing the total
            col_1 = next((c for c in win_cols if '1st' in c), win_cols[0])
            col_2 = next((c for c in win_cols if '2nd' in c), win_cols[-1])
            def _gs(val):
                s = str(val)
                return s if s not in ('nan', 'None', '') else '—'
            p1, p2 = _gs(user_df.at[0, col_1]), _gs(user_df.at[0, col_2])
            r1, r2 = _gs(user_df.at[1, col_1]), _gs(user_df.at[1, col_2])
            combined_pred = f'{p1} / {p2}'
            combined_res  = f'{r1} / {r2}' if r1 not in ('—', '-') else '-'
            combined_pts  = user_df.at[2, col_1] + user_df.at[2, col_2]
            rows.append(_pred_row('1st &amp; 2nd place', combined_pred, combined_res, combined_pts))
        sections.append(
            f'<div class="pred-section">\n'
            f'<div class="pred-section-header">{grp}</div>\n'
            + ''.join(rows) + '</div>\n'
        )

    special_cols = [c for c in all_cols if not any(c.startswith(g + ' ') for g in GROUPS)]
    if special_cols:
        rows = [_pred_row(_special_label(col),
                          user_df.at[0,col], user_df.at[1,col], user_df.at[2,col])
                for col in special_cols]
        sections.append(
            '<div class="pred-section">\n'
            '<div class="pred-section-header">Special Predictions</div>\n'
            + ''.join(rows) + '</div>\n'
        )

    pts_row = pd.to_numeric(user_df.loc[2], errors='coerce')

    match_cols  = [c for c in all_cols if 'Predictions [' in c]
    winner_cols = [c for c in all_cols if 'place' in c]
    special_cols_all = [c for c in all_cols
                        if not any(c.startswith(g + ' ') for g in GROUPS)]

    match_pts   = int(round(pts_row[match_cols].sum()))
    winner_pts  = int(round(pts_row[winner_cols].sum()))
    special_pts = int(round(pts_row[special_cols_all].sum()))
    total       = match_pts + winner_pts + special_pts

    breakdown = (
        '<div class="pred-breakdown">'
        f'Group matches: <strong>{match_pts} pts</strong>'
        f' &nbsp;&middot;&nbsp; '
        f'Group winners: <strong>{winner_pts} pts</strong>'
        f' &nbsp;&middot;&nbsp; '
        f'Special predictions: <strong>{special_pts} pts</strong>'
        '</div>\n'
    )

    badge_parts = [
        f'{emoji}&thinsp;&times;{badge_counts[key]}'
        for key, (emoji, _, _) in _BADGE_DEFS.items()
        if badge_counts[key] > 0
    ]
    badge_summary = (
        '<div class="pred-badge-summary">'
        + ' &nbsp;&middot;&nbsp; '.join(badge_parts)
        + '</div>\n'
    ) if badge_parts else ''

    total_row = (
        '<div class="pred-total">'
        f'Total &nbsp;<span class="pred-total-pts">{total} pts</span>'
        '</div>\n'
    )
    col_header = (
        '<div class="pred-col-header">'
        '<span>Match</span><span>Your pick</span><span>Result</span><span>Pts</span>'
        '</div>\n'
    )
    return (
        '<div class="pred-table">\n'
        + breakdown
        + badge_summary
        + total_row
        + col_header
        + ''.join(sections)
        + '</div>\n'
    )


# ── Public function ───────────────────────────────────────────────────────────

def create_pages(predictions_df):
    from insert_pages import get_team_colors

    output_directory = './pages/'

    # Pre-compute match stats once (for per-match badges)
    match_stats = _compute_match_stats()

    # Pre-compute team colors for all teams (for the personal chart)
    all_teams = (predictions_df['Which team(s) do you belong to?']
                 .str.split(';').explode().str.strip().unique())
    team_colors = get_team_colors(all_teams)

    for _, row in predictions_df.iterrows():
        name     = row['d_name']
        savename = row['f_name']
        group    = row['Which team(s) do you belong to?'].replace(';', ' and ')
        first_team = row['Which team(s) do you belong to?'].split(';')[0].strip()
        team_color = team_colors.get(first_team, '#1a3a2a')

        # ── Personal context (rank, last round, chart data) ───────────────
        ctx = _participant_context(savename, name, row['Which team(s) do you belong to?'])

        personal_section = ''
        if ctx:
            stat_cards = _stat_cards_html(ctx)
            chart = _personal_chart_js(savename, ctx, team_color)
            if chart:
                personal_section = (
                    stat_cards
                    + '## Your score vs averages\n\n'
                    + chart
                    + '\n'
                )
            else:
                personal_section = stat_cards

        # ── Predictions table ─────────────────────────────────────────────
        pickle_path = os.path.join('data', 'user_dfs', savename)
        if os.path.isfile(pickle_path):
            try:
                user_df           = pd.read_pickle(pickle_path)
                predictions_block = _predictions_html(user_df, match_stats)
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
            f'{personal_section}'
            '## Your predictions\n\n'
            f'{predictions_block}\n'
            '[Back](https://christianbanggribsvad.github.io/wc-predictions.github.io/)'
        )

        with open(output_directory + f'{savename}.md', 'w', encoding='UTF-8') as f:
            f.write(markdown_content)

    logger.info(f"[PAGES] Participant pages created ({len(predictions_df)} participants)")
