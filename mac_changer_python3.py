"""
Example of entering interface and new MAC address.
python mac_changer.py --interface eth0 --mac 00:11:22:33:44:55
1) Create repository and clone with html
2) Make sure you're in the right directory. Use "ls" and "cd" to help you.
3) CD into the downloaded clone and put the files into the directory.
4) Use "git status" to see untracked files.
"""

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    # ^^ That allows us to get arguments from the user and parse them
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address.")
    # ^^ This allows the user to enter a value for "-i or interface". (Choose Interface)
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address.")
    # ^^ This allows the user to enter a value for "-m or --mac". (MAC address)
    (options, arguments) = parser.parse_args()
    if not options.interface:
        # Checks if interface is set.
        parser.error("[-] Please specify an interface, use --help for more information")
    elif not options.new_mac:
        # Checks if new_mac is set.
        parser.error("[-] Please specify a new MAC, use --help for more information")
    return options


def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    # ^^ The script is now more secure and will stop manipulation of the variables


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # ^^ Captures the result of the interface.
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    # ^^ searches the ifconfig_result for the regex pattern.
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] Could not read MAC address.")


options = get_arguments()
# ^^ Gets the arguments that the user enters.
current_mac = get_current_mac(options.interface)
print("The current MAC = " + str(current_mac))

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
# ^^ Using the variable as above will change the previously stored data.
if current_mac == options.new_mac:
    print("[+] MAC address was successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")
