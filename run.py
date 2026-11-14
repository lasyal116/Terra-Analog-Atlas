"""Run the completed offline explorer: python run.py (standard library only)."""
import argparse,functools,http.server,webbrowser
from pathlib import Path
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8000);p.add_argument('--no-browser',action='store_true');args=p.parse_args()
    root=Path(__file__).resolve().parent/'dist'
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root))
    with http.server.ThreadingHTTPServer(('127.0.0.1',args.port),handler) as server:
        url=f'http://localhost:{args.port}'
        print('Terra Analog Atlas:',url,'\nPress Ctrl+C to stop.',flush=True)
        if not args.no_browser:webbrowser.open(url)
        try:server.serve_forever()
        except KeyboardInterrupt:print('\nStopped.')
