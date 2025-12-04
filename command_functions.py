from loguru import logger 
import os 
import subprocess 
import toml

pwd = os.path.dirname(os.path.abspath(__file__))

# Load config
try:
    with open(f"{pwd}/pyproject.toml", "r") as f:
        global config
        config = toml.load(f)

except Exception as e:
    logger.error(f"Unable to load config: {e}")


# Constants
ML_PROJ_DIR = config['config']['ml_project_directory']

def initialize(project_id: str) -> None:
    '''Initializes a new machine learning project.
    
    Args:
        project_id (str): The name of project.
    
    Returns: 
        Result: A success or error object
    '''

    try:
        # Copy template python directory into {project_id}/ 
        shell_command = ['cp', '-r', 'python_template', f'{ML_PROJ_DIR}/{project_id}']
        subprocess.run(shell_command, check=True)
        logger.info(f"{project_id} successfully initialized!")
    except Exception as e:
        logger.error("Unable to initialize project! ", e)

    
def ascribe_resource(project_id: str, url_resource: str, api_key = None) -> None:
    try:
        #Write url resource to config
        if url_resource:
            with open(f"{pwd}/{ML_PROJ_DIR}/{project_id}/config.toml", "w") as config:
                config.write(f"url={url_resource}")
                logger.info(f"Resource added to {project_id}'s config.toml file...")

        # Write API key to .env file if provided
        if api_key:
            with open(f"{pwd}/{ML_PROJ_DIR}/{project_id}/.env", 'w') as env:
                env.write(f"API_KEY={api_key}") 
                logger.info(f"Key added to {project_id}'s .env file...")

        with open(f"{pwd}/{ML_PROJ_DIR}/{project_id}/data/retriever.py", 'a') as retriever:
            retriever.write(f"\n\npwd = '{pwd}/{ML_PROJ_DIR}/{project_id}'")

        logger.info(f"Resources successfully ascribed to {project_id}!")
    except Exception as e:
        logger.error(f"Unable to ascribe resource! {e}")



def load_data(project_id: str):
    try:
        shell_command = ['python3', f"{pwd}/{ML_PROJ_DIR}/{project_id}/data/retriever.py"]
        subprocess.run(shell_command, check=True)
    except Exception as e:
        error_msg = f"Make sure you've ascribed a resource and implemented {project_id}'s data/retriever.py method!"
        logger.error(f"Unable to load data from resource: {error_msg} \n{e}")


#TODO: Implement functions
def train(project_id: str) -> None:
    print(project_id)


def evaluate(project_id: str) -> None:
    print(project_id)


def monitor(project_id: str) -> None:
    print(project_id)


def check_project_id(project_id: str) -> bool:
    if " " in project_id:
        logger.error('" " characters not allowed in project_id')
        return False
    elif "," in project_id:
        logger.error('"," characters not allowed in project_id')
        return False
    elif "." in project_id:
        logger.error('"." characters not allowed in project_id')
        return False
    elif "!" in project_id:
        logger.error('"!" characters not allowed in project_id')
        return False
    elif "?" in project_id:
        logger.error('"?" characters not allowed in project_id')
        return False
    
    return True


def project_exists(project_id: str) -> bool:
        project_dir_path = f"{pwd}/{ML_PROJ_DIR}/"
        if project_id in os.listdir(project_dir_path):
            return True
        return False