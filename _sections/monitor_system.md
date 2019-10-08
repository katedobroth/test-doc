# Monitor System



## Cloud Sockets {#cloud_sockets_tab}

The __Cloud Sockets__ tab shows the status (Good Health, Warning or Critical) of preconfigured services such as RStudio and Hue.

![ Service status on Cloud Sockets tab ](assets/documentation/monitor_system/service_status.png " Service status on Cloud Sockets tab")   

If you are connecting to a service via a [Cazena Gateway](#cgw_cazena_gateway), you can also look on the __System > Manage Gateways__ tab to see the status of a Cazena gateway port for the service that you want.
![ Cazena Gateway Port Status ](assets/documentation/cazena_gateway/czgw_manage_ports.png "Cazena Gateway Port Status")


## Dashboard {#dashboard}

1. From the __Datacloud__ tab, click on the name of the data lake or data mart that you want to monitor.  

    Note that dashboard metrics are not available for Kafka clusters.
    {:.note}
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

