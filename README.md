# Memory Optimizer Pro
Memory Optimizer Pro is a PowerShell script designed to optimize your system's memory usage by clearing the working set of processes. It helps free up memory resources, making your system run more efficiently. The script allows you to whitelist specific processes to prevent their working sets from being cleared.

## Features
- Automatically clears the working set of processes
- Whitelist specific processes to prevent memory clearing
- Auto-elevates to administrator privileges
- Runs in a loop, clearing memory every 60 seconds
## Prerequisites
Windows OS with PowerShell 3.0 or higher
## Installation
Clone the repository or download the script `MemoryOptimizerPro.ps1`
Add any processes you'd like to whitelist in the $whitelist array.
Save the script.
## Usage
- Open PowerShell as an administrator.
- Navigate to the directory containing `MemoryOptimizerPro.ps1`
- Run the script by executing `.\MemoryOptimizerPro.ps1`
- The script will automatically clear the working sets of non-whitelisted processes every 60 seconds.
## Customization
You can customize the whitelist and the time interval between memory clearings in the script:

- Edit the `$whitelist` array to include the names of any processes you want to protect from having their working sets cleared.
- Change the `Start-Sleep -Seconds 60` line to modify the interval between memory clearing cycles. Replace 60 with the desired number of seconds.
## License
Memory Optimizer Pro is released under the Apache 2.0 License.

## Contributing
If you'd like to contribute to the project, feel free to submit a pull request or create an issue with your suggestions and feedback.

### Future features
Some features I would like in the future are a standby-list memory cleaner
