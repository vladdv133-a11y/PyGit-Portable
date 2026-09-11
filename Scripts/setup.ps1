$exeName = "PyGit.exe"
$exePath = $null

# 1. Search in current directory and subfolders
$foundInCurrent = Get-ChildItem -Path $ExecutionContext.SessionState.Path.CurrentLocation -Filter $exeName -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1

if ($foundInCurrent) {
    $exePath = $foundInCurrent.FullName
} else {
    # 2. Search in parent directories
    $parentDir = (Get-Item .).Parent
    while ($parentDir -and -not $exePath) {
        $foundInParent = Get-ChildItem -Path $parentDir.FullName -Filter $exeName -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($foundInParent) {
            $exePath = $foundInParent.FullName
        } else {
            $parentDir = $parentDir.Parent
        }
    }
}

if ($exePath) {
    function global:pygit { & $exePath $args }
    Write-Host "PyGit activated: $exePath" -ForegroundColor Green
} else {
    Write-Host "Error: PyGit.exe not found nearby." -ForegroundColor Red
}