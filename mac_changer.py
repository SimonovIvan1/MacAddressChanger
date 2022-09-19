#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-n", "--network", dest="network", help="change network")
    parser.add_option("-m", "--mac", dest="new_mac", help="change mack address")
    (options, arguments) = parser.parse_args()
    if not options.network:
        parser.error("[-] Please, enter network, for more information use --help")
    elif not options.new_mac:
        parser.error("[-] Please, enter mac address, for more information use --help")
    return options


def change_mac(network, new_mac):
    print("[+] Changing mac address for " + network + " on " + new_mac)
    subprocess.call(["ifconfig", network, "down"])
    subprocess.call(["ifconfig", network, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", network, "up"])


def get_current_mac(network):
    ifconfig_result = subprocess.check_output(["ifconfig", network])
    mac_address_search_result = re.search(rb"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read mac address")


options = get_arguments()
current_mac = get_current_mac(options.network)
print("Current mac: " + str(current_mac))
change_mac(options.network, options.new_mac)

current_mac = get_current_mac(options.network)
if current_mac == str.encode(options.new_mac):
    print("[+] Mac address is changed to " + str(current_mac))

else:
    print("[-] Mac address is not changed")