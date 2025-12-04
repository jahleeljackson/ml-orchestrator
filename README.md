# Machine Learning Workflow Orchestrator (CLI Tool): Python


## Project Description 

I command line interface tool which can accomplish the following things:

    - Initialize a ML project instance (generate a directory)
    - List existing ML projects 
    - Within each ML project/directory, the tool should be able to call the following functionality:
        1. Retrieve data from a remote API (status logged to terminal, clean error handling)
        2. Train models on data (progress logged to terminal)
        3. Evaluate and log (to files and terminal) the metrics of models 
        4. Start an inference server for monitoring (events & metrics logged to terminal)
        5. "Spin" up and down the model deployment on AWS

## Purpose 

To increase my familiarity with AWS, model metrics, and model monitoring. 

## Tech Stack 


### Python
    - CLI Tooling = Typer
    - Asynchronous Orchestration = Subprocess
    - Model deployment to AWS = ?
    - Retrieve data from remote API (logging functionality) = httpx, pydantic, logger
    - Train models on data = scikit-learn, pytorch, pandas & numpy (preprocessing), logger
    - Evaluate metrics = MLFlow, logger
    - Inference server for monitoring = FastAPI, Prometheus?  





### Architecture

```bash
ml init project_identifier --> generate template directory/project "project_identifier/"
                               retrieve and process data

project_identifier/
    |_ train.py 
    |_ evaluate.py
    |_ models/
        |_ models.json {model and respective performance metrics will go here} # after train.py  
        |_ model1.joblib # after training
        |_ model2.joblib # after training
        |_ model3.joblib # after training
        |_ champion.joblib # after evaluation
    |_ tests/
    |_ data/
        |_ preprocessing.py
        |_ retriever.py
        |_ {(raw) retrieved data will go here (.csv or .json)} # after retrieve.py
        |_ {processed data will go here (.json for to store meta data)} # after preprocessing.py
    |_ config.toml 
    |_ .env
``` 

Command copies template directory into new directory name after argument (project_identifier). After succesful directory
generation, retriever.py is called to GET data from remote API (undecided at time of writing). Preprocessing is called  


```bash
ml train project_identifier --> train models on processed data 
```

Models are trained on processed data. Performance metrics and meta data logged to terminal and files. 



```bash
ml evaluate project_identifier --> compare performance metrics of models 
```

Metrics loaded from models are compared for champion model. Best model is "crowned" champion.joblib




```bash
ml monitor project_identifier --> start FastAPI server for inference and monitoring.
```

Will start inference server for monitoring model metrics and events.
