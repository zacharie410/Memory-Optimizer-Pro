if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell.exe -ArgumentList "-ExecutionPolicy Bypass", "-File `"$($MyInvocation.MyCommand.Path)`"" -Verb RunAs
    exit
}

$whitelist = @(
    "System",
    "explorer",
    "YourWhitelistedProcess1",
    "YourWhitelistedProcess2"
)

$Definition = @"
using System;
using System.Runtime.InteropServices;

public class Memory {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool SetProcessWorkingSetSize(IntPtr proc, IntPtr min, IntPtr max);
}
"@

$Type = Add-Type -TypeDefinition $Definition -PassThru

while ($true) {
    $processes = Get-Process
    $totalMemoryCleared = 0

    foreach ($process in $processes) {
        if ($whitelist -notcontains $process.ProcessName) {
            
            try {
                $beforeClear = $process.WorkingSet64
                $Type::SetProcessWorkingSetSize($process.Handle, -1, -1) | Out-Null
                $process.Refresh()
                $afterClear = $process.WorkingSet64
                $memoryCleared = $beforeClear - $afterClear
                $totalMemoryCleared += $memoryCleared

                Write-Host "Cleared working set for $($process.ProcessName)"
            } catch {
                Write-Warning "Failed to clear working set for $($process.ProcessName)"
            }
        } else {
            Write-Host "Skipping $($process.ProcessName) as it is in the whitelist"
        }
    }

    Write-Host "Total memory cleared: $($totalMemoryCleared / 1MB) MB"

    Write-Host "Waiting for 60 seconds before running again..."
    Start-Sleep -Seconds 60
}
