import os
from pathlib import Path
import click
import subprocess
from loguru import logger
from typing import List, Tuple

'''Functions'''

# Constants
FONT_COLOR = "magenta"
PROJECT_LIST_WIDTH= 30

def list_projects():
    # Get project path
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects"
    projects = os.listdir(project_dir)


    # Format projects
    click.echo(click.style(f"+{"-" * PROJECT_LIST_WIDTH}+", fg=FONT_COLOR))
    for project in sorted(projects):
        # Get ptype of project
        with open((project_dir + "/" + project + "/src/config.toml"), 'r') as project_config:
            ptype = project_config.readlines()[0].strip()
        click.echo(click.style(f"|{project}: {ptype.upper()}{" " * (PROJECT_LIST_WIDTH - (len(project) + len(ptype) + 1))}|", fg=FONT_COLOR))    
        click.echo(click.style(f"+{"-" * PROJECT_LIST_WIDTH}+", fg=FONT_COLOR))
    

# argument: project_id
def delete_project(project_id: str) -> bool:
    
    try:
        # Get project 
        script_dir = Path(__file__).parent
        target_dir = script_dir / "."
        project_dir = target_dir.__str__() + "/../ml_projects/"
        project = project_dir + project_id
        
        # Delete project
        subprocess.run(['rm', '-rf', project], check=True)
        return True

    except Exception as e:
        print(f"Error deleting {project_id}: ", e)



# argument: project_id
def init_project(project_id: str, ptype: str):
    try:
        # Get project 
        script_dir = Path(__file__).parent
        target_dir = script_dir / "."
        project_dir = target_dir.__str__() + "/../ml_projects/"
        
        if ptype == "c":
            template_dir = target_dir.__str__() + "/../templates/c_project_template"
        else:   
            template_dir = target_dir.__str__() + "/../templates/r_project_template"
            
        project = project_dir + project_id

        # Delete project
        subprocess.run(['cp', '-r', template_dir, project], check=True)

        create_venv(dir_name=project)

        add_dependency(dir_name=project, packages=("loguru", "httpx", "pandas", "pathlib"))


        return True

    except Exception as e:
        print(f"Error deleting {project_id}: ", e)
        return False


# argument: project_id
# option: -t/--title
# option: -p/--prediction (prompt user for input)
# option: -d/--dependencies
def config_project(project_id: str, dependencies: tuple, remove_dependencies: tuple, title: str, ):
    
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects/"
    project = project_dir + project_id

    new_title_dir = project_dir + title if title != None else None

    # Project title update functionality
    if title:
        subprocess.run(['mv', project, new_title_dir])
        logger.info(f"{project_id} title successfully changed to {title}")

    # Add dependencies
    if dependencies:
        add_dependency(dir_name=project, packages=dependencies)

    if remove_dependencies:
        remove_dependency(dir_name=project, packages=remove_dependencies)

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
        add_dependency(dir_name=project, packages=dependencies)

    if component == "retriever":
        file = project + "/src/data/retriever.py"
        subprocess.run(['vim', file], check=True)
    
    if component == "processor":
        file = project + "/src/data/processor.py"
        subprocess.run(['vim', file], check=True)
    
    


def load_data(project_id: str):
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects/"
    project = project_dir + project_id
    retriever_file = project + "/src/data/retriever.py"
    processor_file = project + "/src/data/processor.py" 

    try:
        subprocess.run(['python', retriever_file], check=True)
        subprocess.run(['python', processor_file], check=True)
        return True
    except:
        raise click.UsageError("Error loading data: Ensure you've correctly implemented the retriever and processors.")

