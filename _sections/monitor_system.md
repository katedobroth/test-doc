# Monitor Workloads and System Performance

The Cazena console provides tools for monitoring workloads, data movement progress, and system performance.



###### Service Status
{:.list}

* The [__Cloud Sockets__](#cloud_sockets_tab) tab shows the status of services (e.g., RStudio, Hue).

###### Data Movement Progress and Status of Workloads
{:.list}

* The [__Workloads__](#workloads_tab) tab displays information on individual jobs, which may include queries or data movements. 
  * Depending on the type of data movement, you may be able to view detailed information on the [progress of data movements](#data_movement_progress). 
  * You can [stop or cancel data movements](#cancel_workload) from the workloads tab.

###### Object Store
{:.list}

* Depending on the configuration of your environment, you can view information about your [ADLS](#adls) or [AWS](#aws_object_store) object store .


###### System Performance
{:.list}

* The front page of the [__Datacloud__](#datacloud_overview) tab shows high level metrics for the past hour, as well as statuses for each data lake and data mart.
* Within each data lake or data mart, the [__Dashboard__](#dashboard) tab provides an overview of performance over a period of time.

## Cloud Sockets {#cloud_sockets_tab}

The __Cloud Sockets__ tab shows the status (Good Health, Warning or Critical) of preconfigured services such as RStudio and Hue.

![ Service status on Cloud Sockets tab ](assets/documentation/monitor_system/service_status.png " Service status on Cloud Sockets tab")   

If you are connecting to a service via a [Cazena Gateway](#cgw_cazena_gateway), you can also look on the __System > Manage Gateways__ tab to see the status of a Cazena gateway port for the service that you want.
![ Cazena Gateway Port Status ](assets/documentation/cazena_gateway/czgw_manage_ports.png "Cazena Gateway Port Status")


## Dashboard {#dashboard}

1. From the __Datacloud__ tab, click on the name of the data lake or data mart that you want to monitor.
1. Select the __Dashboard__ tab.
1. By default, the __Dashboard__ tab shows charts for the past hour. You can select a different timeframe at the top of the screen. 


![  Dashboard ](assets/documentation/monitor_system/dashboard.png " Dashboard ")   

### Metrics for Data Lakes {#data_lake_metrics}

For data lakes, the dashboard displays graphs for these metrics over the selected timeframe:

* CPU usage
* Disk usage over the selected timeframe
* Memory usage
* Network received

### Metrics for Data Marts {#data_mart_metrics}

For data marts, the dashboard displays graphs for these metrics over the selected timeframe:

* CPU usage
* Disk usage
* Read and write throughput
    * This includes data going over the network to be imported to or exported from the cloud in a data movement operation as well as data being read from the cloud (For example:  by BI tools for analytic reporting or by an enterprise FTP/SFTP export request.
* Network received and transmitted
* Read and write latency
* Read and write IOPS
* Number of database connections
* Health status (healthy or unhealthy)
* Maintenance mode (off or on)

  
## Workload Status {#workloads_tab}

Within each data lake or data mart, the __Workloads__ tab provides details about the activity that has occurred within a given timeframe. By default, workloads for the past hour are displayed.


* You can select a different time frame in the upper right corner.
* Use the filter buttons at the top of the screen to filter the list by workload type (queries or data movements) or status (e.g., completed, failed, etc)  
  * __Queries__ might include SQL DML, SQL DDL as well as non SQL workloads.
  * __Data Movements__ includes background operations involved in the movement of data at various phases, such as compression of data or selecting sample data
* Use the text search fields to view only the records that contain a particular text string.
* To sort the table, click on any column header. 

![ Workload Filters ](assets/documentation/monitor_system/workload_filters.png "Workload Filters") 

## Data Movement Progress {#data_movement_progress}

Depending on the type of data movement, you may be able to view details on the progress of each table in a data movement. 

In this example, the workload list is filtered to show only data movements that are currently running. To see details about a particular data movement, click on the link in the PID column.

![ Data Movement Filters ](assets/documentation/monitor_system/data_movements.png "Data Movement Filters") 

Details on a selected data movement will contain a list of tables that are to be moved. Each table shows a status (e.g., Running, Complete, Pending). 

![ Data Movement Details ](assets/documentation/monitor_system/workload_details.png "Data Movement Details") 


Depending on the type of data movement, you may be able to see details about the progress of individual tables. If there is a chevron on the left side of a row, click the row to open it for more details.

![ Data Movement Table Progress ](assets/documentation/monitor_system/dm_table_progress.png "Data Movement Progress") 

You can also see performance metrics from the data movement's time of execution.
 
![ Data Movement Charts ](assets/documentation/monitor_system/dm_charts.png "Data Movement Charts") 

## Cancel Jobs {#cancel_workload}

To cancel any data movement job in progress:
{:.list}

1. Use the filter buttons at the top of the screen to select only __Active__ workloads.
1. Click the __Stop__ button, and then confirm the cancellation.

![ Cancel Task ](assets/documentation/monitor_system/cancel_task.png "Cancel Task")

After the job has been stopped it will appear in the list with the stopped icon: <span class="icon-stopped"></span>

__Note__: Workloads that do not have a task ID are background tasks. Although they can affect performance, they cannot be cancelled. You will only see the __Stop__ button for tasks that you are allowed to cancel.
{:.note}
