import { spawn } from 'node:child_process';
import { Writable, Readable } from 'node:stream';
import fs from 'node:fs/promises';
const sdkRoot = 'C:/Users/jingx/AppData/Roaming/npm/node_modules/@agentclientprotocol/codex-acp/node_modules/@agentclientprotocol/sdk/dist/acp.js';
const acp = await import('file:///' + sdkRoot);
const [,, promptPath, outputPath, model='gpt-5.6-luna', effort='high', label='acp-run', ...additionalDirs] = process.argv;
const prompt = await fs.readFile(promptPath, 'utf8');
let text = '';
let updates = [];
const agentExe = 'C:/Users/jingx/AppData/Roaming/npm/codex-acp.cmd';
const child = spawn(agentExe, [], { cwd: process.cwd(), stdio: ['pipe','pipe','pipe'], shell: true, env: {...process.env, DEFAULT_AUTH_REQUEST:'{"methodId":"chat-gpt"}', INITIAL_AGENT_MODE:'read-only'} });
let stderr=''; child.stderr.on('data',d=>stderr+=d.toString());
const client = {
  async sessionUpdate(params){
    const u=params.update; updates.push(u);
    if(u?.sessionUpdate==='agent_message_chunk' && u.content?.type==='text') text += u.content.text;
  },
  async requestPermission(params){
    const preferred = params.options.find(o=>/allow|approve|once/i.test(o.kind||o.name||'')) || params.options[0];
    return {outcome:{outcome:'selected', optionId:preferred.optionId}};
  },
  async writeTextFile(){ throw new Error('read-only client: writeTextFile denied'); },
  async readTextFile(params){ return {content: await fs.readFile(params.path,'utf8')}; }
};
const stream=acp.ndJsonStream(Writable.toWeb(child.stdin), Readable.toWeb(child.stdout));
const conn=new acp.ClientSideConnection(()=>client, stream);
const started=Date.now();
try{
  const init=await conn.initialize({protocolVersion:acp.PROTOCOL_VERSION, clientCapabilities:{fs:{readTextFile:true,writeTextFile:false}}});
  let sess;
  try { sess=await conn.newSession({cwd:process.cwd(), additionalDirectories:additionalDirs, mcpServers:[]}); }
  catch(e){
    if(String(e).includes('auth_required')) { await conn.authenticate({methodId:'chat-gpt'}); sess=await conn.newSession({cwd:process.cwd(), additionalDirectories:additionalDirs, mcpServers:[]}); }
    else throw e;
  }
  const sid=sess.sessionId;
  await conn.setSessionMode({sessionId:sid, modeId:'read-only'}).catch(()=>{});
  await conn.setSessionConfigOption({sessionId:sid, configId:'model', value:model});
  await conn.setSessionConfigOption({sessionId:sid, configId:'reasoning_effort', value:effort});
  const result=await conn.prompt({sessionId:sid, prompt:[{type:'text',text:prompt}]});
  const out={ok:true,label,model,effort,additionalDirectories:additionalDirs,wall_seconds:(Date.now()-started)/1000,text,result,session:sess,init};
  await fs.writeFile(outputPath, JSON.stringify(out,null,2),'utf8');
  await conn.closeSession({sessionId:sid}).catch(()=>{});
} catch(e){
  const out={ok:false,label,model,effort,additionalDirectories:additionalDirs,wall_seconds:(Date.now()-started)/1000,text,error:String(e),stack:e?.stack,stderr,updates};
  await fs.writeFile(outputPath, JSON.stringify(out,null,2),'utf8');
  process.exitCode=1;
} finally { child.kill(); }
