# Cazena Gateways {#cgw_cazena_gateway}

## Overview {#cgw-overview}

There are two ways to securely connect to the Cazena service. Both methods allows Cazena customers to access the private [cloud sockets](#cloud_sockets) in the Cazena service within their private corporate networks. 


#### Site-to-Site {#site-to-site-cgw}

A site-to-site connection establishes an IPSec connection between your enterprise and the Cazena service. 

Cazena supports BGP, which allows HA connections to the Cazena Service. The Cazena service will be provisioned in a CIDR range, which will be confirmed to not overlap with any existing CIDRs used for the enterprise network. This configuration allows full access to services exposed by the Cazena service. A subset of services are only available with site-to site configurations, including:
{:.list}

* Kafka
* Cazena Internal DNS

After the site-to-site connection has been established, a DNS forwarding rule must be added to your enterprise DNS to allow resolution of Cazena FQDNs.

Cazena support will provide you with the correct rule sets, depending on whether you have a routing or policy-based firewall. If your enterprise does not support BGP, Cazena can support static routes. However, this will prevent a HA connection, resulting in longer outages during maintenance periods.


#### Cazena Gateway {#port-forwarding-cgw}
 
The Cazena Gateway is a software device that is packaged as a OVA, which is typically deployed within your DMZ. It manages secure connections between the datacloud and on-premises environments, allowing access to [cloud sockets](#cloud_sockets) via a port forwarding mechanism.

This is a simpler networking configuration than site-to-site connections, and requires minimal networking configuration within the enterprise. There are a few Cazena services that are not available with this connection, including Kafka and Cazena Internal DNS.
This is a simpler networking configuration than site-to-site connections, and requires minimal networking configuration within the enterprise. There are a few Cazena services that are not available with this connection, including Kafka and Cazena Internal DNS.

Cazena Gateways that use the port forwarding configuration can be managed using the Cazena console. The rest of this section describes the following:
 
* [Install a new Cazena gateway](#install_new_gateway)
* [Create custom cloud sockets](#manage_cloud_sockets)
* [Activate and update ports](#update_ports)
* [Troubleshooting](#cgw_troubleshooting)
* [Stop and delete a Cazena gateway](#cgw_delete)



## Install a New Cazena Gateway {#install_new_gateway}

If your site is using Cazena gateways configured with port forwarding, you can install a new Cazena gateway.  You will download an OVA file and then install it on a virtual machine in the enterprise data center. 

### Requirements

#### VMWare
Currently the OVA is supported on VMware systems.
{:.list}

  * VMware Fusion/Player 4.0 or later
  * Workstation 8.0 or later
  * vSphere/ESXi 5.0 to 6.0. VMware vSphere/ESXi 6.5 has deprecated its support for OVAs. If you use vSphere/ESXi 6.5, you will have to manually untar the file. [Instructions](#esxi_65) are in the next section.

#### Hardware
   * 4 virtual CPU cores
   * 2.0 GB free memory (4.0 GB recommended)
   * 25 GB free disk space

#### Connectivity
   * JDBC/IP connectivity to enterprise database servers
   * Outbound Internet connectivity on ports TCP 443 (TLS/SSL), UDP 500 (ISAKMP/IKE), UDP 4500 (IPsec NAT-T), UDP 123 (NTP)


### To install a Cazena gateway: {#cgw_installation}
{:.list}
The steps for installing a Cazena gateway are described in detail in the following sections.

1. [Download and import the Cazena gateway .ova file](#ipsec_tls_download_ova).
1. [Install the Cazena gateway.](#install_cgw)
1. [Run `cgw-auto-start` to connect the gateway to your datacloud.](#ipsec_tls_cgw-auto-start)
1. [Create an A record in the enterprise DNS](#dns_a_record)


### Step 1: Download and Import the Cazena Gateway .ova file {#ipsec_tls_download_ova}
{:.step}

1. Sign into the Cazena support site at <a href="https://support.cazena.com" target="_blank">support.cazena.com</a>
1. Under __Cazena Support__, click on __Downloads__.
1. Click on the __Cazena Gateway__ link to download the .ova file.

##### If you are using vSphere/ESXi 6.5 {#esxi_65}
{:.indent}

 VMware vSphere/ESXi 6.5 and later has deprecated its support for OVAs.  Untar the OVA file to extract the OVF and VMDK files. You will not need the MF file.
{:.indent}

    $ tar -xvf "CazenaGateway.ova"
    x CazenaGateway.ovf
    x CazenaGateway.mf
    x CazenaGateway-disk1.vmdk
{:.indent}


 4. Import the CazenaGateway.ova file.


    <table class="table-30-70 row-borders">
      <tbody>
        <tr>
          <th>Client</th>
          <th>Instructions</th>
        </tr>
        <tr>
          <td>VMWare Fusion</td>
          <td>
          <ol>
              <li>Choose <strong>File > Import...</strong></li>
               <li>Select the CGW OVA file.</li>
           </ol>
           </td>
        </tr>
        <tr>
          <td>Virtual Machine Manager</td>
          <td>
          <ol>
              <li>Choose <strong>Add > Import...</strong></li>
               <li>Select the CGW OVA file.</li>
           </ol>
          </td>
        </tr>
        <tr>
          <td>vSphere/ESXi Web client</td>
          <td>
            <ol>
                <li>Choose <strong>Navigator -> Virtual Machines -> Create/Register VM...</strong></li>
                <li>Select <strong>Deploy a virtual machine from an OVF or OVA file</strong></li>
                <li>Enter a name</li>
                <li>Select file(s)
                    <ul>
                    <li><em>5.0 to 6.0:</em> Add the OVA </li>
                    <li><em>6.5 or later:</em> Add the OVF and VMDK files<br>
                    (See <a href="#esxi_65">instructions</a> for untarring the OVA file.)
                    </li>
                    </ul>
                 </li>
            </ol>
           </td>
        </tr>
      </tbody>
    </table>

    __Important:__ After the import has finished, open the VM's network settings and make sure the network adapter is set to 'bridged mode'. This will allow the CGW ethernet primary interface (eth0) to have an enterprise reachable IP address, so that it will be exposed to enterprise users.
    {:.note}


### Step 2: Install the Cazena Gateway Certificate {#install_cgw}
{:.step}


1. Start the Cazena VM and sign into the gateway:
    * username: `cazena`
    * password: `cazena`
<br><br>


1. Copy the Client Authentication Certificate that was emailed to you to the Cazena gateway.

    * __Option 1__: Use `scp` as in this example: `$ scp cazena.pem cazena@u.v.w.x:~ `
    * __Option 2__: Copy and paste the contents of the `cazena.pem` file into a new file on the Cazena gateway


1. Install the certificate.

    `$ cgw-install-cert cazena.pem` 




### Step 3: Run `cgw-auto-start` to Connect the Cazena Gateway to Your Datacloud {#ipsec_tls_cgw-auto-start}
{:.step}

1. From a terminal window, use the IP address of the VM to connect to the Cazena gateway.

    __Example__:  `$ ssh cazena@w.x.y.z`

1. Change the gateway's default password.

   `$  sudo passwd`


1.	If you haven't already, set up a __dedicated__ user account with system administrator privileges for the Cazena gateway. (See [Instructions for setting up a user account](#users).)

1. <a name="cgw-auto-start"/>Use `cgw-auto-start` to connect to the gateway.


<div class="code-wrapper">
<pre class="indent copy-area" id="cgw-auto-start-cmd">cgw-auto-start -t ipsec-crt -s <span style="color:red">security-gateway-dns-name</span> -u<span style="color:red"> cgw-user-username</span> -p <span style="color:red">cgw-user-password</span> -n <span style="color:red">cgw-name</span> -k <span style="color:red">client-certificate-password</span> -w</pre>
<button class="btn clipboard-btn" data-clipboard-target="#cgw-auto-start-cmd">Copy</button>
</div>


  where:

  * `security-gateway-dns-name` is the DNS name of the security gateway, available in email from Cazena support or in the Cazena console. 

  * `cgw-user-username` and `cgw-user-password` are the username and password of the dedicated gateway user. This may have been emailed to you by Cazena support.

  * `cgw-name` is a unique name for the Cazena gateway. The name may contain `A-Z`, `a-z`, `0-9` and `-`.

  * `client-certificate-password` is the certificate password that was emailed to you.

<br>

#### Example

    cgw-auto-start -t ipsec-crt -s portal.partner.cazena.com -u cazenauser -p password -n mygateway -k clientpassword -w
 
The system will respond:

    Starting up CGW auto restart
    run cgw-auto-show or look in /var/log/cazena/cgw-auto.log to determine status

  Inside of `/var/log/cazena/cgw-auto.log`, there are three lines giving the network address information, similar to this:

  * PDC network: 10.128.80.0/21
  * ENT address: 10.4.132.10
  * ENT network: 10.4.132.0/24 10.4.133.0/24 10.4.130.0/23

  <br> For PDC DNS, the IP address of the IPA server is found in the file /etc/resolv.conf, similar to this:

  *   nameserver  10.128.80.48   # by strongswan
<br><br>

Use `cgw-auto-show` to see the status:

        $ cgw-auto-show
        Tunnel is up
        CGW DMC is up
        CGW DMC version matches PDC version


### Step 4: Create an A Record in the Enterprise DNS {#dns_a_record}
{:.step}

When the Cazena Gateway is installed, onsite administrators will assign a private IP address to the VM. Because all Cazena endpoints are TLS-enabled, accessing [cloud sockets](#cloud_sockets) with the IP address will result in security errors. For this reason, all access must use a FQDN that matches the public certificate used for your single-tenant deployment. You must add an __A record__ to your enterprise DNS, to allow the enterprise to refer to the Cazena gateway using an FQDN rather than the IP address. 

The A record is a DNS entry of the form:
 
<pre class="indent"><span style="color:red"> gateway-name</span>.pvt.<span style="color:red">customer-hash</span>.cazena.com
</pre>

where
{:.indent, .list}

  * `gateway-name` is the name of your Cazena gateway, as specified in `cgw-auto-start`
  * `customer-hash` is the name of your PDC. 

<br>

__Note__: This A record will not prevent you from reaching [www.cazena.com](https://www.cazena.com). The A record is for the subzone `[gateway-name].pvt.[customer-hash].cazena.com`.
{:.note}

---
{:.end-section}

## Custom Cloud Sockets {#manage_cloud_sockets}


You can set up cloud sockets with endpoints in any of these components:

* __Data Lake or Data Mart__: This type of custom cloud socket could be used, for example, to allow access to a tool such as Flume through a second Cazena gateway port.

* __Enterprise__: An enterprise cloud socket could be used, for example, to move data from an enterprise server into the datacloud using Sqoop.

* __AppCloud__:  The AppCloud allows you to deploy any tool (e.g., analytics, machine learning, or proprietary algorithms), with secure access to data in the cloud. An example use would be to install Streamsets on an App Cloud node, and then create a custom cloud socket that allows access to that endpoint. 

### Example: Enterprise Cloud Socket {#create_enterprise_socket}

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
## Troubleshooting {#cgw_troubleshooting}


Follow these steps if you have run `cgw-auto-start` and either:
{:.list}

* The Cazena gateway doesn't appear in the Cazena console.
* You are having trouble moving data.

### Check that the Cazena Gateway is Operating Correctly

First, run `cgw-auto-show`:

        $ cgw-auto-show 
        --Status--
        Tunnel is up
        Tunnel was started at Mon Jun 11 10:20:40 UTC 2018
        Tunnel has been up for 7h:0m:42s
        CGW DMC is up
        CGW DMC version matches PDC version
        CGW was started at Mon Jun 11 10:20:41 UTC 2018
        CGW has been up for 7h:0m:41s

        --Configuration--
        Tunnel type is ipsec
        Server is cazena-cz123.eastus2.cloudapp.azure.com
        User is cz_user
        CGW name is cazena-gw1


Depending on what `cgw-auto-show` returns, refer to one of these sections:

* [Tunnel is down](#cgw_troubleshoot_tunnel)
* [CGW DMC is down](#cgw_troubleshoot_cgw_dmc)
* Both the tunnel and CGW DMC are up, but you are having [trouble moving data](#troubleshoot_connectivity).

### If the Tunnel is Down {#cgw_troubleshoot_tunnel}

* Double-check your  [ cgw-auto-start ](#cgw-auto-start) command.

    * Make sure that you are using the correct user name/password.
    * Check that the name/password are not being used by someone else.
    * Make sure that the secgw name and preshared key (if used) are correct.

&nbsp;&nbsp;&nbsp;&nbsp;If necessary, re-run [cgw-auto-start](#cgw-auto-start).

* Check with Cazena support to see if your site has a whitelist of allowed IP addresses. If so, the IP address of the Cazena gateway must be included in the whitelist.

* Run  `cgw-show-ipsec`.

  If the tunnel is up, you should see:

                $ cgw-show-ipsec

                Redirecting to /bin/systemctl status strongswan.service
                ipsec daemon running
                Security Associations (2 up, 0 connecting):
                      dm-psk[9]: ESTABLISHED 4 minutes ago, 10.1.3.80[dm-user]...40.70.186.53[rw-psk]
                      dm-psk{24}:  INSTALLED, TUNNEL, reqid 1, ESP in UDP SPIs: c111a8c9_i c1b8fff2_o
                      dm-psk{24}:   10.255.252.2/32 === 10.128.8.0/21
                      dm-psk[8]: ESTABLISHED 50 minutes ago, 10.1.3.80[dm-user]...40.70.186.53[rw-psk]
                      dm-psk{22}:  INSTALLED, TUNNEL, reqid 1, ESP in UDP SPIs: c0b0c6ba_i caa3ea03_o
                      dm-psk{22}:   10.255.252.2/32 === 10.128.8.0/21


### If CGW DMC is Down {#cgw_troubleshoot_cgw_dmc}

If `cgw-auto-show` indicates that the tunnel is up but the CGW DMC is down:

1. Check the log files.  Open `/var/log/cazena/<gateway-name>.log`, replacing `<gateway-name>` with the name of your gateway.

    If you see `Operation timed out after`
    : The CGW DMC software may not have not downloaded successfully. Try increasing the timeout value using the `-m` option of the [ cgw-auto-start ](#cgw-auto-start) command.

    If you see WARN or ERROR messages:
    : This indicates that CGW DMC is having internal issues. The range of potential issues here are too numerous to list out.  Contact support/engineering for help.

2. Check that the CGW has the necessary port connectivity by running `cgw-reachable`.

       $ cgw-reachable [DNS-NAME]
        Checking cloud services reachability... 
          Security Gateway TLS reachable: TRUE 
          AWS S3 reachable: TRUE 
          Azure storage reachable: TRUE 

    If any of these targets returns FALSE, confirm that the customer firewall is allowing the following ports outbound access from the Cazena gateway.

    * TCP 443 (TLS/SSL)
    * UDP 500 (ISAKMP/IKE)
    * UDP 4500 (IPsec NAT-T)

### Trouble with data movement {#troubleshoot_connectivity}

If you are having trouble moving data, first follow the steps in the previous section to ensure that the Cazena Gateway is operating correctly. Next, you can:

 * [Check connectivity between the gateway and the datacloud](#cgw_pdc_connection)
 * [Check connections to enterprise services](#cgw_enterprise_connection)
 * [Measure latency and throughput](#cgw_throughput_latency)


#### Check Connectivity Between the Cazena Gateway and the Datacloud {#cgw_pdc_connection}
1. Run `cgw-show-ipservices` to see whether the CGW is allowing access to the required ports/services within the PDC; for example:

        [cazena@cgw ~]$  cgw-show-ipservices
        IpService ID: pdc-kibana (PDC-DNAT rule #4, PDC-FWRD rule #4)
        target     prot opt source               destination
        DNAT       tcp  --  0.0.0.0/0            10.4.131.136         tcp dpt:11494 /* id: pdc-kibana, name: kibana */ to:10.128.16.37:5601
        ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            ctstate NEW,ESTABLISHED ctproto 6 ctorigdst 10.4.131.136 ctorigdstport 11494 /* id: pdc-kibana, name: kibana */

        etc

You can also look on the __System__ tab of the Cazena Console to see whether Cazena gateway ports are active.
![ Activate and Update Ports ](assets/documentation/cazena_gateway/czgw_manage_ports.png "Activate and Update Ports")

#### Check Connections to Enterprise Services {#cgw_enterprise_connection}

__For Netezza or Oracle:__
{:.list}

* Make sure that the needed drivers are present in /home/cazena and are read/executable.
  * __Netezza__: nzjdbc3-7.2.0.0-cazena.jar
  * __Oracle__: ojdbc7-12.1.0.1.0-linux.x64.jar

__For Netezza, Oracle or FTP/SFTP:__
{:.list}

* Make sure the servers can be reached.
  1. If you do not have nmap, install it using `sudo yum install nmap`.
  2. The following commands should show that the ports are open:
      * __Netezza__:  `nmap -p 5480 <NZ IP Address> -Pn`
      * __Oracle__: `nmap -p 1521<Oracle IP Address> –Pn`
      * __FTP__: `nmap -p 21 <FTP Server IP> –Pn`
      * __SFTP__: `nmap -p 22 <SFTP Server IP> –Pn`

* Check that the [data store](#data_stores) contains a valid username and password that can access the database/schema/directory.

<br>


#### Measure Latency and Throughput {#cgw_throughput_latency}

If the tunnel and DMC are both up and the IP service connectivity is correct, then there could be an issue with latency or throughput performance. You can use `cgw-speed-test.py` to test both [latency](#speed-test-latency) and [throughput](#speed-test-throughput).

##### Before You Begin

Connect to the Cazena gateway and get the DNS name for the security gateway.

1. From a terminal window, use the IP address of the VM to connect to the Cazena gateway.

    __Example__:  `$ ssh cazena@w.x.y.z`

1. Run `cgw-auto-show` to see the DNS name for your security gateway. The server name is in the section titled __Configuration__.

        --Configuration--
        Tunnel type is ipsec
        Server is cz123.eastus2.cloudapp.azure.com
        User is dm-user
        CGW name is AUTO-CGW

##### CLI Arguments

The command line arguments for `cgw-speed-test.py` can be displayed by using the -h option:

        $ scripts/cgw-speed-test.py -h

        cgw-test-speed.py -s <secgw name> -c <aws, azure> -l -d -t <duration>
           -s  secgw name used for VPN connection
           -c  cloud type (aws/azure)
           -l  latency tests
           -d  download tests
           -t  maximum time to run each test in seconds

<br>

`-s` &nbsp;&nbsp;Required. Specify the DNS name or the IP address of the PDC's security gateway.

`-c` &nbsp;&nbsp;Optional; default is both platforms. Specify the cloud platform, either `azure` or `aws`.

`-l` &nbsp;&nbsp;Optional. Run the latency tests.

`-d` &nbsp;&nbsp;Optional. Run the download tests.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__Note:__ If neither `-l` or `-d` are specified, both types of tests will be run.

`-t` &nbsp;&nbsp;Optional; default value is 30.
{:.list}
  * For latency: The number of tests executed (e.g. 30 TCP handshakes) to determine minimum/maximum/average round trip times.

  * For throughput: The maximum time boundary in seconds for the test to complete.

##### Network Latency {#speed-test-latency}

The network latency test in `cge-speed-test.py` uses the `nping` utility for network packet generation, response analysis and response time measurement.  All tests use TCP for latency measurement. `nping` does a full TCP handshake, including both setup and teardown.  Latency tests are performed from the CGW to three PDC network interfaces:
{:.list}

* __SGW's public interface__: The script tests routes through the public Internet to the PDC's SSL port (443). Be sure that the port is open on the PDC.  If it is not open, N/A is returned for timing values.
* __SGW's private interface__: The script tests routes through the VPN. Be sure that the VPN is connected and that the SSH port (22) is open.
* __IPA's private interface__: The script tests routes through the VPN. Be sure that the VPN is connected and that the SSH port (22) is open.

<br>

__Sample latency test__


    $ scripts/cgw-speed-test.py -s cz123.cazena.com -c aws -l -t 3

    ------- Parameters --------
    name is cz123.cazena.com
    cloud is aws
    tunnel is True
    latency test is True
    download test is False
    max duration is 3
    -----------------------------

    Beginning Latency Tests:
      SecGW Public IP latency: Max: 2.138ms  Min: 2.058ms  Avg: 2.096ms
      SecGW Private IP latency: Max: 2.485ms  Min: 1.860ms  Avg: 2.144ms
      IPA Private IP latency: Max: 2.785ms  Min: 2.188ms  Avg: 2.505ms
    Complete




##### Network Throughput {#speed-test-throughput}

The network throughput test in `cgi-speed-test.py` uses the `wget` utility to download files to the Cazena gateway from three sources:

 * Data Mover in the PDC
 * AWS S3 storage
 * Azure blob storage

<br>

__Sample throughput test__

    $ scripts/cgw-speed-test.py -s ken0608n6247dev.cazena-dev.com  -d -t 3

    ------- Parameters --------
    name is ken0608n6247dev.cazena-dev.com
    cloud is both
    tunnel is True
    latency test is False
    download test is True
    max duration is 3
    -----------------------------

    Beginning Download Tests:
      Azure Blob Store speed: 20.17 MBps, 161.33 Mbps; size: 60.50 MB
      AWS S3 speed: 35.69 MBps, 285.55 Mbps; size: 107.08 MB
      CGW Software speed: 35.79 MBps, 286.33 Mbps; size: 107.37 MB
    Complete




## Stop and Delete a Cazena Gateway {#cgw_delete}

__To stop a Cazena gateway:__

1. From a terminal window, use the IP address of the VM to connect to the Cazena gateway.

    __Example__:  `$ ssh cazena@w.x.y.z`

2. Use `cgw-auto-stop` to stop the gateway:

        $ cgw-auto-stop
        Shutting down CGW auto restart

2. Use `cgw-auto-show` to see the status. If the Cazena gateway has stopped, you will see:

        $ cgw-auto-show
        Tunnel is down
        CGW DMC is down

3. You may use [ cgw-auto-start ](#cgw-auto-start) to restart the gateway.

__To delete a Cazena gateway from the console:__

4. On the __System__ tab, look at the list of Cazena gateways. A trash can icon will appear next to the name of any stopped gateways. Click the icon and confirm that you want to delete the gateway.

__Note__: If you delete a Cazena gateway, all [enterprise cloud sockets](#create_enterprise_socket) and [data stores](#data_stores) associated with that gateway will also be deleted.
{:.note}

![ Delete a stopped Cazena Gateway ](assets/documentation/cazena_gateway/delete_gateway.png "Delete a stopped Cazena Gateway")

---
{:.end-section}