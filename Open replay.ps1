$path = Read-Host 'Enter path of replay file(s)'
Set-Location $path
$replayPath = Get-ChildItem *.osr
Clear-Content !opened.log -ErrorAction SilentlyContinue
foreach ($file in $replayPath)
{
    Start-Process $file
    $file = $file.ToString()
    Write-Host "Opened $file"
    $file | Out-File !opened.log -Encoding ASCII -Append
}
$path = $path.trim()
Write-Host "`nLog written at "$path'\!opened.log'
pause