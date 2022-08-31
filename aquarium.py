from aquarium import Aquarium
from dotenv import load_dotenv
import os
import logging

def init_logger():
    '''
    Initialise logger with DEBUG level.
    '''
    logging.basicConfig()
    aq_logger = logging.getLogger("aquarium")
    aq_logger.propagate = True
    aq_logger.setLevel(logging.DEBUG)

def load_env_vars():
    '''
    Loads envs from the .env file
    '''
    env = {'AQ_USER' : '',
    'AQ_PASSWORD' : '',
    'SERVER' : ''}
    load_dotenv()
    env['AQ_USER'] = os.getenv('AQ_USER')
    env['AQ_PASSWORD'] = os.getenv('AQ_PASSWORD')
    env['SERVER'] = os.getenv('SERVER')

    return env

def connect(server):
    '''
    Connect to Aquarium server passed as arg.
    returns: an Aquarium() Object
    '''
    aq = Aquarium(server)
    return aq
    
def get_all_projects(aquarium):
    '''
    Queries and returns all projects in an Aquarium data base.
    '''
    return aquarium.project.get_all()

def get_user(user_key):
    '''
    Returns user object.
    '''
    user = aq.user(user_key)
    return user

def get_user_info(user_key):
    '''
    Returns user information.
    '''
    user = aq.user(user_key)
    return user.get()

def get_project(project_key):
    '''
    Return project object.
    '''
    return aq.project(project_key)

def get_project_info(project):
    '''
    Returns project info
    '''
    return project.get()

def get_as_item(aquarium, dict):
    '''
    Returns a traversable item for a given dict, a MeshQL query result.
    aq: Aquarium instance
    dict: data to return as item
    '''
    key = dict['item']['_key']
    item = aquarium.item(key)
    return item

def get_all_project_tasks(project_key):
    """
    Returns a list of tasks that are children of the given template project.
    """
    studio_template = aq.project(project_key)
    tasks = studio_template.traverse("# -()> item.type == 'Task'")
    task_group = studio_template.traverse("# -()> item.type == 'Group' AND item.data.name == 'Taches' UNIQUE")[0]
    task_group = get_as_item(aq, task_group)
    tasks.append(task_group.traverse("# -()> item.type == 'Task'"))

    return tasks

def get_project_task(project_key = None, project_name = None):
    '''
    Returns the task dedicated to the given project (ex: 'Heures_NomDuProjet')

    project_key = int
    project_name = string
    '''
    if project_key is None:
        if project_name is None:
            print('No key or name project given')
        else:
            selected_project = None
            projects = aq.project.get_all()
            for project in projects:
                if project.data.name == project_name:
                    selected_project = project
    else:
        selected_project = aq.project(project_key)
        selected_project = selected_project.get()


    tasks = selected_project.traverse("# -(2)> item.type == 'Task' UNIQUE")
    for task in tasks:
        task = get_as_item(aq, task)
        task = task.get()
        if selected_project.data.name in task.data.name:
            if 'production' not in task.data.tags:
                return task

def get_pipeline_task(aq):
    '''
    Convenience function for testing purposes.
    '''
    return aq.task(282726517)

def add_entry_hours_focus_view(aq):
    '''
    Adds an entry in the timelogs of the Aquarium Focus View
    '''
    task_done = aq.task(293883420)
    parent = task_done.traverse("# <(2)- item")
    job_data ={
    "duration": "PT2H",
    "name": "Work on Heures_Pipe",
    "performedAt": "2022-08-31T12:31:52.330Z",
    "performedBy": "282800450"
    }

    '''
    data information
    Duration: uses ISO 8601 to inform period
    date: ISO 8601 UniversalSortableDateTimePattern
    '''
    pipeline_task = get_pipeline_task(aq)

    pipeline_task.append(type='Job', data = job_data,  edge_type='Child')


    print(aq.query("# -(@Child)> item.type == 'Project' "))



if __name__ == '__main__':
    init_logger()
    env = load_env_vars()
    aq = connect( env['SERVER'])
    aq.connect(env['AQ_USER'], env['AQ_PASSWORD'])

    # TEST QUERIES
    # User Info
    print('USER INFO TEST QUERY: ')
    print(get_user_info(218422670))

    # All Projects
    print('ALL PROJECTS TEST QUERY: ')
    print(get_all_projects(aq))

    # Specific Project
    print('GET PROJECT TEST QUERY: ')
    project = get_project(282726465)
    print(get_project_info(project))

    # Get all task for a project:
    print('ALL PROJECT TASK TEST QUERY: ')
    print(get_all_project_tasks(282726465))

    # Get Task 'Gestion de Prod'
    print('GET SPECIFIC TAK TEST QUERY')
    template = aq.project(282723757)
    template_name = template.traverse("# -()> item.data.name")
    xx_others = template.traverse("# -(@Child)>  item.type == 'Group' AND item.data.name == 'xx_others' ")[0]
    xx_others = get_as_item(aq, xx_others)
    task = xx_others.traverse("# -($Child)> item.type == 'Task' AND item.data.name == 'gestion de prod' ")[0]
    task = get_as_item(aq, task)
    print(task.get())