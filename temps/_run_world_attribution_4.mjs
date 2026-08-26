import { spawn } from 'node:child_process';
import { writeFile } from 'node:fs/promises';
const root='C:/dev/tgn-story-mvp';
const exp=root+'/books/real-exp-world-source-attribution-20260826-v1';
const runner=root+'/temps/_run_acp_generic.mjs';
const arms=['A_current_off','B_current_on','C_neutral_off','D_neutral_on'];
function run(a){return new Promise((resolve)=>{const p=spawn(process.execPath,[runner,`${exp}/prompts/${a}.md`,`${exp}/outputs/${a}.json`,`${exp}/outputs/${a}.md`,a,'gpt-5.6-luna','high'],{cwd:root,stdio:['ignore','pipe','pipe']});let out='',err='';p.stdout.on('data',d=>out+=d);p.stderr.on('data',d=>err+=d);p.on('close',async code=>{await writeFile(`${exp}/outputs/${a}.log`,out+'\nSTDERR\n'+err,'utf8');resolve({a,code,out:out.trim().slice(-1000),err:err.trim().slice(-1000)});});});}
const res=await Promise.all(arms.map(run));console.log(JSON.stringify(res,null,2));if(res.some(x=>x.code!==0))process.exitCode=1;
