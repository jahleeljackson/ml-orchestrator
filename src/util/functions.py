import os
from pathlib import Path
import click
import subprocess

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
            return False

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
        template_dir = target_dir.__str__() + "/../templates/c_project_template"
        project = project_dir + project_id

        # Delete project
        subprocess.run(['cp', '-r', template_dir, project], check=True)
        return True

    except Exception as e:
        print(f"Error deleting {project_id}: ", e)


# argument: project_id
# option: -t/--title
# option: -p/--prediction (prompt user for input)
# option: -d/--dependencies
def config_project(project_id: str, title: str, prediction: str, dependencies: list):
    pass

# argument: project_id
# secondary argument: retriever
# secondary argument: processor
# secondary argument: model
# option: -d/--dependencies
def implement(command: str, project_id: str):
    pass

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



if __name__=="__main__":
    init_project("foobar")