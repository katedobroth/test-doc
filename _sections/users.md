
# Users and Groups {#users_and_groups}

When Cazena creates your Cazena datacloud, Cazena support will create a system administrator account. The administrator will receive a welcome email that contains the IP address of the datacloud, a username and instructions for creating a password.

## Create User Accounts {#create_users}

Before You Start
{:.step}

If your site is using a [port forwarding](#port-forwarding-cgw) configuration, you must have a Cazena gateway running before you can create new user accounts. In addition, the Cazena console must be enabled on that gateway:
{:.list}

1. Select __System__ > __Manage Gateways__. 
1. On the left side of the screen, select __Cazena Datacloud__ under any running gateway.
1. On the right side of the screen, be sure that __Cazena Console__ is active and that the status icon is green, indicating that the port is up .

  ![ Enable Cazena Console ](assets/documentation/users/enable_cazena_console.png "Enable Cazena Console")  

To add a new user:
{:.step}

1. From the __Users__ tab,  click __New User__.
1. Enter the username and email address for the user.
1. Select a [role](#user_roles) for the user, and click __Create__.

![ Users Tab ](assets/documentation/users/users_tab.png "Users Tab")  


The new user will be sent a welcome email with an initial password and instructions for connecting to the console.  

### User Roles {#user_roles}
For every service that is created, Cazena support will designate an owner, or superuser. The privileges and permissions given to the superuser will depend on the type of data lake or data mart. Contact support@cazena.com for details. 

Privileges for the different Cazena user roles are as follows:


| Feature             | System Admin                         | Application Support                  | Data Analyst                         |
|----------------------------|:------------------------------------:|:------------------------------------:|:------------------------------------:|
| Service Page               | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| Transfers                  | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| Move Data                  | <span class="icon-checkmark"></span> |    | |
| Modify Datasets            | <span class="icon-checkmark"></span> |      |      |
| Add User                   | <span class="icon-checkmark"></span> |      |      |
| Delete User                | <span class="icon-checkmark"></span> |      |      |
| Modify User                | <span class="icon-checkmark"></span> |      |      |
| Dashboard Page             | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| Workloads Page             | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| System Page                | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| Edit Cloud Sockets         | <span class="icon-checkmark"></span> |      |      |
| View Cloud Sockets         | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| Create/Edit Data Store     | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |      |
| Delete Data Store          | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |      |
| Access to Admin Tools Menu | <span class="icon-checkmark"></span> |      |      | 
| Access to Log Server Console | <span class="icon-checkmark"></span> |      |      |



## Using Groups to Control Access to Data

Cazena uses IPA authentication with Sentry for role-based authorization to data. You can create IPA groups in the Cazena console to help you manage access to data in a Cazena data lake. At a high level, the steps are as follows:

1.	First, create [create_users](#users) and [groups](#create_groups) in the Cazena console.
1.	Next, [import Cazena groups into Hue](#import_groups_into_hue). By importing groups into Hue, you can ensure that groups and roles will persist across the entire data lake. Persistence cannot be assured with groups that are created directly in Hue.
3.	Use the Hue interface to manage data access for the imported groups.

This section will review the how to create groups in the Cazena console and then import them into Hue.

### Create Groups {#create_groups}
To create a group using the Cazena console:
{:.list}

1. In the __Users__ tab, select the __Groups__ tab.
1. Click __New Group__.
1. Enter a name and short description for the group.
1. Select members for the group. You may have to scroll in the list to see all users in your organization.
1. Click __Save__.

![ Create Group ](assets/documentation/users/create_group.png "Create Group")  


### Import Groups into Hue {#import_groups_into_hue}

#### Sign into Hue

1. Under __Cloud Sockets__, select __Hue Server__ on the left side of the screen.
1. The right side of the screen will show connection details for Hue. Click on the link under __IP Address:Port__.
1. Sign into Hue using the same credentials that you use for the Cazena console.

![ Hue Connection Details ](assets/documentation/users/hue_connection_details.png "Hue Connection Details")

#### After you have signed into Hue:

1. Go to the Hue User Admin page. Consult the Hue documentation for more details.

  __Note:__  You must be a Hue superuser to access the User Admin page. If you cannot access the page, contact support@cazena.com.
  {:.note}
  
2. Select the __Groups__ tab, then __Add/Sync LDAP group__.

  ![ Add LDAP Users ](assets/documentation/users/hue_add_groups.png "Add LDAP Users")  

2. Type in the name of the groups you created in the Cazena console. 
3. Select __Import new members__.
4. Click __Add/Sync Group__.

  ![ Hue Group Options ](assets/documentation/users/create_hue_group.png "Hue Group Options")

__Note__: If you add additional users to this group from the Cazena console, you will have to repeat this process for those users to be added to the Hue group.
{:.note}