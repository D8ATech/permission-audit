from getpass import getpass
from optparse import OptionParser
from requests import Session
from .serverconnections import ServerConnections
try:
    import env
except ModuleNotFoundError:
    pass

class Init():
    def parse_args():
        parser = OptionParser()
        parser.add_option('-b', '--base-url', action='store', dest='base_url', default="", help="Base URL of your environment (Example: https://bitbucket.example.com), Expects following string")
        parser.add_option('-t', '--token', action='store', dest='token', default="", help="Use API token instead of username/password, Expects following string")
        parser.add_option('-u', '--username', action='store', dest='username', default="", help="Bitbucket admin username, Expects following string")
        parser.add_option('-p', '--password', action='store', dest='password', default="", help="Bitbucket admin password, Expects following string")
        parser.add_option('-r', '--personal-repositories', action='store_true', dest='personal_repos', default=False, help="Include personal repositories")
        options, args = parser.parse_args()
        if options.token != "" and (options.username != "" or options.password != ""):
            exit("A token and Username/Password were both provided. Please re-run the tool with only one or the other.")
        return options

    def get_creds(env_vars):
        session = Session()

        if env_vars.base_url == "":
            base_url = Init.get_base_url()
        else:
            base_url = env_vars.base_url

        # If no token flag is seen, default to using Username/Password
        if env_vars.token == "":

            if env_vars.username == "":
                admin_username = Init.get_username()
            else:
                admin_username = env_vars.username

            if env_vars.password == "":
                admin_password = Init.get_password()
            else:
                admin_password = env_vars.password

            session.auth = (admin_username, admin_password)

        # Use token instead of Username/password if it already exists in flag or env_vars
        else:
            token = env_vars.token
            session.headers = {'Authorization': "Bearer " + token}

        Init.confirm_creds(base_url, session)

        return base_url, session

    def get_base_url():
        base_url = input("Please enter the Source instance's Base URL (i.e. https://bitbucket.mycompany.com (Server)):\n")
        return base_url

    def get_username():
        username = input("Please enter the Admin username for your source environment:\n")
        return username

    def get_password():
        password = getpass("Please enter the Admin password for your source environment:\n")
        return password

    def confirm_creds(base_url, session):
        url = f"{base_url}/rest/api/1.0/admin/banner"
        r = ServerConnections.get_api(session, url)
        if r.status_code == 401:
            # Failed to Authenticate
            exit("Credentials provided do not meet the minimum requried permission or the credentials are invalid. Please confirm the credentials and try again.")
        elif r.status_code == 404:
            # Incorrect URL
            exit("The URL provided may not be correct. Please confirm that you enter the full 'Base URL' of your environment, including the context path (if used) and try again.")
        elif r.status_code in range(500, 504):
            exit("The Server appears busy or there was another error, please try again at another time.")
        elif r.status_code in [200, 204]:
            # Valid session and correct auth required
            return
        else:
            exit("Unknown Error, please confirm all provided information and ensure that the tool can reach Bitbucket via the URL provided.")


class InitEnv():
    def __init__(self, **kwargs):
        if kwargs['base_url']:
            self.base_url = kwargs['base_url']
        else:
            # The base URL of the instance you wish to interact with. e.g. "https://bitbucket.example.com"
            try:
                self.base_url = env.base_url
            except NameError:
                # No env.py file found, defaulting to empty string
                self.base_url = ""

        if kwargs['token']:
            self.token = kwargs['token']
        else:
            # The access token of an admin user, to be used instead of Username/Password  https://confluence.atlassian.com/bitbucketserver/personal-access-tokens-939515499.html
            # !!! If this string is not empty, the username/password entries will be ignored and this token will used instead. !!!
            try:
                self.token = env.token
            except NameError:
                # No env.py file found, defaulting to empty string
                self.token = ""

        if kwargs['username']:
            self.username = kwargs['username']
        else:
            # The username of an "System Admin" account from within Bitbucket  https://confluence.atlassian.com/bitbucketserver/global-permissions-776640369.html
            try:
                self.username = env.username
            except NameError:
                # No env.py file found, defaulting to empty string
                self.username = ""

        if kwargs['password']:
            self.password = kwargs['password']
        else:
            # The password matching the account of the above specified user
            try:
                self.password = env.password
            except NameError:
                # No env.py file found, defaulting to empty string
                self.password = ""
