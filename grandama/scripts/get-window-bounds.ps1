# Get window position (Left, Top) for the first window whose title contains the given string.
# Usage: .\get-window-bounds.ps1 [TitleSubstring]
# If no arg, uses foreground window. If arg (e.g. "localhost" or "Project Grandma"), finds that window.
param([string]$TitlePart = "")

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class Win32 {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hwnd, out RECT r);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr hwnd, StringBuilder text, int count);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hwnd);
  public delegate bool EnumWindowsProc(IntPtr hwnd, IntPtr lParam);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
}
"@ -ErrorAction SilentlyContinue

$script:found = $null
$script:search = $TitlePart

if ($TitlePart -ne "") {
  $callback = [Win32+EnumWindowsProc]{
    param($hwnd, $lParam)
    if (-not [Win32]::IsWindowVisible($hwnd)) { return $true }
    $sb = New-Object System.Text.StringBuilder 256
    [Win32]::GetWindowText($hwnd, $sb, $sb.Capacity) | Out-Null
    $title = $sb.ToString()
    if ($title -and $title.IndexOf($script:search, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
      $script:found = $hwnd
      return $false
    }
    return $true
  }
  [Win32]::EnumWindows($callback, [IntPtr]::Zero) | Out-Null
  $h = $script:found
} else {
  $h = [Win32]::GetForegroundWindow()
}

if ($h -eq $null -or $h -eq [IntPtr]::Zero) {
  Write-Error "No matching window found"
  exit 1
}
$r = New-Object Win32+RECT
[Win32]::GetWindowRect($h, [ref]$r) | Out-Null
Write-Output "$($r.Left) $($r.Top)"
