import random
import time
import os

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
UNDERLINE = '\033[4m'
HEADER = '\033[95m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_packet_array(total_packets, acked, failed, base, next_seq_num, window_size):
    status = ""
    for i in range(1, total_packets + 1):
        if base <= i < base + window_size:
            if i == base:
                status += f"{UNDERLINE}["
            if i in acked:
                status += f"{GREEN}{UNDERLINE}{i:2d}{RESET}{UNDERLINE} "
            elif i in failed:
                status += f"{RED}{UNDERLINE}{i:2d}{RESET}{UNDERLINE} "
            elif base <= i < next_seq_num:
                status += f"{YELLOW}{UNDERLINE}{i:2d}{RESET}{UNDERLINE} "
            else:
                status += f"{UNDERLINE}{i:2d} "
            if i == base + window_size - 1 or i == total_packets:
                status += f"]{RESET}"
        else:
            if i in acked:
                status += f"{GREEN}{i:2d}{RESET} "
            elif i in failed:
                status += f"{RED}{i:2d}{RESET} "
            elif base <= i < next_seq_num:
                status += f"{YELLOW}{i:2d}{RESET} "
            else:
                status += f"{i:2d} "
    print(status)

def print_packet_status(base, next_seq_num, window_size, total_packets, acked, failed):
    print(f"{HEADER}Current window: [{base} - {min(base + window_size - 1, total_packets)}]{RESET}")
    for i in range(base, min(base + window_size, total_packets + 1)):
        if i in acked:
            print(f"{GREEN}{i:2d}{RESET} Acknowledged")
        elif i in failed:
            print(f"{RED}{i:2d}{RESET} Failed")
        elif base <= i < next_seq_num:
            print(f"{YELLOW}{i:2d}{RESET} In transit")
        else:
            print(f"{i:2d} Not sent")

def go_back_n(total_packets, window_size, success_rate):
    base = 1
    next_seq_num = 1
    transmissions = 0
    acked = set()
    failed = set()

    while base <= total_packets:
        clear_screen()
        print_packet_array(total_packets, acked, failed, base, next_seq_num, window_size)
        print_packet_status(base, next_seq_num, window_size, total_packets, acked, failed)
        time.sleep(0.5)

        # Send packets within the window
        while next_seq_num < base + window_size and next_seq_num <= total_packets:
            print(f"\nSending packet {next_seq_num}")
            transmissions += 1
            next_seq_num += 1
            clear_screen()
            print_packet_array(total_packets, acked, failed, base, next_seq_num, window_size)
            print_packet_status(base, next_seq_num, window_size, total_packets, acked, failed)
            time.sleep(0.5)

        # Simulate packet transmission and acknowledgment with delay
        for i in range(base, next_seq_num):
            clear_screen()
            print_packet_array(total_packets, acked, failed, base, next_seq_num, window_size)
            print_packet_status(base, next_seq_num, window_size, total_packets, acked, failed)
            print(f"\nWaiting for ACK {i}...")
            time.sleep(0.5)

            if random.random() < success_rate:
                print(f"\nPacket {i} successfully received, ACK {i}")
                acked.add(i)
                failed.discard(i)
            else:
                print(f"\nPacket {i} lost or corrupted")
                failed.add(i)
                next_seq_num = base  # Reset next_seq_num for retransmission
                break

            clear_screen()
            print_packet_array(total_packets, acked, failed, base, next_seq_num, window_size)
            print_packet_status(base, next_seq_num, window_size, total_packets, acked, failed)
            time.sleep(0.5)

        # Slide the window to the next unacknowledged packet
        old_base = base
        while base in acked and base <= total_packets:
            base += 1

        if base > old_base:
            print("\nSliding window...")
            time.sleep(0.5)

    print(f"\nAll packets sent successfully.")
    print(f"Total transmissions: {transmissions}")
    print(f"Efficiency: {total_packets / transmissions:.2%}")

def get_user_input():
    while True:
        try:
            total_packets = int(input("Enter the total number of packets: "))
            if total_packets <= 0:
                raise ValueError("Number of packets must be positive")
            
            window_size = int(input("Enter the window size: "))
            if window_size <= 0:
                raise ValueError("Window size must be positive")
            
            success_rate_percent = float(input("Enter the success rate (0 to 100 percent): "))
            if not 0 <= success_rate_percent <= 100:
                raise ValueError("Success rate must be between 0 and 100 percent")
            success_rate = success_rate_percent / 100
            
            return total_packets, window_size, success_rate
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

def main():
    print("Starting Go-Back-N protocol demonstration")
    total_packets, window_size, success_rate = get_user_input()

    print(f"\nSimulation parameters:")
    print(f"Total packets: {total_packets}")
    print(f"Window size: {window_size}")
    print(f"Success rate: {success_rate:.0%}")
    print("\nStarting simulation ...")
    time.sleep(2)

    go_back_n(total_packets, window_size, success_rate)

if __name__ == "__main__":
    main()
