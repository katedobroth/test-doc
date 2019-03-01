# Manage Cloud Sockets {#manage_cloud_sockets}


You can set up cloud sockets with endpoints in any of these components:

* __Data Lake or Data Mart__.

    Example: Allow access to a tool such as Flume through a second Cazena gateway port.

* __Enterprise__

    Example: Set up a custom Enterprise cloud socket to move data from an enterprise server into the datacloud using Sqoop.

* __AppCloud__

    Example: Install Streamsets on an App Cloud node, and then create a custom cloud socket that allows access to that endpoint. The AppCloud allows you to deploy any tool (e.g., analytics, machine learning, or proprietary algorithms), with secure access to data in the cloud.

## Example: Enterprise Cloud Socket {#create_enterprise_socket}

This examples shows how to set up a custom Enterprise cloud socket, which might be used to move data from an enterprise server into the datacloud using Sqoop. Instructions for using Sqoop can be found in the [Data Movement section](#sqoop).

1. On __System > Manage Gateways__ , select __Enterprise__ on the left side of the screen. If there are multiple Cazena Gateways, make your selection under the gateway that you want to use.
1. Click __New Cloud Socket__.
1. Enter a name and (optional) description for the cloud socket.
1. Select the the port number and protocol that you want to use for the Cazena Gateway. You may use the same port number with different protocols. For example, you could have two cloud sockets that both use port 11300, with one over TCP and one over UDP.
1. In the __Endpoint__ section, enter the IP address and port for the enterprise server.
1. <em>Optional:</em> You may enter an additional path to the location on the enterprise server.
1. Click __Save__.

  ![ Enterprise Cloud Socket ](assets/documentation/cloud_sockets/ent_cloud_socket.png "Enterprise Cloud Socket")
  {:.image-no-outline}

## Activate and Update Ports {#update_ports}

From the Cazena console, system administrators may specify the ports in the environment that will be used for each service on Cazena gateway(s).

To manage ports, click on the __System__ tab. By default, you will see a list Cazena gateways on the left side of the screen. Under each gateway, you will see each of your data lakes and/or data marts, as well as an option to view [enterprise services](#enterprise_cloud_socket) associated with that gateway.
{:.list}

1. Under any Cazena gateway in the list, click on the name of a data lake or data mart, or Enterprise Services.
1. Click on any port number on the right to change its default value.

    __Note:__ Port numbers must be in the range 32768 - 60999.
    {:.note}

1. Use the slider in the __Active__ column to activate or deactivate any port.


![ Activate and Update Ports ](assets/documentation/cazena_gateway/czgw_manage_ports.png "Activate and Update Ports")

___
{:.end-section}