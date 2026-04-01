# OpenClaw Backup Script
$date = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$branch = "main"

Set-Location "C:\Users\Texeira\.openclaw"

git add -A
git commit -m "backup: $date"
git push origin $branch

Write-Host "Backup concluido: $date"
