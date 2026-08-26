import { spawn } from 'node:child_process';
import { Writable, Readable } from 'node:stream';
import { readFile, writeFile } from 'node:fs/promises';
import { performance } from 'node:perf_hooks';
import * as acp from 'file:///C:/Users/jingx/AppData/Roaming/npm/node_modules/@agentclientprotocol/codex-acp/node_modules/@agentclientprotocol/sdk/dist/acp.js';
const [promptPath,outPath,mdPath,label,model='gpt-5.6-luna',effort='high'] = process.argv.slice(2);
if (!promptPath || !outPath || !mdPath || !label) throw new Error('usage: prompt outjson outmd label [model] [effort]');
const prompt = await readFile(promptPath,'utf8');
const ps = spawn('pwsh.exe',['-NoProfile','-File','C:/Users/jingx/AppData/Roaming/npm/codex-acp.ps1'],{cwd:'C:/dev/tgn-story-mvp',env:{...process.env,INITIAL_AGENT_MODE:'read-only'},stdio:['pipe','pipe','inherit']});
const stream=acp.ndJsonStream(Writable.toWeb(ps.stdin),Readable.toWeb(ps.stdout));
let chunks=''; const updates=[]; const t0=performance.now();
const client=acp.client({name:'tgn-controlled-llm-probe'}).onRequest(acp.methods.client.session.requestPermission,async({params})=>{const reject=params.options.find(o=>String(o.kind).includes('reject'))||params.options[0]; return {outcome:{outcome:'selected',optionId:reject.optionId}};});
try{
 const result=await client.connectWith(stream,async(ctx)=>{
  const init=await ctx.request(acp.methods.agent.initialize,{protocolVersion:acp.PROTOCOL_VERSION,clientCapabilities:{}});
  return await ctx.buildSession('C:/dev/tgn-story-mvp').withSession(async(session)=>{
   await ctx.request(acp.methods.agent.session.setMode,{sessionId:session.sessionId,modeId:'read-only'});
   await ctx.request(acp.methods.agent.session.setConfigOption,{sessionId:session.sessionId,configId:'model',value:model});
   await ctx.request(acp.methods.agent.session.setConfigOption,{sessionId:session.sessionId,configId:'reasoning_effort',value:effort});
   const pp=session.prompt(prompt);
   for(;;){const msg=await session.nextUpdate(); if(msg.kind==='stop'){const response=await pp; return {init,session:session.newSessionResponse,response};} const u=msg.update; if(u.sessionUpdate==='agent_message_chunk'&&u.content?.type==='text') chunks+=u.content.text; if(['tool_call','tool_call_update','plan','usage_update'].includes(u.sessionUpdate)) updates.push(u);}
  });
 });
 const wall=(performance.now()-t0)/1000; await writeFile(mdPath,chunks,'utf8'); const slim={ok:true,label,model,effort,mode:'read-only',wall_seconds:Number(wall.toFixed(3)),text:chunks,stopReason:result.response?.stopReason,sessionId:result.session?.sessionId,models:result.session?.models,modes:result.session?.modes,configOptions:result.session?.configOptions,updates}; await writeFile(outPath,JSON.stringify(slim,null,2),'utf8'); console.log(JSON.stringify({ok:true,wall_seconds:slim.wall_seconds,chars:chunks.length,stopReason:slim.stopReason,updates:updates.length},null,2));
}catch(e){const wall=(performance.now()-t0)/1000; await writeFile(outPath,JSON.stringify({ok:false,label,model,effort,wall_seconds:Number(wall.toFixed(3)),error:String(e?.stack||e),text:chunks,updates},null,2),'utf8'); console.error(e); process.exitCode=1;}finally{ps.kill();}
