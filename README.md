# PortScanCLI

Python CLI tool that scans a target IP or domain for open, closed, and unknown TCP ports. The program supports retries, timeout configuration, and writes results
to an output file. (Default output file: scanResults.txt)

## Overview

The tool scans each port in the user defined range and reports the status of the ports to the screen and then to an output file. If the user interupts the scan it inputs all progress into the output file.

## Modules

- argparse: for command line arguments\
- socket: for TCP connections to ports\
- sys: for error codes\
- time: for delays between retries\
- datetime: for timestamps in the output file\

## Standard arguments

    py PortScanCLI.py -t <TARGET> --start-port <STARTPORT> --end-port <ENDPORT>

### Required Arguments

  Argument       Description
  -------------- -----------------------------------------------
  -t, --target   Target IP or domain (example: www.google.com)
  --start-port   Starting port number (1--65535)
  --end-port     Ending port number (must be ≥ start-port)

### Optional Arguments

  Argument       Description                                       Default
  -------------- ------------------------------------------------- ------------------
  -o, --output   Output filename                                   scanResults.txt
  --timeout      Seconds to wait before a port attempt times out   1.0
  --retries      Retry attempts if a port times out                1

## Example usage

### Example 1 - Basic Scan

    py PortScanCLI.py -t www.google.com --start-port 80 --end-port 100

### Example 2 - Custom Output File & Timeouts

    py PortScanCLI.py -t 192.168.1.20 --start-port 1 --end-port 200 --timeout 0.5 --retries 2 --output "outputFileName.txt"

## Output File

Example:

    Simple Port Scanner Results
    =================================
    Scan time : 2025-12-03 14:00:00
    Target    : www.google.com
    Resolved  : 142.251.46.164
    Port range: 80-443
    =================================

    Port 80: open
    Port 81: closed
    Port 82: closed
    Port 83: unknown


## Error Handling

The program handles:

-   Invalid port numbers\
-   Invalid port range order\
-   Hostname resolution failure\
-   Socket connection errors\
-   Keyboard interruption by users (i.e Ctrl+C)\
-   File write errors

