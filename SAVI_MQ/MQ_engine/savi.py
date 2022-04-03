import time
import paramiko
import logging


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


# Runs a command over an established SSH session
#
# Input:
#   - sshSession: An active SSH session to a VM
#   - command: A string command to run within the VM
#
# Returns:
#   - A tuple containing strings of stdout and stderr (stdout, stderr), or
#     else None if an exception occurred from SSH
def runCommandOverSSH(sshSession, command):
    assert type(sshSession) is paramiko.client.SSHClient,\
            "'sshSession' is type %s" % type(sshSession)
    assert type(command) in (str, unicode), "'command' is type %s" % type(command)
    logger.debug("Running command in host %s" % sshSession._transport.sock.getpeername()[0])
    logger.debug("\t\"%s\"" % command)

    try:
        stdin, stdout, stderr = sshSession.exec_command(command)

        # Wait for command to finish (may take a while for long commands)
        while not stdout.channel.exit_status_ready() or \
                not stderr.channel.exit_status_ready():
            time.sleep(1)
    except Exception as e:
        logger.error(e)
        logger.error("ERROR: Unable to execute command over SSH:")
        logger.error("\t%s" % command)

        return None
    else:
        # exec_command() completed successfully
        # Check if command printed anything to stderr
        err = stderr.readlines()
        err = ''.join(err) # Convert to single string
        if err:
            logger.error("%s\n" % err)

        # Check if command printed anything to stdout
        out = stdout.readlines()
        out = ''.join(out) # Convert to single string
        if out:
            logger.debug("%s\n" % out)

        return (out, err)