# Connect to the Datacloud Via Cloud Sockets {#cloud_sockets}

The  __Cloud Sockets__ tab displays the URLs, hostnames and ports needed to connect to various services exposed on the Cazena Gateway. This tab also displays the status (Good Health, Warning, or Critical) of preconfigured services. Click on any service on the left side of the screen to view connection details for that service.


In this section, we review examples of how to use cloud sockets to make the following kinds of connections:
{:.list}

* [Kafka and Zookeeper](#kafka_strings)
* [Connect to Hive or Impala with the RStudio Connections Pane](#rstudio_connection_pane)
* [Connect to Hive or Impala via RJDBC using RStudio](#rjdbc)
* [Connect to Hive using beeline](#beeline)
* [Connect to Impala using the Impala shell](#impala_shell)
* [SparkR in RStudio Server](#sparkr)
* [SQL Workbench](#sql_workbench)

For examples of using cloud sockets for moving data, see the [Move Data](#move_data) section.


## Kafka and Zookeeper {#kafka_strings}

Depending on the Cazena configuration at your site, you may have access to a Kafka cluster.

* This type of cluster requires a [site-to-site configuration](#cgw_cazena_gateway) for the Cazena gateway.
* Endpoints are TLS and require Kerberos authentication.

### Step 1: Kerberos setup
{:.step}

1. The Kafka service is Kerberos-enabled as well as TLS-enabled. You will need to obtain the appropriate credentials prior to any actions. The following is an example file that holds authentication details. In this example, the file is called `client.properties`.

<div class="code-wrapper">
<pre class="indent copy-area" id="client-properties">
sasl.kerberos.service.name = kafka
sasl.mechanism = GSSAPI
security.protocol = SASL_SSL
sasl.jaas.config=com.sun.security.auth.module.Krb5LoginModule required \
        useTicketCache=true; 
</pre>
<button class="btn clipboard-btn" data-clipboard-target="#client-properties">Copy</button>
</div>

1. Obtain a Kerberos ticket. To do this interactively on the command line you can run `kinit <username>` and provide your password when prompted. 


### Step 2: Broker / Zookeeper strings
{:.step}

1. In the Cazena console, select the __Cloud Sockets__ tab.
1. On the left side of the screen, select one of the Kafka cloud sockets:
    * __Kafka Broker__ for producers or consumers
    * __Kafka Zookeeper__ for topics
    ![ Kafka Strings ](assets/documentation/cloud_sockets/kafka_strings.png "Kafka Strings")
1. Use the strings on the right side of the screen to create commands as follows:

##### Producer
{:.indent}

<div class="code-wrapper">
<pre class="indent copy-area" id="kafka-producer-string">kafka-console-producer --broker-list <span style="color:red">BoostrapBrokerString</span> --topic <span style="color:red">yourtopic</span> --producer.config <span style="color:red">client.properties</span>
</pre>
<button class="btn clipboard-btn" data-clipboard-target="#kafka-producer-string">Copy</button>
</div>

  * Replace __BootstrapBrokerString__ with the string copied from the Kafka Broker cloud socket page.
  * Replace __client.properties__ with the name of the file that you created in step 1.
  * Replace __yourtopic__ with your kafka topic. 
  {:.indent}

##### Consumer
{:.indent}


<div class="code-wrapper">
<pre class="indent copy-area" id="kafka-consumer-string">kafka-console-consumer --bootstrap-server <span style="color:red">BoostrapBrokerString</span> --topic <span style="color:red">yourtopic</span> --from-beginning --consumer.config <span style="color:red">client.properties</span>
</pre>
<button class="btn clipboard-btn" data-clipboard-target="#kafka-consumer-string">Copy</button>
</div>

  * Replace __BootstrapBrokerString__ with the string copied from the Kafka Broker cloud socket page.
  * Replace __client.properties__ with the name of the file that you created in step 1.
  * Replace __yourtopic__ with your kafka topic. 

  {:.indent}


##### Topic
{:.indent}


<div class="code-wrapper">
<pre class="indent copy-area" id="kafka-topic-string">kafka-topics --create --zookeeper <span style="color:red">ZookeeperConnectString</span> --replication-factor 1 --partitions 1 --topic <span style="color:red">yourtopic</span> 
</pre>
<button class="btn clipboard-btn" data-clipboard-target="#kafka-topic-string">Copy</button>
</div>

  * Replace __ZookeeperConnectString__ with the string copied from the Kafka Zookeeper cloud socket page.
  * Replace __yourtopic__ with your kafka topic. 
  {:.indent}

---
{:.end-section}

## Oozie {#oozie_email}

#### Email service
Oozie workflows allow email actions to inform users of workflow status. To optimize the delivery of these emails, please supply Cazena support with:
  * The details of your enterprise SMTP service
  * A __From:__ email address. This allows status emails to originate with a known email address, so that emails are not filtered to spam folders.

If the Enterprise SMTP is not used, then the Cazena service will default to a built-in SMTP service. This component is not designed for high volumes of email, and can therefore cannot guarantee delivery of large number of messages.

## Connect to Hive or Impala With the RStudio Connections Pane {#rstudio_connection_pane}

In this section, we review how to connect to Hive or Impala using the RStudio Connections Pane. We use Hive in this example; however, you can follow similar steps to connect to Impala.

### Step 1: Connect to the RStudio web interface {#connect_to_rstudio}
{:.step}


1. Select the __Cloud Sockets__ tab.
1. On the left side of the screen, click on __RStudio Server__. You may use the text filter at the top of the list to help you find the service.
1. Click on the URL that appears on the right side of the screen. Depending on the configuration at your site, there may be more than one link; you can use any of them.
1. RStudio will open in a new tab. Sign in using your Cazena credentials.

    ![ R Connection Details ](assets/documentation/cloud_sockets/rstudio_cloud_socket.png "R Connection Details")

1. In RStudio, open the Connections Pane by selecting the __Connections__ tab, then __New Connection__.

    ![ RStudio Connection Pane ](assets/documentation/cloud_sockets/rstudio_connection_pane.png "RStudio Connection Pane")
    {:.width-50}

1. Scroll down and select __Hive__ (or Impala) from the options.

Step 2: Add the Hostname and Port to the Connection Pane
{:.step}

1. In the Cazena console, on the __Cloud Sockets__ tab, select __Hive__ (or Impala) on the left side of the screen. 
1. Copy the DNS address and port from the top of of the screen, then paste them into the Connection Pane in RStudio.
1. Add `,SSL=1` to the connection string, before the final parentheses.


![ Hive Connection ](assets/documentation/cloud_sockets/hive_connection.png "Hive Connection")


---
{:.end-section}


## Connect to Hive or Impala via RJDBC using RStudio {#rjdbc}

In this section, we review how to connect to Hive or Impala via RJDBC. We use Hive in this example; however, you can follow similar steps to connect to Impala.

#### Location of Hadoop JARs {#hadoop_jars}
{:.step}

In order to use Hive with RStudio, you will need to access Hadoop JARs. The JARs are located in the standard install locations that are used by Cloudera:

    HADOOP_HOME=/opt/cloudera/parcels/CDH/lib/hadoop

    HIVE_HOME=/opt/cloudera/parcels/CDH/lib/hive

__Note__: Cloudera's standard install locations are different from the locations used by open source Hadoop (`/usr/lib/hadoop/lib/` and `/usr/lib/hive/lib/`, respectively).
{:.note}

This example shows how you would set up RStudio to connect to Hive via RJDBC.

### Step 1: Set up the Hive environment in RStudio 
{:.step}

1. Follow the instructions for [connecting to the RStudio web interface through your browser](#connect_to_rstudio).

1. From RStudio, load the RJDBC library.

    ```
    > library(RJDBC)
    ```

1. Load the Hive driver.

    ```
    > hd <- JDBC('org.apache.hive.jdbc.HiveDriver', '/opt/cloudera/parcels/CDH/lib/hive/lib/hive-jdbc.jar')
    ```
    
1. Add HADOOP_HOME and HIVE_HOME to the class path.

    ```
    > for(l in list.files('/opt/cloudera/parcels/CDH/lib/hadoop/')){ .jaddClassPath(paste('/opt/cloudera/parcels/CDH/lib/hadoop/',l,sep=''))}
    
    
    > for(l in list.files('/opt/cloudera/parcels/CDH/lib/hive/lib/')){ .jaddClassPath(paste('/opt/cloudera/parcels/CDH/lib/hive/lib/',l,sep=''))}
        
    ```

### Step 2: Get the Hive host address and port from the Cazena console {#hive_cloud_socket}
{:.step}
        
1. On the __Cloud Sockets__ tab, select __Hive__ on the left side of the screen.
1. Under __From inside the datacloud__, copy the DNS address and port.

    ![ Hive IP:Port ](assets/documentation/cloud_sockets/hive_cloud_socket.png "Hive IP:Port ")
    {:.indent}

3. Connect to your database using the Hive (or Impala) hostname and port in this command:

    ```
    jdbc:hive2://<HIVE-HOST>:<HIVE-PORT>/<DATABASE>;ssl=true 
    ```
    
    For example:
    ```
    > c <- dbConnect(hd,'jdbc:hive2://hive-ai2ywz3kliv408jx.pvt.qa0930aws1.cazena-sqa.com:10000/my_database; ssl=true;','my_username', 'my_password') 
    
    ```


---
{:.end-section}

## Connect to Hive using beeline {#beeline}

1. Follow the instructions to find the [Hive host address and port](#hive_cloud_socket) from the Cazena console.

1. Copy the host and port into the following string:

    ```
    !connect jdbc:hive2://<HIVE-HOST>:<HIVE-PORT>/<DATABASE>;ssl=true
    ```
    
    For example:
    ```
    beeline> !connect jdbc:hive2://hive-ysewsr7iqy8qm6eb.qa0213aws2.pvt.cazena-sqa.com:10000/my_database;ssl=true 
    ```
    {:.indent}
    
---
{:.end-section}

## Connect to Impala using the Impala Shell {#impala_shell}

Step 1: Copy the Hostname and Port for Impala
{:.step}

1. On the __Cloud Sockets__ tab, select __Impala__ on the left side of the screen.
1. Under __From inside the datacloud__, copy the DNS address and port.

    ![ Impala Cloud Socket ](assets/documentation/cloud_sockets/impala_cloud_socket.png "Impala Cloud Socket ")
    {:.indent}

Step 2: Connect to the Impala Shell
{:.step}


Paste the DNS address and port into the following command:
```
impala-shell -i <IMPALA-HOST>:<IMPALA-PORT> -–ssl
```

For example:
```
impala-shell -i impala.5631b377b0cc20e.pvt.cazena-sqa.com:21050 --ssl
```

## SparkR in RStudio Server {#sparkr}

Within a Cazena data lake, you can use SparkR from any R shell, including a Hue notebook or RStudio Server.



Step 1: Connect to RStudio Server Through Your Browser:
{:.step}

Follow the instructions to [connect to RStudio through your browser](#connect_to_rstudio).

Step 2: Run Sample Code
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
 

---
{:.end-section}

## Use JDBC to connect to SQL Workbench {#sql_workbench}

This example shows how to use SQL Workbench to query a database in a data mart.

* You can download SQL Workbench <a href="http://www.sql-workbench.net/downloads.html" target="_blank">here</a>.
* You will also need a postgreSQL JDBC driver, which you can download <a href="https://jdbc.postgresql.org/download.html" target="_blank">here</a>.

Step 1: Copy the IP Address and Port for MPP SQL
{:.step}

1. In the Cazena console: From the __Cloud Sockets__ tab, select __MPP SQL__ on the left side of the screen.
1. Under __From inside the datacloud__, copy the __Internal IP:Port__ address and port.

![ MPP SQL ](assets/documentation/cloud_sockets/mpp_sql.png "MPP SQL")
{:.indent}


Step 1: Paste the IP Address and Port into SQL Workbench
{:.step}

1. Start SQL Workbench, then select __File__ > __Connect Window__.
1. Select a PostgreSQL JDBC driver (download here)
1. Enter the URL:

    `jdbc:postgres://IP ADDRESS:PORT/czdataset`
    
    where:

    * IP ADDRESS:PORT comes from the Cloud Sockets tab.
    * If you moved data using the Cazena console, use __czdataset__ as the name of the database. 
    
1. Ask your system administrator for the username and password.

![ SQL Workbench ](assets/documentation/cloud_sockets/SQL_workbench.png "SQL Workbench")
{:.image-no-outline}


__Note:__ Data moved to a Cazena data mart goes into a database named __czdataset__. The schema name matches the name of the dataset used when moving data into the cloud.
{:.note}

---
{:.end-section}
