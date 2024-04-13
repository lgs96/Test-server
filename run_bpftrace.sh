#!/bin/bash

# Check if save directory and port number arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <save_directory> <port_number>"
    exit 1
fi

SAVE_DIR="result/$1"
PORT_NUMBER="$2"

echo "Directory to save files: $SAVE_DIR"
echo "Monitoring TCP traffic on port: $PORT_NUMBER"

mkdir -p "$SAVE_DIR"
if [ ! -d "$SAVE_DIR" ]; then
    echo "Failed to create directory: $SAVE_DIR"
    exit 1
fi

# Embed the port number directly into the script
sudo bpftrace -e "
tracepoint:tcp:tcp_probe {
    \$sport = args->sport;
    \$dport = args->dport;
    \$hsport = ((\$sport & 0xff00) >> 8) | ((\$sport & 0x00ff) << 8);
    \$hdport = ((\$dport & 0xff00) >> 8) | ((\$dport & 0x00ff) << 8);
    if (\$sport == $PORT_NUMBER || \$dport == $PORT_NUMBER) {
        printf(\"%d,%u,%u\n\", nsecs, args->snd_cwnd*1460, args->srtt);
    }
}" > "$SAVE_DIR/cwnd.csv" &
CWND_PID=$!

sudo bpftrace -e "
tracepoint:tcp:tcp_retransmit_skb {
    \$sport = args->sport;
    \$dport = args->dport;
    \$hsport = ((\$sport & 0xff00) >> 8) | ((\$sport & 0x00ff) << 8);
    \$hdport = ((\$dport & 0xff00) >> 8) | ((\$dport & 0x00ff) << 8);
    if (\$sport == $PORT_NUMBER || \$dport == $PORT_NUMBER) {
        printf(\"%d\n\", nsecs);
    }
}" > "$SAVE_DIR/retx.csv" &
RETX_PID=$!

wait $CWND_PID
wait $RETX_PID