from .operations import Operations
import concurrent.futures

thread_executor = concurrent.futures.ThreadPoolExecutor()


class Audit():
    def get_group_details(base_url, session, group):
        group_data = {'name': group['name'], 'members': []}
        for user in Operations.get_group_members(base_url, session, group['name']):
            group_data['members'].append({'displayName': user['displayName'], 'slug': user['slug'], 'id': user['id']})
        return group_data

    def get_repo_details(base_url, session, project_key, personal, repo):
        repo_data = {'name': repo['name'], 'slug': repo['slug'], 'public': repo['public'], 'groups': [], 'users': []}
        for repo_group in Operations.get_repo_groups(base_url, session, project_key, personal, repo['slug']):
            repo_data['groups'].append({'name': repo_group['group']['name'], 'permission': repo_group['permission']})
        for repo_user in Operations.get_repo_users(base_url, session, project_key, personal, repo['slug']):
            repo_data['users'].append({'displayName': repo_user['user']['displayName'], 'slug': repo_user['user']['slug'],
                                       'id': repo_user['user']['id'], 'permission': repo_user['permission']})
        return repo_data

    def audit_globals(base_url, session):
        global_permissions = {'LICENSED_USER': {'groups': [], 'users': []},
                              'PROJECT_CREATE': {'groups': [], 'users': []},
                              'ADMIN': {'groups': [], 'users': []},
                              'SYS_ADMIN': {'groups': [], 'users': []}
                              }

        # Global Permissions
        for group in Operations.get_global_group_permissions(base_url, session):
            global_permissions[group['permission']]['groups'].append({'name': group['group']['name']})
        for user in Operations.get_global_user_permissions(base_url, session):
            global_permissions[user['permission']]['users'].append({'displayName': user['user']['displayName'], 'slug': user['user']['slug'], 'id': user['user']['id']})

        return ["GLOBAL", global_permissions]

    def audit_groups(base_url, session):
        group_tasks = []
        group_data = []

        for group in Operations.get_groups(base_url, session):
            group_tasks.append(thread_executor.submit(Audit.get_group_details, base_url, session, group))

        for result in concurrent.futures.as_completed(group_tasks):
            group_data.append(result.result())

        return ["GROUP", group_data]

    def audit_projects(base_url, session):
        all_projects = []
        project_counter = 0
        repo_counter = 0

        for project in Operations.get_projects(base_url, session):
            personal = False
            project_counter += 1

            project_default_permission = Operations.get_project_default_permission(base_url, session, project['key'])

            project_data = {'name': project['name'], 'key': project['key'], 'public': project['public'], 'defaultPermission': project_default_permission, 'groups': [], 'users': [], 'repos': []}
            for project_group in Operations.get_project_groups(base_url, session, project['key']):
                project_data['groups'].append({'name': project_group['group']['name'], 'permission': project_group['permission']})
            for project_user in Operations.get_project_users(base_url, session, project['key']):
                project_data['users'].append({'displayName': project_user['user']['displayName'], 'slug': project_user['user']['slug'],
                                              'id': project_user['user']['id'], 'permission': project_user['permission']})

            for repo in Operations.get_repos(base_url, session, project['key'], personal):
                repo_counter += 1
    #            repo_tasks.append(executor.submit(get_repo_details, base_url, session, project['key'], personal, repo))
                repo_data = Audit.get_repo_details(base_url, session, project['key'], personal, repo)
                project_data['repos'].append(repo_data)

    #        for repo in concurrent.futures.as_completed(repo_tasks):
    #            project_data['repos'].append(repo.result())

            all_projects.append(project_data)
        return ["PROJECT", all_projects, project_counter, repo_counter]

    def audit_personal_repos(base_url, session):
        personal = True
        personal_projects = []
        user_counter = 0
        repo_counter = 0

        for user in Operations.get_users(base_url, session):
            user_counter += 1

            user_project_data = {'displayName': user['displayName'], 'slug': user['slug'], 'id': user['id'], 'repos': []}
            for repo in Operations.get_repos(base_url, session, user['slug'], personal):
                repo_counter += 1
#                personal_tasks.append(executor.submit(get_repo_details, base_url, session, user['slug'], personal, repo))
                personal_repo_data = Audit.get_repo_details(base_url, session, user['slug'], personal, repo)
                user_project_data['repos'].append(personal_repo_data)

#            for repo in concurrent.futures.as_completed(personal_tasks):
#                user_project_data['repos'].append(repo.result())

            personal_projects.append(user_project_data)
        return ["PERSONAL", personal_projects, user_counter, repo_counter]
