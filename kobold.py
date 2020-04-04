#!/home/hgf/.miniconda/envs/tamagotchi/bin/python
import typer
import hashlib
from subprocess import run
import os
from typing import List
from pathlib import Path
from kobold.task import Task, PrettyTask
from kobold.task_db import TaskDB, PrettyTaskDB

app = typer.Typer()
tdb = None


class Config:
    db = Path.home().joinpath(".kobold")


@app.command("rofi_select")
def select_task_in_rofi():
    rv = run(["rofi", "-dmenu", "-p", "kobold"], input=str(tdb).encode(), capture_output=True)
    print(rv)
    run(["pom", f"{rv.stdout.decode().strip()}"])


@app.command("done")
def mark_task_done(hash: str):
    hash = int(hash, base=16)
    tdb.tasks[hash].complete()
    tdb.save_tasks()


@app.command("edit")
def edit_tasks_in_editor():
    run([os.getenv("EDITOR", "vi"), Config.db])


@app.command("rm")
def remove_task(hash: str):
    tdb.remove_task(int(hash, base=16))
    tdb.save_tasks()


@app.command("ls")
def list_tasks(filters: List[str] = typer.Argument(None), hide_done: bool = True):
    typer.echo(PrettyTaskDB(tdb, hide_done=hide_done, filters=filters))


@app.command("add")
def add_task(entry: List[str]):
    t = tdb.add_task(" ".join(entry))
    tdb.save_tasks()
    typer.echo(PrettyTask(t))


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    global tdb
    tdb = TaskDB(Config.db)
    if ctx.invoked_subcommand is None:
        list_tasks(filters = None)


if __name__ == "__main__":
    app()
