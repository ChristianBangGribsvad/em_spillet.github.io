import os
import json
import colorsys
import pandas as pd
from loguru import logger

# ── Chart.js HTML template ────────────────────────────────────────────────────
# CHART_ID and CHART_DATA are replaced at build time; all { } are JS literals.
_CHART_TMPL = """\
<div class="chart-wrapper">
<div class="chart-controls">
<button id="CHART_ID-toggle" class="chart-toggle">Show Rank</button>
</div>
<canvas id="CHART_ID"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("CHART_ID");
var btn=document.getElementById("CHART_ID-toggle");
var data=CHART_DATA;
var N=data.datasets.length;

/* store original colours for highlight/reset */
data.datasets.forEach(function(ds){ds._c=ds.borderColor;ds._b=ds.backgroundColor;});

/* pre-compute rank at each time point (1 = highest score) */
var pts=data.datasets.map(function(ds){return ds.data.slice();});
var rnk=pts.map(function(myPts,di){
  return myPts.map(function(v,li){
    var r=1;pts.forEach(function(op,oi){if(oi!==di&&op[li]>v)r++;});return r;
  });
});

var hl=null,isRank=false;

function resetHL(){
  data.datasets.forEach(function(ds){
    ds.borderWidth=2.5;ds.borderColor=ds._c;ds.backgroundColor=ds._b;
  });
  hl=null;
}

var chart=new Chart(el,{
  type:"line",data:data,
  options:{
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:"index",intersect:false},
    plugins:{
      legend:{
        position:"right",
        labels:{boxWidth:12,padding:12,usePointStyle:true},
        /* click legend entry to highlight one line, click again to reset */
        onClick:function(e,item){
          var idx=item.datasetIndex;
          if(hl===idx){resetHL();}
          else{
            data.datasets.forEach(function(ds,i){
              if(i===idx){ds.borderWidth=4;ds.borderColor=ds._c;ds.backgroundColor=ds._b;}
              else{ds.borderWidth=1;ds.borderColor="rgba(0,0,0,0.1)";ds.backgroundColor="rgba(0,0,0,0.02)";}
            });
            hl=idx;
          }
          chart.update();
        }
      },
      tooltip:{callbacks:{label:function(c){
        return c.dataset.label+": "+(isRank?"#"+Math.round(c.raw):Math.round(c.raw)+" pts");
      }}}
    },
    scales:{
      x:{grid:{color:"rgba(0,0,0,0.05)"},ticks:{maxTicksLimit:10}},
      y:{beginAtZero:true,title:{display:true,text:"Points"},grid:{color:"rgba(0,0,0,0.05)"}}
    }
  }
});

/* toggle between Points and Rank views */
btn.addEventListener("click",function(){
  isRank=!isRank;
  resetHL();
  data.datasets.forEach(function(ds,i){
    ds.data=isRank?rnk[i]:pts[i];
    ds.tension=isRank?0:0.3;
    ds.fill=!isRank;
  });
  var y=chart.options.scales.y;
  if(isRank){
    y.reverse=true;y.beginAtZero=false;y.min=0.5;y.max=N+0.5;
    y.title.text="Position";
    y.ticks={stepSize:1,callback:function(v){return v%1===0?"#"+v:"";}};
  } else {
    y.reverse=false;y.beginAtZero=true;y.min=undefined;y.max=undefined;
    y.title.text="Points";y.ticks={};
  }
  btn.textContent=isRank?"Show Points":"Show Rank";
  btn.classList.toggle("active",isRank);
  chart.update();
});
})()
</script>
"""


def _build_chart(chart_id, chart_data_json):
    """Stamp chart_id and JSON data into the line-chart template."""
    return _CHART_TMPL.replace('CHART_ID', chart_id).replace('CHART_DATA', chart_data_json)


# ── Best-round horizontal bar chart template ──────────────────────────────────
_BAR_TMPL = """\
<div class="chart-wrapper" style="height:HEIGHTpx">
<canvas id="CHART_ID"></canvas>
</div>
<script>
(function(){
var d=CHART_DATA;
new Chart(document.getElementById("CHART_ID"),{
  type:"bar",
  data:{
    labels:d.labels,
    datasets:[{data:d.values,backgroundColor:d.colors,borderRadius:5,borderWidth:0}]
  },
  options:{
    indexAxis:"y",responsive:true,maintainAspectRatio:false,
    plugins:{
      legend:{display:false},
      title:{display:true,text:d.title,color:"#666",
             font:{family:"Inter,system-ui,sans-serif",size:11},padding:{bottom:6}},
      tooltip:{callbacks:{label:function(c){return " "+Math.round(c.raw)+" pts";}}}
    },
    scales:{
      x:{beginAtZero:true,
         title:{display:true,text:"Points earned",font:{size:11}},
         grid:{color:"rgba(0,0,0,0.05)"}},
      y:{grid:{display:false},ticks:{font:{family:"Inter,system-ui,sans-serif",size:11}}}
    }
  }
});
})()
</script>
"""


