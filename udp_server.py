import os
import sys
import socket
import threading
from io import BytesIO
import time

def start_tcpdump(sname, iname, hname, port):
    cmd = 'tcpdump -ttt -w data/trace_%s.pcap -i %s dst %s and dst port %d &' % (sname, iname, hname, port)
    # cmd = str(cmd)
    # print(cmd)
    # cmd = 'tcpdump -ttt -w data/trace_%s.pcap &' % ('hello')
    sudoPassword = 'glaakstp'
    print('echo %s|sudo -S %s' % (sudoPassword, cmd))
    p = os.system('sudo -S %s' % (cmd))

def stop_tcpdump():
    os.system("kill -9 `ps -aux | grep tcpdump | awk '{print $2}'`")
    
def process_uplink(c, addr, tx_start):
    recv_size = 0
    start = time.time()
    print('Start processing uplink')
    while True:
        data = c.recv(8192)
        #print('uplink data: ', ('done' in str(data[0:4])))
        recv_size = recv_size + len(data)
        print('process_uplink %d' % (recv_size), end="\r")
        #print('data: ',data)
        if ('done' in str(data)):
            print("\nObject uploaded")
            break
        #if not data:
        #    break
    end = time.time()
    print('Total received size', recv_size/(1024*1024), 'Mbytes ', ' Time: ', (end-start), 'sec Throughput: ', (recv_size*8)/((end-start)*1e6), 'Mbps')
    print('Disconnected', addr)
    print('Upload time: ', round(end*1000) - tx_start)
    #c.close()
    #stop_tcpdump()

def process_downlink(c, addr):
    send_size = 0    
    start = time.time()
    while True:
        try:
            c.send(bytes(4096))
            send_size = send_size + 4096
            print('process_uplink %d' % (send_size), end="\r")
        except:
            break
    end = time.time()
    c.close()
    print('Total send size: ', send_size, 'bytes')
    print('Disconnected', addr)
    stop_tcpdump()    
    
if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Input parameter is not avlid')
        print('example) python3 server.py <interface:wlan0>')
        exit()
    else:
        iname = sys.argv[1]
        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 8888
    s.bind(('', port))
    
    print('Start Server with port %d' % (port))
    while True:
        data, addr = s.recvfrom(30);
        #print('data',data[0])
        if 'up' in str(data):
          sname = data[2:30].decode("ascii").strip().strip('\x00')
          print(data, sname)
          print('Uplink')
          process_uplink(s, addr, (int)(sname))
      
