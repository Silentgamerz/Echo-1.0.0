# get-dir.ps1
$shell = New-Object -ComObject "Shell.Application"
$windows = $shell.Windows()
foreach ($win in $windows) {
    try {
        $folder = $win.Document.Folder
        if ($folder.Self.Path) {
            Write-Output $folder.Self.Path
            exit
        }
    } catch {}
}
