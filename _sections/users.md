
# Users and Groups {#users_and_groups}

Cazena support will create a system administrator account. The administrator will receive a welcome email that contains the IP address of the datacloud, a username and instructions for creating a password.

## Create User Accounts {#create_users}

For Port Forwarding Configurations
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
1. Select a [role](#user_roles) for the user, then click __Create__.

![ Users Tab ](assets/documentation/users/users_tab.png "Users Tab")  


The new user will be sent a welcome email with an initial password and instructions for connecting to the console.  

### User Roles {#user_roles}
For every service that is created, Cazena support will designate an owner, or superuser. The privileges and permissions given to the superuser will depend on the type of data lake or data mart. Contact support@cazena.com for details. 

Privileges for the different Cazena user roles are as follows:


| Feature             | System Admin                         | Application Support                  | Data Analyst                         |
|----------------------------|:------------------------------------:|:------------------------------------:|:------------------------------------:|
| View Cloud Sockets               | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| Manage Cloud Sockets         | <span class="icon-checkmark"></span> |      |      |
| Manage Users and Groups                   | <span class="icon-checkmark"></span> |      |      |
| View Cazena Gateways        | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> | <span class="icon-checkmark"></span> |
| Manage Cazena Gateways        | <span class="icon-checkmark"></span> |  |  |


## Create Groups

Cazena uses IPA authentication with Sentry for role-based authorization to data. You can create IPA groups in the Cazena console to help you manage access to data in a Cazena data lake. When you create and manage groups in the console, the groups will automatically be imported into Hue.

### Create Groups {#create_groups}
To create a group using the Cazena console:
{:.list}

1. Under the __Users__ tab, select the __Groups__ tab.
1. Click __New Group__.
1. Enter a name and short description for the group, then click __Save__.
1. After the group is created, the group will be selected on the left side of the screen. To add members, select the __Non_Members__ tab.


  ![ New Group ](assets/documentation/users/new_group.png "New Group")

5. Use the toggle switches to add new members to the group.

![ Add Users ](assets/documentation/users/add_users.png "Add Users")

