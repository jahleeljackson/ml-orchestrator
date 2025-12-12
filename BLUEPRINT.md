# Machine Learning Workflow Orchestrator (CLI Tool): Python


## Project Description 

I command line interface tool which can accomplish the following things:

    - List existing ML projects 
    - Initialize a ML project instance (generate a template directory)
    - Configure remote data resources (url->config.toml, api_key->.env)
    - Implement data retrieving script (opens vim terminal)
        Store data in file (.txt unless .csv or .json can be distinguished)
    - Implement data processing script (opens vim terminal)
    - Train either all available or specific models (specified via arguments)
        Store model, metrics, and metadata permanently (files or database)
    - Evaluate the best model
    - Start an inference server for monitoring 
    - Build and run a container for project
    - Deploy project on AWS

## Commands

```bash
haj list # list existing projects
```

```bash
haj delete (project)
```

```bash
haj init (project) -p/--prediction (prompt user for regression or classification model)
```

```bash
haj config (project) -t/--title (new title)
haj config (project) -p/--prediction # prompt user for regression or classification prediction types
haj config (project) -d/--dependencies # add desired dependencies
```

```bash
haj impl (project) retriever -d/--dependencies (dependencies to be installed) # open vim for foo/retriever.py
haj impl (project) processor -d/--dependencies (dependencies to be installed) # open vim for foo/processor.py
haj impl (project) model -d/--dependencies (dependencies to be installed) # open vim for foo/retriever.py
```

```bash
haj train (project) # train's models dependent on prediction type
haj train (project) -m/--model {}# train's models dependent on prediction type
```

```bash
haj evaluate (project) # "crowns" a champion model based on best performance metrics (default accuracy)
haj evaluate (project) rmse 
haj evaluate (project) mae 
haj evaluate (project) mse

haj evaluate (project) precision 
haj evaluate (project) acc 
haj evaluate (project) recall 
haj evaluate (project) f1 
```

```bash
haj run (project) # start fastapi inference server for monitoring 
# add these endpoints
# /health
# /metrics
# /predictions_count
# /latency

```

```bash
haj build (project) # create docker image and run server
```

```bash
haj deploy (project) # deploy on AWS
```


## Architecture 


```bash
haj list # list existing projects
```

- Iterate through ml_projects/ and print existing directories

```bash
haj delete (project)
```

- Check if project exists
- rm -rf on specified project


```bash
haj init (project) -p/--prediction (prompt user for regression or classification model)
```

- Generate template directory in ml_projects/
- Template models dependent on prediction type (regression or classification)

```bash
haj config (project) -t/--title (new title)
```
- Rename title of directory
- Update config file

```bash
haj config (project) -p/--prediction # prompt user for regression or classification prediction types
```

- Update models (mv old_train.py new_train.py)
- Update config file

```bash
haj config (project) -d/--dependencies # add desired dependencies
```

- Add dependencies to requirements.txt 
- Install dependencies for project

```bash
haj impl (project) retriever -d/--dependencies (dependencies to be installed) # retriever.py will have functionality for saving raw data to file (with automatic data versioning), logging both metadata and data metrics to terminal and log files
```

- Add dependencies to requirements.txt if provided
- Open file in vim

```bash
haj impl (project) processor -d/--dependencies (dependencies to be installed) # processor.py will unfortunately have the most work as all data is processed in vastly different ways
```

- Add dependencies to requirements.txt if provided
- Open file in vim

```bash
haj impl (project) model -d/--dependencies (dependencies to be installed) # model.py will have functionality for saving models to a "registry" models/ and logging model metadata and modele metrics to terminal and files
```

- Add dependencies to requirements.txt if provided
- Open file in vim

```bash
haj train (project) # train's models dependent on prediction type
```

- Run train.py for project
- Log metadata to terminal/file [DATETIME PROJECT_ID (MODEL-#) DATA_VERSION]
- Log all model metrics to file

```bash
haj evaluate (project) # "crowns" a champion model based on best performance metrics (default accuracy)
```

- Pull log file
- Pick best performing model based on (accuracy if classification, rmse if regression)
- Change name of best performing model
- Log to terminal

```bash
haj evaluate (project) rmse 
```

- Pick best performing model based on rmse


```bash
haj evaluate (project) mae 
```

- Pick best performing model based on mae

```bash
haj evaluate (project) mse
```

- Pick best performing model based on mse

```bash
haj evaluate (project) precision 
```

- Pick best performing model based on precision

```bash
haj evaluate (project) acc 
```

- Pick best performing model based on accuracy

```bash
haj evaluate (project) recall 
```

- Pick best performing model based on recall

```bash
haj evaluate (project) f1 
```

- Pick best performing model based on f1

```bash
haj run (project) # start fastapi inference server for monitoring 
# add these endpoints
# /health
# /metrics
# /predictions_count
# /latency
```

- Start (server.py) FastAPI server for inferencing champion model 

```bash
haj build (project) # create docker image and run server
```

- Containerize project
- Run container

```bash
haj deploy (project) # deploy on AWS
```

- ? come back to this 

### Functions

```python
def check_project_exists(project_id: str) -> bool:

def switch_ptype(project_id: str):

def assign_ptype(project_id: str, ptype: bool):

def add_dependencies(project_id: str, dependencies: list):

def crown_champion(project_id: str, metric: str = "acc"):
    '''For classification prediction type.'''

def crown_champion(project_id: str, metric: str = "rmse"):
    '''For regression prediction type.'''

def containerize_project(project_id: str):
```


### Sequence of Development

1. Construct CLI Tool schema ✅
2. Implement retrieve, processing, and model templates
    - How will I implement logging, tracking, and versioning?
    - How do I control dependencies for individual projects?
3. Construct schema of command functions
4. Implement util functions
5. Implement server functionality
6. Implement deployment functionality
7. Write tests

### TODOs

1. logging and tracking functionality (MLFlow?) to train.py functions
2. data versionining to retriever.py and processor.py
2. data retrieval from a file function _get_data() -> np.ndarray to train.py
3. metrics for mae and mse to regression models
3. metrics for precision, recall to regression models