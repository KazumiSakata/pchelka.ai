#!/usr/bin/env python3
"""Local Pchelka server, Python standard library only. No account keys required."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.request import Request, urlopen
from urllib.parse import urlparse, parse_qs, urlencode
from pathlib import Path
import argparse, json, time, threading
ROOT=Path(__file__).resolve().parent/'public'
FIELDS='code,product_name,product_name_ru,product_name_en,brands,ingredients_text,ingredients_text_ru,ingredients_text_en,quantity,image_front_small_url,categories_tags,last_modified_t'
RATE={}; LOCK=threading.Lock()
def gtin(value):
    if not value.isascii() or not value.isdigit() or len(value) not in (8,12,13,14):return False
    s=sum(int(x)*(3 if i%2==0 else 1) for i,x in enumerate(value[-2::-1]));return (10-s%10)%10==int(value[-1])
def clean(product):
    out={}
    for k in FIELDS.split(','):
        v=product.get(k)
        if isinstance(v,str):out[k]=v[:5000 if k.startswith('ingredients') else 500]
        elif isinstance(v,list):out[k]=[x for x in v if isinstance(x,str)][:20]
        elif isinstance(v,(int,float)):out[k]=v
    return out
def lookup(q):
    barcode=q.isascii() and q.isdigit()
    if barcode and not gtin(q):return {'error':'Проверьте штрихкод: неверная длина или контрольная цифра.'},400
    if barcode: endpoint='https://world.openfoodfacts.org/api/v2/product/'+q+'.json?'+urlencode({'fields':FIELDS})
    else:
        import re
        term=re.sub(r'[+!(){}\[\]^"~*?:\\/|&-]',' ',q).strip()
        endpoint='https://search.openfoodfacts.org/search?'+urlencode({'q':term,'page_size':5,'fields':FIELDS,'langs':'ru,en'})
    try:
        with urlopen(Request(endpoint,headers={'User-Agent':'Pchelka/2.0 product-card prototype','Accept':'application/json'}),timeout=15) as r:
            if urlparse(r.url).hostname not in ('world.openfoodfacts.org','search.openfoodfacts.org'):raise ValueError('Unexpected host')
            body=r.read(1_000_001)
            if len(body)>1_000_000:raise ValueError('Too large')
            data=json.loads(body)
        products=([data['product']] if data.get('status')==1 else []) if barcode else data.get('hits',data.get('products',[]))
        from datetime import datetime,timezone
        return {'source':'Open Food Facts','license':'ODbL','matched_by':'barcode' if barcode else 'text','query':q,'retrieved_at':datetime.now(timezone.utc).isoformat(),'products':[clean(p) for p in products[:5]]},200
    except Exception:return {'error':'База товаров временно недоступна. Не найденные сведения не подставлены.'},503
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):super().__init__(*args,directory=str(ROOT),**kwargs)
    def log_message(self,*args):pass
    def end_headers(self):
        self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer');self.send_header('X-Frame-Options','DENY');super().end_headers()
    def json(self,data,status):
        b=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/':self.send_response(302);self.send_header('Location','/welcome.html');self.end_headers();return
        if u.path=='/api/products':
            q=parse_qs(u.query).get('q',[''])[0].strip()
            if not 2<=len(q)<=120:self.json({'error':'Введите штрихкод или название от 2 до 120 символов.'},400);return
            key=self.client_address[0];t=time.monotonic()
            with LOCK:
                ticks=[x for x in RATE.get(key,[]) if t-x<60]
                if len(ticks)>=10:self.json({'error':'Подождите минуту перед следующим поиском.'},429);return
                ticks.append(t);RATE[key]=ticks
            data,status=lookup(q);self.json(data,status);return
        return super().do_GET()
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--host',default='127.0.0.1');parser.add_argument('--port',type=int,default=8000);a=parser.parse_args()
    print(f'Pchelka: http://{a.host}:{a.port}',flush=True);ThreadingHTTPServer((a.host,a.port),Handler).serve_forever()
