from resources.serverconnections import ServerConnections


##### Run Operations
class Operations():
    def get_projects(base_url, session, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            url = f"{base_url}/rest/api/1.0/projects"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_project_default_permission(base_url, session, project_key):
        url = f"{base_url}/rest/api/1.0/projects/{project_key}/permissions/project-read/all"
        r = ServerConnections.get_api(session, url)
        if r.json()['permitted'] is True:
            url = f"{base_url}/rest/api/1.0/projects/{project_key}/permissions/project-write/all"
            if r.json()['permitted'] is True:
                permission = "write"
            else:
                permission = "read"
        else:
            permission = "noAccess"
        return permission

    def get_project_users(base_url, session, project_key, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            url = f"{base_url}/rest/api/1.0/projects/{project_key}/permissions/users"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_project_groups(base_url, session, project_key, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            url = f"{base_url}/rest/api/1.0/projects/{project_key}/permissions/groups"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_repos(base_url, session, project_key, personal, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            if personal is False:
                url = f"{base_url}/rest/api/1.0/projects/{project_key}/repos/"
            else:  # Personal project/repositories are stored under "~<user-slug>"
                url = f"{base_url}/rest/api/1.0/projects/~{project_key}/repos/"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_repo_users(base_url, session, project_key, personal, repo_slug, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            if personal is False:
                url = f"{base_url}/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/permissions/users"
            else:  # Personal project/repositories are stored under "~<user-slug>"
                url = f"{base_url}/rest/api/1.0/projects/~{project_key}/repos/{repo_slug}/permissions/users"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_repo_groups(base_url, session, project_key, personal, repo_slug, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            if personal is False:
                url = f"{base_url}/rest/api/1.0/projects/{project_key}/repos/{repo_slug}/permissions/groups"
            else:  # Personal project/repositories are stored under "~<user-slug>"
                url = f"{base_url}/rest/api/1.0/projects/~{project_key}/repos/{repo_slug}/permissions/groups"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_users(base_url, session, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            url = f"{base_url}/rest/api/1.0/users"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_groups(base_url, session, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            url = f"{base_url}/rest/api/1.0/admin/groups"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_group_members(base_url, session, group, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit, 'context': group}
            url = f"{base_url}/rest/api/1.0/admin/groups/more-members"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_global_group_permissions(base_url, session, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            url = f"{base_url}/rest/api/1.0/admin/permissions/groups"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']

    def get_global_user_permissions(base_url, session, paged_start=None, paged_limit=None):
        while True:
            params = {'start': paged_start, 'limit': paged_limit}
            url = f"{base_url}/rest/api/1.0/admin/permissions/users"
            r = ServerConnections.get_api(session, url, params)
            r_data = r.json()
            for json_result in r_data['values']:
                yield json_result
            if r_data['isLastPage'] is True:
                return
            paged_start = r_data['nextPageStart']
