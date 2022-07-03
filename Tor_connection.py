from datetime import datetime
import stem
import stem.connection

# Connect to tor
with stem.control.Controller.from_port(port=9051) as controller:
    controller.authenticate()
    print("Tor connection established")
    
    #get a list of all the relays
    relays = controller.get_network_statuses()

    #get the number of relays
    relays1 = list(relays)
    num_relays = len(relays1)

    #get the number of relays that are running
    num_running_relays = 0
    for relay in relays:
        if relay.flags.is_set('Running'):
            num_running_relays += 1

    #get the total bandwidth of all the running relays
    total_bandwidth = 0
    for relay in relays:
        if relay.flags.is_set('Running'):
            total_bandwidth += relay.bandwidth

    #format the relay by ip address, nickname, flags, and bandwidth and save it to a json file with the file name format of "tor_relay_MM_DD_YY_hh_mm.json"
    with open("tor_relay_" + datetime.now().strftime("%m_%d_%y_%H_%M") + ".json", "w") as f:
        f.write("{")
        f.write("\"num_relays\": " + str(num_relays) + ",")
        f.write("\"num_running_relays\": " + str(num_running_relays) + ",")
        f.write("\"total_bandwidth\": " + str(total_bandwidth) + ",")
        f.write("\"relays\": [")
        for relay in relays:
            f.write("{")
            f.write("\"ip\": \"" + relay.address + "\",")
            f.write("\"nickname\": \"" + relay.nickname + "\",")
            f.write("\"flags\": \"" + relay.flags.summary() + "\",")
            f.write("\"bandwidth\": " + str(relay.bandwidth))
            if relay != relays[-1]:
                f.write("},")
            else:
                f.write("}")
        f.write("]}")
        f.close()
    print("Saved to tor_relay_" + datetime.now().strftime("%m_%d_%y_%H_%M") + ".json")
    print("Number of relays: " + str(num_relays))
    print("Number of running relays: " + str(num_running_relays))
    print("Total bandwidth: " + str(total_bandwidth))
    print("\n")
