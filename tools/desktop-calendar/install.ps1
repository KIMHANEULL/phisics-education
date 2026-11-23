# 연구소 바탕화면 달력 설치 (관리자 권한 필요 없음)
# 실행: powershell -NoProfile -ExecutionPolicy Bypass -Command "irm <이 파일의 raw 주소> | iex"
$ErrorActionPreference = 'Stop'
$ref = 'claude/explore-all-y9sauy'
$base = "https://raw.githubusercontent.com/KIMHANEULL/phisics-education/refs/heads/$ref/tools/desktop-calendar"
$dir = Join-Path $env:LOCALAPPDATA 'LabCalendar'
New-Item -ItemType Directory -Force -Path $dir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding $false

Write-Host "`n[1/4] 파일 받는 중..." -ForegroundColor Cyan
foreach ($f in 'index.html', 'sync.ps1', 'LivelyInfo.json') {
    $r = Invoke-WebRequest -UseBasicParsing -Uri "$base/$f"
    [IO.File]::WriteAllBytes((Join-Path $dir $f), $r.RawContentStream.ToArray())
}

$cfgPath = Join-Path $dir 'config.json'
if (Test-Path $cfgPath) {
    Write-Host "[2/4] 저장된 설정을 그대로 씁니다. (다시 넣으려면 $cfgPath 를 지우고 다시 실행)" -ForegroundColor Cyan
} else {
    Write-Host "[2/4] 설정" -ForegroundColor Cyan
    Write-Host "  구글 캘린더 > 설정 > 내 캘린더(이름) > 캘린더 통합 > 'iCal 형식의 비공개 주소'를 복사해 오세요."
    do { $ics = (Read-Host '  비공개 주소 붙여넣기').Trim() } until ($ics -like 'https://calendar.google.com/*')
    $sec = Read-Host '  할 일판 토큰(github_pat_...) 붙여넣기 (할 일 안 보이게 하려면 그냥 Enter)' -AsSecureString
    $token = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec))
    $cfg = [ordered]@{ ics = $ics; token = $token.Trim(); repo = 'KIMHANEULL/lab-hq' }
    [IO.File]::WriteAllText($cfgPath, ($cfg | ConvertTo-Json), $utf8)
}

Write-Host "[3/4] 일정 받아오는 중..." -ForegroundColor Cyan
& powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $dir 'sync.ps1')

# 컴퓨터를 켤 때 한 번, 그 뒤로 1시간마다 갱신 (시작프로그램 폴더, 관리자 권한 불필요)
$startup = [Environment]::GetFolderPath('Startup')
$cmd = "@echo off`r`nstart `"`" /min powershell -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$dir\sync.ps1`" -Loop`r`n"
[IO.File]::WriteAllText((Join-Path $startup 'LabCalendarSync.cmd'), $cmd, [Text.Encoding]::Default)
Start-Process powershell -WindowStyle Hidden -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$dir\sync.ps1`" -Loop"

Write-Host "[4/4] 끝! 이제 Lively Wallpaper 에서 아래 파일을 배경으로 추가하세요." -ForegroundColor Green
Write-Host "  $dir\index.html" -ForegroundColor Yellow
Write-Host "  (배경 그림을 바꾸려면 그 폴더에 bg.jpg 를 넣으세요)"
Start-Process explorer.exe $dir
