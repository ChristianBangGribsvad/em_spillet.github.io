---
layout: default
team_color: "#0e7c7c"
---

# Team Beta

## Team Beta participants:
- [Bob Johnson](./Bob_Jo.html)
- [Carol Davis](./Carol_Da.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./Bob_Jo.html">Bob Johnson</a></span><span class="ts-pts">769 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./Carol_Da.html">Carol Davis</a></span><span class="ts-pts">701 pts</span></div>
</div>

<div class="chart-wrapper">
<canvas id="chart-Team_Beta"></canvas>
</div>
<script>
(function(){
new Chart(document.getElementById("chart-Team_Beta"),{
  type:"line",data:{"labels": ["2026-06-12", "2026-06-16", "2026-06-20"], "datasets": [{"label": "Bob Johnson", "data": [219.0, 469.0, 769.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Carol Davis", "data": [192.0, 403.0, 701.0], "borderColor": "#1ba7a7", "backgroundColor": "rgba(27,167,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]},
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

![Team Beta](./group_plots/bars_Team_Beta.svg?raw=true)
 
[← Back to standings](../)
