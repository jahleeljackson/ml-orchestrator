import click
from loguru import logger 

from util.functions import list_projects, delete_project, init_project

models_list = ['lr', 'rfc', 'xgb', 'svc', 'svr', 'knn', 'nn', 'all']
metrics_list = ['rmse', 'mae', 'mse', 'acc', 'f1', 'recall', 'precision', ]

# Commands
@click.group()
def cli():
    '''haj is a machine learning workflow orchestrator for supervised learning algorithms \n
    haj simplifies the development, monitoring, and deployment of ML projects. '''
    pass 

@cli.command()
def list():
    """List existing projects."""
    list_projects()


@cli.command()
@click.argument("project_id")
def delete(project_id: str):
    """Delete specified project."""
    logger.info(f"Deleting {project_id}...")
    if delete_project(project_id):
        logger.info(f"{project_id} successfully deleted")



@cli.command()
@click.argument("project_id")
def init(project_id: str):
    """Initialize specified project."""

    logger.info(f"Initializing {project_id}...")
    logger.info(f"Prediction type defaulted to classification.\nUse config command to update prediction type")

    init_project(project_id)

    # handle logic here

    logger.info(f"{project_id} successfully initialized...")


@cli.command()
@click.argument("project_id")
@click.option("--dependencies", "-d", multiple=True, help="Add any number of dependencies to project.")
@click.option("--prediction", "-p", type=click.Choice(['regression', 'classification']), help="Update prediction type to project.")
@click.option("--title", "-t", help="Update project's title.")
def config(project_id: str, dependencies: tuple, prediction: str, title: str):
    """Set configurations for specified project."""


    if dependencies:
        print(dependencies)


    if title:
        print(title)

    # Handling cases
    if not dependencies and not prediction and not title:
        raise click.UsageError("At least one option must be passed to config command!")

    logger.info(f"Configuring {project_id}...")

    # handle logic

    logger.info("Configurations saved!")



@cli.command()
@click.argument("component", type=click.Choice(['retriever', 'processor', 'model']))
@click.argument("project_id")
@click.option("--dependencies", "-d", multiple=True, help="Add any number of dependencies to project.")
def impl(project_id: str, component: str, dependencies: tuple):
    """Implement specified project component."""
    

    if component == "retriever":
        print("retriever accessed")


    if component == "processor":
        print("processor accessed")

    if component == "model":
        print("model accessed")

    if dependencies:
        print(dependencies)

@cli.command()
@click.argument("project_id")
@click.option("--model", "-m", type=click.Choice(models_list), multiple=True, help="Run specified model")
def train(project_id: str, model: str = 'all'):
    """Train models for specified project (defaults to all)."""

    print(project_id)

    if model:
        print(model)
    

@cli.command()
@click.argument("metric", type=click.Choice(metrics_list))
@click.argument("project_id")
def evaluate(project_id: str, metric: str = 'acc'):
    """Evaluate models for specified project and metric."""

    print(project_id)
    print(metric)



@cli.command()
@click.argument("project_id")
def run(project_id: str):
    """Run model inference server with monitoring."""

    print(project_id)



@cli.command()
@click.argument("project_id")
def build(project_id: str):
    """Build and run Docker image."""

    print(project_id)



@cli.command()
@click.argument("project_id")
def deploy(project_id: str):
    """Deploy server on AWS."""

    print(project_id)



if __name__=="__main__":
    cli()