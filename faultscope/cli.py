import argparse
import json
import sys
from pathlib import Path
from importlib.resources import files
from .studies import run
from .model import validate

def example_names():return sorted(p.name[:-5] for p in files('faultscope').joinpath('examples').iterdir() if p.name.endswith('.json'))
def load_case(path):
    if path.startswith('example:'):
        key=path.split(':',1)[1]
        if key not in example_names():raise ValueError('Unknown example')
        return json.loads(files('faultscope').joinpath('examples',key+'.json').read_text())
    text=sys.stdin.read() if path=='-' else Path(path).read_text(encoding='utf-8')
    return validate(json.loads(text))

def main(argv=None):
    parser=argparse.ArgumentParser(prog='faultscope');sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('examples')
    serve=sub.add_parser('serve');serve.add_argument('--port',type=int,default=8768)
    study=sub.add_parser('study');study.add_argument('network');study.add_argument('--action',default='analyze');study.add_argument('--options',default='{}');study.add_argument('--output')
    args=parser.parse_args(argv)
    try:
        if args.command=='serve':
            from .server import serve
            serve(args.port);return 0
        if args.command=='examples':result=example_names()
        else:result=run(load_case(args.network),args.action,json.loads(args.options))
        text=json.dumps(result,indent=2,allow_nan=False)
        if getattr(args,'output',None):Path(args.output).write_text(text,encoding='utf-8')
        else:print(text)
        return 1 if isinstance(result,dict) and result.get('converged') is False else 0
    except (ValueError,OSError,ArithmeticError) as exc:
        print(json.dumps({'error':str(exc)}),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
