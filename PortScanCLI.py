###
# Port Scanner CLI TOOL - Anthony Palinkas 000820541
#
# Imported modules:
# - argparse: for command line arguments
# - socket: for TCP connections to ports
# - sys: for error codes
# - time: for delays between retries
# - datetime: for timestamps in the output file
###

import argparse
import socket
import sys
import time
from datetime import datetime


def parseArguments():
    parser = argparse.ArgumentParser(
        description="Simple TCP port scanner. "
                    "Given a target and port range, scan and output open/closed ports."
    )

    #target: -t or --target
    parser.add_argument(
        "-t",
        "--target",
        dest="target",
        required=True,
        help="Target IP address or domain name (i.e, 192.168.1.10 or domainName.com)"
    )

    #startPort: --start-port
    parser.add_argument(
        "--start-port",
        dest="startPort",
        type=int,
        required=True,
        help="Starting port number (1-65535)"
    )

    #endPort: --end-port
    parser.add_argument(
        "--end-port",
        dest="endPort",
        type=int,
        required=True,
        help="Ending port number (1-65535)"
    )

    #output: -o or --output
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        default="scanResults.txt",
        help="Output file to save results"
    )

    #timeout: --timeout
    parser.add_argument(
        "--timeout",
        dest="timeout",
        type=float,
        default=1.0,
        help="Timeout in seconds for each connection attempt"
    )

    #retries: --retries, stored as args.retries
    parser.add_argument(
        "--retries",
        dest="retries",
        type=int,
        default=1,
        help="Number of retries per port if connection times out"
    )

    args = parser.parse_args()
    return args


def validatePorts(startPort, endPort):
    if startPort < 1 or startPort > 65535:
        raise ValueError("start port must be between 1 and 65535")

    if endPort < 1 or endPort > 65535:
        raise ValueError("end port must be between 1 and 65535")

    if endPort < startPort:
        raise ValueError("end port must be greater than or equal to start port")


def resolveTarget(target):
    ipAddress = socket.gethostbyname(target)
    return ipAddress


def scanPort(ipAddress, port, timeout, retries):
    attempt = 0

    while attempt <= retries:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        try:
            result = sock.connect_ex((ipAddress, port))
            if result == 0:
                sock.close()
                return "open"
            else:
                sock.close()
                return "closed"

        except socket.timeout:
            #If timed out we can retry
            attempt = attempt + 1
            sock.close()

            if attempt > retries:
                return "unknown"

            #Delay before retrying
            time.sleep(0.1)
    return "unknown"


def writeResultsToFile(fileName, target, ipAddress, startPort, endPort, results):
    try:
        with open(fileName, "w") as fileHandle:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            fileHandle.write("Port Scanner Results\n")
            fileHandle.write("=================================\n")
            fileHandle.write("Scan time : " + timestamp + "\n")
            fileHandle.write("Target    : " + target + "\n")
            fileHandle.write("IP Address  : " + ipAddress + "\n")
            fileHandle.write("Port range: " + str(startPort) + "-" + str(endPort) + "\n")
            fileHandle.write("=================================\n\n")

            for port, status in results:
                line = "Port " + str(port) + ": " + status + "\n"
                fileHandle.write(line)

    except IOError as error:
        print("Error writing to file:", error)
        print("Results will only be shown in CLI.")


def main():
    try:
        args = parseArguments()

        #Validate ports
        try:
            validatePorts(args.startPort, args.endPort)
        except ValueError as valueError:
            print("Port validation error:", valueError)
            sys.exit(1)

        #Resolve target
        try:
            targetIp = resolveTarget(args.target)
        except socket.gaierror as resolveError:
            print("Error: could not resolve target:", args.target)
            print("Details:", resolveError)
            sys.exit(1)

        print("Starting scan on target:", args.target, "(", targetIp, ")")
        print("Port range:", args.startPort, "-", args.endPort)
        print("Timeout per attempt:", args.timeout, "seconds")
        print("Retries per port:", args.retries)
        print("---------------------------------")

        results = []

        #Scan port by port
        try:
            for port in range(args.startPort, args.endPort + 1):
                status = scanPort(targetIp, port, args.timeout, args.retries)
                results.append((port, status))
                print("Port", port, "->", status)

        except KeyboardInterrupt:
            print("\nScan interrupted by user.")
            if len(results) > 0:
                writeResultsToFile(
                    args.output,
                    args.target,
                    targetIp,
                    args.startPort,
                    args.endPort,
                    results
                )
            sys.exit(1)

        #Save results to file
        writeResultsToFile(
            args.output,
            args.target,
            targetIp,
            args.startPort,
            args.endPort,
            results
        )

        print("---------------------------------")
        print("Scan complete. Results saved to:", args.output)

    except Exception as unexpectedError:
        #Catch any unexpected errors
        print("An unexpected error occurred:", unexpectedError)
        sys.exit(1)


if __name__ == "__main__":
    main()
