# Purpose:

Permission Audit script will generate a report of every repository in every project.

Currently the output is limited to a table format output to the screen as well as saved to a "save-data.txt" (in the 'pretty table' format) and "save-data.json" (in it's raw unparsed form).

# Support:

This is not an Atlassian product and is not entitled to full support from any level of Atlassian. Do not open cases at [https://getsupport.atlassian.com](https://getsupport.atlassian.com) for this script. We will work to move this repository to Bitbucket.org as soon as we can and will have a public issue tracker. There will be no SLAs for any type of response.

As with all new software and scripts we strongly encourage you to test in a non production enviornment. This script only makes read only requests but it can be very CPU intensive and we recommend running the script during non working hours or during a scheduled maintenance widow.

# Installation:

- To install the script clone it to the system that will run the script using

        git clone https://bitbucket.miwalker.net/scm/scripts/permission-audit.git

- Prepare the system to be able to run the script by installing the package requirements with pip3

        pip3 install -r requirements.txt

If you do not want to install the packages globally you can use Python's environment capabilities. To do this, before installing the requirements do the following in the scripts main directory:

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

- Run the script using Python 3.6+ (developed and tested with Python 3.7+)

        python3 audit.py

If you are using Python's environment, first make sure the environment is activated and then run

        python audit.py

# The configuration file

If you will be running the script regularly you might find it useful to use the configuration file.

There is a sample configuration file, env-template.py. If you want to use the configuration file instead of passing the options on the command line, copy this file to env.py and then make your changes to the env.py file. You can also just make your changes to env-template.py but if you need to pull the most recent changes to the script you will get errors from Git that pulling would cause you to lose data. If this happens you would need to revert any changes to env-template.py.

To use the configuration properly do the following (one time step)

- cp env-template.py env.py
- edit env.py in your favorite editor

If there are ever changes to env-template.py you would need to manually add those changes to your env.py file

# Feature Options

There are several command line switches that you can use:

- no command line options and no changes to env.py (or env-template.py), the script will prompt you for the Base URL, System Admin User Name, and System Admin User Password.

- options set in env.py (or env-template.py) will be used and will not be prompted at runtime. You can add some or all of the options in env.py

- passing options on the command line. You can pass any or all of the options for the script on the command line:

| Short | Full                    | Description                                                                                                                                                                                                                                                                                                      |
| ----- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| -b    | --base-url              | this is the base url that you access Bitbucket with. Include ports and context path if that is required in your instance                                                                                                                                                                                         |
| -t    | --token                 | to use an access token instead of a username and password                                                                                                                                                                                                                                                        |
| -u    | --username              | this is the username of a System Admin. You can use a Project or Repository Admin but then the results will be limited to only the projects or repositories that the user has access to                                                                                                                          |
| -p    | --password              | this is the passord for the username provided with the -u command line option, added to the env.py file, or entered at runtime. Please be aware that passwords entered as command line option will be visible on the screen and may show up in your bash history. Use caution when using this capability         |
| -r    | --personal-repositories | this will report on personal repositories as well as all of the other projects and repositories. Depending on how extensive your organization uses personal repositories this could dramatically increase the number of REST API calls that need to be made and the length of time the script takes to complete. |

## Note:

- Basic Auth is the default but if you use the "-t" flag it will prompt for your API Token instead of username/password

# Output:

Here is a basic example of the output

```
+---------------+-------------------+--------+--------------------+----------------------------+---------------+-------------------------+
| Project (key) | Repository (slug) | Public |       Groups       |        Users (slug)        |   Permission  |          Origin         |
+---------------+-------------------+--------+--------------------+----------------------------+---------------+-------------------------+
| Testing (TES) |                   | False  |                    |                            |               |                         |
|               | Testing (testing) | False  |                    |                            |               |                         |
|               |                   |        | [ GLOBAL-GROUPS ]  |            ---             |      ---      |           ---           |
|               |                   |        |    globaladmins    |                            |     ADMIN     | Implicit (Global Group) |
|               |                   |        |                    |       userc (userc)        |     ADMIN     | Implicit (Global Group) |
|               |                   |        |  [ GLOBAL-USERS ]  |            ---             |      ---      |           ---           |
|               |                   |        |                    | Admin (admin)              |     ADMIN     |  Implicit (Global User) |
|               |                   |        |  [ REPO-GROUPS ]   |            ---             |      ---      |           ---           |
|               |                   |        |     someusers      |                            |   REPO_READ   |     Explicit (Group)    |
|               |                   |        |                    |       user b (userb)       |   REPO_READ   |     Explicit (Group)    |
|               |                   |        |    stash-users     |                            |   REPO_READ   |     Explicit (Group)    |
|               |                   |        |                    | Admin (admin)              |   REPO_READ   |     Explicit (Group)    |
|               |                   |        |                    |        User (usera)        |   REPO_READ   |     Explicit (Group)    |
|               |                   |        |                    |       user b (userb)       |   REPO_READ   |     Explicit (Group)    |
|               |                   |        |                    |       userc (userc)        |   REPO_READ   |     Explicit (Group)    |
|               |                   |        | [ PROJECT-GROUPS ] |            ---             |      ---      |           ---           |
|               |                   |        |     someusers      |                            |  PROJECT_READ | Implicit (From Project) |
|               |                   |        |                    |       user b (userb)       |  PROJECT_READ | Implicit (From Project) |
|               |                   |        |   [ REPO-USERS ]   |            ---             |      ---      |           ---           |
|               |                   |        |                    | Admin (admin)              |   REPO_WRITE  |     Explicit (User)     |
|               |                   |        |                    |        User (usera)        |   REPO_ADMIN  |     Explicit (User)     |
|               |                   |        | [ PROJECT-USERS ]  |            ---             |      ---      |           ---           |
|               |                   |        |                    | Admin (admin)              | PROJECT_ADMIN | Implicit (From Project) |
|               |                   |        |                    |       user b (userb)       |  PROJECT_READ | Implicit (From Project) |
+---------------+-------------------+--------+--------------------+----------------------------+---------------+-------------------------+
```

# About running the script - Some thoughts

If you can, you should run this script during non working hours directly on the Bitbucket Server or one of the Bitbucket Data Center nodes while logged in as the user that runs the Bitbucket service.

This will eliminate all of the network latency. If you do run this locally you would want to use the base_url of http://localhost:7990 so that the request is localized to the node you are running on (note: http://localhost:7990 assumes that you are using the defaults, your instance may be different)

If you can't run the script directly on the server/node, because you can't install Python on the server or you can't install one or more of the required packages, then you can install this script on any workstation that can run Python and install all the packages but and that has access to your instance of Bitbucket, in this case you would need to use your actual base_url just like you use when accessing Bitbucket from the browser.

This script can be very CPU intensive for Bitbucket and the client that runs the script. That is why we recommend that you run it after hours.

The script can make hundreds, thousands, even 10's of thousands of REST API calls. If you have enabled Rate Limiting (see [Improving Instance Stability With Rate Limiting](https://confluence.atlassian.com/bitbucketserver/improving-instance-stability-with-rate-limiting-976171954.html) introduced in Bitbucket 6.6) then the number of requests this script makes could trip these limits and you would want to provide an exemption for the user that is used to run the scripts (see the documentation for this feature for more details). The script will still run to completion if Rate Limiting is enabled, but it will take much longer to complete.

# Support:
This script is being provided as is, without warranty or support.  You can use it as the base for your own script or you can use it as is, but you *MUST NOT* request support from Atlassian related to the use of (or failure to use) this script. We will not be able to make customizations for you if the script doesn't do everything that you need. 

The script was created during our own personal time and being donated for use by customers who are willing to accept these conditions.

