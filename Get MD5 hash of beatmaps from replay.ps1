$path = Read-Host 'Enter path of replay file(s)'
Set-Location $path
$replayPath = Get-ChildItem *.osr
Clear-Content !MD5.txt -ErrorAction SilentlyContinue
foreach ($file in $replayPath)
{
    $content = Get-Content -LiteralPath $file -encoding byte -totalcount 39
    $content = [System.Collections.ArrayList]($content)
    $content.RemoveRange(0,7)
    $content = [System.Text.Encoding]::ASCII.GetString($content)
    Write-Host "Beatmap MD5: $content for $file"
    $content | Out-File !MD5.txt -Encoding ASCII -Append
}
#Remove duplicate
$unique = Get-Content !MD5.txt | Sort-Object | Get-Unique
$unique | Out-File !MD5.txt -Encoding ASCII

$path = $path.trim()
Write-Host "`nMD5 hash written at "$path'\!MD5.txt'
pause