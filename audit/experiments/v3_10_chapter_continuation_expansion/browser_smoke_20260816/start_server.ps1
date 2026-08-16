$browserRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:NOVEL_REFERENCE_CORPUS_ROOT = 'C:\GoogleDrive\笔记\卡片盒子\20_Knowledge\修仙小说素材库\reference-corpus'
$stdoutPath = Join-Path $browserRoot 'server.stdout.log'
$stderrPath = Join-Path $browserRoot 'server.stderr.log'
$pythonPath = 'C:\Users\jingx\anaconda3\python.exe'
$serverPath = Join-Path $browserRoot 'server.py'
$process = Start-Process -WindowStyle Hidden -FilePath $pythonPath -ArgumentList @('-S', $serverPath) -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath -PassThru
$process.Id | Set-Content (Join-Path $browserRoot 'server.pid')
