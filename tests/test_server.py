"""HTTP contract tests with the external source mocked; no extra dependencies."""
import importlib.util,json,threading,unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen,Request
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('pchelka_server',Path(__file__).resolve().parents[1]/'server.py')
server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)
class ServerContractTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.httpd=server.ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
  cls.thread=threading.Thread(target=cls.httpd.serve_forever,daemon=True);cls.thread.start()
  cls.base='http://127.0.0.1:'+str(cls.httpd.server_port)
 @classmethod
 def tearDownClass(cls):
  cls.httpd.shutdown();cls.httpd.server_close();cls.thread.join(timeout=3)
 def setUp(self):server.RATE.clear()
 def request(self,path,method='GET'):
  try:r=urlopen(Request(self.base+path,method=method),timeout=3)
  except HTTPError as error:r=error
  with r:return r.status,r.headers,r.read(),r.geturl()
 def test_root_opens_landing(self):
  code,h,b,url=self.request('/');self.assertEqual(code,200);self.assertTrue(url.endswith('/welcome.html'));self.assertIn('Пчёлка'.encode(),b);self.assertEqual(h['X-Content-Type-Options'],'nosniff')
 def test_contract_and_wasm_are_served(self):
  code,_,body,_=self.request('/api-contract.json');self.assertEqual(code,200);self.assertIn('/api/products',json.loads(body)['paths'])
  code,h,body,_=self.request('/ai/ort-wasm-simd-threaded.wasm','HEAD');self.assertEqual(code,200);self.assertEqual(h.get_content_type(),'application/wasm');self.assertGreater(int(h['Content-Length']),10000000);self.assertEqual(body,b'')
 def test_invalid_search_does_not_call_source(self):
  with patch.object(server,'lookup') as lookup:
   for path in ['/api/products','/api/products?q=x','/api/products?q='+'a'*121]:
    code,h,b,_=self.request(path);self.assertEqual(code,400);self.assertIn('error',json.loads(b));self.assertEqual(h['Cache-Control'],'no-store')
   lookup.assert_not_called()
 def test_candidates_keep_source_metadata(self):
  expected={'source':'Open Food Facts','license':'ODbL','matched_by':'text','query':'demo','retrieved_at':'2026-10-25T00:00:00+00:00','products':[]}
  with patch.object(server,'lookup',return_value=(expected,200)) as lookup:
   code,_,b,_=self.request('/api/products?q=demo');self.assertEqual(code,200);self.assertEqual(json.loads(b),expected);lookup.assert_called_once_with('demo')
 def test_source_failure_is_not_fabricated(self):
  with patch.object(server,'lookup',return_value=({'error':'source unavailable'},503)):
   code,_,b,_=self.request('/api/products?q=demo');self.assertEqual(code,503);self.assertNotIn('products',json.loads(b))
 def test_search_rate_limit(self):
  with patch.object(server,'lookup',return_value=({'products':[]},200)) as lookup:
   for _ in range(10):self.assertEqual(self.request('/api/products?q=demo')[0],200)
   code,_,b,_=self.request('/api/products?q=demo');self.assertEqual(code,429);self.assertIn('error',json.loads(b));self.assertEqual(lookup.call_count,10)
 def test_gtin_and_response_sanitization(self):
  self.assertTrue(server.gtin('3017620422003'));self.assertFalse(server.gtin('3017620422004'));self.assertFalse(server.gtin('１２３４５６７８'))
  v=server.clean({'product_name':'x'*1000,'ingredients_text':'x'*6000,'categories_tags':['ok',42],'secret':'no'});self.assertEqual(len(v['product_name']),500);self.assertEqual(len(v['ingredients_text']),5000);self.assertEqual(v['categories_tags'],['ok']);self.assertNotIn('secret',v)
 def test_source_files_not_exposed(self):
  for path in ['/server.py','/../server.py','/.env','/api/v1/drafts']:self.assertEqual(self.request(path)[0],404)
if __name__=='__main__':unittest.main()
