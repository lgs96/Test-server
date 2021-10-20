import os
import time
import sys
import subprocess

def cmd_run(cmd):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

def delete_cmd (interface):
    exeStr = ""
    exeStr = exeStr + "tc qdisc del dev "+interface+" root \n"
    print(exeStr)
    cmd_run(exeStr)
    
if __name__ == "__main__":
    delete_cmd('enp4s0')