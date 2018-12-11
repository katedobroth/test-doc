# Cazena Gateways {#cgw_cazena_gateway}

A Cazena Gateway manages secure connections between the datacloud and on-premises environments, allowing networking, VPN, data access, user access, analytics tools and manageability.

From the Cazena console, you can [manage cloud sockets](#manage_cloud_sockets), which establish port forwarding rules between the Cazena gateway and endpoints. Endpoints can be located in data lakes, data marts, on-premise locations, or the [AppCloud](#ovw_overview). For more information, see the sections on [managing](#manage_cloud_sockets) and [using](#integration_with_datacloud) cloud sockets.

  The screen below shows the services that can be reached through ports on the Cazena gateway named __cz_gw_01__. The columns under __Cazena Gateway Port__ show the status of the port (up or down), the port number and whether the port is activated.

![ Cazena Gateway on Console ](assets/documentation/cazena_gateway/cazena_gateway.png "Cazena Gateway on Console")


You can connect the Cazena gateway to the datacloud using either of these methods:
{:.list}

* [__Port forwarding__](#cgw_installation): This is a simple configuration of the Cazena Gateway that requirements minimum networking configuration within the enterprise. It allows access to UIs as well as tool connectivity to APIs that have a single end point e.g. ODBC / JDBC.

    The port forwarding configuration can use either IPsec or TLS VPN types. All traffic between the datacloud and the enterprise flows only through the [cloud sockets](#integration_with_datacloud) configured for the Cazena Gateway.


* [__Site-to-Site__](#s2s_installation): This is a more complex configuration that requires networking configuration within the enterprise. It provides a wider range of tool connectivity options which include tools that rely on APIs that have multiple end points e.g. direct communication with Hadoop Namenode API.

    The site-to-site configuration uses IPsec site-to-site VPN, joining the datacloud and enterprise networks virtually, as if they both were within a private enterprise network. In this way, all of the hosts in the PDC network can reach all the hosts in the enterprise network, and vice versa.  Additionally, any [cloud sockets](#integration_with_datacloud) configured for the Cazena Gateway are also available.

### Requirements
To install a Cazena gateway, you will download an OVA file and then install it on a virtual machine in the enterprise data center. The requirements for the virtual machine are described here.

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

## Port Forwarding Configuration {#cgw_installation}

__Note:__ Only system administrators may install Cazena gateways.
{:.note}

To install a Cazena gateway using port forwarding:
{:.list}

1. [Download the Cazena gateway .ova file](#ipsec_tls_download_ova).
1. [Download JDBC files](#download_jdbc) (optional)
1. [Gather information from the Cazena console,](#security_gateway) including the DNS name of the security gateway, the OpenVPN certificate (for TLS) and the pre-shared key (for IPSec).
1. [Install the Cazena gateway.](#install_cgw)
1. [Run `cgw-auto-start` to connect the gateway to your datacloud.](#ipsec_tls_cgw-auto-start)

<br>
These steps are described in detail in the following sections.

### Step 1: Download the Cazena Gateway .ova file {#ipsec_tls_download_ova}
{:.step}

1. Sign into the Cazena support site at <a href="https://support.cazena.com" target="_blank">support.cazena.com</a>
1. Under __Cazena Support__, click on __Downloads__.
1. Click on the __Cazena Gateway__ link to download the .ova file.

##### If you are using vSphere/ESXi 6.5 {#esxi_65}

VMware vSphere/ESXi 6.5 and later has deprecated its support for OVAs.  Untar the OVA file to extract the OVF and VMDK files. You will not need the MF file.

    $ tar -xvf "CazenaGateway.ova"
    x CazenaGateway.ovf
    x CazenaGateway.mf
    x CazenaGateway-disk1.vmdk


### Step 2: Download JDBC Files (optional) {#download_jdbc}
{:.step}

If you are connecting to Oracle or Netezza, you will need a database-specific JDBC driver. Currently, the Cazena Gateway has been qualified with the following JDBC drivers:
{:.list}

* Netezza 7.2.0, release ojdbc7-12.1.0.1.0-linux.x64.jar
* Oracle 11gR2, release nzjdbc3.jar

These files can be downloaded from the appropriate vendor.

### Step 3: Gather Information from the Cazena Console {#security_gateway}
{:.step}

__Note:__ If you are unable to sign into the Cazena console, contact support@cazena.com for the information necessary for installing a Cazena gateway.
{:.note}

1. In the Cazena Console, select the __System__ tab.
1. On the __Manage Gateways__ tab, click __Add a New Gateway__
1. If you are using TLS, click on __OpenVPN config__ to download the certificate.
1. Make a note of the __Security Gateway__ field.
1. If you are using ipsec, you will also need the __Pre-Shared Key__.
1. You can copy the commands with most of the fields filled in from this screen.

![ New Gateway ](assets/documentation/cazena_gateway/new_gateway.png "New Gateway button")


### Step 4: Install the Cazena Gateway {#install_cgw}
{:.step}


1. Import the CazenaGateway.ova file.


    <table class="table-30-70">
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

1. __Important:__ After the import has finished, open the VM's network settings and make sure the network adapter is set to 'bridged mode'. This will allow the CGW ethernet primary interface (eth0) to have an enterprise reachable IP address, so that it will be exposed to enterprise users.


1. Start the Cazena VM and sign into the gateway:
    * username: `cazena`
    * password: `cazena`
<br><br>


1. __If you are using TLS__: Copy the certificate that you downloaded in the previous steps to the cazena user home directory. Do not unpack the file.

    __Example__: `$ scp cazena-openvpn.tar cazena@u.v.w.x:~`

1. If you are connecting to Oracle or Netezza, copy any needed JDBC driver(s) to the __Downloads__ directory

    __Example__: `$ scp ~/Downloads/ojdbc7-12.1.0.1.0-linux.x64.jar cazena@v.x.y.z`



### Step 5: Run `cgw-auto-start` to Connect the Cazena Gateway to Your Datacloud {#ipsec_tls_cgw-auto-start}
{:.step}

1. From a terminal window, use the IP address of the VM to connect to the Cazena gateway.

    __Example__:  `$ ssh cazena@w.x.y.z`

1. Change the gateway's default password.

   `$  sudo passwd`


1.	If you haven't already, set up a __dedicated__ user account with system administrator privileges for the Cazena gateway. (See [Instructions for setting up a user account](#users).)

1. <a name="cgw-auto-start"/>Use `cgw-auto-start` to connect to the gateway.

__Note__: You can copy these commands with some of the fields filled in from the screen that appears when you click __Add a New Gateway__.  See __[Step 3](#security_gateway)__.
{:.note}



  __TLS__:

        cgw-auto-start -s [security-gateway-url] -t tls -u [cgw-user-username] -p [cgw-user-password] -n [cgw-name]

  __ipsec__:

      cgw-auto-start -s [security-gateway-dns-name] -t ipsec -u [cgw-user-username] -p [cgw-user-password] -n [cgw-name] -k [preshared-key]


  where:

  * `[security-gateway-dns-name]` is the DNS name of the security gateway. (See __[Step 3](#security_gateway)__ ).


  * `[cgw-user-username]` and `[cgw-user-password]` are the username and password of the dedicated gateway user.

  * `[cgw-name]` is a unique name for the Cazena gateway.

  * `[preshared-key]` is the preshared key.  (See __[Step 3](#security_gateway)__ ).

  * (Optional): Use `-m` to set a different timeout from the default timeout of 30 seconds (e.g., `-m 120`). This timeout is used when downloading the Cazena gateway software. You may want to change it if you have to [troubleshoot](#cgw_troubleshooting) the Cazena gateway.



  __Note__: The gateway name that you choose here will show on the __System__ tab. See the sections on [updating ports](#update_ports), creating [data stores](#data_stores) and [integration with the datacloud](#integration_with_datacloud).
  {:.note}

#### Example

     cgw-auto-start -s production.xxx.cazena.com -t tls -u cg_user -p my_password -n my_gateway

1. The system will respond:

        Starting up CGW auto restart
        run cgw-auto-show or look in /var/log/cazena/cgw-auto.log to determine status

      Inside of /var/log/cazena/cgw-auto.log, there are three lines giving the network address info, similar to this:

      * PDC network: 10.128.80.0/21
      * ENT address: 10.4.132.10
      * ENT network: 10.4.132.0/24 10.4.133.0/24 10.4.130.0/23

      <br> For PDC DNS, the IP address of the IPA server is found in the file /etc/resolv.conf, similar to this:

      *   nameserver  10.128.80.48   # by strongswan
<br>

2. Use `cgw-auto-show` to see the status:

        $ cgw-auto-show
        Tunnel is up
        CGW DMC is up
        CGW DMC version matches PDC version

---
{:.end-section}

## Site-to-Site Configuration {#s2s_installation}

Before You Begin
{:.step}


The following can be obtained from Cazena support (support@cazena.com):
{:.list}

* PDC CIDR network address
* An IPsec site-to-site Pre-Shared Key (PSK) exclusively for machine authentication
* Dedicated Cazena user account for the site-to-site VPN connection
* DNS name of the security gateway

The following must be obtained from the enterprise network administrator:
{:.list}

* Enterprise CIDR network address(es) that cater for all user and source locations within the enterprise network

* Enterprise IP address assigned to the CGW (must be within one of the Enterprise network addresses)

<br>
To install a Cazena gateway using IPSec site-to-site VPN, follow these steps:
{:.list}

1. [Download and install the Cazena gateway](#s2s_download_ova).
1. [Run `cgw-auto-start`](#s2s_step2) to connect the gateway to your datacloud.
1. [Modify the enterprise routing table](#routing_table) to add a static route for the PDC network.
1. (Optional) Add a DNS forwarding entry to the enterprise DNS for forwarding `cazena.internal` requests to the IPA server.

See the sections below for more details.

### Step 1: Download and Install the Cazena Gateway .ova file {#s2s_download_ova}
{:.step}

1. Sign into the Cazena support site at <a href="https://support.cazena.com" target="_blank">support.cazena.com</a>
1. Under __Cazena Support__, click on __Downloads__.
1. Click on the __Cazena Gateway__ link to download the .ova file.

##### If you are using vSphere/ESXi 6.5 {#esxi_65}

VMware vSphere/ESXi 6.5 and later has deprecated its support for OVAs.  Untar the OVA file to extract the OVF and VMDK files. You will not need the MF file.

    $ tar -xvf "CazenaGateway.ova"
    x CazenaGateway.ovf
    x CazenaGateway.mf
    x CazenaGateway-disk1.vmdk


1. Import the CazenaGateway.ova file.


    <table class="table-30-70">
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

1. __Important:__ After the import has finished, open the VM's network settings and make sure the network adapter is set to 'bridged mode'. This will allow the CGW ethernet primary interface (eth0) to have an enterprise reachable IP address, so that it will be exposed to enterprise users.


1. Start the Cazena VM and sign into the gateway:
    * username: `cazena`
    * password: `cazena`
<br><br>


### Step 2: Run `cgw-auto-start` to Connect the Cazena Gateway to Your Datacloud {#s2s_step2}
{:.step}


1. From a terminal window, use the IP address of the VM to connect to the Cazena gateway.

    __Example__:  `$ ssh cazena@w.x.y.z`

1. Change the gateway's default password.

   `$  sudo passwd`


1. <a name="cgw-auto-start"/>Use `cgw-auto-start` to connect to the gateway:

         cgw-auto-start -t ipsec-s2s -s [security-gateway-dns-name] -u [cgw-user-username] -p [cgw-user-password]  -n [cgw-name] -k [preshared-key] -e [enterprise-cidr-net-addresses]


  where:

  * `[security-gateway-dns-name]` is the DNS name of the security gateway. (Contact support@cazena.com for the DNS name).


  * `[cgw-user-username]` and `[cgw-user-password]` are the username and password of the dedicated gateway user.

  * `[cgw-name]` is a unique name for the Cazena gateway.

  * `[preshared-key]` is the preshared key.

      __Note:__ The preshared key for site-to-site is shown in the Cazena console, on the __System > VPN Configuration__ page. If you update the key, you will have to re-run `cgw-auto-start`.
      {:.note}

  * `[enterprise-cidr-net-addresses]` is one or more enterprise CIDR net addresses.

    * You may specify multiple address, either with separate `-e` flags or as a comma separated list (e.g., `-e 10.4.133.0/24,10.4.130.0/23`).
    * If an address is not specified, the address of the enterprise LAN network where the Cazena gateway resides will be used.

For help with `cgw-auto-start` use `cgw-auto-start --help`.

#### Example

       cgw-auto-start -t ipsec-s2s -u cg_user -p my_password -s production.xxx.cazena.com -n my_gateway -k my-key -e 10.4.132.0/24 -e 10.4.133.0/24,10.4.130.0/23

1. The system will respond:

          Starting up CGW auto restart
          run cgw-auto-show or look in /var/log/cazena/cgw-auto.log to determine status

      Inside of /var/log/cazena/cgw-auto.log, there are three lines giving the network address info, similar to this:

      * PDC network: 10.128.80.0/21
      * ENT address: 10.4.132.10
      * ENT network: 10.4.132.0/24 10.4.133.0/24 10.4.130.0/23

      <br> For PDC DNS, the IP address of the IPA server is found in the file /etc/resolv.conf, similar to this:

      *   nameserver  10.128.80.48   # by strongswan
<br>
2. Use `cgw-auto-show` to see the status:

          $ cgw-auto-show
          Tunnel is up
          CGW DMC is up
          CGW DMC version matches PDC version

If the system responds differently to these commands, see the section on [troubleshooting.](#cgw_troubleshooting)

### Step 3: Make changes in your network {#routing_table}
{:.step}

1. Modify the enterprise routing table to add a static route for the PDC network.

    __Example:__ For a Linux network, add a route for the PDC network using the CGW’s enterprise network IP address as the gateway, e.g.:

             sudo route add –net 10.128.80.0/21 gw 10.4.132.10


1. (Optional) Add a DNS forwarding entry to the enterprise DNS for forwarding `cazena.internal` requests to Cazena's internal DNS.





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

* Run one of the following commands (depending on the type of tunnel):

    * __For a TLS tunnel__:

        <a name="cgw-show-tls"/>Run `cgw-show-tls`.

        If the tunnel is up, you should see:

            $ cgw-show-tls
            tls tunnel up: connected to <DNS-NAME> (34.192.178.80:443) on Fri Nov 18 13:28:26 UTC 2016


    * __For an ipsec tunnel__:

        <a name="cgw-show-ipsec"/>Run  `cgw-show-ipsec`.

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

###Trouble with data movement {#troubleshoot_connectivity}

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

Before You Begin
{:.step}

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

<br>
__Measure latency and throughput from an external Linux or Mac system:__

You can use `nping` and `wget` to measure latency and throughput through the Cazena gateway.

1. On the __Cloud Sockets__ tab, select __Cazena Console__ on the left side of the screen.

    ![ Cazena Gateway IP and port ](assets/documentation/cazena_gateway/cgw_ip_port.png "Cazena Gateway IP and port")

2. Use __IP Address:Port__ to run these commands:

    * `nping <IP address> -p <PORT>`
    * `wget -O /dev/null http://<IP address>:<PORT> /CazenaGateway.ova`
    *
    {:.list-unstyled}

    <br>
   __Example:__

   * `nping 	192.131.12.2 -p 11092`
   *  `wget -O /dev/null http://192.131.12.2:11092/CazenaGateway.ova`
   {:.list-unstyled}



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