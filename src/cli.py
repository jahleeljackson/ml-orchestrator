import click
from loguru import logger 

from util.functions import  _check_project_exists, list_projects, delete_project, init_project, config_project, implement, load_data, train_project

c_models_list = ['lgr', 'rfc', 'xgbc', 'svc', 'knn']
r_models_list = ['lnr', 'rfr', 'xgbr', 'svr']
metrics_list = ['mae', 'mse', 'r2', 'acc', 'f1', 'recall', 'precision']

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

    if not _check_project_exists(project_id):
        raise click.UsageError(f"{project_id} is not an existing project.")

    if delete_project(project_id):
            logger.info(f"{project_id} successfully deleted")



@cli.command()
@click.argument("ptype", type=click.Choice(["c", "r"]))
@click.argument("project_id")
def init(project_id: str, ptype: str):
    """Initialize specified project and prediction type."""


    if _check_project_exists(project_id):
        raise click.UsageError(f"{project_id} already exists.")

    logger.info(f"Initializing {project_id}...")
    logger.info(f"Prediction type set to {"classification" if ptype == "c" else "regression"}")

    if init_project(project_id=project_id, ptype=ptype):
        logger.info(f"{project_id} successfully initialized...")


@cli.command()
@click.argument("project_id")
@click.option("--dependencies", "-d", multiple=True, help="Add any number of dependencies to project.")
@click.option("--remove-dependencies", "-rd", "remove_dependencies", multiple=True, help="Remove dependencies from project.")
@click.option("--title", "-t", help="Update project's title.")
def config(project_id: str, dependencies: tuple = None, remove_dependencies: tuple = None, title: str = None):
    """Set configurations for specified project."""

    # Handling cases

    if not _check_project_exists(project_id):
        raise click.UsageError(f"{project_id} is not an existing project.")
    
    if not dependencies and not title and not remove_dependencies:
        raise click.UsageError("At least one option must be passed to config command!")

    
    logger.info(f"Configuring {project_id}...")

    if config_project(project_id=project_id, dependencies=dependencies, remove_dependencies=remove_dependencies, title=title):

        logger.info("Configurations saved!")



@cli.command()
@click.argument("component", type=click.Choice(['retriever', 'processor']))
@click.argument("project_id")
@click.option("--dependencies", "-d", multiple=True, help="Add any number of dependencies to project.")
def impl(project_id: str, component: str, dependencies: tuple):
    """Implement specified project component (via vim editor)."""
    
    # Handling cases
    if not _check_project_exists(project_id):
        raise click.UsageError(f"{project_id} is not an existing project.")

    implement(project_id, component, dependencies)


@cli.command()
@click.argument("project_id")
def load(project_id: str):
    """Load data for specified project (after implementing retriever and processor)."""

    # Handling cases
    if not _check_project_exists(project_id):
        raise click.UsageError(f"{project_id} is not an existing project.")
    
    logger.info(f"Loading data for {project_id}...")
    if load_data(project_id):
        logger.info(f"Data successfully loaded for {project_id}!")
    



@cli.command()
@click.argument("project_id")
@click.argument("model", type=click.Choice((c_models_list+r_models_list + ["all"])))
@click.option("-C", "C_option", type=float, help="Smaller values specify stronger regularization.")
@click.option("--nestimators", type=int, help="The number of trees in the forest.")
@click.option("--maxdepth", type=int, help="The maximum depth of the tree.")
@click.option("--lrate", type=float, help="Specify learning rate.")
@click.option("--kernel", "-k", type=click.Choice(["linear", "poly", "rbf", "sigmoid"]), help="Specifies the kernel type to be used in the algorithm.")
@click.option("--gamma", "-g", type=click.Choice(["scale", "auto"]), help="Kernel coefficient for 'rbf', 'poly' and 'sigmoid'.")
@click.option("--neighbors", "-n", type=int, help="Number of neighbors to use.")
@click.option("--weights", "-w", type=click.Choice(["uniform", "distance"]), help="Weight function used in prediction.")
@click.option("--epsilon", "-e", type=float, help="Epsilon in the epsilon-SVR model.")
def train(project_id: str, model: str,
            C_option: float,
            nestimators: int,
            maxdepth: int,
            lrate: float,
            kernel: str,
            gamma: str,
            neighbors: int,
            weights: str,
            epsilon: float
        ):
    """Train models for specified project."""


    # Handling cases
    if not _check_project_exists(project_id):
        raise click.UsageError(f"{project_id} is not an existing project.")
    if model == "all" and (C_option != None or  nestimators != None or maxdepth != None
                            or lrate != None or kernel != None or gamma != None or 
                            neighbors != None or weights != None or epsilon != None):
        raise click.UsageError("Parameters cannot be defined when training all models at once.")

    logger.info(f"Finding {"model" if model != "all" else "models"} for {project_id}...")

    if train_project(project_id=project_id, model=model,
                  C_option=C_option,
                  nestimators=nestimators,
                  maxdepth=maxdepth,
                  lrate=lrate,
                  kernel=kernel,
                  gamma=gamma,
                  neighbors=neighbors,
                  weights=weights,
                  epsilon=epsilon):
        logger.info(f"{"Model" if model != "all" else "Models"} successfully trained!")
    


    

@cli.command()
@click.argument("project_id")
@click.argument("metric", type=click.Choice(metrics_list))
def evaluate(project_id: str, metric: str):
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