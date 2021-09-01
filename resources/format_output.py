from prettytable import PrettyTable


class FormatOutput():
    def create_table_data(json_data):
        # Create table with given column headers
        table = PrettyTable(['Project (key)', 'Repository (slug)', 'Public', 'Groups', 'Users (slug)', 'Permission', 'Origin'])

        global_groups, global_users = FormatOutput.get_global_accounts(json_data['global'])

        for project in json_data['projects']:
            group, user, permission = FormatOutput.check_project_default_permission(project['defaultPermission'])
            table = FormatOutput.add_row(table, project=f"{project['name']} ({project['key']})", public=project['public'], permission=permission, group=group, user=user)

            for repo in project['repos']:
                table = FormatOutput.add_row(table, repo=f"{repo['name']} ({repo['slug']})", public=repo['public'])
                table = FormatOutput.add_global_rows(table, global_groups, global_users, json_data['groups'])

                if len(repo['groups']) > 0:
                    table = FormatOutput.add_row(table, group="[ REPO-GROUPS ]", user="---", permission="---", origin="---")
                for group in repo['groups']:
                    table = FormatOutput.add_row(table, group=group['name'], permission=group['permission'], origin="Explicit (Group)")
                    for user in FormatOutput.get_group_members(json_data['groups'], group['name']):
                        table = FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission=group['permission'], origin="Explicit (Group)")

                if len(project['groups']) > 0:
                    table = FormatOutput.add_row(table, group="[ PROJECT-GROUPS ]", user="---", permission="---", origin="---")
                for group in project['groups']:
                    table = FormatOutput.add_row(table, group=group['name'], permission=group['permission'], origin="Implicit (From Project)")
                    for user in FormatOutput.get_group_members(json_data['groups'], group['name']):
                        table = FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission=group['permission'], origin="Implicit (From Project)")

                if len(repo['users']) > 0:
                    table = FormatOutput.add_row(table, group="[ REPO-USERS ]", user="---", permission="---", origin="---")
                for user in repo['users']:
                    table = FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission=user['permission'], origin="Explicit (User)")

                if len(project['users']) > 0:
                    table = FormatOutput.add_row(table, group="[ PROJECT-USERS ]", user="---", permission="---", origin="---")
                for user in project['users']:
                    table = FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission=user['permission'], origin="Implicit (From Project)")

        for user in json_data['personal-projects']:
            if len(user['repos']) > 0:
                table = FormatOutput.add_row(table, project=f"~{user['slug']} ({user['displayName']})")
                for repo in user['repos']:
                    table = FormatOutput.add_row(table, repo=f"{repo['name']} ({repo['slug']})", public=repo['public'])
                    table = FormatOutput.add_global_rows(table, global_groups, global_users, json_data['groups'])

                    if len(repo['groups']) > 0:
                        table = FormatOutput.add_row(table, group="[ REPO-GROUPS ]", user="---", permission="---", origin="---")
                    for group in repo['groups']:
                        table = FormatOutput.add_row(table, group=group['name'], permission=group['permissions'], origin="Explicit (Group)")

                    table = FormatOutput.add_row(table, group="[ REPO-OWNER ]", user="---", permission="---", origin="---")
                    table = FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission="Admin", origin="Explicit (Repo Owner)")

                    if len(repo['users']) > 0:
                        table = FormatOutput.add_row(table, group="[ REPO-USERS ]", user="---", permission="---", origin="---")
                    for user in repo['users']:
                        table = FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission=user['permission'], origin="Explicit (User)")

        print("\n")
        print(table)
        with open("save-data.txt", 'w') as out_file:
            out_file.write(str(table))

    def get_global_accounts(global_mapping):
        # Find all Users/groups in an admin like capacity (They will have read/write/admin on all projects/repos)
        groups = []
        users = []
        for group in global_mapping['PROJECT_CREATE']['groups']:
            groups.append({'name': group['name'], 'permission': 'PROJECT_CREATE'})
        for group in global_mapping['ADMIN']['groups']:
            groups.append({'name': group['name'], 'permission': 'ADMIN'})
        for group in global_mapping['SYS_ADMIN']['groups']:
            groups.append({'name': group['name'], 'permission': 'SYS-ADMIN'})

        for user in global_mapping['PROJECT_CREATE']['users']:
            users.append({'displayName': user['displayName'], 'slug': user['slug'], 'permission': 'PROJECT_CREATE'})
        for user in global_mapping['ADMIN']['users']:
            users.append({'displayName': user['displayName'], 'slug': user['slug'], 'permission': 'ADMIN'})
        for user in global_mapping['SYS_ADMIN']['users']:
            users.append({'displayName': user['displayName'], 'slug': user['slug'], 'permission': 'SYS_ADMIN'})
        return groups, users

    def add_global_rows(table, global_groups, global_users, group_json):
        if len(global_groups) > 0:
            table = FormatOutput.add_row(table, group="[ GLOBAL-GROUPS ]", user="---", permission="---", origin="---")

        for group in global_groups:
            FormatOutput.add_row(table, group=group['name'], permission=group['permission'], origin="Implicit (Global Group)")
            for user in FormatOutput.get_group_members(group_json, group['name']):
                table = FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission=group['permission'], origin="Implicit (Global Group)")

        if len(global_users) > 0:
            table = FormatOutput.add_row(table, group="[ GLOBAL-USERS ]", user="---", permission="---", origin="---")
        for user in global_users:
            FormatOutput.add_row(table, user=f"{user['displayName']} ({user['slug']})", permission=user['permission'], origin="Implicit (Global User)")

        return table

    def check_project_default_permission(project_default_permission):
        if project_default_permission != "noAccess":
            group = "All Authenticated Groups"
            user = "All Authenticated Users"
            permission = project_default_permission
        else:
            group = ""
            user = ""
            permission = ""
        return group, user, permission

    def get_group_members(group_json, find_group):
        for group in group_json:
            if group['name'].lower() == find_group.lower():
                return group['members']

    def add_row(table, project="", repo="", public="", group="", user="", permission="", origin=""):
        table.add_row([project, repo, public, group, user, permission, origin])
        return table
