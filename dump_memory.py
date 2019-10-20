#!/usr/bin/env python3
''' 
    Dumps Seagate Flash Memory.

    HDD must be connected to the computer via serial,
    configuration of the port variable may be necessary.

    The process is slow (around 2 seconds per 512 byte sector)

    Tested on Seagate ST3160318AS only.

    Use at your own risk... it is easy to brick a HDD, trust me ;)

'''

import sys
import serial
import re

port = '/dev/ttyUSB0'
baudrate = 38400
timeout = 1

def send_command(cmd):
    cmd += '\r'
    ser.write(cmd.encode())

with serial.Serial(port, baudrate, timeout=timeout) as ser:
    try:
        start = sys.argv[1]
        end = sys.argv[2]
        if int(end, 16) < int(start, 16):
            raise Exception
    except Exception as e:
        print('''
            Usage: dump_memory.py [start_address] [end_address]

            Adresses in hexadecimal (format: deadbeef)''')
        sys.exit(1)

    filename = f'{start}_{end}.dump'

    end_value = int(end, 16)
    high_start = start[:4]
    low_start = start[4:]

    send_command('/1') # Go to the right level
    with open(filename,'a') as f:
        while True:
            send_command(f'D{high_start},{low_start}')
            for line in ser.readlines():
                if re.match('[0-9A-F]{8}', line.decode('ascii')[:8]) != None:
                    print(line.decode('ascii'), end='')
                    f.write(line.decode('ascii'))
                else:
                    #print(f'No match > {line.decode("ascii")[:8]}')
                    pass
            start_value = int(start, 16) + 512
            if start_value > end_value:
                sys.exit(0)
            start = f'{start_value:08x}'
            high_start = start[:4]
            low_start = start[4:]
