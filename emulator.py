import os
import time
import sys
import subprocess

def cmd_run(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

def run_emulation(interface, bandwidth, delay, packetLoss, first=False):
    exeStr1 = ""
    if not first:
        exeStr1 = exeStr1 + 'tc class change dev ' + interface + ' parent 1: classid 1:12 htb rate ' + str(bandwidth) + 'kbps\n'
    else:
        exeStr1 = exeStr1 + "tc qdisc del dev "+interface+" root \n"        
        if int(bandwidth)>0:
            exeStr1 = exeStr1 + "tc qdisc add dev "+interface+" root handle 1: htb default 12 \n"
            exeStr1 = exeStr1 + "tc class add dev "+interface+" parent 1: classid 1:12 htb rate " + str(bandwidth) + "kbps \n"
        if int(delay)>0 or int(packetLoss)>0:
            exeStr1 = exeStr1 + "tc qdisc add dev "+interface+" parent 1:12 netem "
            if int(delay)>0:
                exeStr1 = exeStr1 + "delay " + str(delay) + "ms "
                exeStr1 = exeStr1 + "\n"
        cmd_run( exeStr1)
        print(exeStr1)
        exeStr2 = ""
        exeStr2 =  exeStr2 + "tc filter add dev " + interface + " protocol ip parent 1:0 prio 1 u32 match ip dst " + "223.38.35.163" + "/32 flowid 1:12 \n"
        #exeStr2 = exeStr2 + "tc filter add dev " + interface + " protocol ip parent 1:0 prio 1 u32 match ip src 223.38.35.16\32 flowid 1:12 \n"
        cmd_run( exeStr2)
        print(exeStr2)


def repeat(interface, repeat_cnt=10):
    sleep_time = 5
    for i in range(repeat_cnt):
        if i % 2 == 0:
            run_emulation(interface, 10000, 25, 0, i == 0)
            time.sleep(sleep_time)
        else:
            run_emulation(interface, 1000, 25, 0, i == 0)
            time.sleep(sleep_time)
            
    exeStr1 = ""
    exeStr1 = exeStr1 + "tc qdisc del dev "+interface+" root \n"
    print(exeStr1)
    cmd_run( exeStr1 )    
    

def delete_cmd (interface):
    exeStr = ""
    exeStr = exeStr + "tc qdisc del dev "+interface+" root \n"
    print(exeStr)
    cmd_run(exeStr)

if __name__ == "__main__":
    #repeat('eno2', repeat_cnt=50)
    if len(sys.argv)==1:
        run_emulation(interface = 'enp4s0', bandwidth = 100000, delay = 60, packetLoss = 0, first = True)
    else:
        run_emulation(interface = sys.argv[1], bandwidth = sys.argv[2], delay = sys.argv[3], packetLoss = 0, first = True)
# exeStr1 = ""
# exeStr1 = exeStr1 + "tc qdisc del dev enp3s0 root \n"
# print(exeStr1)
# cmd_run( exeStr1 )    
