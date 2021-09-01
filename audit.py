from custom_functions import CustomFunctions
from resources.init import Init
from resources.init import InitEnv
from resources.auditing import Audit
from resources.format_output import FormatOutput
from json import dump
import concurrent.futures


process_executor = concurrent.futures.ProcessPoolExecutor()


def export_data(export_content):
    with open('save-data.json', 'w') as out_file:
        dump(export_content, out_file)


def main():
    options = Init.parse_args()
    env = InitEnv(base_url=options.base_url, token=options.token, username=options.username, password=options.password)
    base_url, session = Init.get_creds(env)

    project_counter = 0
    user_counter = 0
    repo_counter = 0
    personal_repo_counter = 0

    multi_process_tasks = []

    multi_process_tasks.append(process_executor.submit(Audit.audit_globals, base_url, session))
    multi_process_tasks.append(process_executor.submit(Audit.audit_groups, base_url, session))
    multi_process_tasks.append(process_executor.submit(Audit.audit_projects, base_url, session))
    if options.personal_repos is True:
        multi_process_tasks.append(process_executor.submit(Audit.audit_personal_repos, base_url, session))
    else:
        personal_data = []

    for task in concurrent.futures.as_completed(multi_process_tasks):
        if task.result()[0] == "GLOBAL":
            global_data = task.result()[1]
        elif task.result()[0] == "GROUP":
            group_data = task.result()[1]
        elif task.result()[0] == "PROJECT":
            project_data = task.result()[1]
            project_counter = task.result()[2]
            repo_counter = task.result()[3]
        elif task.result()[0] == "PERSONAL":
            personal_data = task.result()[1]
            user_counter = task.result()[2]
            personal_repo_counter = task.result()[3]

    all_repo_counter = repo_counter + personal_repo_counter

    all_data = {'global': global_data,
                'groups': group_data,
                'projects': project_data,
                'personal-projects': personal_data
                }

    FormatOutput.create_table_data(all_data)
    export_data(all_data)

    exit(f"\nAudited {all_repo_counter} Repositories across {project_counter} Projects and {user_counter} Users.\nDone.")


if __name__ == '__main__':
    main()
