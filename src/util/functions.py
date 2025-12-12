import os
from pathlib import Path
import click
import subprocess
from loguru import logger

'''Functions'''

# Constants
FONT_COLOR = "magenta"
PROJECT_LIST_WIDTH= 20

def list_projects():
    # Get project path
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects"
    projects = os.listdir(project_dir)

    # Format projects
    click.echo(click.style(f"+{"-" * PROJECT_LIST_WIDTH}+", fg=FONT_COLOR))
    for project in sorted(projects):
        click.echo(click.style(f"|{project}{" " * (PROJECT_LIST_WIDTH - len(project))}|", fg=FONT_COLOR))    
        click.echo(click.style(f"+{"-" * PROJECT_LIST_WIDTH}+", fg=FONT_COLOR))
    

# argument: project_id
def delete_project(project_id: str) -> bool:
    
    try:
        # Get project 
        script_dir = Path(__file__).parent
        target_dir = script_dir / "."
        project_dir = target_dir.__str__() + "/../ml_projects/"
        project = project_dir + project_id
        existing_projects = os.listdir(project_dir)


        # Check if project even exists
        if project_id not in existing_projects:
            raise click.UsageError(f"{project_id} is not a project.")

        # Delete project
        subprocess.run(['rm', '-rf', project], check=True)
        return True

    except Exception as e:
        print(f"Error deleting {project_id}: ", e)



# argument: project_id
def init_project(project_id: str):
    try:
        # Get project 
        script_dir = Path(__file__).parent
        target_dir = script_dir / "."
        project_dir = target_dir.__str__() + "/../ml_projects/"
        template_dir = target_dir.__str__() + "/../templates/project_template"
        project = project_dir + project_id

        # Delete project
        subprocess.run(['cp', '-r', template_dir, project], check=True)
        return True

    except Exception as e:
        print(f"Error deleting {project_id}: ", e)
        return False


# argument: project_id
# option: -t/--title
# option: -p/--prediction (prompt user for input)
# option: -d/--dependencies
def config_project(project_id: str, dependencies: tuple, prediction: str, title: str, ):
    
    # Project title update functionality
    if title:
        script_dir = Path(__file__).parent
        target_dir = script_dir / "."
        project_dir = target_dir.__str__() + "/../ml_projects/"
        new_title_dir = project_dir + title
        project = project_dir + project_id

        subprocess.run(['mv', project, new_title_dir])
        logger.info(f"{project_id} title successfully changed to {title}")

    if dependencies:
        add_dependencies(project_id=project_id, dependencies=dependencies)

    return True

# argument: project_id
# secondary argument: retriever
# secondary argument: processor
# secondary argument: model
# option: -d/--dependencies
def implement(project_id: str, component: str, dependencies: tuple):
    
    
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects/"
    project = project_dir + project_id


    if dependencies:
        add_dependencies(project_id=project_id, dependencies=dependencies)

    if component == "retriever":
        file = project + "/src/data/retriever.py"
        print(file)
        subprocess.run(['vim', file], check=True)
    
    if component == "processor":
        file = project + "/src/data/processor.py"
        subprocess.run(['vim', file], check=True)
    
    if component == "model":
        file = project + "/src/train.py"
        subprocess.run(['vim', file], check=True)


# argument: project_id
def train_project(project_id: str):
    pass

# argument: project_id
# secondary argument: rmse
# secondary argument: mse
# secondary argument: acc
# secondary argument: f1
def evaluate_project(project_id: str, rmse: int = 0):
    pass


#------------------------------------------------------------------------------------------------------------------------
# Helpers


def add_dependencies(project_id: str, dependencies: tuple):
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects/"
    project = project_dir + project_id
    
    # Script for activating venv
    venv_activate = project + "/.venv/bin/activate"

    formatted_dependencies = list(dependencies)

    print(venv_activate)
    print(formatted_dependencies)
    subprocess.run(['source', venv_activate], check=True)
    subprocess.run((['pip', 'install'] + formatted_dependencies), check=True)
    subprocess.run(['source', 'deactivate'], check=True)
    






if __name__=="__main__":
    # add_dependencies(project_id="foo", dependencies=("numpy", "pandas"))
    implement("foo", "retriever")