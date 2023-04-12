# Based on the powershell idea from:
# https://gist.github.com/samiru/80a80916a1d1ebabf7b472f3aecca1b0
$initpath = Get-Location

# Check each folder in current working directory
foreach ($path in Get-ChildItem -Directory) {
    # Check if the directory has git files (.git)
    if (Test-Path (Join-Path $path.FullName ".git")) {
        # Print to screen each folder name to make it easier to see folders that fail updates (stashed files etc)
        Write-Host "##################################################"
        Write-Host "Updating git repository in $($path.FullName)"
        Write-Host "##################################################"

        # Run git command in folder
        Set-Location $path.FullName
        & git pull
    } else {
        # skipping dir if it doesn't have .git files
        Write-Host "$($path.FullName) is not a git repository, skipping..."
    }
}

Set-Location $initpath
pause
