# 3rd party 
import typer
from loguru import logger 
from enum import Enum

from command_functions import initialize, check_project_id, project_exists, ascribe_resource, load_data, train, evaluate, monitor

app = typer.Typer()

class Command(Enum):
    INIT = "init"
    ASCRIBE = "ascribe"
    LOAD = "load"
    TRAIN = "train"
    EVAL = "eval"
    MONITOR = "monitor"


class InvalidIDError(Exception):
    '''Error for Invalid Project Identification.'''
    def __init__(self, message="Invalid ID"):
        super().__init__(message)

class DoesNotExistError(Exception):
    '''Error for '''
    def __init__(self, message="Project Does Not Exist"):
        super().__init__(message)


@app.command()
def ml(
    subcommand: Command,
    project_id: str, 
    api_key: str = typer.Option(None, "--key", "-k", help="Write API Key to .env file when initializing project."),
    url_resource: str = typer.Option(None, "--resource", "-r", help="Define a url to retrieve and load data from. (ascribe)")
    ):


    # Validate formatting of ID
    if not check_project_id(project_id):
        raise InvalidIDError
    
    # Ensure that commands for initialized projects already exists
    if subcommand != Command.INIT:
        if not project_exists(project_id):
            raise DoesNotExistError

    if subcommand == Command.INIT:
        logger.info(f"Initializing {project_id}...")
        initialize(project_id)

    if subcommand == Command.ASCRIBE:
        logger.info(f"Ascribing resources to {project_id}...")
        ascribe_resource(project_id, url_resource, api_key)

    if subcommand == Command.LOAD:
        logger.info(f"Loading data to {project_id}...")
        load_data(project_id)



if __name__ == "__main__":
    app()

