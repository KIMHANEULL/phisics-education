# Installs this repo's subagent team into %USERPROFILE%\.claude\agents (all projects).
# Old-name files from the previous version are moved to .claude\agents-old, not deleted.
$ErrorActionPreference = 'Stop'
$base = 'https://raw.githubusercontent.com/KIMHANEULL/phisics-education/9198c2526a509934ec2a28ae53dcd76cb0ba331f/.claude/agents/'
$dst  = Join-Path $env:USERPROFILE '.claude\agents'
$new  = 'tricky','picky','tidy','artsy','sharpy','fizzy','handy','grumpy','geeky','nerdy','sniffy','chatty','sunny'
$old  = 'exam-writer','exam-checker','hwp-operator','manim-director','video-qa','lab-analyst','web-builder','security-guard','code-reviewer','error-hunter','physics-checker','quiz','doc','movie','eagle','rocket','pixel','lock','lens','newton','hunter','peeky','clicky'

New-Item -ItemType Directory -Force $dst | Out-Null
$oldDir = Join-Path $env:USERPROFILE '.claude\agents-old'
foreach ($n in $old) {
  $f = Join-Path $dst "$n.md"
  if (Test-Path $f) { New-Item -ItemType Directory -Force $oldDir | Out-Null; Move-Item -Force $f $oldDir; "moved old: $n.md -> agents-old\" }
}
foreach ($n in $new) {
  Invoke-WebRequest -UseBasicParsing -Uri "$base$n.md" -OutFile (Join-Path $dst "$n.md")
  $line = (Get-Content (Join-Path $dst "$n.md") -Encoding UTF8 -TotalCount 2)[1]
  "installed: $n.md  ($line)"
}
"done. $((Get-ChildItem (Join-Path $dst '*.md')).Count) agent files in $dst"
