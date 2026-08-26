$ErrorActionPreference = 'Stop'
$root = 'C:\dev\tgn-story-mvp'
$exp = Join-Path $root 'books\real-exp-private-prototype-final-novel-20260826-v1'
$helper = Join-Path $root 'temps\private_final_pipeline.py'
$python = Join-Path $root '.venv\Scripts\python.exe'
$runner = 'C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs'
$log = Join-Path $exp 'RUN_LOG.txt'
function Log($s) { $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $s"; Add-Content -Encoding utf8 $log $line; Write-Output $line }
function RunACP($prompt,$out,$model,$effort) {
  Log "START $model/$effort :: $prompt"
  node $runner $prompt $out $model $effort $root | Add-Content -Encoding utf8 $log
  if ($LASTEXITCODE -ne 0) { throw "ACP failed: $prompt" }
  Log "DONE $model/$effort :: $out"
}
Log 'waiting for outline'
while (-not (Test-Path (Join-Path $exp 'OUTLINE_ACP.json'))) { Start-Sleep -Seconds 5 }
& $python $helper outline | Add-Content -Encoding utf8 $log
if ($LASTEXITCODE -ne 0) { throw 'outline materialize failed' }
Log 'outline materialized'
for ($n=1; $n -le 5; $n++) {
  $rd = Join-Path $exp ("runs\chapter-{0:d4}" -f $n)
  & $python $helper director $n | Add-Content -Encoding utf8 $log
  RunACP (Join-Path $rd 'director_prompt.md') (Join-Path $rd 'director_acp.json') 'gpt-5.6-luna' 'high'
  & $python $helper materialize $n director | Add-Content -Encoding utf8 $log
  & $python $helper curator $n | Add-Content -Encoding utf8 $log
  RunACP (Join-Path $rd 'curator_prompt.md') (Join-Path $rd 'curator_acp.json') 'gpt-5.6-luna' 'high'
  & $python $helper materialize $n curator | Add-Content -Encoding utf8 $log
  & $python $helper primary $n | Add-Content -Encoding utf8 $log
  RunACP (Join-Path $rd 'primary_prompt.md') (Join-Path $rd 'primary_acp.json') 'gpt-5.6-terra' 'high'
  & $python $helper body $n | Add-Content -Encoding utf8 $log
  & $python $helper state $n | Add-Content -Encoding utf8 $log
  RunACP (Join-Path $rd 'state_prompt.md') (Join-Path $rd 'state_acp.json') 'gpt-5.6-luna' 'low'
  & $python $helper apply $n | Add-Content -Encoding utf8 $log
  Log "CHAPTER $n COMPLETE"
}
& $python $helper combine | Add-Content -Encoding utf8 $log
Log 'ALL COMPLETE'
Set-Content -Encoding utf8 (Join-Path $exp 'RUN_COMPLETE.txt') 'ok'
