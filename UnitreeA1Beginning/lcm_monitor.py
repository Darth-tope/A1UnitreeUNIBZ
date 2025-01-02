import lcm
import time
import select
from datetime import datetime
import struct
import sys

# Open a log file with timestamp
log_filename = f"lcm_death_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    full_message = f"[{timestamp}] {message}"
    try:
        with open(log_filename, 'a', buffering=1) as f:
            f.write(full_message + '\n')
            f.flush()
        print(full_message)
        sys.stdout.flush()
    except Exception as e:
        print(f"Logging error: {e}")

class LCMMonitor:
    def __init__(self):
        self.start_time = None
        self.msg_count = 0
        self.last_cmd = None
        self.death_detected = False

    def monitor_handler(self, channel, data):
        current_time = datetime.now()
        
        if self.start_time is None:
            self.start_time = current_time
            log_message("Starting message monitoring")

        elapsed = (current_time - self.start_time).total_seconds()
        self.msg_count += 1

        msg = f"Time: {elapsed:.3f}s - Channel: {channel}"
        msg += f"\nMessage #{self.msg_count}"
        msg += f"\nData length: {len(data)} bytes"

        # Look for changes in the data
        if channel == "LCM_High_Cmd":
            if self.last_cmd is None:
                self.last_cmd = data
                msg += "\nInitial command received"
            elif data != self.last_cmd:
                msg += "\nCommand changed!"
                # Compare differences
                for i in range(min(len(data), len(self.last_cmd))):
                    if data[i] != self.last_cmd[i]:
                        msg += f"\nByte {i} changed: {hex(self.last_cmd[i])} -> {hex(data[i])}"
                self.last_cmd = data

        # Monitor for potential death indicators
        if elapsed > 0.5:  # After first 0.5 seconds
            if self.msg_count == 0:
                msg += "\nWARNING: No messages received!"
            
            # Look for patterns that might indicate imminent failure
            try:
                # Try to decode some basic command structure
                if channel == "LCM_High_Cmd":
                    cmd_data = struct.unpack('fff', data[:12])  # Assuming first 3 floats are important
                    msg += f"\nCommand values: {cmd_data}"
            except Exception as e:
                msg += f"\nError decoding data: {e}"

        log_message(msg)

def main():
    log_message("=== Starting LCM Death Monitor ===")
    monitor = LCMMonitor()

    try:
        lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=255")
        
        # Subscribe to both specific and wildcard channels
        channels = ["LCM_High_Cmd", "LCM_High_State", ".*"]
        for channel in channels:
            lc.subscribe(channel, monitor.monitor_handler)
            log_message(f"Subscribed to channel: {channel}")

        log_message("Monitor running - waiting for messages...")
        
        start_time = time.time()
        while True:
            rfds, wfds, efds = select.select([lc.fileno()], [], [], 0.1)
            if rfds:
                lc.handle()
            
            # Log periodic status
            elapsed = time.time() - start_time
            if int(elapsed) % 1 == 0:  # Every second
                log_message(f"Monitor active for {elapsed:.1f}s - Messages received: {monitor.msg_count}")

    except KeyboardInterrupt:
        log_message("Monitor stopped by user")
    except Exception as e:
        log_message(f"Error: {str(e)}")
    finally:
        log_message("Monitor terminated")

if __name__ == '__main__':
    main()
