import sys
from scapy.all import sr1, IP, ICMP
from colorama import Fore, init
import random
import time
 
 
# Initialize colorama for colored console output
init()
 
 
# Function to craft and send an ICMP Echo Request packet with retries
def craft_and_send_packet(dst_ip, retry_count=3, timeout=5):
   for i in range(retry_count):
       print(f"{Fore.BLUE}[DEBUG] Sending ICMP Echo Request to: {dst_ip}")
       start_time = time.time()
       response = sr1(IP(dst=dst_ip) / ICMP(), timeout=timeout, verbose=False)
       end_time = time.time()
       if response:
           print(f"{Fore.BLUE}[DEBUG] Received response from {response.src}: {response.summary()}")
           return response, end_time - start_time
       else:
           print(f"{Fore.RED}[DEBUG] No response received, retrying ({i + 1}/{retry_count})...")
           time.sleep(1)  # Wait for a short time before retrying
   return None, timeout
 
 
# Function to analyze the response
def analyze_response(response, response_time):
   if response:
       print(f"{Fore.GREEN}[+] Response received from {response.src}: {response.summary()}")
       print(f"    Response time: {response_time:.5f} seconds")
       # Additional analysis can be added here
   else:
       print(f"{Fore.RED}[-] No response received")
 
 
# Function to display an error message
def display_error(message):
   print(f"{Fore.RED}[-] Error: {message}")
 
 
# Main function
def main():
   if len(sys.argv) != 2:
       display_error("Invalid number of arguments. Please run as: python script.py <destination_ip>")
       sys.exit(1)
 
 
   destination_ip = sys.argv[1]
 
 
   print(f"{Fore.YELLOW}[+] Sending ICMP Echo Requests to: {destination_ip}\n")
 
 
   response, response_time = craft_and_send_packet(destination_ip)
   analyze_response(response, response_time)
 
 
if __name__ == "__main__":
   main()
