# Script to calculate average for each type of local IPC from
# grouped_results.txt

FILE = "../ThesisData/grouped_results.txt"

machines = []
fifos = []
pipes = []
tcp = []
udp = []
unix = []

with open(FILE, "r") as inFile:
    inFile.readline()
    for line in inFile:
        splitLine = line.split()
        i = 0
        while not splitLine[i].isnumeric():
            i += 1
        machines.append(int(splitLine[i]))
        fifos.append(int(splitLine[i + 1]))
        pipes.append(int(splitLine[i + 2]))
        tcp.append(int(splitLine[i + 3]))
        # i + 4 is total TCP
        udp.append(int(splitLine[i + 5]))
        # i + 6 is total UDP
        unix.append(int(splitLine[i + 7]))
        print(splitLine[i + 7])

print(f"MACHINES: min: {0} max: {1} avg: {2}", min(machines), max(machines), sum(machines) / len(machines))
print(f"FIFOS: min: {0} max: {1} avg: {2}", min(fifos), max(fifos), sum(fifos) / len(fifos))
print(f"PIPES: min: {0} max: {1} avg: {2}", min(pipes), max(pipes), sum(pipes) / len(pipes))
print(f"TCP: min: {0} max: {1} avg: {2}", min(tcp), max(tcp), sum(tcp) / len(tcp))
print(f"UDP: min: {0} max: {1} avg: {2}", min(udp), max(udp), sum(udp) / len(udp))
print(f"UNIX: min: {0} max: {1} avg: {2}", min(unix), max(unix), sum(unix) / len(unix))