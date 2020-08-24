import subprocess
import re
import optparse
import random


def get_arguments():
	parser = optparse.OptionParser()
	parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
	parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address")
	parser.add_option("-r", "--random", action="store_true", dest="rand_mac", help="Random MAC Address")
	(options, arguments) = parser.parse_args()
	if not options.interface:
		parser.error("[-] Please specify an interface, use --help for more info.")
	elif str(options.new_mac) == "None" and str(options.rand_mac) == "None":
	 	parser.error("[-] Please specify a new MAC or choose -r for random MAC, use --help for more info.")
	return options

def random_mac(interface):
	create_random_mac = "02:00:00:%02x:%02x:%02x" % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", create_random_mac])
	subprocess.call(["ifconfig", interface, "up"])
	global RANDOM_MAC
	RANDOM_MAC = create_random_mac

def change_mac(interface, new_mac):
	print("[+] Changing MAC address for " + interface + " to " + new_mac)
	subprocess.call(["ifconfig", interface, "down"])
	subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
	subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
	ifconfig_result = subprocess.check_output(["ifconfig", interface])
	mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

	if mac_address_search_result:
		return mac_address_search_result.group(0)
	else:
		print("[-] Could not read MAC address")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))
backup_cmd = "echo '" + current_mac + "' > backup_mac.txt"
subprocess.check_output(backup_cmd, shell=True)


if options.rand_mac == True:
	# Call random_mac function.
	random_mac(options.interface)
	# Get the new MAC address in use and print the message.
	current_mac = get_current_mac(options.interface)
	print(current_mac)
	if current_mac == RANDOM_MAC:
		print("[+] MAC address changed successfully to " + current_mac)
	else:
		print("[-] Could not change MAC address")
elif str(options.new_mac) != "None": 
	# Execute the change_mac function.
	change_mac(options.interface, options.new_mac)
	# Get the new MAC address in use and print the message.
	current_mac = get_current_mac(options.interface)
	print(current_mac)
	if current_mac == options.new_mac:
		print("[+] MAC address changed successfully to " + current_mac)
	else:
		print("[-] Could not change MAC address")
else:
	# IF something goes wrong.
	print("Error changing MAC")