import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile,access} from 'node:fs/promises';
import {resolve} from 'node:path';
test('Les ressources locales et les destinations internes existent',async()=>{
 const html=await readFile('web/index.html','utf8');
 for(const [,url] of html.matchAll(/(?:href|src)="([^"]+)"/g)){
  if(url.startsWith('https:'))continue;
  if(url.startsWith('#')){if(url.length>1)assert.ok(html.includes(`id="${url.slice(1)}"`),url);continue;}
  await access(resolve('web',url.split('?')[0]));
 }
});
test('Le déploiement inclut les protections et le plan du site',async()=>{
 const headers=await readFile('web/_headers','utf8');
 assert.ok(headers.includes("script-src 'self'"));
 assert.ok((await readFile('web/sitemap.xml','utf8')).includes('https://vibecoding.chezmehdi.net/'));
});
