# Authoring utility, Windows only. CI renders the saved outlines without fonts.
param([string]$OnlyTheme)
Add-Type -AssemblyName System.Drawing
$styles = @{
    'phosphor' = @('Lucida Console', 'Regular')
    'desktop95' = @('Tahoma', 'Bold')
    'construction' = @('Times New Roman', 'Bold')
    'matrix' = @('Courier New', 'Bold')
    'y2k' = @('Arial', 'Bold, Italic')
    'aqua' = @('Georgia', 'Regular')
    'aero' = @('Segoe UI Light', 'Regular')
    'metro' = @('Segoe UI Light', 'Regular')
    'material' = @('Bahnschrift', 'Regular')
    'glass' = @('Segoe UI', 'Bold')
    'field-notes' = @('Palatino Linotype', 'Regular')
}
$labels = @('Robin-G0','ROBIN-G0','Motion Input Grid','Motion','Input Grid','Public activity',
    'Phosphor','Desktop 95','Under Construction','Matrix / Construct','Y2K Chrome','Aqua',
    'Frutiger Aero','Metro','Material','Glass / Fluent','Field Notes')
$result = @{}
foreach ($key in $styles.Keys) {
    if ($OnlyTheme -and $key -ne $OnlyTheme) { continue }
    $family = [System.Drawing.FontFamily]::new($styles[$key][0])
    $fontStyle = [System.Enum]::Parse([System.Drawing.FontStyle], $styles[$key][1])
    $entries = [System.Collections.Generic.Dictionary[string,object]]::new([System.StringComparer]::Ordinal)
    $themeLabels = if ($key -eq 'aero') { $labels + @('About me','GitHub activity') } else { $labels }
    foreach ($label in $themeLabels) {
        $path = [System.Drawing.Drawing2D.GraphicsPath]::new()
        $path.AddString($label, $family, [int]$fontStyle, 100,
            [System.Drawing.PointF]::new(0,0), [System.Drawing.StringFormat]::GenericTypographic)
        $bounds = $path.GetBounds()
        $points = $path.PathPoints
        $types = $path.PathTypes
        $parts = [System.Collections.Generic.List[string]]::new()
        $ci = [System.Globalization.CultureInfo]::InvariantCulture
        for ($i = 0; $i -lt $points.Length; $i++) {
            $x = ($points[$i].X - $bounds.X).ToString('0.##', $ci)
            $y = ($points[$i].Y - $bounds.Y).ToString('0.##', $ci)
            $kind = $types[$i] -band 7
            if ($kind -eq 0) { $parts.Add("M$x $y") }
            elseif ($kind -eq 1) { $parts.Add("L$x $y") }
            elseif ($kind -eq 3) {
                $x2 = ($points[$i+1].X - $bounds.X).ToString('0.##', $ci)
                $y2 = ($points[$i+1].Y - $bounds.Y).ToString('0.##', $ci)
                $x3 = ($points[$i+2].X - $bounds.X).ToString('0.##', $ci)
                $y3 = ($points[$i+2].Y - $bounds.Y).ToString('0.##', $ci)
                $parts.Add("C$x $y $x2 $y2 $x3 $y3")
                $i += 2
            }
            if (($types[$i] -band 128) -ne 0) { $parts.Add('Z') }
        }
        $entries[$label] = @{ d = $parts -join ''; width = [double]$bounds.Width; height = [double]$bounds.Height }
        $path.Dispose()
    }
    $result[$key] = @{ family = $styles[$key][0]; glyphs = $entries }
    $family.Dispose()
}
$target = Join-Path $PSScriptRoot 'typefaces.json'
if ($OnlyTheme) { $target = Join-Path $PSScriptRoot "../.design-work/typefaces-$OnlyTheme.json" }
[System.IO.File]::WriteAllText($target, ($result | ConvertTo-Json -Depth 6 -Compress), [System.Text.UTF8Encoding]::new($false))
