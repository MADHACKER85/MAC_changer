
import subprocess
import optparse
import re


def get_arguments():
	parser = optparse.OptionParser()

	parser.add_option("-i", "--interface", dest ="interface", help = "Change the MAC address of this interface")
	parser.add_option("-m", "--mac", dest ="new_mac", help = "Change the MAC to this address")
	(options, arguments) = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify an interface to use --help for more info.")
	elif not options.new_mac:
		parser.error("[-] Please specify a MAC to use --help for more info.")
	return options



def change_mac(interface, new_mac):
	print("[+] Changing MAC address for " +  interface + " to " + new_mac)

	subprocess.call(["sudo", "ifconfig", interface, "down"])
	subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface])
	ifconfig_result = str(ifconfig_result)
	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("\n" + "[-] Could not reach MAC address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("Current MAC = ", current_mac)

change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
	print("[+] MAC address was successfully changed to " + current_mac)
else:
	print("[-] MAC address did not get changed")