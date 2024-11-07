#!/usr/bin/env python3
"""
MAC Address Changer - A tool to modify network interface MAC addresses.
Python 3 compatible version with enhanced user interface.

Usage:
    python3 app.py -i <interface> -m <new_mac>
    python3 app.py --interface <interface> --mac <new_mac>

Example:
    python3 app.py -i eth0 -m 00:11:22:33:44:55
"""

import subprocess
import optparse
import re
from typing import Tuple, Optional
import sys

def display_banner() -> None:
    """Display the application's ASCII art banner."""
    banner = """

 ███▄ ▄███▓ ▄▄▄       ▄████▄      ▄████▄   ██░ ██  ▄▄▄       ███▄    █   ▄████ ▓█████  ██▀███  
▓██▒▀█▀ ██▒▒████▄    ▒██▀ ▀█     ▒██▀ ▀█  ▓██░ ██▒▒████▄     ██ ▀█   █  ██▒ ▀█▒▓█   ▀ ▓██ ▒ ██▒
▓██    ▓██░▒██  ▀█▄  ▒▓█    ▄    ▒▓█    ▄ ▒██▀▀██░▒██  ▀█▄  ▓██  ▀█ ██▒▒██░▄▄▄░▒███   ▓██ ░▄█ ▒
▒██    ▒██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒   ▒▓▓▄ ▄██▒░▓█ ░██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒░▓█  ██▓▒▓█  ▄ ▒██▀▀█▄  
▒██▒   ░██▒ ▓█   ▓██▒▒ ▓███▀ ░   ▒ ▓███▀ ░░▓█▒░██▓ ▓█   ▓██▒▒██░   ▓██░░▒▓███▀▒░▒████▒░██▓ ▒██▒
░ ▒░   ░  ░ ▒▒   ▓▒█░░ ░▒ ▒  ░   ░ ░▒ ▒  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒  ░▒   ▒ ░░ ▒░ ░░ ▒▓ ░▒▓░
░  ░      ░  ▒   ▒▒ ░  ░  ▒        ░  ▒    ▒ ░▒░ ░  ▒   ▒▒ ░░ ░░   ░ ▒░  ░   ░  ░ ░  ░  ░▒ ░ ▒░
░      ░     ░   ▒   ░           ░         ░  ░░ ░  ░   ▒      ░   ░ ░ ░ ░   ░    ░     ░░   ░ 
       ░         ░  ░░ ░         ░ ░       ░  ░  ░      ░  ░         ░       ░    ░  ░   ░     
                     ░           ░                                                             

                                                        [Version 1.0][Pejman Ebrahimi]
    """
    print(banner)
    print("[*] Python 3 MAC Address Changer Tool")
    print("[*] Use --help for more information\n")

def parse_command_line_args() -> Tuple[str, str]:
    """
    Parse command line arguments for interface and MAC address.
    
    Returns:
        Tuple[str, str]: A tuple containing (interface_name, new_mac_address)
        
    Raises:
        SystemExit: If required arguments are missing or invalid
    """
    parser = optparse.OptionParser(usage="usage: %prog -i interface -m new_mac")
    parser.add_option("-i", "--interface", dest="interface", 
                      help="Network interface to modify (e.g., eth0, wlan0)")
    parser.add_option("-m", "--mac", dest="new_mac", 
                      help="New MAC address (format: xx:xx:xx:xx:xx:xx)")
    
    options, _ = parser.parse_args()
    
    if not options.interface:
        parser.error("[-] Interface is required. Use --help for more information.")
    if not options.new_mac:
        parser.error("[-] New MAC address is required. Use --help for more information.")
        
    return options.interface, options.new_mac

def validate_mac_address(mac_address: str) -> bool:
    """
    Validate MAC address format.
    
    Args:
        mac_address: MAC address string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    mac_pattern = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")
    return bool(mac_pattern.match(mac_address))

def change_mac_address(interface: str, new_mac: str) -> bool:
    """
    Change MAC address of specified network interface.
    
    Args:
        interface: Network interface name
        new_mac: New MAC address
        
    Returns:
        bool: True if successful, False otherwise
        
    Raises:
        subprocess.CalledProcessError: If system commands fail
    """
    try:
        subprocess.check_call(["ifconfig", interface, "down"])
        subprocess.check_call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.check_call(["ifconfig", interface, "up"])
        return True
    except subprocess.CalledProcessError:
        return False

def get_current_mac(interface: str) -> Optional[str]:
    """
    Get current MAC address of specified interface.
    
    Args:
        interface: Network interface name
        
    Returns:
        Optional[str]: Current MAC address or None if not found
        
    Raises:
        subprocess.CalledProcessError: If ifconfig command fails
    """
    try:
        ifconfig_output = subprocess.check_output(["ifconfig", interface], 
                                                stderr=subprocess.STDOUT).decode()
        mac_address_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)
        return mac_address_search.group(0) if mac_address_search else None
    except subprocess.CalledProcessError:
        return None

def main() -> None:
    """Main execution function."""
    try:
        display_banner()
        
        interface, new_mac = parse_command_line_args()
        
        if not validate_mac_address(new_mac):
            sys.exit("[-] Invalid MAC address format. Use format: xx:xx:xx:xx:xx:xx")
            
        current_mac = get_current_mac(interface)
        if not current_mac:
            sys.exit(f"[-] Could not find MAC address for interface {interface}")
            
        print(f"[+] Current MAC address: {current_mac}")
        
        if not change_mac_address(interface, new_mac):
            sys.exit("[-] Failed to change MAC address")
            
        new_current_mac = get_current_mac(interface)
        if new_current_mac == new_mac:
            print(f"[+] MAC address successfully changed to {new_current_mac}")
        else:
            print("[-] MAC address change verification failed")
            
    except KeyboardInterrupt:
        print("\n[-] Program terminated by user")
    except Exception as e:
        print(f"[-] An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()