---
layout: default
---

# Hanne Hornshøj

<div class="participant-meta"><span class="pmeta-team">GeH Fys</span></div>

<div class="stat-cards">
<div class="stat-card"><span class="stat-icon">🏆</span><div class="stat-body"><span class="stat-main">#18th out of 35 players across the game</span><span class="stat-sub">You beat 49% of all players</span></div></div>
<div class="stat-card"><span class="stat-icon stat-down">↓</span><div class="stat-body"><span class="stat-main">10 pts last round</span><span class="stat-sub">-2 pts vs global avg (12 pts) &middot; Moved down 17 places &middot; 18th out of 35 total players</span></div></div>
</div>
## Your score vs averages

<div class="chart-wrapper">
<canvas id="personal-Hanne_Ho"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("personal-Hanne_Ho");
var data={"labels": ["2026-06-11", "2026-06-12"], "datasets": [{"label": "Your score", "data": [0.0, 10.0], "borderColor": "#1e40af", "backgroundColor": "rgba(30,64,175,0.08)", "borderWidth": 3, "tension": 0.3, "pointRadius": 6, "pointHoverRadius": 9, "fill": true, "order": 1}, {"label": "Team average", "data": [0.0, 12.5], "borderColor": "#7c0e6c", "backgroundColor": "rgba(124,14,108,0.04)", "borderWidth": 1.5, "borderDash": [3, 3], "tension": 0.3, "pointRadius": 3, "pointHoverRadius": 5, "fill": false, "order": 2}, {"label": "Global average", "data": [0.0, 12.0], "borderColor": "rgba(0,0,0,0.28)", "backgroundColor": "rgba(0,0,0,0.02)", "borderWidth": 1.5, "borderDash": [5, 5], "tension": 0.3, "pointRadius": 3, "pointHoverRadius": 5, "fill": false, "order": 3}]};
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

## Your predictions

