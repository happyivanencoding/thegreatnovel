$ErrorActionPreference='Stop'
$root='C:\dev\tgn-story-mvp'
$exp=Join-Path $root 'books\reader-feedback-world-fix-v2'
$py=Join-Path $root '.venv\Scripts\python.exe'
$helper=Join-Path $root 'temps\rf_world_fix_helper.py'
$runner=Join-Path $root 'temps\acp_readonly_runner.mjs'
$env:PYTHONPATH=Join-Path $root 'src'
& $py $helper prepare
for($n=4; $n -le 8; $n++){
  $rd=Join-Path $exp ("runs\chapter-{0:D4}" -f $n)
  Write-Output "=== CHAPTER $n DIRECTOR ==="
  & $py $helper director $n
  node $runner (Join-Path $rd 'director_prompt.md') (Join-Path $rd 'director_acp.json') gpt-5.6-luna high ("worldfix-ch{0}-director" -f $n)
  & $py $helper materialize $n director
  Write-Output "=== CHAPTER $n CURATOR ==="
  & $py $helper curator $n
  node $runner (Join-Path $rd 'curator_prompt.md') (Join-Path $rd 'curator_acp.json') gpt-5.6-luna high ("worldfix-ch{0}-curator" -f $n)
  & $py $helper materialize $n curator
  Write-Output "=== CHAPTER $n PRIMARY ==="
  & $py $helper primary $n
  node $runner (Join-Path $rd 'primary_prompt.md') (Join-Path $rd 'primary_acp.json') gpt-5.6-terra high ("worldfix-ch{0}-primary" -f $n)
  & $py $helper body $n
  Write-Output "=== CHAPTER $n STATE ==="
  & $py $helper state $n
  node $runner (Join-Path $rd 'state_prompt.md') (Join-Path $rd 'state_acp.json') gpt-5.6-luna low ("worldfix-ch{0}-state" -f $n)
  & $py $helper apply $n
}
Write-Output '=== ALL DONE ==='
Get-ChildItem (Join-Path $exp 'chapters') -File | Select-Object Name,Length
