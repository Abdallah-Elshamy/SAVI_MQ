# SAVI MQ Web

A web app that exposes the functionality of [SAVI MQ Engine](../README.md).

# Used technologies
* [`openstacksdk`](https://docs.openstack.org/openstacksdk/latest/): Used to launch and manage message queues.
* [`Paramiko`](https://www.paramiko.org/): Used to establish an ssh session with the message queues to finalize the configuration.
* [`Django`](https://www.djangoproject.com/): Used to build the web application.

# How to install the app
1. `cd` to `SAVI_MQ/SAVI_MQ_web`
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

# How to run the app
1. `cd` to `SAVI_MQ/SAVI_MQ_web`
2. Activate the venv by running: 
```
source env/bin/activate
```
3. Start the Django web app by running:
```
python3 manage.py runserver
```
You can access the dashboard via: `http://127.0.0.1:8000/mqs/`