<div class="pred-table">
<div class="pred-breakdown">Group matches: <strong>10 pts</strong> &nbsp;&middot;&nbsp; Group winners: <strong>0 pts</strong> &nbsp;&middot;&nbsp; Special predictions: <strong>0 pts</strong></div>
<div class="pred-total">Total &nbsp;<span class="pred-total-pts">10 pts</span></div>
<div class="pred-col-header"><span>Match</span><span>Your pick</span><span>Result</span><span>Pts</span></div>
<div class="pred-section">
<div class="pred-section-header">Group A</div>
<div class="pred-row pts-10"><span class="pred-match"><small class="match-date">Jun 11th · 21:00</small>Mexico vs South Africa</span><span class="pred-guess">2-1</span><span class="pred-result">2-0</span><span class="pts-badge">10</span></div>
<div class="pred-row pts-0"><span class="pred-match"><small class="match-date">Jun 12th · 04:00</small>South Korea vs Czechia</span><span class="pred-guess">0-2</span><span class="pred-result">2-1</span><span class="pts-badge">0</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 18th · 18:00</small>Czechia vs South Africa</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 19th · 03:00</small>Mexico vs South Korea</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 25th · 03:00</small>Czechia vs Mexico</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 25th · 03:00</small>South Africa vs South Korea</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Czechia / Czechia</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group B</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 12th · 21:00</small>Canada vs Bosnia-Herzegovina</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 13th · 21:00</small>Qatar vs Switzerland</span><span class="pred-guess">0-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 18th · 21:00</small>Switzerland vs Bosnia-Herzegovina</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 19th · 00:00</small>Canada vs Qatar</span><span class="pred-guess">0-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 24th · 21:00</small>Switzerland vs Canada</span><span class="pred-guess">3-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 24th · 21:00</small>Bosnia-Herzegovina vs Qatar</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Switzerland / Bosnia-Herzegovina</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group C</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 14th · 00:00</small>Brazil vs Morocco</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 14th · 03:00</small>Haiti vs Scotland</span><span class="pred-guess">0-4</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 20th · 00:00</small>Scotland vs Morocco</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 20th · 02:30</small>Brazil vs Haiti</span><span class="pred-guess">5-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 25th · 00:00</small>Morocco vs Haiti</span><span class="pred-guess">4-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 25th · 00:00</small>Scotland vs Brazil</span><span class="pred-guess">2-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Brazil / Scotland</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group D</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 13th · 03:00</small>United States vs Paraguay</span><span class="pred-guess">0-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 14th · 06:00</small>Australia vs Turkey</span><span class="pred-guess">0-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 19th · 21:00</small>United States vs Australia</span><span class="pred-guess">2-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 20th · 05:00</small>Turkey vs Paraguay</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 26th · 04:00</small>Turkey vs United States</span><span class="pred-guess">3-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 26th · 04:00</small>Paraguay vs Australia</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Turkey / Paraguay</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group E</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 14th · 19:00</small>Germany vs Curaçao</span><span class="pred-guess">4-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 15th · 01:00</small>Ivory Coast vs Ecuador</span><span class="pred-guess">0-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 20th · 22:00</small>Germany vs Ivory Coast</span><span class="pred-guess">5-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 21st · 02:00</small>Ecuador vs Curaçao</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 25th · 22:00</small>Ecuador vs Germany</span><span class="pred-guess">1-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 25th · 22:00</small>Curaçao vs Ivory Coast</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Germany / Ecuador</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group F</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 14th · 22:00</small>Netherlands vs Japan</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 15th · 04:00</small>Sweden vs Tunisia</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 20th · 19:00</small>Netherlands vs Sweden</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 21st · 06:00</small>Tunisia vs Japan</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 26th · 01:00</small>Tunisia vs Netherlands</span><span class="pred-guess">1-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 26th · 01:00</small>Japan vs Sweden</span><span class="pred-guess">1-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Netherlands / Tunisia</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group G</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 15th · 21:00</small>Belgium vs Egypt</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 16th · 03:00</small>Iran vs New Zealand</span><span class="pred-guess">0-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 21st · 21:00</small>Belgium vs Iran</span><span class="pred-guess">3-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 22nd · 03:00</small>New Zealand vs Egypt</span><span class="pred-guess">1-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 27th · 05:00</small>New Zealand vs Belgium</span><span class="pred-guess">0-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 27th · 05:00</small>Egypt vs Iran</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Belgium / Egypt</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group H</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 15th · 18:00</small>Spain vs Cape Verde Islands</span><span class="pred-guess">4-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 16th · 00:00</small>Saudi Arabia vs Uruguay</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 21st · 18:00</small>Spain vs Saudi Arabia</span><span class="pred-guess">4-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 22nd · 00:00</small>Uruguay vs Cape Verde Islands</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 27th · 02:00</small>Uruguay vs Spain</span><span class="pred-guess">1-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 27th · 02:00</small>Cape Verde Islands vs Saudi Arabia</span><span class="pred-guess">1-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Spain / Uruguay</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group I</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 16th · 21:00</small>France vs Senegal</span><span class="pred-guess">5-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 17th · 00:00</small>Iraq vs Norway</span><span class="pred-guess">0-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 22nd · 23:00</small>France vs Iraq</span><span class="pred-guess">3-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 23rd · 02:00</small>Norway vs Senegal</span><span class="pred-guess">1-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 26th · 21:00</small>Norway vs France</span><span class="pred-guess">1-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 26th · 21:00</small>Senegal vs Iraq</span><span class="pred-guess">2-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">France / Norway</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group J</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 17th · 03:00</small>Argentina vs Algeria</span><span class="pred-guess">3-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 17th · 06:00</small>Austria vs Jordan</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 22nd · 19:00</small>Argentina vs Austria</span><span class="pred-guess">3-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 23rd · 05:00</small>Jordan vs Algeria</span><span class="pred-guess">0-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 28th · 04:00</small>Jordan vs Argentina</span><span class="pred-guess">0-4</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 28th · 04:00</small>Algeria vs Austria</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Argentina / Algeria</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group K</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 17th · 19:00</small>Portugal vs Congo DR</span><span class="pred-guess">4-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 18th · 04:00</small>Uzbekistan vs Colombia</span><span class="pred-guess">0-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 23rd · 19:00</small>Portugal vs Uzbekistan</span><span class="pred-guess">3-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 24th · 04:00</small>Colombia vs Congo DR</span><span class="pred-guess">3-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 28th · 01:30</small>Colombia vs Portugal</span><span class="pred-guess">1-3</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 28th · 01:30</small>Congo DR vs Uzbekistan</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">Portugal / Colombia</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Group L</div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 17th · 22:00</small>England vs Croatia</span><span class="pred-guess">2-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 18th · 01:00</small>Ghana vs Panama</span><span class="pred-guess">1-1</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 23rd · 22:00</small>England vs Ghana</span><span class="pred-guess">3-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 24th · 01:00</small>Panama vs Croatia</span><span class="pred-guess">1-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 27th · 23:00</small>Panama vs England</span><span class="pred-guess">0-2</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match"><small class="match-date">Jun 27th · 23:00</small>Croatia vs Ghana</span><span class="pred-guess">2-0</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-divider">Group winners</div>
<div class="pred-row pts-unplayed"><span class="pred-match">1st &amp; 2nd place</span><span class="pred-guess">England / Croatia</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
<div class="pred-section">
<div class="pred-section-header">Special Predictions</div>
<div class="pred-row pts-unplayed"><span class="pred-match">Final winner</span><span class="pred-guess">France</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Final loser</span><span class="pred-guess">Portugal</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Top scorer</span><span class="pred-guess">Kylian Mbappe</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
<div class="pred-row pts-unplayed"><span class="pred-match">Scorer goals</span><span class="pred-guess">6</span><span class="pred-result">&mdash;</span><span class="pts-badge">&mdash;</span></div>
</div>
</div>

[Back](https://christianbanggribsvad.github.io/wc-predictions.github.io/)