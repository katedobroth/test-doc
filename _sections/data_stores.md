# Data Stores {#data_stores}

__Note__: Users with System Administrator or Application Support privileges can create, edit or delete data stores.
{:.note}

Data stores contain the information that are used to connect to repositories of data that reside outside the Cazena datacloud.
{:.list}

* Data stores con connect to [Netezza](#netezza_data_store), [Oracle](#oracle_data_store), [enterprise FTP/SFTP](#ent_ftp_data_store), and [internet FTP/SFTP servers](#int_ftp_data_store).  
* For Netezza or Oracle, a data store can be viewed as being equivalent to a JDBC data source. It contains the connection information not only to the DBMS server, but also to the specific database, and optionally the schema within the database. 
* __Local File System__ is a preconfigured data store used for moving files from your local file system (e.g., your desktop or a remote drive).


This table shows which types of data stores can be used to import or export data from the datacloud.

Connector         |  Import to the Cloud | Export from the Cloud   
:---------------- |  :------------------ | :----------------------   
Oracle            |  <span class="icon-checkmark"></span>             | 
Netezza           |  <span class="icon-checkmark"></span>             | 
Enterprise FTP/SFTP    |  <span class="icon-checkmark"></span>             | <span class="icon-checkmark"></span>                 
Internet FTP/SFTP      |  <span class="icon-checkmark"></span>             | <span class="icon-checkmark"></span>             
Custom Data Adapter      |  <span class="icon-checkmark"></span>             |                  
Local File System |  <span class="icon-checkmark"></span>             |

__Note__:  Moving data between two Cazena services does not require a data store.
{:.note}

__To create a data store:__

1. From the __System__ tab, select __Data Stores__. 
1. To create a data store, click __New Data Store__. (To edit an existing data store, click the pencil icon (<span class="icon-edit"></span>) on the right edge of the row.)<br><br>
  ![ Data Stores ](assets/documentation/data_stores/data_stores.png "Data Stores")

1. Complete the form that appears. Refer to the sections below for more information about the type of data store that you are creating: 
    * [Oracle](#oracle_data_store)
    * [Netezza](#netezza_data_store)
    * [Enterprise FTP/SFTP](#ent_ftp_data_store)
    * [Internet FTP/SFTP](#int_ftp_data_store)
    * [Custom Data Store](#custom_data_store)

## Oracle Data Store {#oracle_data_store}

You can connect to either a database (SID) or a service.<br><br>The user must have the following permissions: <br><br> __CREATE SESSION__ for the database instance <br><br> __SELECT__ on any tables are to be imported           |  <img src="assets/documentation/data_stores/oracle_data_store.png">
{:.table-image}


## Netezza Data Store {#netezza_data_store}

The user must have the following permissions:  <br><br>__LIST__ on the database <br><br>__SELECT__ on any tables that are to be imported<br><br> __CREATE EXTERNAL TABLE__ privilege           |  <img src="assets/documentation/data_stores/netezza_data_store.png">
{:.table-image}


## Enterprise FTP/SFTP Data Store {#ent_ftp_data_store}

### For Exporting Data

__Cazena Gateway__: Select any gateway other than __INTERNET__ <br><br> __Connector__: Select either FTP or SFTP <br><br> __Path__: Provide a path to a directory relative to the home directory, e.g., `home/_my_username/banktest`.<br><br> The directory must exist and the user must have read/write access.<br><br>Exported data will go into a directory that is named `<dataset>/<YYYYMMDD_**T**HHMISS-MSEC/<table>/<datafile>` <br><br>Files are exported as they are stored on the system. This means that there may be multiple files exported for a single table. <br><br> Exported files are in DSV file format.           |  <img src="assets/documentation/data_stores/ftp_export_data_store.png">
{:.table-image}


### For Importing Data
* Provide a complete string to the directory where the files are located. 
* The user must have read access to the directory. Write access is not required.




## Internet FTP/SFTP Data Store {#int_ftp_data_store}

__Cazena Gateway__: Select  __INTERNET__ <br><br> __Connector__: Select either FTP or SFTP <br><br> __Path__: the directory path at the FTP host<br><br>__Host__: the name or IP of the public FTP/SFTP site. Be sure to exclude `"http://"`.<br><br>__Username__: If the site supports public access, this might be `anonymous`.|  <img src="assets/documentation/data_stores/internet_data_store.png">
{:.table-image}


## Custom Data Store {#custom_data_store}

__Cazena Gateway__: Select  the Cazena gateway that you want to use <br><br> __Connector__: select __Custom Data Adapter__<br><br>__Program__: the path to your program file on the Cazena gateway.<br><br>__Arguments__: Argument to be passed to your program <br><br>__Note__: All text in the __Arguments__ field will be wrapped in double-quotes when used by Cazena. Don't put double-quotes in this field unless your program needs them around your argument string.|  <img src="assets/documentation/data_stores/adapter_data_store.png">
{:.table-image}


