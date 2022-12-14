# from: https://gist.github.com/samiru/80a80916a1d1ebabf7b472f3aecca1b0
$initpath = Get-Location
foreach($path in Get-ChildItem) {
    if ($path.Attributes -eq "Directory") {
        Set-Location $path.FullName
        git pull
    }
}
Set-Location $initpath


