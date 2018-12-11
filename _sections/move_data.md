
# Move Data {#move_data}


The section covers the following types of data movements:
{:.list}
  * [Move to HDFS using Sqoop](#sqoop)
  * [Move to HDFS using WebHDFS](#hdfs)
  * [Move to ADLS using WebHDFS](#adls_webhdfs)
  * [Move Using the Cazena Data Mover](#move_cz_datamover)




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
1. Make a note of the IP address and port that appears on the left side of the page. You might want to copy the information and paste it into a text editor as you assemble the commands in the next steps.

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


## Move Using the Cazena Data Mover {#move_cz_datamover}

From the Cazena console, you can initiate the following types of data movements:
{:.list}
  * Move data from [a Netezza or Oracle server located within your enterprise](#console_import_enterprise)
  * [Import](#console_import_ftp) or [export](#console_export_ftp) data to/from a FTP or SFTP server. FTP/SFTP servers can be located either inside your enterprise or on the public internet.
  * Import data from [your local file system](#console_import_local_file)
  * Move data from other types of data sources, using a [custom data adapter](#custom_data_adapter).
  * Move data from one Cazena service into another.
  * After a data movement has successfully completed via the Cazena console, you can generate a script that will allow you to easily repeat the transfer outside of the Cazena console. For more information, see the section on [Scripting Transfers](#script_transfers).


### From a Netezza or Oracle Server {#import_enterprise}

Before You Begin
{:.step}
You must have a [data store](#data_stores) configured that contains the information needed to connect to the Netezza or Oracle server.


Step 1: Select Source and Destination
{:.step}

1. From the __Datacloud__ tab, click the __Move Data__ button. 
1. *On the dialog that appears:* Under __Select Source__, select __Data Store__, then select the  [data store](#data_stores) for the server that contains your source data.  If you do not see the data store that you need, check that it has been set up. 
1. Under __Select Destination__, select __Cazena Service__, then select the data lake/data mart and dataset where your data should go. 
    * To create a new dataset, select __New__.
1. Click __Continue__.

 
 __Note__: Currently the database used for all objects created in an MPP SQL service called __czdataset__. The __dataset__ name you enter here will become the schema name in the __czdataset__ database in the MPP SQL service.
{:.note}

![ Select Source and Destination ](assets/documentation/data_movement/datastore_source_destination.png "Select Source and Destination")
{:.image-no-outline}

Step 2: Select Tables from the Source (Netezza or Oracle) Database
{:.step}

Next, you will search for and select tables from your source database. When moving from Netezza or Oracle, you can select several tables at once.

#### About Data Conversion

When moving data, the Cazena dataset manager attempts to map column names, datatypes and keys from the source database to the target Cazena workload engine. For example, if a source Netezza database has a distribution column, the system will make the same distribution column if the target is a MPP SQL-based workload engine. For more details, see the section on [__Data Movement Details__](#data_movement_details).

As you select tables to move from your source database, you may choose whether or not you want to review the mappings. 
{:.list}

* If you __Review__ a table, you can view and edit mappings of datatypes, column names and keys.
* If you __Finalize__ a table, you accept the proposed mappings without reviewing them.

To help you decide, Cazena will flag tables that appear to have conversion issues.

__To select tables from your source database:__
{:.list}

1. Enter a text string to search for tables whose names contain the string, then click __Search__.
2. From the search results, select tables that you want to move:
    * Use the checkboxes to select multiple tables to either __Review__ or __Finalize__.
    * You may also select __Review__ or __Finalize__ for individual tables using the dropdown menu in the Action column.

    The three columns on the right indicate whether there are conversion issue. For more information, hover over the numbers in the three columns on the right. 
    
    Your selection (__Review__ or __Finalize__) for each table will appear in the __Actions__ column. The total number of selections will also appear in the __Your Selection__ box on the right side of the screen.

3. Click __Continue__.
 
![ Select Tables ](assets/documentation/data_movement/select_tables.png "Select Tables")


Step 3: Review and Finalize Table Definitions
{:.step}

Next, review the table definitions for tables that you have selected for review. Table definitions consist of:
{:.list}

* Table names
* Column names
* Datatypes
* Keys (optional; MPP SQL only)

The __Review__ page lists all of the tables that you have selected. 
{:.list}

* Tables that you have selected for review are listed in the left column.
* The table currently under review appears in the middle of the page. 
* Tables that are ready to be finalized appear in the right column. If you are following the example, the two tables that you elected to finalize without review will appear here.

__Note:__ You may skip this page altogether if, on the previous page, you chose to finalize all selected tables without reviewing them.
{:.note}


![ Review Table Definition ](assets/documentation/data_movement/review_table_def_ent.png "Review Table Definition")

__Review the table definition:__
{:.list}
1. Review the table name, column names and datatype conversions for each page. 
1. If your table supports keys, select the __Keys__ tab to review or add keys to your table definition.
1. To accept the table definition for the table under review, click __Approve__.

    ![ Enter Keys](assets/documentation/data_movement/keys.png "Enter Keys")
    {:.width-75}

4. After you have reviewed all table definitions, click __Finalize Tables__ on the right side of the screen. This will move all of your approved table definitions to the datacloud.

![ Finalize Table](assets/documentation/data_movement/finalize_button.png "Finalize Table ")


Step 4: Move Data (Optional)
{:.step}

After you finalize tables, the table definition will be moved to the destination service. At this point, no data will have been moved to those tables. This allows you to schedule and run a data movement at a different time. 

If you like, you can move data on the next page.
{:.list}

* To specify a __WHERE__ clause for a table, click  __Add a Filter__.   
* To move the first 100 rows of data, select the checkbox in the __Move a Sample__ column.  

To move data, click __Move Tables__.
 
![Move All Tables](assets/documentation/data_movement/move_tables.png "Move tables Tables")

You can also generate a script for recurring transfers. For more information, see the section on [generating scripts for recurring data movements](#script_transfers).


If you want to check on the progress of your data movement, see the section on [data movement progress](#data_movement_progress).

### From FTP/SFTP Servers {#import_ftp}

You may import data from an FTP or SFTP server that is located either within the enterprise, or on the internet.

Before You Begin
{:.step}
{:.list}
* You must have a [data store](#data_stores) configured that contains the information needed to connect to the FTP/SFTP server.
* Data that you import from an FTP or SFTP server must be in the DSV (Delimeter Separated Values) format. For details about DSV format rules, see the section that describes [ Delimiter Separated Values (DSV) Files ](#dmg_dsv_files).

Step 1: Select Source and Destination 
{:.step}
{:.list}

1. From the __Datacloud__ tab, click the __Move Data__ button.
1. Under __Source__, select __Data Store__, then the data store where the source data is located.
1. Under __Destination__, select __Cazena Service__, then select the data lake or data mart and dataset where you want to import data.
1. Click __Continue__.


![ Select FTP/SFTP Source/Destination ](assets/documentation/data_movement/ftp_source_destination.png "Select FTP/SFTP Source/Destination")
{:.image-no-outline}

Step 2: Search for Files on the FTP/SFTP Server 
{:.step}

__Note__: Files to be imported must be in DSV format in order to be imported into a cloud service.  For details about DSV format rules, see: [ Supported Format for Delimiter Separated Values (DSV) Files ](#dmg_dsv_files).
{:.note}

1. In the search box, enter a regular expression to search for files on the FTP/SFTP server.  
1. Review your search results. Cazena will use the first file in the results to create a table definition. If you need to, you can enter a different regular expression to revise your search results.
1. Click __Create Table Definition__.

![ Search FTP/SFTP ](assets/documentation/data_movement/ftp_search.png "Search FTP/SFTP")


Step 3: Review Table Definition 
{:.step}

1. Select the delimiters (e.g., comma, tab, etc) and whether the file has a header row.
1. Click __OK__. A list of columns in the file will appear.
1. To reload the file with different parameters (e.g., delimiters), make changes and then click __OK__ again.
1. Give the table a name and review the table definition (column names and datatypes).  
1. Click __Finalize__ to move the table definition to the cloud.

![ Review table definition ](assets/documentation/data_movement/ftp_review_table_definition.png "Review table definition")

Step 4: Move Data (Optional) 
{:.step}

Finalizing the file will move the table definition to the cloud. On the next screen, you may select files to move into the table that you have created.

![ Move data ](assets/documentation/data_movement/ftp_import_move_data.png "Move data")



If you want to check on the progress of your data movement, see the section on [data movement progress](#data_movement_progress).


### From Your Local File System {#console_import_local_file}

Data that you import from your local file system server must be in the DSV (Delimeter Separated Values) format. For details about DSV format rules, see the section that describes [__Delimiter Separated Values (DSV) Files__](#dmg_dsv_files).


Step 1: Identify Source and Destination
{:.step}

1. From the __Datacloud__ tab, click the __Move Data__ button.
3. Under __Source__, select __Local File System__.
4. Under __Destination__, first select Cazena Service, then select the data lake/data mart and dataset that you want. If you want to create a new dataset, select __New__.
5. Click __Continue__.

![ Select Destination  ](assets/documentation/data_movement/local_source_destination.png "Select Destination ") 
{:.image-no-outline}

__Note__: The database used for all objects created in an MPP SQL service is __czdataset__. The __dataset__ name you enter here will become the schema name in the __czdataset__ database in the MPP SQL service.
   {:.note}

Step 2: Upload Data From Your Local File System
{:.step}

On the next screen, select the file that you want to upload.

![ Select Local File ](assets/documentation/data_movement/select_file.png "Select Local File")
{:.width-50}

After the file is uploaded, the parameters for the file will appear.
{:.list}  
1. Select the delimiters (e.g., comma, tab, etc) and whether the file has a header row.
1. Click __OK__. A list of columns in the file will appear.
1. To reload the file with different parameters (e.g., delimiters), make changes and then click __OK__ again.

![ Datacloud Tab, Select Local File ](assets/documentation/data_movement/local_parameters.png "Datacloud Tab, Select Local File")

Step 3: Review Datatypes and Column Names
{:.step}

Column names will be take from the header row in the source file, if you selected that option. Datatypes are assigned based on a sampling of the data. Where applicable, precision or length will also appear in the Datatype column.

Review the table definition:
{:.list}
1. Give the table a name.
1. Click on any column name to change it.
1. Review datatypes, precisions and lengths and make any changes that you desire.

![ Review Table Definition ](assets/documentation/data_movement/local_table_definition.png "Review Table Definition")

Step 4: Move Data (Optional)
{:.step}

After you have finalized the table definition, the table schema will be created in the destination data mart or data lake. No actual data will be loaded into the table at this point. This allows you to schedule and run data movements at a different time. For more information, see the section on [scripting transfers](#script_transfers).

In order to actually load data into the table, click __Move Files__. 

![ Move Data Definition Confirmation ](assets/documentation/data_movement/local_move_data.png "Move Data Definition Confirmation")

If you want to check on the progress of your data movement, see the section on [data movement progress](#data_movement_progress).



### Custom Data Adapters {#custom_data_adapter}

You may use a custom data adapter to import data from sources other than Netezza, Oracle, FTP/SFTP or local files. At a high level, custom data adapters work like this:
{:.list}
 * You or Cazena Support can write a program that will be installed on the Cazena gateway. The program must:
    * Connect to the desired data source.
    * Transform source data into [DSV-compatible format](#dsv_details) (if not already DSV-compatible), and then output it to `stdout`. Cazena will capture `stdout` and move it to the datacloud.
    * Additional requirements for the program are [described in more detail](#adapter_program_reqs) below. 
 * On the Cazena console, you then [create a data store](#custom_data_store) using the path to the program and any arguments that the program needs. 

* In the console, you will then [follow steps](#console_use_data_adapter) that are similar to moving data from FTP/SFTP, using the data store that references your program and its arguments. You will be able to to review column and table names, set datatypes, etc in the console.
    
#### Sample Code

There is a directory of sample custom adapters available on the Cazena gateway, in the directory `/home/cazena/custom-adapters`. Each adapter has a README file that describes the requirements for using that adapter.


If you use the sample adapters, __be sure that you copy them into a different directory__. If the Cazena gateway is updated, new samples may overwrite the samples in `/home/cazena/custom-adapters`.
{:.note}

##### Example: Move a File From an AWS Bucket to the Datacloud

1. The program <a href="assets/documents/s3_adapter.py" target="_blank">__s3_adapter.py__</a> is a simple Python program that moves a file, <a href="aseets/documents/bankemps.dsv" target="_blank">bankemps.dsv</a>, from an AWS S3 bucket onto the datacloud. 
1. <a href="assets/documents/s3_adapter.ini" target="_blank">__s3_adapter.ini__</a> contains arguments that are used in the program. Add your own credentials, etc to this file as described in the comments in that file.
1. If the programs are not already on a Cazena gateway, copy them onto a Cazena gateway. 
1. Make sure that the files’ permissions allow them to be read and executed, e.g., `chmod 755 <filename>`.
1. Test the program by running it in the command line from the Cazena gateway. Be sure to test the four commands that are described in the next section.
1. Set up a [data store](#custom_data_store) that contains the path to s3_adapter.py and s3_adapter.ini.

    ![ S3 sample data store](assets/documentation/data_movement/s3_sample_data_store.png "S3 sample data store")  

1. Follow the [steps](#console_use_data_adapter) for moving data using the Cazena console.


#### Program Requirements {#adapter_program_reqs}


Your program must meet these requirements:
{:.list}

* The program must return 0 on success.
* The program must return 1 on failure. 
* The program will be run with [arguments](#adapter_arguments) and one of four [options](#adapter_options). As you test your program in the command line, make sure that it supports the following commands:

`<your program> -pgm_args "<text from data store>" -version` ([see example](#example_version))

`<your program> -pgm_args "<text from data store>" -list`  ([see example](#example_list))

`<your program> -pgm_args "<text from data store>" -move <entity>`  ([see example](#example_move))

`<your program> -pgm_args "<text from data store>" -move <entity> -rows <number>`  ([see example](#example_move_number))

##### Arguments {#adapter_arguments}

The text in the __Arguments__ field of the data store will be passed in to your program via the `-pgm_args` option. You can use any type of argument that you want, including a file name (such as the sample code)or a list of options, such as `-text1 -text2`

__Note__: All text in the __Arguments__ field will be wrapped in double-quotes when your program is run. Don't put double-quotes in this field unless your program needs them around your argument string.
{:.note}

    

##### Options {#adapter_options}

Your program must support four options: `-version`, `-list`, `-move <entity>`, and `-rows <max_number>`

###### -version

This option outputs the API version that your program is using. Cazena will run this command to check for possible incompatibilities.
{:.list}
* The version must be equal to or less than the current API version.
* The format must be `<major>.<minor>`, e.g., `1.0`.
* As the time of writing this documentation, the API version is 1.0. 

###### __Example__: {#example_version}

Running your program with the `-version` option might look something like this:

    $ python s3_adapter.py -pgm_args "~/s3_adapter.ini" -version
    1.0


###### -list
This option must list all files/entities that the data adapter knows about. Cazena will run this option to test which entities are available.

The list must output the following information for each entity/file, with commas separating fields:

      <entity 1 name>, <size in bytes>, <last modified time in milliseconds since Epoch>
      <entity 2 name>, <size in bytes>, <last modified time in milliseconds since Epoch>
      <entity 3 name>, <size in bytes>, <last modified time in milliseconds since Epoch>
      
Cazena will read the standard output, assuming newlines at the end of each line, and stopping at EOF.



###### __Example__ {#example_list}
Running your program from the command line with the `-list` option from the command line might look something like this:

    $ python s3_adapter.py -pgm_args "~/s3_adapter.ini" -list
    
    bankemps.dsv, 464, 1472607957
    bankempsMore.dsv, 530, 1473444917
    nycflights.dsv, 343491, 1473444917
    titanic_training_data.dsv, 60316, 1473444918


##### -move  &lt;entity>

This option will start a data movement of the entity that comes from the `-list` output. 
{:.list}

* When you run your program with this option from the command line, it should output data that you want to move into `stdout`. 
* Data that your program outputs must be compatible with [DSV](#dsv_details) format. 
* A value for `<entity>` must be provided; no default value is assumed.

###### __Example__ {#example_move}

Running your program from the command line with the `-move <entity>` option might look something like this:

        $ python s3_adapter.py -pgm_args "~/s3_adapter.ini" -move bankemps.dsv
        
        1, Jones, Tom, 020345678, 1/1/1990, Branch Manager
        2, Smith, Harry, 254567891, 1/1/1992, Teller
        3, White, Ted, 254567896, 1/1/1994, Teller
        4, Gray, George, 254567901, 1/1/1996, Teller
        5, Taylor, Mary, 254567906, 1/1/1998, Assistant Branch Manager
        6, Evans, Bob, 254567911, 1/1/1980, Vice President
        7, Doe, John, 254567916, 1/1/1981, Marketing Specialist
        8, Doe, Jane, 254567921, 1/1/1982, Portfolio Manager
        9, Hardy, Helen, 254567926, 1/1/1983, Branch Manager
        10, Johnson, Leo, 254567931, 1/1/1984, Branch Manager
   

##### -rows  &lt;max_number>

This option is used in combination with `-move <entity>` to specify the maximum number of rows to extract. If no value is provided, all rows will be moved.

###### __Example__ {#example_move_number}

    $ python s3_adapter.py -pgm_args "~/s3_adapter.ini" -move bankemps.dsv -rows 2
    
    1, Jones, Tom, 020345678, 1/1/1990, Branch Manager
    2, Smith, Harry, 254567891, 1/1/1992, Teller


### Other Assumptions
* If the user stops the movement, a SIGTERM will be sent to the program.



### Using the custom data adapter from the Cazena console {#console_use_data_adapter}

Before you begin
{:.step}
  
1. Copy program files to the machine that is running the Cazena gateway. 
1. If your program assumes the existence of certain packages, libraries, etc in the environment, make sure that they are available on the machine that runs the Cazena gateway.
1. Make sure that the files' permissions allow them to be read and executed, e.g., `chmod 755 <filename>`.
1. Set up a [data store](#data_stores) that references the path to the file and any arguments.

Step 1: Select Source and Destination 
{:.step}
{:.list}

1. From the __Datacloud__ tab, click on the data lake or data mart where you want to move data.
1. Click __Move Data__.
1. Under __Source__, select __Data Store__, then the data store that refers to your program and arguments.
1. Under __Destination__, select __Cazena Service__, then select the service and dataset where you want to import data.
1. Click __Continue__.


![ Select Adapter Source/Destination ](assets/documentation/data_movement/adapter_source_destination.png "Select Source/Destination")
{:.image-no-outline}

Step 2: Search for Entities
{:.step}

1. In the search box, enter a regular expression to search for names of entities that you want to move.  
1. Review your search results. Cazena will use the first item in the results to create a table definition. If you need to, you can enter a different regular expression to revise your search results.
1. Click __Create Table Definition__.

![ Search for filenames ](assets/documentation/data_movement/adapter_search.png "Search for filenames")


Step 3: Review Table Definition 
{:.step}

1. Select the delimiters (e.g., comma, tab, etc) and whether the file has a header row.
1. Click __Apply Changes__. A list of columns in the file will appear.
1. To reload the file with different parameters (e.g., delimiters), make changes and then click __Apply Changes__ again.
1. Give the table a name and review the table definition (column names and datatypes).  
1. Click __Finalize__ to move the table definition to the cloud.

![ Review table definition ](assets/documentation/data_movement/adapter_review_table_definition.png "Review table definition")

Step 4: Move Data (optional) 
{:.step}

Finalizing the file will move the table definition to the cloud. On the next screen, you may select files to move into the table that you have created.

![ Move data ](assets/documentation/data_movement/adapter_move_data.png "Move data")


If you want to check on the progress of your data movement, see the section on [data movement progress](#data_movement_progress).



### Move Additional Data into a Table
 

#### From the Cazena Console

From the Cazena console, you can append or replace data in a table. 
{:.list}

1. Navigate to the table where you want to move additional data.
1. Click __Move More Data...__
1. The dialog that opens will depend on how the original table was set up.
  * If you set up the original table with a local file, the dialog will let you upload an additional file. It is assumed that the new file has the same table definition as the original table.
  * If you moved data from server, the dialog will be prepopulated with the information needed to connect to that server.
1. Select whether you want to append to existing data (__INSERT__) or replace data (__DELETE ALL__ followed by __INSERT__).  

![ Move More Data ](assets/documentation/data_movement/move_more_data.png "Move More Data")  
{:.image-no-outline}

#### Transfer Scripts {#script_transfers}

If you moved data from a server or a Cazena service, you can generate a script for recurring transfers. 
{:.list}

* A script enables you to monitor data movement activities as well as initiate them.
* Scripts can be run on a scheduled basis. For example, they can be integrated into your enterprise process scheduler.

The script will also allow you to check the status of data movement activity.

API scripts are available for any type of data movement that leverages a Cazena service, except for data movements from the local file system.

__To Generate an API Script:__
{:.list}

1. From the __Datacloud__ tab, click on the name of the data lake or data mart that was the source or destination for the desired movement.
2. Click the __Transfers__ tab. A list of transfers will appear on the left side of the screen.
3. You may use the search field to filter the list of transfers, e.g., to find a transfer that moved data into a particular table.
4. Select the transfer that you want to replicate, then select a gateway on the right side of the screen.
5. Click __Get API__. 

![ Dataset Transfer ](assets/documentation/transfers/transfer.png "Dataset Transfer")


__To use the script:__ 
{:.list}

1. Copy the script to a machine that has connectivity to a Cazena gateway.
1. Check that  the machine that runs the script has the '__curl__' utility installed on it. Note that __curl__ is standard on most operating systems. 
1. Change the permissions on the script file to be executable. 

<br>

__During a terminal session:__
{:.list}

* Use the `--help` argument to get help (e.g., `my_script.sh --help`)

{: .show-whitespaces .indent}


    $ ./nz_bankdemoTransfer.sh --help
       --new {operation} : To create a new job. Valid operations: append, replace
       --status {id} : View the stats of job with a given id
       --stop {id} : Stop the job with the given id permanently
       --test : Tests the connection to the console
       --help : View this message

* To append data to the table(s), use the `--new append` argument. This will initiate a new data movement job that will append data to the service table(s) using the same configuration as the original data movement.

{: .show-whitespaces .indent}

    $ ./nz_bankdemoTransfer.sh --new append
    
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                           a         Dload  Upload   Total   Spent    Left  Speed
    100  1032    0  1009  100    23    573     13  0:00:01  0:00:01 --:--:--   572   
    Successfully started job with id: 12


* To replace data in the table(s), use the `--new replace` argument.

{: .show-whitespaces .indent}

    $ ./nz_bankdemoTransfer.sh --new replace
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1034    0  1010  100    24    450     10  0:00:02  0:00:02 --:--:--   450
    Successfully started job with id: 14
 
 * To check the status of the job, use the argument use the argument `--status` with the `ID` that appears next to the message: `Successfully started job with id:`, such as `12` above. The complete argument would be `--status 12` 

{: .show-whitespaces .indent}

    $ ./nz_bankdemoTransfer.sh --status 12
    
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current Dload  Upload
                                                             Total   Spent    Left  Speed
        100  1020    0  1020    0     0  17591      0 --:--:-- --:--:-- --:--:-- 17894
        in progress




### Export Data from the Cloud {#console_export_ftp}

Step 1: Select Source and Destination
{:.step}


1. From the __Datacloud__ tab, click on the data lake or data mart where you want to move data.
1. Click __Move Data__.
1. Under __Source__, select __Cazena Service__, then select the service and dataset from which you want to export data.
1. Under __Destination__, select __Data Store__, then the data store for the FTP/SFTP server that you want. This 
1. Click __Continue__.

![ Select Source and Destination for FTP/SFTP ](assets/documentation/data_movement/export_source_destination.png "Select Source and Destination for FTP/SFTP")
{:.image-no-outline}

__Note__:  If you do not see the FTP/SFTP server that you want, be sure that your system administrator has configured a [data store](#data_stores) that contains the information needed to sign into the server.
{:.note}


Step 2: Select Tables To Be Exported 
{:.step}
On the next page, you will see a list of tables that can be exported.

1. Select the tables that you want to export (e.g., __customers__ and __employees__).
2. Click __Move Tables__.

![ Enterprise FTP/SFTP Move Data Selection ](assets/documentation/data_movement/ftp_export_move_data_selection.png "Enterprise FTP/SFTP Move Data Selection")

If you want to check on the progress of your data movement, see the section on [data movement progress](#data_movement_progress).
