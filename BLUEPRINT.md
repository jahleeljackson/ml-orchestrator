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
haj init {c|r} (project)
```

```bash
haj config (project) -t/--title (new title)
haj config (project) -d/--dependencies # add desired dependencies
haj config (project) -rd/--remove-dependencies # remove desired dependencies
```

```bash
haj impl (project) retriever -d/--dependencies (dependencies to be installed) # open vim for foo/retriever.py
haj impl (project) processor -d/--dependencies (dependencies to be installed) # open vim for foo/processor.py
```


```bash
haj load (project)
```

```bash
# Classification models
haj train (project) all
haj train (project) lgr -C {float}
haj train (project) rfc --nestimators {int} --maxdepth {int}
haj train (project) xgbc --nestimators {int} --maxdepth {int} --lrate {float}
haj train (project) svc -k/--kernel {linear|poly|rbf|sigmoid} -C {float} -g/--gamma {scale|auto}
haj train (project) knn -n/--neighbors {int} -w/--weights {uniform|distance}

# Regression models
haj train (project) all
haj train (project) lnr
haj train (project) rfr --nestimators {int} --maxdepth {int}
haj train (project) xgbr --nestimators {int} --maxdepth {int} --lrate {float}
haj train (project) svr -k/--kernel {linear|poly|rbf|sigmoid} -C {float} -e/--epsilon {float}


```

```bash
haj evaluate (project) # "crowns" a champion model based on best performance metrics (default accuracy)


# Classification models
haj evaluate (project) precision 
haj evaluate (project) acc 
haj evaluate (project) recall 
haj evaluate (project) f1 

# Regression models
haj evaluate (project) mae 
haj evaluate (project) mse
haj evaluate (project) r2

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



### Functions

```python
def add_dependencies(project_id: str, dependencies: list):

def crown_champion(project_id: str, metric: str):

def get_ptype(project_id: str) -> str:

def containerize_project(project_id: str):
```


### Sequence of Development

1. Construct CLI Tool schema ✅
2. Implement retrieve, processing, and model templates 
    - How will I implement logging, tracking, and versioning?
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