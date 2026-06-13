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
- [Sebastian Lefmann](./Sebastian_Le.html)

<div class="team-standings">
<div class="ts-row ts-gold"><span class="ts-pos">🥇</span><span class="ts-name"><a href="./Matias_Bu.html">Matias Bundgaard-Nielsen</a></span><span class="ts-pts">50 pts</span></div>
<div class="ts-row ts-silver"><span class="ts-pos">🥈</span><span class="ts-name"><a href="./sexy_os.html">sexy ossi</a></span><span class="ts-pts">42 pts</span></div>
<div class="ts-row ts-bronze"><span class="ts-pos">🥉</span><span class="ts-name"><a href="./Oscar_En.html">Oscar Engberg</a></span><span class="ts-pts">37 pts</span></div>
<div class="ts-row "><span class="ts-pos">4</span><span class="ts-name"><a href="./Joachim_Gl.html">Joachim Glenthøj</a></span><span class="ts-pts">37 pts</span></div>
<div class="ts-row "><span class="ts-pos">5</span><span class="ts-name"><a href="./Bjarke_Ha.html">Bjarke Haugan</a></span><span class="ts-pts">25 pts</span></div>
<div class="ts-row "><span class="ts-pos">6</span><span class="ts-name"><a href="./Sarah_Me.html">Sarah Melberg</a></span><span class="ts-pts">20 pts</span></div>
<div class="ts-row "><span class="ts-pos">7</span><span class="ts-name"><a href="./Sebastian_Le.html">Sebastian Lefmann</a></span><span class="ts-pts">19 pts</span></div>
<div class="ts-row "><span class="ts-pos">8</span><span class="ts-name"><a href="./Christian_Gr.html">Christian Gribsvad</a></span><span class="ts-pts">14 pts</span></div>
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
var data={"labels": ["2026-06-11", "2026-06-12", "2026-06-13"], "datasets": [{"label": "sexy ossi", "data": [0.0, 17.0, 42.0], "borderColor": "#a71b84", "backgroundColor": "rgba(167,27,132,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Joachim Glenth\u00f8j", "data": [0.0, 30.0, 37.0], "borderColor": "#61a71b", "backgroundColor": "rgba(97,167,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Sarah Melberg", "data": [0.0, 10.0, 20.0], "borderColor": "#1b3ea7", "backgroundColor": "rgba(27,62,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Bjarke Haugan", "data": [0.0, 20.0, 25.0], "borderColor": "#a71b1b", "backgroundColor": "rgba(167,27,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Christian Gribsvad", "data": [0.0, 12.0, 14.0], "borderColor": "#a7841b", "backgroundColor": "rgba(167,132,27,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Oscar Engberg", "data": [0.0, 25.0, 37.0], "borderColor": "#1ba7a7", "backgroundColor": "rgba(27,167,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Matias Bundgaard-Nielsen", "data": [0.0, 25.0, 50.0], "borderColor": "#1ba73e", "backgroundColor": "rgba(27,167,62,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}, {"label": "Sebastian Lefmann", "data": [0.0, 7.0, 19.0], "borderColor": "#611ba7", "backgroundColor": "rgba(97,27,167,0.08)", "tension": 0.3, "pointRadius": 5, "pointHoverRadius": 8, "borderWidth": 2.5, "fill": true}]};
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

<div class="chart-wrapper" style="height:486px">
<canvas id="bar-Frederiksborg_Gymnasium"></canvas>
</div>
<script>
(function(){
var d={"labels": ["sexy ossi", "Matias Bundgaard-Nielsen", "Oscar Engberg", "Sebastian Lefmann", "Sarah Melberg", "Joachim Glenth\u00f8j", "Bjarke Haugan", "Christian Gribsvad"], "values": [25.0, 25.0, 12.0, 12.0, 10.0, 7.0, 5.0, 2.0], "colors": ["#a71b84", "#1ba73e", "#1ba7a7", "#611ba7", "#1b3ea7", "#61a71b", "#a71b1b", "#a7841b"], "title": "Points earned \u2192 2026-06-12 to 2026-06-13"};
new Chart(document.getElementById("bar-Frederiksborg_Gymnasium"),{
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
