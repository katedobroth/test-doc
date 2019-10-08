
# Move Data {#move_data}


The section covers the following types of data movements:
{:.list}
  * [Move to HDFS using Sqoop](#sqoop)
  * [Move to HDFS using WebHDFS](#hdfs)
  * [Move to ADLS using WebHDFS](#adls_webhdfs)




## Move to HDFS Using Sqoop  {#sqoop}

Cazena will install any JDBC drivers that you need to use Sqoop for moving data from the enterprise into the datacloud. At a high level, you'll follow these steps to move data into the Cazena datacloud using Sqoop:

1.  Either a system administrator or Cazena support will [set up an enterprise cloud socket](#create_enterprise_socket) that contains the information needed to connect to the enterprise resource.
1. Use the hostname and port provided by the enterprise cloud socket when you set up a Sqoop job. The example below will show how to use this information in Hue.

### Before You Begin
{:.step}

* You must have an [enterprise cloud socket](#create_enterprise_socket), which contains the information needed to connect to the enterprise resource where the data resides. The cloud socket must be set up by a system administrator or Cazena support.

* If you are moving data from an Oracle server, the time zone of the data lake must be available to the Oracle database.


### Step 1: Get Hostname and Port from the Cazena console {#enterprise_cloud_socket}
{:.step}


__On the Cazena console:__
{:.list}

1. Select the __Cloud Sockets__ tab. On the left side of the screen, click on the name of the cloud socket you want to use. To search for a particular cloud socket, use your browser's __Find__ command.
1. The hostname and port will appear on the right side of the screen. Copy the hostname and port.

    ![ Enterprise Service ](assets/documentation/data_movement/enterprise_cloud_socket.png "Enterprise Service")


### Step 2: Use Hue to Create Connection Links {#cgw_hue_connection_links}
{:.step}

#### Connect to Hue
1. On the __Cloud Sockets__ tab, select __Hue Server__ on the left side of the screen
1. Click on the link on the right side of the screen to open Hue.
1. Sign into Hue using your Cazena credentials.
1. From the Hue user interface, open the left menu, then select __Browsers > Sqoop__.
1. Click __New Job__ in the upper right corner.
1. In the next step, you will use the hostname and port to create a link for the __From link:__ field.

    ![ Sqoop New Link ](assets/documentation/cazena_gateway/sqoop_new_link.png "Sqoop New Link")
    {:.image-no-outline .width-75}

#### Create a link to the enterprise resource

Use the following information when you create the __From link:__ for a Sqoop job.
{:.list}

1. For __Connector__, select `generic-jdbc-connector`.
1. For __JDBC Driver Class__, enter one of the following:
    * Oracle: `oracle.jdbc.OracleDriver`
    * Netezza: `org.netezza.Driver`
    * PostgreSQL: `org.postgresql.Driver`

1. Use Hostname and Port from the enterprise cloud socket (see Step 1) to create a JDBC string. For example, a JDBC string for Netezza might be:


        jdbc:netezza://czgw.cazena.internal:11000/marketing-db

    ...where __czgw.cazena.internal:11000__ is the hostname and port from the enterprise cloud socket.



##### Troubleshooting connection links

If you are unable to save a JDBC connection link:
{:.list}

* On the __Manage Gateways__ page, make sure that the enterprise service that you are using is running and has been activated. On the left side of the screen, select __Enterprise__, then find the service on the right side of the screen. The switch in the __Active__ column should be blue, and the status for the port should be green.

    ![ Troubleshoot enterprise cloud socket ](assets/documentation/cazena_gateway/troubleshoot_ent_service.png "Troubleshoot enterprise cloud_socket")
* From the machine that is running the gateway, run `cgw-show-ipservices`. If the service exists, it should show in the results, with the server IP and port that appears on the list of enterprise gateways (see above).

    ![ Results of cgw-show-ipservices ](assets/documentation/cazena_gateway/cgw-show-ipservices.png "Results of cgw-show-ipservices")

* To check that the link really has been created: In Hue, select __Data Browsers > Sqoop Transfer__, the click on __Manage Links__ in the upper right corner. See if the link that you tried to create is on the list.

#### Create a link for HDFS
{:.list}

1. From the __New Job__ screen, click __Add a New Link__ to add a second link.
1. Give the connector a name.
1. For __Connector__, select __hdfs-connector__.
1. For __HDFS URI__, enter `hdfs://nameservice:8020`
1. Click __Save__.
  ![ Sqoop To Link ](assets/documentation/cazena_gateway/sqoop_to_link.png "Sqoop To Link")
  {:.width-75}

1. Back on the __New Job__ screen, select that link as the __To link__.


### Step 3: Create and Run the Sqoop Job {#cgw_hue_sqoop_job}
{:.step}


#### Step 1 (Hue)
{:.list}

Select the __To__ and __From__ links (described in the previous step), then click __Next__.           |  <img src="assets/documentation/cazena_gateway/sqoop_job_step1.png">
{:.table-image}


#### Step 2 (Hue)
{:.list}

For __Table name__, enter the name of the table you want to import from your database. <br><br> For __Partition Column__ (optional): Enter the name of the partition column, if applicable. The partition column is often the table's primary key, but it can also be any column of your choosing. <br><br>Click __Next__.         |  <img src="assets/documentation/cazena_gateway/sqoop_job_step2.png">
{:.table-image}


#### Step 3 (Hue)
{:.list}

For __Output Format__, select __TEXT_FILE__.<br><br>For __Compression Format__, select __NONE__.<br><br>For __Output directory__, enter `/user/sqoop2/postgres`<br><br>Leave all other fields blank.<br><br>Click __Save and Run__.         |  <img src="assets/documentation/cazena_gateway/sqoop_job_step3.png">
{:.table-image}

---
{:.end-section}


## Move to HDFS Using WebHDFS {#hdfs}

This example describes how to move a file (__nycflights.dsv__) into a directory (__user/my_username/my_directory__) on your Cazena data lake.

Step 1: Get the IP address and Port for WebHDFS
{:.step}

1. Select the __Cloud Sockets__ tab. On the left side of the screen, under __APIs__ , select __WebHDFS__.
1. Copy the __Cazena DNS__ address and port.

![ HDFS Cloud Socket ](assets/documentation/data_movement/webhdfs_cloud_socket.png "HDFS Cloud Socket")


Step 2: Get the HDFS Location Where You Want to Move Data
{:.step}

From a terminal window, run the following command to determine the location in HDFS where the data will go:


        curl -i -k -u <USERNAME>:<PASSWORD> -X PUT "http://<IP-ADDRESS>:<PORT>/gateway/cazena/webhdfs/v1/<DIRECTORY>/<FILENAME>?op=CREATE"

Where:

`<USERNAME>` and `<PASSWORD>` are your username and password for the Cazena console

`<IP-ADDRESS>` and `<PORT>` are the server and port from the Cloud Socket (HDFS-REST-API)

`<DIRECTORY>` is the path to the HDFS directory.

  __Note__: The full path to the directory will always begin with __user/&lt;username>__  . You can sign into Hue to see your directory structure.
  {:.note}


`<FILENAME>` is the name of the file. You must include the filename, and it must match the name of the source file.




__Example:__  To move the file __nycflights.dsv__ to the directory __/user/my_username/my_directory__ , you would start with a command like this:

        curl -i -k -u my_username:mypassword -X PUT "http://1.2.3.4:11979/gateway/cazena/webhdfs/v1/user/my_username/my_directory/nycflights.dsv?op=CREATE”

The system will return several values, including the HDFS location, e.g.,

      Location: http://1.2.3.4:11979/gateway/cazena/webhdfs/data/v1/webhdfs/v1/user/my_username/my_directory/nycflights.dsv?_=AAAACAAAABAAAAEAzrO5cJpwRtgS_VvH60NYdTGHgRY5YOcHT7bHdAPh5uADDoHlpHWuA5BkU7D_IwOWGQa7FSBj12Q0vwQ3LmYAx01AICxQ3ZCyY1TD29nHJdhMjSFVcdhDS5POisjHIS8gEeWgIWMdYOP51xi0HDjjO0iddgpnnCDiZ1NYqEZxhpuVtw9Hu_QX3IAYtuN11wP9AGqWccrDI6EiOaWkuoDMV_wiFySp02SGsFC2VpqjVgLxuF7y_TcjTfz_n5V6-ATadpKijxatihot_XGFoNwMUAnV_vMwYqOvYnEt0k6QegqbmTOUXUMpE2ocZ4VlXK13toqQKmDUS_kOFBrrqwaClA0wRpw2K1Tf4jPsOnjGQ_6PTPNtwYaGXg


Step 3: Move Data to HDFS
{:.step}

Use the location from the previous step in the command that will move the data into HDFS:

      curl -i -k -u <USERNAME>:<PASSWORD> -X PUT -T <FILENAME> "<LOCATION>"

`<USERNAME>` and `<PASSWORD>` are your username and password for the Cazena console

`<FILENAME>` is the file containing the data that you want to move. This might include the path to the file. The name of the actual file must be the same as the name that you used in the previous step.

`<LOCATION>` is the location from the previous step

__Example:__ To move the file nycflights.dsv into the location from the previous step, you would use a command like this:

      curl -i -k -u my_username:mypassword -X PUT -T nycflights.dsv "http://1.2.3.4:11979/gateway/cazena/webhdfs/data/v1/webhdfs/v1/user/my_username/my_directory/nycflights.dsv?_=AAAACAAAABAAAAEAzrO5cJpwRtgS_VvH60NYdTGHgRY5YOcHT7bHdAPh5uADDoHlpHWuA5BkU7D_IwOWGQa7FSBj12Q0vwQ3LmYAx01AICxQ3ZCyY1TD29nHJdhMjSFVcdhDS5POisjHIS8gEeWgIWMdYOP51xi0HDjjO0iddgpnnCDiZ1NYqEZxhpuVtw9Hu_QX3IAYtuN11wP9AGqWccrDI6EiOaWkuoDMV_wiFySp02SGsFC2VpqjVgLxuF7y_TcjTfz_n5V6-ATadpKijxatihot_XGFoNwMUAnV_vMwYqOvYnEt0k6QegqbmTOUXUMpE2ocZ4VlXK13toqQKmDUS_kOFBrrqwaClA0wRpw2K1Tf4jPsOnjGQ_6PTPNtwYaGXg"

The system response will include:

    HTTP/1.1 201 Created

To verify that the data has been moved, you can sign into Hue and navigate to the file.

---
{:.end-section}


## Move to ADLS Using WebHDFS {#adls_webhdfs}
If your datacloud runs on Microsoft Azure infrastructure, you may have direct access to a shared folder in the object data store. From the Cazena console, you can view and copy information needed to [move data into ADLS](#move_adls) using WebHDFS.

#### ADLS Account Information {#adls_account}

When your datacloud is provisioned, Cazena sets up a dedicated Customer Access User that has access to the Azure object data store. When you move data, use the username and password for the Customer Access User (i.e., not your own username and password).

1. From the __System__ tab, select __ADLS__.
1. Your account data is displayed at the top of the page, including:
   * Tenant ID
   * Client ID
   * Instance name
   * ADLS Base URL (used in commands such as creating tables and databases)
   * Customer Access username

![ ADLS Account Information ](assets/documentation/data_movement/adls_account_info.png " ADLS Account Information")

##### About ADLS Customer Access User {#adls_user}

On the __System > ADLS__ page, there is a link for changing the password of the Customer Access user. To change the password, you will need to know the existing password, which is initially set by Cazena Support. If you don't know the password, contact support@cazena.com.

If you are signed in to your own Microsoft account on your browser when you click the __Change Password__ link, you may go to a Microsoft screen for changing your own password, rather than the password for the Customer Access user. To avoid this situation, either sign out of your own Microsoft account, or open the link in an incognito browser window.


#### ADLS Commands {#move_adls}

The Cazena console displays the information needed to move data into ADLS using WebHDFS. Your account data is incorporated into a series of commands that you can use to set environment variables, obtain and refresh access tokens, and access the ADLS object store.

![ System > ADLS ](assets/documentation/data_movement/system_adls.png "System > ADLS")

This example will show how to move data from your local file system into the ADLS shared folder.

Step 1: Set Client and Tenant IDs
{:.step}

1. In a terminal window, navigate to the directory that contains the data to be moved.
1. From the Cazena console, select the __System__ tab, then __ADLS__.
1. Copy each of the first two commands and paste them into the terminal window. These commands will set the environment variables CLIENT_ID and TENANT_ID.


        export CLIENT_ID=685800e4-02d3-4fd4-b6f2-152b16aafe49

        export TENANT_ID=2e941617-a05d-4a55-918f-757a04a7be11

Step 2: Set Access and Refresh Tokens
{:.step}
1. To set the CODES environment variable, copy the third command onto your clipboard and paste it into a text editor. Replace ADD-PASSWORD with the password for the [Customer Access user](#adls_account).

    ![ ADLS Commans ](assets/documentation/data_movement/adls_replace_password.png "ADLS Command")

2. Paste the command containing the password into the terminal window.

        export CODES=$(curl -X POST https://login.microsoftonline.com/$TENANT_ID/oauth2/token -F grant_type=password -F resource=https://management.azure.com/ -F client_id=$CLIENT_ID -F username=cz123@cz123.cazena.com -F password=your-password)

    The system will respond with something like the following:


        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                         Dload  Upload   Total   Spent    Left  Speed
           100  3080  100  2434  100   646   6396   1697 --:--:-- --:--:-- --:--:--  6405

1. To check whether the access code was generated, use `echo $CODES`.


       echo $CODES

        {"token_type":"Bearer","scope":"user_impersonation","expires_in":"3600","ext_expires_in":"0","expires_on":"1503072287","not_before":"1503068387","resource":"https://management.azure.com/","access_token":"eyJ

       etc...

1. Copy and paste the commands next to __Get initial access and refresh tokens__. These commands will set the ACCESS_TOKEN and REFRESH_TOKEN variables that will be used in subsequent commands.

        export ACCESS_TOKEN=$(echo $CODES | jq .access_token | sed -e "s/\"//g")
        export REFRESH_TOKEN=$(echo $CODES | jq .refresh_token | sed -e "s/\"//g")


__Refresh Access Codes__

5. Access codes will expire after 5 minutes. To refresh the access code, use the next command next to __Refresh ACCESS_TOKEN__.

        export ACCESS_TOKEN=$(curl -X POST https://login.microsoftonline.com/$TENANT_ID/oauth2/token -F grant_type=refresh_token -F resource=https://management.core.windows.net/ -F client_id=$CLIENT_ID -F refresh_token=$REFRESH_TOKEN | jq .access_token | sed -e "s/\"//g")


Step 3: Move Data into the ADLS folder
{:.step}

1. The final command on the __System > ADLS__ page will access the ADLS folder.


       curl -X GET -H "Authorization: Bearer ${ACCESS_TOKEN}" "https://cz123.azuredatalakestore.net/webhdfs/v1/share?op=LISTSTATUS" | jq

  If the folder is empty, the system will respond with something like this:

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
        100    34  100    34    0     0     39      0 --:--:-- --:--:-- --:--:--    39
        {
          "FileStatuses": {
            "FileStatus": []
          }
        }


1. Set a variable with the name of the file, for example:

        export FILE_TO_USE=nycflights.dsv

1. Use a command such as the following to move the file:

        curl -i -X PUT -L -T $FILE_TO_USE -H "Authorization: Bearer ${ACCESS_TOKEN}" "https://cz123.azuredatalakestore.net/webhdfs/v1/share/${FILE_TO_USE}?op=CREATE"

1. After the movement is complete, you can re-use the command to access the ADLS folder to see the data that you moved:

{: .show-whitespaces .indent}

    curl -X GET -H "Authorization: Bearer ${ACCESS_TOKEN}" "https://cz123.azuredatalakestore.net/webhdfs/v1/share?op=LISTSTATUS" | jq

             % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                            Dload  Upload   Total   Spent    Left  Speed
               100   305  100   305    0     0    457      0 --:--:-- --:--:-- --:--:--   457

             {
            "FileStatuses": {
              "FileStatus": [
               {
                  "length": 1591,
                  "pathSuffix": "dmm.log.snippet",
                  "type": "FILE",
                  "blockSize": 268435456,
                  "accessTime": 1503061325322,
                  "modificationTime": 1503061325528,
                  "replication": 1,
                  "permission": "770",
                  "owner": "7b8783fe-e118-4632-91c4-3049cb85e28a",
                  "group": "bae379d5-e7f6-4c9f-aa89-37d9f71a7744"
                  }
                ]
              }
            }



Alternately, you could use the [ADLS Data Explorer](#adls_object_store) to see the file that you moved.

---
{:.end-section}

