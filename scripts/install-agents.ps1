# Installs this repo's subagent team into %USERPROFILE%\.claude\agents (all projects).
# Old-name files from the previous version are moved to agents\_old, not deleted.
$ErrorActionPreference = 'Stop'
$base = 'https://raw.githubusercontent.com/KIMHANEULL/phisics-education/claude/explore-all-y9sauy/.claude/agents/'
$dst  = Join-Path $env:USERPROFILE '.claude\agents'
$new  = 'quiz','picky','doc','movie','eagle','rocket','pixel','lock','lens','newton','hunter'
$old  = 'exam-writer','exam-checker','hwp-operator','manim-director','video-qa','lab-analyst','web-builder','security-guard','code-reviewer','error-hunter','physics-checker'

New-Item -ItemType Directory -Force $dst | Out-Null
$oldDir = Join-Path $dst '_old'
foreach ($n in $old) {
  $f = Join-Path $dst "$n.md"
  if (Test-Path $f) { New-Item -ItemType Directory -Force $oldDir | Out-Null; Move-Item -Force $f $oldDir; "moved old: $n.md -> _old\" }
}
foreach ($n in $new) {
  Invoke-WebRequest -UseBasicParsing -Uri "$base$n.md" -OutFile (Join-Path $dst "$n.md")
  $line = (Get-Content (Join-Path $dst "$n.md") -Encoding UTF8 -TotalCount 2)[1]
  "installed: $n.md  ($line)"
}
"done. $((Get-ChildItem (Join-Path $dst '*.md')).Count) agent files in $dst"
