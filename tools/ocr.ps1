param(
    [int]$Start = 1,
    [int]$End = 229,
    [string]$PagesDir = "_book\pages",
    [string]$OutDir = "_book\ocr"
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
})[0]

function Await($WinRtTask, $ResultType) {
    $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}

$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Globalization.Language, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.Streams.InMemoryRandomAccessStream, Windows.Foundation, ContentType = WindowsRuntime]
$null = [Windows.Storage.Streams.DataWriter, Windows.Foundation, ContentType = WindowsRuntime]

$lang = New-Object Windows.Globalization.Language "zh-Hans-CN"
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
if ($null -eq $engine) { $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages() }
if ($null -eq $engine) { throw "no OCR engine available" }

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Force -Path $OutDir | Out-Null }

for ($i = $Start; $i -le $End; $i++) {
    $name = "page_{0:d3}.jpg" -f $i
    $src = Join-Path $PagesDir $name
    $dst = Join-Path $OutDir ("page_{0:d3}.txt" -f $i)
    if (-not (Test-Path $src)) { Write-Output "MISSING $name"; continue }
    if (Test-Path $dst) { continue }
    try {
        $bytes = [System.IO.File]::ReadAllBytes((Resolve-Path $src).Path)
        $ras = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
        $dw = New-Object Windows.Storage.Streams.DataWriter($ras)
        $dw.WriteBytes($bytes)
        Await ($dw.StoreAsync()) ([uint32]) | Out-Null
        Await ($dw.FlushAsync()) ([bool]) | Out-Null
        $dw.DetachStream() | Out-Null
        $ras.Seek(0)
        $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($ras)) ([Windows.Graphics.Imaging.BitmapDecoder])
        $bitmap = Await ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
        $result = Await ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
        $sb = New-Object System.Text.StringBuilder
        foreach ($line in $result.Lines) { [void]$sb.AppendLine($line.Text) }
        $text = $sb.ToString()
        [System.IO.File]::WriteAllText((Join-Path (Get-Location) $dst), $text, [System.Text.UTF8Encoding]::new($false))
        $ras.Dispose()
        $bitmap.Dispose()
        Write-Output ("OK {0} lines={1}" -f $name, $result.Lines.Count)
    }
    catch {
        Write-Output ("FAIL {0} {1}" -f $name, $_.Exception.Message)
    }
}
Write-Output "DONE $Start-$End"
