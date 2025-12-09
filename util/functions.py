from enum import Enum 


'''Enumeration types for distinguishing secondary arguments.'''

class Implementation(Enum):
    RETRIEVER = "retriever"
    PROCESSOR = "processor"
    MODEL = "model"

class RegressionMetrics(Enum):
    RMSE = "rmse"
    MAE = "mae"
    MSE = "mse"

class ClassificationMetrics(Enum):
    PRECISION = "precision"
    ACCURACY = "acc"
    RECALL = "recall"
    F1 = "f1"


'''Functions'''

def list_projects():
    pass

# argument: project_id
def delete_project(project_id: str):
    pass

# argument: project_id
# option: -p/--prediction (prompt user for input)
def init_project(project_id: str, prediction: str):
    pass 


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
def implement(command: Implementation, project_id: str, dependencies: list):
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