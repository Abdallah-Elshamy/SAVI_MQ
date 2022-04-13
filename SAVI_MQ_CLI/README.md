# SAVI MQ CLI

A CLI tool that exposes the functionality of [SAVI MQ Engine](../README.md).

# Used technologies
* [`openstacksdk`](https://docs.openstack.org/openstacksdk/latest/): Used to launch and manage message queues.
* [`Paramiko`](https://www.paramiko.org/): Used to establish ssh sessions with the message queues to finalize the configuration.
* [`Typer`](https://typer.tiangolo.com/): Used to build the CLI application.

# How to install the tool
1. `cd` to `SAVI_MQ/SAVI_MQ_CLI`
2. Create a [virtual environment for python](https://docs.python.org/3/library/venv.html) by running: 
```
python3 -m venv env
```
3. Activate the venv by running: 
```
source env/bin/activate
```
4. Install the required packages by running: 
```
pip install -r requirements.txt
```

# How to configure OpenStack SDK to use your credentials
1. Create a file with the name `clouds.yaml`
2. Edit `clouds.yaml` to have the following format:
```
clouds:
  savi:
    region_name: <THE_DESIRED_REGION>
    auth:
      username: <YOUR_USERNAME>
      password: <YOUR_PASSWORD>
      project_name: <PROJECT_NAME>
      auth_url: 'http://iamv3.savitestbed.ca:5000/v2.0/'
```

# How to run the tool
1. `cd` to `SAVI_MQ/SAVI_MQ_CLI`
2. Activate the venv by running: 
```
source env/bin/activate
```
The CLI tool currently supports four commands:
* `python -m savimq launch <JSON_CONFIG_FILE>`: This command launches a message queue from a JSON configuration file. [This is an example for the configuration file](./config.json)
* `python -m savimq list`: This commands lists the existing message queues
* `python -m savimq info <MQ_NAME_OR_ID>`: This command lists detailed information about the message queue with the given name or ID
* `python -m savimq delete <MQ_ID>`: This command deletes the message queue with the given ID