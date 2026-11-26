from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from html.parser import HTMLParser
from urllib.parse import urljoin
import json, os, re

ROOT=os.path.dirname(os.path.abspath(__file__))
NEWS_URL='https://www.bennett.edu.in/media-center/'
IN_NEWS_URL='https://www.bennett.edu.in/media-center/bu-in-news/'

class LinkParser(HTMLParser):
    def __init__(self, base):
        super().__init__(); self.base=base; self.items=[]; self.in_a=False; self.href=''; self.buf=''
    def handle_starttag(self, tag, attrs):
        if tag=='a':
            self.in_a=True; self.href=dict(attrs).get('href',''); self.buf=''
    def handle_data(self, data):
        if self.in_a: self.buf += data+' '
    def handle_endtag(self, tag):
        if tag=='a' and self.in_a:
            title=' '.join(self.buf.split())
            if len(title)>24 and self.href:
                self.items.append({'title':title,'url':urljoin(self.base,self.href)})
            self.in_a=False

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): super().__init__(*args,directory=ROOT,**kwargs)
    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
            return
        if self.path.startswith('/api/news'):
            self.news(); return
        if self.path=='/api/health':
            self.send_json({'ok':True,'app':'CampusCompass'}); return
        super().do_GET()
    def send_json(self,obj):
        raw=json.dumps(obj).encode(); self.send_response(200); self.send_header('Content-Type','application/json; charset=utf-8'); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def news(self):
        collected=[]; errors=[]
        for source, label in [(NEWS_URL,'Bennett Media Centre'),(IN_NEWS_URL,'Bennett in the News')]:
            try:
                req=Request(source,headers={'User-Agent':'Mozilla/5.0 CampusCompass student project'})
                html=urlopen(req,timeout=12).read().decode('utf-8','ignore')
                p=LinkParser(source); p.feed(html)
                for item in p.items:
                    if 'bennett.edu.in' in item['url'] and item['url'] not in [x['url'] for x in collected]:
                        item['source']=label; collected.append(item)
            except Exception as e: errors.append(str(e))
        # Prefer Bennett's own media centre links; remove navigation and generic links.
        cleaned=[]
        for x in collected:
            t=x['title'].strip()
            if len(t)>28 and not any(k in t.lower() for k in ['admission','know more','click here','about us','read more']):
                cleaned.append(x)
        self.send_json({'items':cleaned[:35], 'updatedAt':__import__('datetime').datetime.now().astimezone().isoformat(), 'live':bool(cleaned), 'source':NEWS_URL, 'errors':errors[:2]})

if __name__=='__main__':
    os.chdir(ROOT)
    port = int(os.environ.get('PORT', 8000))
    print(f'CampusCompass running on port {port}')
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
