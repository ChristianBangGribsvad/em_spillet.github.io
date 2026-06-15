---
layout: default
team_color: "#7c0e6c"
---

# GeH Fys

## GeH Fys participants:
- [Thomas Petersen](./Thomas_Pe.html)
- [Renee Petersen](./Renee_Pe.html)
- [Hanne Hornshøj](./Hanne_Ho.html)
- [Bobinho Hjorth](./Bobinho_Hj.html)
- [Nicholas Sommer-Lykke](./Nicholas_So.html)
- [Godske G](./Godske_G.html)
- [lisbeth Ulnits](./lisbeth_Ul.html)
- [Bjarke Haugan](./Bjarke_Ha.html)
- [Andreas Mikkelsen](./Andreas_To.html)
- [RK  Fysioterapi](./RK__Fy.html)
- [Simon Lund-Hansen](./Simon_Lu.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./RK__Fy.html">RK  Fysioterapi</a></span><span class="ts-pts">71 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./Bjarke_Ha.html">Bjarke Haugan</a></span><span class="ts-pts">66 pts</span></div>
<div class="ts-row ts-bronze"><span class="ts-pos">🥉</span><span class="ts-name"><a href="./Nicholas_So.html">Nicholas Sommer-Lykke</a></span><span class="ts-pts">63 pts</span></div>
<div class="ts-row "><span class="ts-pos">4</span><span class="ts-name"><a href="./Godske_G.html">Godske G</a></span><span class="ts-pts">63 pts</span></div>
<div class="ts-row "><span class="ts-pos">5</span><span class="ts-name"><a href="./Thomas_Pe.html">Thomas Petersen</a></span><span class="ts-pts">62 pts</span></div>
<div class="ts-row "><span class="ts-pos">6</span><span class="ts-name"><a href="./Simon_Lu.html">Simon Lund-Hansen</a></span><span class="ts-pts">61 pts</span></div>
<div class="ts-row "><span class="ts-pos">7</span><span class="ts-name"><a href="./Hanne_Ho.html">Hanne Hornshøj</a></span><span class="ts-pts">48 pts</span></div>
<div class="ts-row "><span class="ts-pos">8</span><span class="ts-name"><a href="./lisbeth_Ul.html">lisbeth Ulnits</a></span><span class="ts-pts">48 pts</span></div>
<div class="ts-row "><span class="ts-pos">9</span><span class="ts-name"><a href="./Renee_Pe.html">Renee Petersen</a></span><span class="ts-pts">45 pts</span></div>
<div class="ts-row "><span class="ts-pos">10</span><span class="ts-name"><a href="./Bobinho_Hj.html">Bobinho Hjorth</a></span><span class="ts-pts">44 pts</span></div>
<div class="ts-row "><span class="ts-pos">11</span><span class="ts-name"><a href="./Andreas_To.html">Andreas Mikkelsen</a></span><span class="ts-pts">37 pts</span></div>
</div>

## Score progression

<div class="chart-wrapper">
<div class="chart-controls">
<button id="chart-GeH_Fys-toggle" class="chart-toggle">Show Rank</button>
</div>
<canvas id="chart-GeH_Fys"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("chart-GeH_Fys");
var btn=document.getElementById("chart-GeH_Fys-toggle");
var data={"labels": ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-15"], "datasets": [{"label": "Thomas Petersen", "data": [0.0, 12.0, 26.0, 43.0, 62.0], "borderColor": "#9a1ba7", "backgroundColor": "rgba(154,27,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Renee Petersen", "data": [0.0, 2.0, 11.0, 26.0, 45.0], "borderColor": "#1b35a7", "backgroundColor": "rgba(27,53,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Hanne Hornsh\u00f8j", "data": [0.0, 10.0, 25.0, 42.0, 48.0], "borderColor": "#1ba735", "backgroundColor": "rgba(27,167,53,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Bobinho Hjorth", "data": [0.0, 17.0, 21.0, 38.0, 44.0], "borderColor": "#9aa71b", "backgroundColor": "rgba(154,167,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Nicholas Sommer-Lykke", "data": [0.0, 17.0, 34.0, 51.0, 63.0], "borderColor": "#1ba781", "backgroundColor": "rgba(27,167,129,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Godske G", "data": [0.0, 15.0, 42.0, 46.0, 63.0], "borderColor": "#4ea71b", "backgroundColor": "rgba(78,167,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "lisbeth Ulnits", "data": [0.0, 10.0, 27.0, 44.0, 48.0], "borderColor": "#a71b67", "backgroundColor": "rgba(167,27,103,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Bjarke Haugan", "data": [0.0, 20.0, 25.0, 42.0, 66.0], "borderColor": "#a7671b", "backgroundColor": "rgba(167,103,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Andreas Mikkelsen", "data": [0.0, 10.0, 10.0, 25.0, 37.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "RK  Fysioterapi", "data": [0.0, 25.0, 45.0, 60.0, 71.0], "borderColor": "#1b81a7", "backgroundColor": "rgba(27,129,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Simon Lund-Hansen", "data": [0.0, 0.0, 32.0, 54.0, 61.0], "borderColor": "#4e1ba7", "backgroundColor": "rgba(78,27,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
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

## Points earned — latest round

<div class="chart-wrapper" style="height:642px">
<canvas id="bar-GeH_Fys"></canvas>
</div>
<script>
(function(){
var d={"labels": ["Bjarke Haugan", "Renee Petersen", "Thomas Petersen", "Godske G", "Andreas Mikkelsen", "Nicholas Sommer-Lykke", "RK  Fysioterapi", "Simon Lund-Hansen", "Hanne Hornsh\u00f8j", "Bobinho Hjorth", "lisbeth Ulnits"], "values": [24.0, 19.0, 19.0, 17.0, 12.0, 12.0, 11.0, 7.0, 6.0, 6.0, 4.0], "colors": ["#a7671b", "#1b35a7", "#9a1ba7", "#4ea71b", "#a71b1b", "#1ba781", "#1b81a7", "#4e1ba7", "#1ba735", "#9aa71b", "#a71b67"], "title": "Points earned \u2192 2026-06-14 to 2026-06-15"};
new Chart(document.getElementById("bar-GeH_Fys"),{
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

[← Back to standings](../)
