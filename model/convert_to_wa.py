
import json
icons={'sleep':{'x':5,'y':7,'icon':'sleep.png'},
       'meal':{'x':8,'y':4,'icon':'meal.png'},
       'toilet':{'x':3,'y':9,'icon':'toilet.png'},
       'out':{'x':1,'y':1,'icon':'out.png'}}
pred=json.load(open('output/predictions.json'))
act=pred['predicted_action']
wa={'event':'behavior_prediction','timestamp':pred['timestamp'],'action':act,'visual':icons.get(act,{'x':0,'y':0,'icon':'none.png'})}
json.dump(wa,open('output/wa_events.json','w'),indent=2)
print('wa_events.json generated.')
