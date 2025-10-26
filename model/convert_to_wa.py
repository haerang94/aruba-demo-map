
import json, os, pandas as pd
icons={'sleep':{'x':5,'y':7,'icon':'sleep.png'},
       'meal':{'x':8,'y':4,'icon':'meal.png'},
       'toilet':{'x':3,'y':9,'icon':'toilet.png'},
       'out':{'x':1,'y':1,'icon':'out.png'}}
pred=json.load(open('output/predictions.json'))
act=pred['predicted_action']
wa={'event':'behavior_prediction','timestamp':pred['timestamp'],'action':act,'visual':icons.get(act,{'x':0,'y':0,'icon':'out.png'})}
os.makedirs('web/output', exist_ok=True)
with open('web/output/wa_events.json','w') as f:
    json.dump(wa,f,indent=2)
print('web/output/wa_events.json generated.')