def train_project(project_id: str,
                    model: str,
                    C_option: float,
                    nestimators: int,
                    maxdepth: int,
                    lrate: float,
                    kernel: str,
                    gamma: str,
                    neighbors: int,
                    weights: str,
                    epsilon: float) -> bool:
    
    # Get Project directory
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects/"
    project = project_dir + project_id


    # Get ptype of project
    with open((project + "/src/config.toml"), 'r') as project_config:
        ptype = project_config.readlines()[0].strip()
    

    if model == "all":
        if ptype == "classification":
            logger.info("Training all classification models.")
            subprocess.run(['python', (project + "/src/model_funcs/logistic_regression.py")], check=True)
            subprocess.run(['python', (project + "/src/model_funcs/kneighbors_classifier.py")], check=True)
            subprocess.run(['python', (project + "/src/model_funcs/random_forest_classifier.py")], check=True)
            subprocess.run(['python', (project + "/src/model_funcs/svc.py")], check=True)
            subprocess.run(['python', (project + "/src/model_funcs/xgb_classifier.py")], check=True)
        else:
            logger.info("Training all regression models.")
            subprocess.run(['python', (project + "/src/model_funcs/linear_regression.py")], check=True)
            subprocess.run(['python', (project + "/src/model_funcs/random_forest_regressor.py")], check=True)
            subprocess.run(['python', (project + "/src/model_funcs/svr.py")], check=True)
            subprocess.run(['python', (project + "/src/model_funcs/xgb_regressor.py")], check=True)


    # Models appropriate to prediction type
    classification_models = ['lgr', 'rfc', 'xgbc', 'svc', 'knn']
    regression_models = ['lnr', 'rfr', 'xgbr', 'svr']


    # Handle cases
    if model in classification_models and ptype != "classification":
        raise click.UsageError("Classification models can only be called on projects initialized as classification prediction type.")
    
    if model in regression_models and ptype != "regression":
        raise click.UsageError("Regression models can only be called on projects initialized as regression prediction type.")

    # Classifiers
    if model == "lgr":
        logger.info(f"Training Logistic Regression model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/logistic_regression.py")], check=True)
    if model == "rfc":
        logger.info(f"Training Random Forest Classifier model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/random_forest_classifier.py")], check=True)
    if model == "xgbc":
        logger.info(f"Training XGBoost Classifier model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/xgb_classifier.py")], check=True)
    if model == "svc":
        logger.info(f"Training SVClassifer model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/svc.py")], check=True)
    if model == "knn":
        logger.info(f"Training KNNeighbors Classifier model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/kneighbors_classifier.py")], check=True)
    
    # Regressors
    if model == "lnr":
        logger.info(f"Training Linear Regression model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/linear_regression.py")], check=True)
    if model == "rfr":
        logger.info(f"Training Random Forest Regression model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/random_forest_regressor.py")], check=True)
    if model == "xgbr":
        logger.info(f"Training XGBoost Regressor model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/xgb_regressor.py")], check=True)
    if model == "svr":
        logger.info(f"Training SVRegressor model for {project_id}.")
        subprocess.run(['python', (project + "/src/model_funcs/svr.py")], check=True)

    return True



# argument: project_id
# secondary argument: rmse
# secondary argument: mse
# secondary argument: acc
# secondary argument: f1
def evaluate_project(project_id: str, rmse: int = 0):
    pass


#------------------------------------------------------------------------------------------------------------------------
# Helpers

def _venv_python(dir_name: str) -> str:
    """Return the absolute path to the venv python interpreter."""
    return os.path.join(dir_name, "venv", "bin", "python")


def _venv_pip(dir_name: str) -> str:
    """Return the absolute path to the venv pip executable."""
    return os.path.join(dir_name, "venv", "bin", "pip")


def _check_project_exists(project_id: str) -> bool:
    script_dir = Path(__file__).parent
    target_dir = script_dir / "."
    project_dir = target_dir.__str__() + "/../ml_projects/"

    if project_id not in os.listdir(project_dir):
        return False 
    
    return True

# ---------------------------------------------------------------------
# CREATE VENV
# ---------------------------------------------------------------------

def create_venv(dir_name: str) -> None:
    """
    Create a virtual environment inside directory/venv.
    Does nothing if it already exists.
    """
    venv_path = os.path.join(dir_name, "venv")

    if os.path.exists(venv_path):
        print(f"Venv already exists at: {venv_path}")
        return

    subprocess.run(
        ["python3", "-m", "venv", venv_path],
        check=True
    )
    print(f"Created virtual environment at: {venv_path}")


# ---------------------------------------------------------------------
# ADD DEPENDENCY
# ---------------------------------------------------------------------

def add_dependency(dir_name: str, packages: tuple) -> None:
    """
    Install a package into the venv.
    Example: add_dependency("proj", "scikit-learn")
    """
    pip_path = _venv_pip(dir_name)
    for package in packages:
        subprocess.run([pip_path, "install", package], check=True)
        print(f"Installed {package} into {dir_name}/venv")



# ---------------------------------------------------------------------
# REMOVE DEPENDENCY
# ---------------------------------------------------------------------

def remove_dependency(dir_name: str, packages: tuple) -> None:
    """
    Uninstall a package from the venv.
    Example: remove_dependency("proj", "scikit-learn")
    """
    pip_path = _venv_pip(dir_name)
    for package in packages:
        subprocess.run([pip_path, "uninstall", "-y", package])
        print(f"Removed {package} from {dir_name}/venv")



