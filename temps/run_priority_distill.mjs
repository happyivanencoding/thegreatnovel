import { spawn } from 'node:child_process';
import fs from 'node:fs/promises';
const manifestPath='C:/dev/tgn-story-mvp/temps/priority_distill_jobs.json';
const runner='C:/dev/tgn-story-mvp/temps/acp_readonly_runner.mjs';
const manifest=JSON.parse(await fs.readFile(manifestPath,'utf8'));
const jobs=manifest.jobs; const root=manifest.gbrain_root; const concurrency=6;
let next=0, active=0, done=0, failed=0;
async function isOk(path){ try{ const x=JSON.parse(await fs.readFile(path,'utf8')); return x.ok===true && (x.text||'').length>500; }catch{return false;} }
async function launch(job){
  if(await isOk(job.output)){ console.log(`SKIP ${job.id}`); done++; return; }
  await fs.mkdir(job.output.replace(/[/\\][^/\\]+$/,''),{recursive:true});
  console.log(`START ${job.id} ${job.model}`); active++;
  const t=Date.now();
  const child=spawn(process.execPath,[runner,job.prompt,job.output,job.model,job.effort,job.id,root],{cwd:'C:/dev/tgn-story-mvp',stdio:['ignore','pipe','pipe'],env:process.env});
  let err=''; child.stderr.on('data',d=>{err+=d.toString(); if(err.length>4000)err=err.slice(-4000);});
  child.on('exit',async code=>{
    active--; const ok=await isOk(job.output); if(ok){done++; console.log(`DONE ${job.id} ${((Date.now()-t)/1000).toFixed(1)}s`);} else {failed++; console.log(`FAIL ${job.id} code=${code} ${err.slice(-800)}`);} pump();
  });
}
function pump(){
  while(active<concurrency && next<jobs.length){ launch(jobs[next++]); }
  if(next>=jobs.length && active===0){ console.log(`ALL_FINISHED done=${done} failed=${failed}`); process.exit(failed?2:0); }
}
pump();
