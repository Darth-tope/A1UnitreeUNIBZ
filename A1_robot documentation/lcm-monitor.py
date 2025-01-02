#!/usr/bin/env python3
import lcm
import time
import select
from datetime import datetime
import struct

def decode_high_cmd(data):
    try:
        print(f"Raw data length: {len(data)}")
        print(f"Raw hex: {data.hex()}")
        
        # First 5 fields: mode, forwardSpeed, sideSpeed, rotateSpeed, yaw
        fmt = 'fffff'  # 5 floats
        size = struct.calcsize(fmt)
        values = struct.unpack(fmt, data[:size])
        
        print("HighCmd decoded values:")
        print(f"  Mode: {values[0]}")
        print(f"  Forward Speed: {values[1]}")
        print(f"  Side Speed: {values[2]}")
        print(f"  Rotate Speed: {values[3]}")
        print(f"  Yaw: {values[4]}")
        
    except Exception as e:
        print(f"Decode error: {str(e)}")

def my_handler(channel, data):
    timestamp = datetime.now().strftime('%H:%M:%S.%f')
    print(f"\n[{timestamp}] Channel: {channel}")
    print(f"Message length: {len(data)} bytes")

    if channel == "LCM_High_Cmd":
        decode_high_cmd(data)
        
    # Print non-zero bytes
    non_zero = []
    for i in range(len(data)):
        if data[i] != 0:
            non_zero.append(f"byte {i}: 0x{data[i]:02x}")
    if non_zero:
        print("Non-zero bytes:", ", ".join(non_zero))

def main():
    lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=255")
    lc.subscribe(".*", my_handler)
    
    print("Monitoring LCM messages...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            rfds, wfds, efds = select.select([lc.fileno()], [], [], 0.1)
            if rfds:
                lc.handle()
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == '__main__':
    main()