def _build_bar_chart(chart_id, chart_data_json, height):
    """Stamp id, JSON data, and pixel height into the bar-chart template."""
    return (_BAR_TMPL
            .replace('CHART_ID', chart_id)
            .replace('CHART_DATA', chart_data_json)
            .replace('HEIGHT', str(height)))


def _hex_to_rgba(hex_color, alpha):
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    return f'rgba({r},{g},{b},{alpha})'


def _make_dataset(label, values, color):
    return {
        'label': label,
        'data': values,
        'borderColor': color,
        'backgroundColor': _hex_to_rgba(color, 0.08),
        'tension': 0.3,
        'pointRadius': 5,
        'pointHoverRadius': 8,
        'borderWidth': 2.5,
        'fill': True,
    }


def _participant_colors(participants):
    """Distinct line colors for individual participants within a chart."""
    n = len(participants)
    result = {}
    for i, name in enumerate(sorted(participants)):
        h = i / n if n > 1 else 0.0
        r, g, b = colorsys.hls_to_rgb(h, 0.38, 0.72)
        result[name] = '#{:02x}{:02x}{:02x}'.format(
            int(round(r * 255)), int(round(g * 255)), int(round(b * 255))
        )
    return result


def _participant_chart_js(slug, df_grp, members):
    """Chart.js line chart for participant progress within a team."""
    if df_grp is None or df_grp.empty:
        return '<p class="chart-placeholder"><em>Chart will appear once matches are scored.</em></p>\n'
    df_grp = df_grp.ffill()   # fill gaps for participants who scored 0 in a round
    labels   = [str(d) for d in df_grp.index.tolist()]
    colors   = _participant_colors(list(df_grp.columns))
    datasets = [
        _make_dataset(name,
                      [round(float(df_grp.at[d, name]), 1) for d in df_grp.index],
                      colors[name])
        for name in df_grp.columns
    ]
    return _build_chart(f'chart-{slug}', json.dumps({'labels': labels, 'datasets': datasets}))


def _best_round_chart_js(slug, df_grp):
    """
    Horizontal bar chart: points each participant earned in the latest round.
    Bars are sorted descending (top scorer at top), colored per participant.
    Only rendered when at least two scoring runs exist.
    """
    if df_grp is None or df_grp.empty or len(df_grp) < 2:
        return (
            '<p class="chart-placeholder">'
            '<em>Best round chart appears after the first two scoring updates.</em>'
            '</p>\n'
        )
    df_grp = df_grp.ffill()   # fill gaps for participants who scored 0 in a round
    delta  = (df_grp.iloc[-1] - df_grp.iloc[-2]).sort_values(ascending=False)
    colors = _participant_colors(list(df_grp.columns))
    title  = f'Points earned → {df_grp.index[-2]} to {df_grp.index[-1]}'
    chart_data = json.dumps({
        'labels': list(delta.index),
        'values': [round(float(v), 1) for v in delta.values],
        'colors': [colors.get(n, '#1a3a2a') for n in delta.index],
        'title':  title,
    })
    # Height scales with the number of participants
    height = max(120, len(delta) * 52 + 70)
    return _build_bar_chart(f'bar-{slug}', chart_data, height)


def _team_avg_chart_js(df_avg, team_colors):
    """Chart.js line chart for the Team vs Team (group_avg) view."""
    if df_avg is None or df_avg.empty:
        return '<p class="chart-placeholder"><em>Chart will appear once matches are scored.</em></p>\n'
    df_avg = df_avg.ffill()   # fill gaps for rounds with no new results
    labels   = [str(d) for d in df_avg.index.tolist()]
    datasets = [
        _make_dataset(team,
                      [round(float(df_avg.at[d, team]), 1) for d in df_avg.index],
                      team_colors.get(team, '#1a3a2a'))
        for team in df_avg.columns
    ]
    return _build_chart('chart-team-vs-team', json.dumps({'labels': labels, 'datasets': datasets}))

