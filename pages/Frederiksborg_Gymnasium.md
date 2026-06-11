---
layout: default
team_color: "#0e7c4d"
---

# Frederiksborg Gymnasium

## Frederiksborg Gymnasium participants:
- [sexy ossi](./sexy_os.html)
- [Joachim Glenthøj](./Joachim_Gl.html)
- [Sarah Melberg](./Sarah_Me.html)
- [Bjarke Haugan](./Bjarke_Ha.html)
- [Christian Gribsvad](./Christian_Gr.html)
- [Oscar Engberg](./Oscar_En.html)
- [Matias Bundgaard-Nielsen](./Matias_Bu.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./sexy_os.html">sexy ossi</a></span><span class="ts-pts">0 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./Joachim_Gl.html">Joachim Glenthøj</a></span><span class="ts-pts">0 pts</span></div>
<div class="ts-row ts-bronze"><span class="ts-pos">🥉</span><span class="ts-name"><a href="./Sarah_Me.html">Sarah Melberg</a></span><span class="ts-pts">0 pts</span></div>
<div class="ts-row "><span class="ts-pos">4</span><span class="ts-name"><a href="./Bjarke_Ha.html">Bjarke Haugan</a></span><span class="ts-pts">0 pts</span></div>
<div class="ts-row "><span class="ts-pos">5</span><span class="ts-name"><a href="./Christian_Gr.html">Christian Gribsvad</a></span><span class="ts-pts">0 pts</span></div>
<div class="ts-row "><span class="ts-pos">6</span><span class="ts-name"><a href="./Oscar_En.html">Oscar Engberg</a></span><span class="ts-pts">0 pts</span></div>
<div class="ts-row "><span class="ts-pos">7</span><span class="ts-name"><a href="./Matias_Bu.html">Matias Bundgaard-Nielsen</a></span><span class="ts-pts">0 pts</span></div>
</div>

## Score progression

<div class="chart-wrapper">
<div class="chart-controls">
<button id="chart-Frederiksborg_Gymnasium-toggle" class="chart-toggle">Show Rank</button>
</div>
<canvas id="chart-Frederiksborg_Gymnasium"></canvas>
</div>
<script>
(function(){
var el=document.getElementById("chart-Frederiksborg_Gymnasium");
var btn=document.getElementById("chart-Frederiksborg_Gymnasium-toggle");
var data={"labels": ["2026-06-11"], "datasets": [{"label": "sexy ossi", "data": [0.0], "borderColor": "#a71b93", "backgroundColor": "rgba(167,27,147,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Joachim Glenth\u00f8j", "data": [0.0], "borderColor": "#43a71b", "backgroundColor": "rgba(67,167,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Sarah Melberg", "data": [0.0], "borderColor": "#431ba7", "backgroundColor": "rgba(67,27,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Bjarke Haugan", "data": [0.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Christian Gribsvad", "data": [0.0], "borderColor": "#a7931b", "backgroundColor": "rgba(167,147,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Oscar Engberg", "data": [0.0], "borderColor": "#1b6ba7", "backgroundColor": "rgba(27,107,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Matias Bundgaard-Nielsen", "data": [0.0], "borderColor": "#1ba76b", "backgroundColor": "rgba(27,167,107,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
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

<p class="chart-placeholder"><em>Best round chart appears after the first two scoring updates.</em></p>

[← Back to standings](../)
