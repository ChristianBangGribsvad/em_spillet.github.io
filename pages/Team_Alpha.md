---
layout: default
team_color: "#7c0e0e"
---

# Team Alpha

## Team Alpha participants:
- [Alice Smith](./Alice_Sm.html)
- [Carol Davis](./Carol_Da.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./Alice_Sm.html">Alice Smith</a></span><span class="ts-pts">937 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./Carol_Da.html">Carol Davis</a></span><span class="ts-pts">701 pts</span></div>
</div>

<div class="chart-wrapper">
<canvas id="chart-Team_Alpha"></canvas>
</div>
<script>
(function(){
new Chart(document.getElementById("chart-Team_Alpha"),{
  type:"line",data:{"labels": ["2026-06-12", "2026-06-16", "2026-06-20"], "datasets": [{"label": "Alice Smith", "data": [299.0, 540.0, 937.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Carol Davis", "data": [192.0, 403.0, 701.0], "borderColor": "#1ba7a7", "backgroundColor": "rgba(27,167,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]},
  options:{
    responsive:true,maintainAspectRatio:false,
    interaction:{mode:"index",intersect:false},
    plugins:{
      legend:{position:"right",labels:{boxWidth:12,padding:12,usePointStyle:true}},
      tooltip:{callbacks:{label:function(c){return c.dataset.label+": "+Math.round(c.raw)+" pts";}}}
    },
    scales:{
      x:{grid:{color:"rgba(0,0,0,0.05)"},ticks:{maxTicksLimit:10}},
      y:{beginAtZero:true,
         title:{display:true,text:"Points"},
         grid:{color:"rgba(0,0,0,0.05)"}}
    }
  }
});
})()
</script>

![Team Alpha](./group_plots/bars_Team_Alpha.svg?raw=true)
 
[← Back to standings](../)
