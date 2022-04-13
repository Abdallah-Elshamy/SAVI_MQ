# SAVI MQ

This project aims to provide [SAVI](https://www.savinetwork.ca/) with a Messaging Broker as a Service feature. This will facilitate the deployment of message brokers on [SAVI](https://www.savinetwork.ca/). The message broker will follow a standard API of an open-source broker engine ([RabbitMQ](https://www.rabbitmq.com/) and [Mosquitto](https://mosquitto.org/)) which makes it easy to port existing code to SAVI.

This project consists of three parts:
* [An engine](savi_mq_engine.py) that is responsible for provisioning and configuring message queues.
* [A web portal](SAVI_MQ_web/README.md) that exposes the functionality of the engine via a web portal.
* [A CLI tool](SAVI_MQ_CLI/README.md) that exposes the functionality of the engine via a cli tool.

## SAVI MQ Engine
As [SAVI](https://www.savinetwork.ca/) is built using [OpenStack](https://www.openstack.org/), the engine uses [openstacksdk](https://docs.openstack.org/openstacksdk/latest/) to create servers based on images that was created as a part of this project. The images created are `RabbitMQ` and `Mosquitto` which contain a configured instance of the desired message queue. After the images are created, the engine uses [Paramiko](https://www.paramiko.org/) to establish an ssh session with the created server and uses it to finalize the configuration.

Currently, the engine supports four operations:
* `launch_mq`: This operation consumes the desired configuration from the user and creates and configures the message queue. The configurations should be on the form of a Python dictionary that has the following keys:
    * `name`: The name of the server
    * `image`: The name of the image used to create the server (Supported images are `RabbitMQ` and `Mosquitto`)
    * `flavor`: The name of the flavor used to create the server
    * `network`: The name of the network that the server will be in
    * `key`: The name of the keypair that can access the server
    * `admin_username`: The username of the admin user of the broker and [RabbitMQ management plugin](https://www.rabbitmq.com/management.html)
    * `admin_password`: The password of the admin user of the broker and [RabbitMQ management plugin](https://www.rabbitmq.com/management.html)
* `list_mqs`: This operation lists the existing message queues. It returns the following:
    * `id`: The id of the server that runs the message queue
    * `Name`: The name of the message queue
    * `Endpoint`: The endpoint of the message queue
    * `DashboardURL`: The URL of the dashboard of the management plugin of RabbitMQ (if it is the chosen engine)
    * `Flavor`: The flavor of the server that runs the message queue
    * `KeyPair`: The keypair that can access the server that runs the message queue
    * `Engine`: The type of the message queue (`RabbitMQ` or `Mosquitto`)
    * `Status`: The status of the server that runs the message queue
* `delete_mq`: This operation deletes a message queue given its name or id
* `get_mq_info`: This operation lists [some information](https://docs.openstack.org/openstacksdk/latest/user/resources/compute/v2/server.html#openstack.compute.v2.server.Server) about a message queue given its name or id

## SAVI MQ Web
The functionality of this engine is exposed via a web portal. To know more about the portal and how to run it, check its [README.md](SAVI_MQ_web/README.md).

## SAVI MQ CLI
The functionality of this engine is exposed via a CLI tool. To know more about the tool and how to run it, check its [README.md](SAVI_MQ_CLI/README.md). 