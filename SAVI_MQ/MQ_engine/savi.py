import time
import paramiko
import logging
import openstack


# Set logging format and logging level
# Can change INFO to DEBUG for more information, or WARNING for less information
logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__) # Get logger for *this* module
logger.setLevel(logging.INFO)


# Sets up an SSH session with a target host
#
# Input:
#   - targetIP: The target host's IP address
#   - username: The username to log-in with
#   - password: The password associated with the username
#
# Returns:
#   - A Paramiko SSH session object
def getSSHSession(targetIP, username, password):
    # Set up SSH
    sshSession = paramiko.SSHClient()
    sshSession.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    while True:
        try:
            sshSession.connect(targetIP, username = username, password = password)
            logger.debug("SSH to %s successful" % targetIP)
            break
        except Exception as e:
            logger.debug("Waiting for SSH daemon to come up in %s..." % targetIP)
            time.sleep(5)

    return sshSession


# Runs a command that requires sudo access over an established SSH session
#
# Input:
#   - sshSession: An active SSH session to a VM
#   - command: A string command to run within the VM
#   - sudoPassword: Password for sudo access
#
# Returns:
#   - strings of stdout or else None if an exception occurred from SSH
def runSudoCommandOverSSH(sshSession, command, sudoPassword):
    assert type(sshSession) is paramiko.client.SSHClient,\
            "'sshSession' is type %s" % type(sshSession)
    assert type(command) is str, "'command' is type %s" % type(command)
    
    logger.debug("Running command in host %s" % sshSession._transport.sock.getpeername()[0])
    logger.debug("\t\"%s\"" % command)

    try:
        transport = sshSession.get_transport()
        session = transport.open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        session.exec_command(command)
        stdin = session.makefile('w', -1)
        stdout = session.makefile('r', -1)
        # Enter the password for sudo
        stdin.write(sudoPassword + '\n')
        stdin.flush()

        # Wait for command to finish (may take a while for long commands)
        while not stdout.channel.exit_status_ready():
            time.sleep(1)
    except Exception as e:
        logger.error(e)
        logger.error("ERROR: Unable to execute command over SSH:")
        logger.error("\t%s" % command)

        return None
    else:
        # Check if command printed anything to stdout
        out = stdout.readlines()
        out = ''.join(out) # Convert to single string
        if out:
            logger.debug("%s\n" % out)

        return out


def create_server(config):
    conn = openstack.connect(cloud='savi')
    print("Creating server %s" % config["name"])
    print(config)

    image = conn.compute.find_image(config["image"])
    flavor = conn.compute.find_flavor(config["flavor"])
    network = conn.network.find_network(config["network"])
    keypair = conn.compute.find_keypair(config["key"])

    server = conn.compute.create_server(
        name=config["name"], image_id=image.id, flavor_id=flavor.id,
        networks=[{"uuid": network.id}], key_name=keypair.name)

    server = conn.compute.wait_for_server(server)
    print("Server %s is active" % config["name"])

    return server


def list_mqs():
    conn = openstack.connect(cloud='savi')
    servers = []
    for server in conn.compute.servers():
        if(server.name.startswith("mq-")):
            addresses = []
            for network in server.addresses.values():
                for addresses_dict in network:
                    addresses.append(addresses_dict["addr"])
            image = conn.compute.find_image(server.image["id"]).name
            dashboards = []
            # Add port number to a broker's IP
            port = ""
            if image == "RabbitMQ":
                dashboards = ["http://" + s + ":15672/" for s in addresses]
                port = ":5672"
            elif image == "Mosquitto":
                port = ":1883"
            addresses = [s + port for s in addresses]
            servers.append({
                "id": server.id,
                "Name": server.name[3:],
                "Endpoint": "\n".join(addresses),
                "DashboardURL": "\n".join(dashboards),
                "Flavor": server.flavor["original_name"],
                "KeyPair": server.key_name,
                "Engine": image,
                "Status": server.status,
            })

    return servers


def launch_mq(config):
    server = create_server(config)
    server_ip = list(server.addresses.values())[0][0]["addr"]
    # ssh into the created server and configure the mq if the broker 
    # is rabbitmq
    if config["image"] == "RabbitMQ":
        sshSession = getSSHSession(server_ip, "mqadmin", "mqadmin")
    
        command = (f"sudo rabbitmqctl add_user -- {config['console_username']} {config['console_password']} &&"
                   f"sudo rabbitmqctl set_user_tags {config['console_username']} administrator &&"
                   f"sudo rabbitmqctl set_permissions -p / {config['console_username']} \".*\" \".*\" \".*\"")
    
        runSudoCommandOverSSH(sshSession, command, "mqadmin")


def delete_mq(id):
    conn = openstack.connect(cloud='savi')
    conn.compute.delete_server(id)


def get_mq_info(id):
    conn = openstack.connect(cloud='savi')
    server_dict = dict()
    server = conn.compute.find_server(id)
    for field in server:
        server_dict[field] = server[field]
    # Delete the fields that contain objects so it can
    # be serialized to JSON
    del server["image"]
    del server["location"]
    return server
