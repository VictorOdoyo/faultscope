import hashlib,json
from datetime import datetime,timezone
from .solver import analyze
from .scan import scan
from .screening import screen
from .duty import duty

def run(data,action='analyze',options=None):
    actions={'analyze':analyze,'scan':scan,'screen':screen,'duty':duty}
    if action not in actions:raise ValueError('Unknown study action')
    if options is not None and not isinstance(options,dict):raise ValueError('Options must be an object')
    try:result=actions[action](data,**(options or {}))
    except TypeError as exc:raise ValueError('Invalid study options: '+str(exc)) from exc
    result['provenance']={'version':'1.0.0','action':action,'timestamp':datetime.now(timezone.utc).isoformat(),'model_sha256':hashlib.sha256(json.dumps(data,sort_keys=True,allow_nan=False).encode()).hexdigest(),'options':options or {}}
    return result
