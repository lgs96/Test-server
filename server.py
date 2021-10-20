import os
import sys
import socket
import threading
from io import BytesIO
import time

start_tx = 0

def start_tcpdump(sname, iname, hname, port):
    cmd = 'tcpdump -ttt -w data/trace_%s.pcap -i %s dst %s and dst port %d &' % (sname, iname, hname, port)
    # cmd = str(cmd)
    # print(cmd)
    # cmd = 'tcpdump -ttt -w data/trace_%s.pcap &' % ('hello')
    sudoPassword = 'glaakstp'
    #print('echo %s|sudo -S %s' % (sudoPassword, cmd))
    #p = os.system('sudo -S %s' % (cmd))

def stop_tcpdump():
    os.system("kill -9 `ps -aux | grep tcpdump | awk '{print $2}'`")
    
def process_uplink(c, addr, tx_start):
    recv_size = 0
    start = time.time()
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
    print('Total received size', recv_size/(1024*1024), 'Mbytes ', ' Fisrt to last time: ', (end-start), 'sec Throughput: ', (recv_size*8)/((end-start)*1e6), 'Mbps')
    print('Disconnected', addr)
    print('Upload time: ', round(end*1000) - tx_start)
    c.close()
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

    if len(sys.argv) != 3:
        print('Input parameter is not avlid')
        print('example) python3 server.py <interface:wlan0>')
        exit()
    else:
        iname = sys.argv[1]
        pname = sys.argv[2]
        
    s = socket.socket()
    port = (int)(pname)
    s.bind(('', port))
    s.listen(10)
    print('Start Server with port %d' % (port))
    while True:
        c, addr = s.accept()
        print('Connected by', addr)
        data = c.recv(5000)
        print('data', data[0])
        
        sname = data[1:30].decode("ascii").strip().strip('\x00')
        print('name ', sname, ' iname ', iname, ' addr0 ', addr[0], ' addr1 ', addr[1])
        start_tcpdump(sname, iname, addr[0], addr[1])
        
        if 'u' in str(data):
           print('Uplink')
           t = threading.Thread(target=process_uplink, args=(c, addr, (int)(sname)))
           t.start()
        elif 'd' in str(data[0:1]):
           print('Downlink')
           t = threading.Thread(target=process_downlink, args=(c, addr))

t.start()
