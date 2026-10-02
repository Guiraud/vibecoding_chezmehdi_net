import { cp, mkdir, rm } from 'node:fs/promises';
await rm('dist', { recursive: true, force: true });
await mkdir('dist');
await cp('web', 'dist', { recursive: true });
console.log('Site statique construit dans dist/');
