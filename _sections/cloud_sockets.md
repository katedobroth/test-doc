# Access the Datacloud Via Cloud Sockets {#integration_with_datacloud}

The  __Cloud Sockets__ tab displays the information needed to connect to various services exposed on the Cazena Gateway. You can use cloud sockets for [moving data](#move_data) as well as for connecting tools to the datacloud. 

This tab displays the status (Good Health, Warning, or Critical) of preconfigured services. Click on any service on the left side of the screen to view cloud socket connection details for that service.

![ RStudio Cloud Socket ](assets/documentation/cloud_sockets/sample_cloud_socket.png "RStudio Cloud Socket")



The details for a cloud socket contain two sections:
{:.list}

##### From outside the datacloud
 Use the URL on the right side to connect to a service (e.g., RStudio) from outside of the datacloud. This will establish a secure connection to the service through the Cazena Gateway. 


![ RStudio URL ](assets/documentation/cloud_sockets/rstudio_url.png "RStudio IP Address:Port")
{:.width-75}

<br/>
<br/>

##### From inside the datacloud
 Use __Internal IP:Port__ to connect to a service from an endpoint inside the datacloud. For example, once you had connected to RStudio, you could [connect to Hive via RJDBC](#hive) using __Internal IP:Port__.  (See the example below for details about [Hadoop Jars](#hadoop_jars).)

![ Hive Internal IP:Port ](assets/documentation/cloud_sockets/hive_ip_address.png "Hive Internal IP:Port")
{:.width-75}


In this section, we review examples of how to use cloud socket information for the following tools:
{:.list}

* [SparkR in RStudio Server](#rstudio)
* [Connect to Hive via RJDBC using RStudio](#hive)
* [SQL Workbench](#sql_workbench)

For examples of using cloud sockets for moving data, see the [Move Data](#move_data) section.

---
{:.end-section}

## Example: SparkR in RStudio Server {#rstudio}

Cazena data lakes include support for SparkR, an R package that provides a front end to use Apache Spark from R. Within a Cazena data lake, you can use SparkR from any R shell, including a Hue notebook or RStudio Server.



Step 1: Setup (Optional)
{:.step}

This example shows how you would use RStudio with a table that you move into a data lake. To follow the example, you would first use the Cazena console to move a file, <a href="assets/documents/nycflights.dsv" target="_blank">nycflights.dsv</a>, onto a data lake. 
{:.list}

* You can download the sample file here:  <a href="/documents/nycflights.dsv" target="_blank">nycflights.dsv</a>
* Follow the [instructions](#console_import_local_file) for moving data from a local file.
  * Name the dataset __db1__ and name the table __nycflights__. 
  * For __Text Delimiters__, select __Double Quote__, and select the checkbox for __First Row is Header__

![ Move Sample File ](assets/documentation/cloud_sockets/r_example.png "Move Sample File")
{:.image-no-outline}

Step 2: Connect to RStudio Server Through Your Browser:
{:.step}

1. Select the __Cloud Sockets__ tab.
1. On the left side of the screen, click on __RStudio Server__.
1. Click on the URL that appears on the right side of the screen. If your company has more than one Cazena gateway, you may see more than one link; you can use any of them.
1. RStudio will open in a new tab. Sign in using your Cazena credentials.

    ![ R Connection Details ](assets/documentation/cloud_sockets/rstudio_cloud_socket.png "R Connection Details")


Step 3: Run Sample Code
{:.step}

From the RStudio web client or a Hue notebook:

1. Load SparkR and the magrittr library.

        library(SparkR)
        library(magrittr)

 
1. Create a SparkContext

        sc <- SparkR::sparkR.init(master = "yarn-client")
  
1. Initialize the SQL context, which loads the required Hive libraries.

         hiveContext <- sparkRHive.init(sc)
         df <- table(hiveContext, 'db1.nycflights')
 
    __Note__: In this command, __db1__ corresponds to the name of your Cazena dataset. __nycflights__ corresponds to the name of the table that you want to load.
    {:.note}
    
1. View the first few rows of data, and print the schema of the data.

         showDF(df)
         printSchema(df)
 
1. Run some basic summary stats, and display the results.
 
       finaldf <- filter(df, df$distance > 1000) %>%
       group_by(df$dep_hour)%>%
       summarize(mean=mean(df$distance))
         arrange(finaldf, desc(finaldf$mean)) %>% head
 

1. Release the resources used for this session

       sparkR.stop()

---
{:.end-section}

## Example: Connect to Hive via RJDBC using RStudio {#hive}

#### Location of Hadoop JARs {#hadoop_jars}
{:.step}

In order to use Hive with RStudio, you will need to access Hadoop JARs. The JARs are located in the standard install locations that are used by Cloudera:

    HADOOP_HOME=/opt/cloudera/parcels/CDH/lib/hadoop

    HIVE_HOME=/opt/cloudera/parcels/CDH/lib/hive

__Note__: Cloudera's standard install locations are different from the locations used by open source Hadoop (`/usr/lib/hadoop/lib/` and `/usr/lib/hive/lib/`, respectively).
{:.note}

This example shows how you would set up RStudio to connect to Hive via RJDBC.

Step 1: Setup
{:.step}

1. On the __Cloud Sockets__ tab, select __RStudio Server__ on the left side of the screen.
1. Under __From outside the datacloud__, click on the  link under __IP Address:Port__.
1. RStudio will open in a new tab. Sign in using your Cazena credentials.

![ R Connection Details ](assets/documentation/cloud_sockets/rstudio_cloud_socket.png "R Connection Details")
{:.indent}

4. From RStudio, load the RJDBC library

        library(RJDBC)

5. Load the Hive driver.

        hd <- JDBC('org.apache.hive.jdbc.HiveDriver', '/opt/cloudera/parcels/CDH/lib/hive/lib/hive-jdbc.jar')

6. Add HADOOP_HOME and HIVE_HOME to the class path.

        for(l in list.files('/opt/cloudera/parcels/CDH/lib/hadoop/')){ .jaddClassPath(paste('/opt/cloudera/parcels/CDH/lib/hadoop/',l,sep=''))}
        
        
        for(l in list.files('/opt/cloudera/parcels/CDH/lib/hive/lib/')){ .jaddClassPath(paste('/opt/cloudera/parcels/CDH/lib/hive/lib/',l,sep=''))}

Step 2: Connect to Hive
{:.step}

        
1. On the __Cloud Sockets__ tab, select __Hive__ on the left side of the screen.
1. Under __From inside the datacloud__, use __Internal IP:Port__ .

![ Hive IP:Port ](assets/documentation/cloud_sockets/hive_cloud_socket.png "Hive IP:Port ")
{:.indent}

3. Connect to your database using this command:

        c <- dbConnect(hd,'jdbc:hive2://HIVE-IP-ADDRESS:PORT/DATABASE_NAME','USERNAME', 'PASSWORD')
    
    where:

    * __HIVE-IP-ADDRESS:PORT__ is the Hive IP address and port from the __Cloud Sockets__ tab.
    * __DATABASE_NAME__ is the name of the database or dataset. 
    * __USERNAME__ and __PASSWORD__ are your Cazena Credentials. 
        
    <br>
   
    For example:

          c <- dbConnect(hd,'jdbc:hive2://10.128.8.133:10000/cldftpds09222017145029530','my_username', 'my_password')

4. Use __dblistTables__ to see the tables in your dataset.


        dbListTables(c)

---
{:.end-section}

## Example: Use JDBC to connect to SQL Workbench {#sql_workbench}


On the __Cloud Sockets__ tab, you can find the information that you need to connect various third-party tools to databases that you have loaded into a data mart. In this example, we use SQL Workbench to query a database in a data mart.

* You can download SQL Workbench <a href="http://www.sql-workbench.net/downloads.html" target="_blank">here</a>.
* You will also need a postgreSQL JDBC driver, which you can download <a href="https://jdbc.postgresql.org/download.html" target="_blank">here</a>.

__From the Cazena console:__

1. From the __Cloud Sockets__ tab, select __MPP SQL__ on the left side of the screen.
1. Under __From inside the datacloud__, copy the __Internal IP:Port__ address and port.

![ MPP SQL ](assets/documentation/cloud_sockets/mpp_sql.png "MPP SQL")
{:.indent}


__From SQL Workbench:__
{:.list}

1. Start SQL Workbench, then select __File__ > __Connect Window__.
1. Select a PostgreSQL JDBC driver (download here)
1. Enter the URL:

    `jdbc:postgres://IP ADDRESS:PORT/czdataset`
    
    where:

    * IP ADDRESS:PORT comes from the Cloud Sockets tab.
    * Use __czdataset__ as the name of the database. 
    
1. Ask your system administrator for the username and password.

![ SQL Workbench ](assets/documentation/cloud_sockets/SQL_workbench.png "SQL Workbench")
{:.image-no-outline}


__Note:__ Data moved to a Cazena data mart goes into a database named __czdataset__. The schema name matches the name of the dataset used when moving data into the cloud.
{:.note}

---
{:.end-section}
