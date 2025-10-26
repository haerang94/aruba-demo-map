console.log('Loading Aruba plugin');
fetch('https://adventuretestfordemo.netlify.app/output/wa_events.json')
 .then(r=>r.json())
 .then(d=>{
   console.log('Predicted',d.action);
   const icon='/web/assets/icons/'+d.visual.icon;
   WA.room.showLayer(icon,{x:d.visual.x,y:d.visual.y});
 });