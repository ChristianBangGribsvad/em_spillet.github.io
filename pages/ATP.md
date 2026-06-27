---
layout: default
team_color: "#7c0e0e"
---

# ATP

## ATP participants:
- [Michael  Gribsvad](./Michael__Gr.html)
- [Jenus  Saleh](./Jenus__Sa.html)
- [*Gosia Jørgensen](./Gosia_N.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./Jenus__Sa.html">Jenus  Saleh</a></span><span class="ts-pts">472 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./Michael__Gr.html">Michael  Gribsvad</a></span><span class="ts-pts">436 pts</span></div>
<div class="ts-row ts-bronze"><span class="ts-pos">🥉</span><span class="ts-name"><a href="./Gosia_N.html">*Gosia Jørgensen</a></span><span class="ts-pts">370 pts</span></div>
</div>

## Score progression

<div class="chart-wrapper">
<div class="chart-controls">
<button id="chart-ATP-toggle" class="chart-toggle">Show Rank</button>
</div>
<canvas id="chart-ATP"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("chart-ATP");
var btn=document.getElementById("chart-ATP-toggle");
var data={"labels": ["2026-06-11", "2026-06-12", "2026-06-13", "2026-06-14", "2026-06-15", "2026-06-16", "2026-06-17", "2026-06-18", "2026-06-19", "2026-06-20", "2026-06-21", "2026-06-22", "2026-06-23", "2026-06-24", "2026-06-25", "2026-06-26", "2026-06-27"], "datasets": [{"label": "Michael  Gribsvad", "data": [0.0, 7.0, 32.0, 51.0, 88.0, 100.0, 100.0, 145.0, 170.0, 192.0, 213.0, 233.0, 260.0, 292.0, 314.0, 396.0, 436.0], "borderColor": "#1b1ba7", "backgroundColor": "rgba(27,27,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Jenus  Saleh", "data": [0.0, 12.0, 29.0, 59.0, 70.0, 80.0, 85.0, 122.0, 157.0, 186.0, 212.0, 224.0, 261.0, 306.0, 355.0, 442.0, 472.0], "borderColor": "#1ba71b", "backgroundColor": "rgba(27,167,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "*Gosia J\u00f8rgensen", "data": [0.0, 10.0, 12.0, 27.0, 34.0, 41.0, 71.0, 87.0, 92.0, 109.0, 136.0, 151.0, 173.0, 218.0, 240.0, 325.0, 370.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
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

<div class="chart-wrapper" style="height:226px">
<canvas id="bar-ATP"></canvas>
</div>
<script>
(function(){
var d={"labels": ["*Gosia J\u00f8rgensen", "Michael  Gribsvad", "Jenus  Saleh"], "values": [45.0, 40.0, 30.0], "colors": ["#a71b1b", "#1b1ba7", "#1ba71b"], "title": "Points earned \u2192 2026-06-26 to 2026-06-27"};
new Chart(document.getElementById("bar-ATP"),{
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
