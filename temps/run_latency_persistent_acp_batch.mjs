import { spawn } from 'node:child_process';
import { Writable, Readable } from 'node:stream';
import fs from 'node:fs/promises';
import * as acp from 'file:///C:/Users/jingx/AppData/Roaming/npm/node_modules/@agentclientprotocol/codex-acp/node_modules/@agentclientprotocol/sdk/dist/acp.js';

const [jobsPath, outputPath, cwd] = process.argv.slice(2);
if (!jobsPath || !outputPath || !cwd) {
  console.error('usage: node persistent-acp-batch.mjs <jobs.json> <output.json> <cwd>');
  process.exit(2);
}
const jobs = JSON.parse(await fs.readFile(jobsPath, 'utf8'));
const agentEntry = 'C:/Users/jingx/AppData/Roaming/npm/node_modules/@agentclientprotocol/codex-acp/dist/index.js';
const child = spawn(process.execPath, [agentEntry], {
  stdio: ['pipe', 'pipe', 'inherit'],
  env: { ...process.env, INITIAL_AGENT_MODE: 'read-only' },
  cwd,
});
const stream = acp.ndJsonStream(Writable.toWeb(child.stdin), Readable.toWeb(child.stdout));
const totalStarted = Date.now();
const records = [];
try {
  await acp.client({ name: 'tgn-latency-persistent-probe' })
    .onRequest(acp.methods.client.session.requestPermission, (ctx) => {
      const allow = ctx.params.options.find(o => o.kind === 'allow_once') ?? ctx.params.options[0];
      return allow ? { outcome: { outcome: 'selected', optionId: allow.optionId } } : { outcome: { outcome: 'cancelled' } };
    })
    .connectWith(stream, async (ctx) => {
      const initStarted = Date.now();
      const init = await ctx.request(acp.methods.agent.initialize, {
        protocolVersion: acp.PROTOCOL_VERSION,
        clientCapabilities: {},
      });
      const initSeconds = (Date.now() - initStarted) / 1000;
      const builder = ctx.buildSession(cwd);
      for (const job of jobs) {
        const prompt = await fs.readFile(job.prompt_path, 'utf8');
        let streamedText = '';
        let sessionId = '';
        const started = Date.now();
        const result = await builder.withSession(async (session) => {
          sessionId = session.sessionId;
          await ctx.request(acp.methods.agent.session.setConfigOption, {
            sessionId, configId: 'model', value: job.model,
          });
          await ctx.request(acp.methods.agent.session.setConfigOption, {
            sessionId, configId: 'reasoning_effort', value: job.effort,
          });
          session.prompt(prompt);
          for (;;) {
            const message = await session.nextUpdate();
            if (message.kind === 'stop') return message.response;
            const update = message.update;
            if (update?.sessionUpdate === 'agent_message_chunk' && update.content?.type === 'text') {
              streamedText += update.content.text;
            }
          }
        });
        records.push({
          label: job.label,
          model: job.model,
          effort: job.effort,
          sessionId,
          wall_seconds: (Date.now() - started) / 1000,
          text: streamedText.trim(),
          stopReason: result.stopReason,
          init_seconds_shared: initSeconds,
        });
      }
    });
  await fs.writeFile(outputPath, JSON.stringify({
    ok: true,
    total_wall_seconds: (Date.now() - totalStarted) / 1000,
    records,
  }, null, 2), 'utf8');
} catch (error) {
  await fs.writeFile(outputPath, JSON.stringify({
    ok: false,
    total_wall_seconds: (Date.now() - totalStarted) / 1000,
    records,
    error: String(error?.stack ?? error),
  }, null, 2), 'utf8');
  process.exitCode = 1;
} finally {
  child.kill();
}
