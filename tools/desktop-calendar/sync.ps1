# 연구소 바탕화면 달력: 구글 캘린더(비공개 iCal 주소)와 할 일판(widget.json)을 받아 events.js 로 저장한다.
# config.json 은 이 폴더에만 있고 깃에 올라가지 않는다. -Loop 를 주면 1시간마다 반복한다.
param([switch]$Loop)
$dir = Split-Path -Parent $MyInvocation.MyCommand.Path
$utf8 = New-Object System.Text.UTF8Encoding $false

function Sync-Once {
    $cfg = Get-Content (Join-Path $dir 'config.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $out = Join-Path $dir 'events.js'
    $old = $null
    if (Test-Path $out) { $old = [IO.File]::ReadAllText($out, $utf8) }

    $ics = $null; $todos = $null; $err = @()
    try {
        $r = Invoke-WebRequest -UseBasicParsing -Uri $cfg.ics -TimeoutSec 30
        $ics = [Text.Encoding]::UTF8.GetString($r.RawContentStream.ToArray())
        if ($ics -notmatch 'BEGIN:VCALENDAR') { $ics = $null; $err += '캘린더 주소 확인' }
    } catch { $err += '캘린더 받기 실패' }

    if ($cfg.token) {
        try {
            $h = @{ Authorization = "Bearer $($cfg.token)"; Accept = 'application/vnd.github.raw+json'; 'User-Agent' = 'lab-calendar' }
            $r = Invoke-WebRequest -UseBasicParsing -Uri "https://api.github.com/repos/$($cfg.repo)/contents/widget.json" -Headers $h -TimeoutSec 30
            $todos = ([Text.Encoding]::UTF8.GetString($r.RawContentStream.ToArray()) | ConvertFrom-Json).todos
        } catch { $err += '할 일 받기 실패' }
    }

    # 실패한 쪽은 지난번 자료를 그대로 둔다
    if ($old -and ($ics -eq $null -or ($cfg.token -and $todos -eq $null))) {
        try {
            $prev = ($old -replace '^window\.LAB = ', '' -replace ';\s*$', '') | ConvertFrom-Json
            if ($ics -eq $null) { $ics = $prev.ics }
            if ($cfg.token -and $todos -eq $null) { $todos = $prev.todos }
        } catch {}
    }
    $data = [ordered]@{ ics = $ics; todos = $todos; synced = (Get-Date -Format 'yyyy-MM-dd HH:mm'); error = ($err -join ', ') }
    [IO.File]::WriteAllText($out, 'window.LAB = ' + ($data | ConvertTo-Json -Depth 6 -Compress) + ';', $utf8)
}

do {
    try { Sync-Once } catch {}
    if ($Loop) { Start-Sleep -Seconds 3600 }
} while ($Loop)
