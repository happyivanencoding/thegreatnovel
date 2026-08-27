$ErrorActionPreference='Stop'
$root='C:\dev\tgn-story-mvp'
$py=Join-Path $root '.venv\Scripts\python.exe'
$helper=Join-Path $root 'temps\run_orientation_world_entry_final.py'
$runner='C:\Users\jingx\AppData\Local\Temp\run-codex-acp.mjs'
$exp=Join-Path $root 'books\real-exp-private-prototype-orientation-world-entry-final-20260827-v1'
function Run-Acp([string]$prompt,[string]$output,[string]$model,[string]$effort){
  & node $runner $prompt $output $model $effort $root
  if($LASTEXITCODE -ne 0){throw "ACP failed: $prompt"}
}
for($n=3;$n -le 5;$n++){
  $nn='{0:D4}' -f $n
  $run=Join-Path $exp "runs\chapter-$nn"
  Write-Output "=== CHAPTER $n DIRECTOR ==="
  & $py $helper director $n
  Run-Acp (Join-Path $run 'director_prompt.md') (Join-Path $run 'director_acp.json') 'gpt-5.6-luna' 'high'
  & $py $helper mat $n director
  Write-Output "=== CHAPTER $n CURATOR ==="
  & $py $helper curator $n
  Run-Acp (Join-Path $run 'curator_prompt.md') (Join-Path $run 'curator_acp.json') 'gpt-5.6-luna' 'high'
  & $py $helper mat $n curator
  Write-Output "=== CHAPTER $n PRIMARY ==="
  & $py $helper primary $n
  Run-Acp (Join-Path $run 'primary_prompt.md') (Join-Path $run 'primary_acp.json') 'gpt-5.6-terra' 'high'
  & $py $helper body $n
  Write-Output "=== CHAPTER $n STATE ==="
  & $py $helper state $n
  Run-Acp (Join-Path $run 'state_prompt.md') (Join-Path $run 'state_acp.json') 'gpt-5.6-luna' 'low'
  & $py $helper apply $n
}
& $py $helper combine
& $py $helper metrics
Write-Output '=== DONE ==='
