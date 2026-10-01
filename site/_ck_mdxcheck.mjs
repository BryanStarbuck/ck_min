// Compiles pages the way the REAL Docusaurus build does.
// Do NOT add @slorber/remark-comment here: the site config does not enable
// mdx1Compat.comments, so <!-- --> is a hard error in BOTH .md and .mdx.
// Adding it once made every laws/*.md page pass locally and fail the deploy.
import { compile } from '@mdx-js/mdx';
import gfm from 'remark-gfm';
import fs from 'fs';
let bad = 0;
for (const f of process.argv.slice(2)) {
  let s = fs.readFileSync(f, 'utf8').replace(/^---\n[\s\S]*?\n---\n/, '');
  try { await compile(s, { remarkPlugins: [gfm] }); }
  catch (e) { bad++; console.log('FAIL\t' + f + '\t' + String(e.message).split('\n')[0]); }
}
console.log('compiled ' + (process.argv.length - 2) + ' files, ' + bad + ' failing');
