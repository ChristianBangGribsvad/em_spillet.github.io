---
layout: default
team_color: "#7c6c0e"
---

# Buzzanova

## Buzzanova participants:
- [Isabella  Isaacs](./Isabella__Is.html)
- [Sarah-Alberte Bennetzen](./Sarah-Alberte_Be.html)
- [caroline Preisler](./caroline_Pr.html)
- [Noah Elias](./Noah_El.html)
- [John Karim](./John_Ka.html)
- [Jacob Harder](./Jacob_Ha.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./Isabella__Is.html">Isabella  Isaacs</a></span><span class="ts-pts">127 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./Noah_El.html">Noah Elias</a></span><span class="ts-pts">123 pts</span></div>
<div class="ts-row ts-bronze"><span class="ts-pos">🥉</span><span class="ts-name"><a href="./Sarah-Alberte_Be.html">Sarah-Alberte Bennetzen</a></span><span class="ts-pts">107 pts</span></div>
<div class="ts-row "><span class="ts-pos">4</span><span class="ts-name"><a href="./caroline_Pr.html">caroline Preisler</a></span><span class="ts-pts">103 pts</span></div>
<div class="ts-row "><span class="ts-pos">5</span><span class="ts-name"><a href="./Jacob_Ha.html">Jacob Harder</a></span><span class="ts-pts">89 pts</span></div>
<div class="ts-row "><span class="ts-pos">6</span><span class="ts-name"><a href="./John_Ka.html">John Karim</a></span><span class="ts-pts">61 pts</span></div>
</div>

## Score progression

<div class="chart-wrapper">
<div class="chart-controls">
<button id="chart-Buzzanova-toggle" class="chart-toggle">Show Rank</button>
</div>
<canvas id="chart-Buzzanova"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("chart-Buzzanova");
var btn=document.getElementById("chart-Buzzanova-toggle");
var data={"labels": ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-15", "2026-06-16", "2026-06-17", "2026-06-18"], "datasets": [{"label": "Isabella  Isaacs", "data": [0.0, 17.0, 22.0, 34.0, 60.0, 75.0, 105.0, 127.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Sarah-Alberte Bennetzen", "data": [0.0, 17.0, 34.0, 49.0, 61.0, 71.0, 83.0, 107.0], "borderColor": "#1b1ba7", "backgroundColor": "rgba(27,27,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "caroline Preisler", "data": [NaN, NaN, 2.0, 29.0, 43.0, 53.0, 81.0, 103.0], "borderColor": "#a71ba7", "backgroundColor": "rgba(167,27,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Noah Elias", "data": [NaN, NaN, 0.0, 25.0, 54.0, 71.0, 103.0, 123.0], "borderColor": "#1ba7a7", "backgroundColor": "rgba(27,167,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "John Karim", "data": [NaN, NaN, 12.0, 29.0, 35.0, 42.0, 57.0, 61.0], "borderColor": "#1ba71b", "backgroundColor": "rgba(27,167,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Jacob Harder", "data": [NaN, NaN, 7.0, 24.0, 35.0, 44.0, 72.0, 89.0], "borderColor": "#a7a71b", "backgroundColor": "rgba(167,167,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
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

<div class="chart-wrapper" style="height:382px">
<canvas id="bar-Buzzanova"></canvas>
</div>
<script>
(function(){
var d={"labels": ["Sarah-Alberte Bennetzen", "Isabella  Isaacs", "caroline Preisler", "Noah Elias", "Jacob Harder", "John Karim"], "values": [24.0, 22.0, 22.0, 20.0, 17.0, 4.0], "colors": ["#1b1ba7", "#a71b1b", "#a71ba7", "#1ba7a7", "#a7a71b", "#1ba71b"], "title": "Points earned \u2192 2026-06-17 to 2026-06-18"};
new Chart(document.getElementById("bar-Buzzanova"),{
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
