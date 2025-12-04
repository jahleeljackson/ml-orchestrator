import typer
from enum import Enum 

class Command(Enum):
    INIT = "init"
    TRAIN = "train"
    EVAL = "eval"
    MONITOR = "monitor"

app = typer.Typer()


@app.command()
def ml(command: Command, project_id: str):
    print(project_id)


if __name__ == "__main__":
    app()