_MEDALS     = {1: '🥇', 2: '🥈', 3: '🥉'}
_CLASSES    = {1: 'lb-gold',  2: 'lb-silver',  3: 'lb-bronze'}
_TS_CLASSES = {1: 'ts-gold',  2: 'ts-silver',  3: 'ts-bronze'}


def _standings_html(team, members, df_grp=None):
    """
    Return an HTML standings block for a team.
    df_grp: already-loaded group DataFrame (pass None to load from pickle).
    """
    placeholder = (
        '<div class="team-standings">\n'
        '<p class="ts-empty"><em>Standings will appear once the first matches are scored.</em></p>\n'
        '</div>\n'
    )
    if df_grp is None:
        pickle_path = os.path.join("data", "group_dfs", team)
        if not os.path.isfile(pickle_path):
            return placeholder
        try:
            df_grp = pd.read_pickle(pickle_path)
        except Exception:
            return placeholder
    if df_grp.empty:
        return placeholder
    try:
        latest = df_grp.iloc[-1].sort_values(ascending=False)
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
        # Load group_df once; share between standings and chart
        pickle_path = os.path.join("data", "group_dfs", team)
        df_grp = None
        if os.path.isfile(pickle_path):
            try:
                df_grp = pd.read_pickle(pickle_path)
            except Exception:
                pass

        standings  = _standings_html(team, members, df_grp=df_grp)
        line_chart = _participant_chart_js(slug, df_grp, members)
        bar_chart  = _best_round_chart_js(slug, df_grp)

        page = (
            "---\n"
            "layout: default\n"
            f'team_color: "{color}"\n'
            "---\n\n"
            f"# {team}\n\n"
            f"## {team} participants:\n"
            f"{member_lines}\n\n"
            f"{standings}\n"
            "## Score progression\n\n"
            f"{line_chart}\n"
            "## Points earned — latest round\n\n"
            f"{bar_chart}\n"
            "[← Back to standings](../)\n"
        )
        with open(f"pages/{slug}.md", "w", encoding="UTF-8") as f:
            f.write(page)

    logger.info(f"[PAGES] Group pages written: {sorted(all_teams)}")


def _div_block(css_class, items, empty_msg):
    """Build a <div> block from a list of strings, one <p> per item."""
    if items:
        inner = "".join(f"<p>{item}</p>\n" for item in items)
    else:
        inner = f"<p><em>{empty_msg}</em></p>\n"
    return [f'<div class="{css_class}">\n', inner, '</div>\n']


def update_next_matches_only(raw_matches=None):
    """
    Refresh both the Next Matches and Yesterday's Results sections in
    index.md on every pipeline run, even when no game results have changed.
    Pass raw_matches=fetch_raw_matches() to avoid a redundant API call.
    """
    try:
        from get_results import get_upcoming_matches, get_recent_results
        upcoming = get_upcoming_matches(raw_matches)
        recent   = get_recent_results(raw_matches)
    except Exception:
        return  # API unavailable — leave file untouched

    logger.info(f"[SCHEDULE] Upcoming: {len(upcoming)} matches | Recent results: {len(recent)}")
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
                 upcoming_matches=None, recent_results=None, raw_matches=None):
    """Write index.md from the template.
    Pass upcoming_matches=[] / recent_results=[] to skip API calls (e.g. tests).
    Pass raw_matches=fetch_raw_matches() to reuse an already-fetched API response."""

    if upcoming_matches is None:
        try:
            from get_results import get_upcoming_matches
            upcoming_matches = get_upcoming_matches(raw_matches)
        except Exception:
            upcoming_matches = []

    if recent_results is None:
        try:
            from get_results import get_recent_results
            recent_results = get_recent_results(raw_matches)
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

    # Team vs Team chart
    avg_path = os.path.join("data", "group_avg")
    if os.path.isfile(avg_path):
        try:
            df_avg     = pd.read_pickle(avg_path)
            avg_teams  = list(df_avg.columns)
            team_chart = _team_avg_chart_js(df_avg, get_team_colors(avg_teams))
        except Exception:
            team_chart = '<p class="chart-placeholder"><em>Chart could not be loaded.</em></p>\n'
    else:
        team_chart = '<p class="chart-placeholder"><em>Chart will appear once matches are scored.</em></p>\n'

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

    for i, line in enumerate(content):
        if "TEAM_CHART" in line:
            content = content[:i] + [team_chart] + content[i + 1:]
            break

    with open("index.md", "w", encoding="UTF-8") as f:
        f.writelines(content)
