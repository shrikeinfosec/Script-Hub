$scriptPath = $MyInvocation.MyCommand.Path
$dir = Split-Path $scriptPath

Push-Location $dir

Clear-Host
Write-Host "`nGenerate Markdown Report v1.0.0`n"

$filename = $args[0]
$fullFilePath = Get-ChildItem $filename | Select-Object -ExpandProperty FullName
$fileDirectory = Split-Path -Path $fullFilePath

if ( $filename -match "\.\w{1,5}$" ) {
    # Strip the extension off of the filename so we can set the output format as PDF.
    $filename = [System.IO.Path]::GetFileNameWithoutExtension($filename)
}

$outputName = $filename + ".pdf"


Write-Host $("=" * 5)
Write-Host "Selected File: $filename"
Write-Host "File Path: $fullFilePath"
Write-Host "Directory: $fileDirectory"
Write-Host "Output Filename: $outputName"
Write-Host $("=" * 5)`n

Set-Location $fileDirectory

Write-Host "Generating PDF Report..."
pandoc "$fullFilePath" -o "$dir\$outputName" --from markdown+yaml_metadata_block+raw_html --template eisvogel --table-of-contents --toc-depth 6 --number-sections --top-level-division=chapter --highlight-style breezedark --variable colorlinks=true

Set-Location $dir

Write-Host "PDF Report Generation complete.`n"
Write-Host "You can find your file at $dir\$filename.pdf`n"