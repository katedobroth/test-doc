# Object Store {#object_store}

Depending on the configuration of your environment, data may be stored on Microsoft [ADLS](#adls_object_store) or [AWS](#aws_object_store) object storage.

## ADLS {#adls_object_store}

You may be able to link to two pages in [Azure Monitor](#azure_monitor) from the Cazena console.
{:.list}

* The ADLS Data Explorer allows you to browse through your ADLS directory.


* The ADLS Metrics Overview displays metrics such as data storage utilization, read/write requests, and ingress/egress.

You may also view [ADLS account information](#adls_account_information) including IDs and instance names in the Cazena console.

### Link to Azure Monitor from the Cazena console {#azure_monitor}

You must initiate sessions with Azure Monitor by linking from the Cazena console.

1. From the __Cloud Sockets__ tab, select either __ADLS Metrics Overview__ or __ADLS Data Explorer__ on the left side.

1. Links to the Metrics Overview and Data Explorer will appear on the right side of the screen.

1. Sign in to ADLS as the [Customer Access User](#adls_user). If you see a message in ADLS that tells you that you don't have access to the Metrics Overview, check that you are signed in as the Customer Access User, and not into your own Microsoft account.

    ![ ADLS Cloud Socket ](assets/documentation/monitor_system/adls_cloud_socket.png " ADLS Cloud Socket")


__Note__:  At the top of the ADLS Metrics Overview, there is a link labeled __Data Explorer__. The link leads to an inaccessible directory. Use the links provided in the Cazena console to link to the data explorer.
    ![ ADLS Data Explorer ](assets/documentation/monitor_system/adls_metrics_data_link.png " ADLS Data Explorer")
{:.note .indent}

### View ADLS IDs and Instance Name {#adls_account_information}

To view variables such as tenant ID, client ID and ADLS Instance name, select the __System__ tab, then __ADLS__. Links to ADLS Metrics Overview and ADLS Data Explorer are also available on this page.

![ ADLS Account Information ](assets/documentation/data_movement/adls_account_info.png " ADLS Account Information")

See the section on [Moving Data to ADLS Using WebHDFS](#adls_webhdfs) for an example of how to use these variables.

## AWS S3 {#aws_object_store}

From the Cazena console, you may link to the AWS bucket and [view keys and tokens](#aws_account_information) that can be used to access the bucket.

### Link to AWS bucket from the Cazena console

To link to the S3 bucket:

1. From the __Cloud Sockets__ tab, select __AWS Console Login__ on the left side of the screen.

1. A link to the AWS bucket will appear on the right side. Sessions that you initial from this link will expire after 12 hours.

    ![ AWS Console Login ](assets/documentation/object_store/aws_login_link.png "AWS Console Login")

### View AWS Keys and Token {#aws_account_information}

To view the bucket name, AWS access key, secret access key and session token, select the __System__ tab, then __S3__. The AWS login link is also available on this page.

  ![ AWS Keys and Token ](assets/documentation/object_store/s3_variables.png "AWS Keys and Token ")

__Note__: Keys and tokens will expire after 12 hours.
{:.note}