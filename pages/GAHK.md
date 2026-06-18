---
layout: default
team_color: "#2d0e7c"
---

# GAHK

## GAHK participants:
- [Ditlev Bigum](./Ditlev_Bi.html)
- [Sebastian Lefmann](./Sebastian_Le.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./Sebastian_Le.html">Sebastian Lefmann</a></span><span class="ts-pts">107 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./Ditlev_Bi.html">Ditlev Bigum</a></span><span class="ts-pts">102 pts</span></div>
</div>

## Score progression

<div class="chart-wrapper">
<div class="chart-controls">
<button id="chart-GAHK-toggle" class="chart-toggle">Show Rank</button>
</div>
<canvas id="chart-GAHK"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("chart-GAHK");
var btn=document.getElementById("chart-GAHK-toggle");
var data={"labels": ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-15", "2026-06-16", "2026-06-17", "2026-06-18"], "datasets": [{"label": "Ditlev Bigum", "data": [0.0, 10.0, 17.0, 39.0, 53.0, 62.0, 85.0, 102.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Sebastian Lefmann", "data": [0.0, 7.0, 19.0, 34.0, 52.0, 67.0, 90.0, 107.0], "borderColor": "#1ba7a7", "backgroundColor": "rgba(27,167,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
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

<div class="chart-wrapper" style="height:174px">
<canvas id="bar-GAHK"></canvas>
</div>
<script>
(function(){
var d={"labels": ["Ditlev Bigum", "Sebastian Lefmann"], "values": [17.0, 17.0], "colors": ["#a71b1b", "#1ba7a7"], "title": "Points earned \u2192 2026-06-17 to 2026-06-18"};
new Chart(document.getElementById("bar-GAHK"),{
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
