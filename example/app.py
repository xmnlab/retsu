"""Example of usage retsu with a flask app."""

import os
import signal

from typing import Optional

from flask import Flask
from tasks import MyTaskManager

app = Flask(__name__)

task_manager = MyTaskManager()
task_manager.start()


def signal_handler(signum: int, frame: Optional[int]) -> None:
    """Define signal handler."""
    print(f"Received signal {signum}, shutting down...")
    try:
        task_manager.stop()
    except Exception:
        ...
    # Perform any other cleanup here if necessary
    os._exit(0)


# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


@app.route("/")
def api() -> str:
    """Define the root endpoint."""
    menu = """
    Select an endpoint for your request:

    * serial
    * parallel
    * status
    * result
    """

    return menu


@app.route("/serial/<int:a>/<int:b>")
def serial(a: int, b: int) -> str:
    """Define the serial endpoint."""
    task1 = task_manager.get_task("serial")
    key = task1.request(a=a, b=b)
    return f"your task ({key}) is running now, please wait until it is done."


@app.route("/parallel/<int:a>/<int:b>")
def parallel(a: int, b: int) -> str:
    """Define the parallel endpoint."""
    task2 = task_manager.get_task("parallel")
    key = task2.request(a=a, b=b)
    return f"your task ({key}) is running now, please wait until it is done."


@app.route("/serial/status/<string:task_id>")
def serial_status(task_id: str) -> str:
    """Define serial/status endpoint."""
    task1 = task_manager.get_task("serial")
    _status = task1.status(task_id)
    return {"status": _status, "task_id": task_id}


@app.route("/parallel/status/<string:task_id>")
def parallel_status(task_id: str) -> str:
    """Define parallel/status endpoint."""
    task2 = task_manager.get_task("parallel")
    _status = task2.status(task_id)
    return {"status": _status, "task_id": task_id}


@app.route("/serial/result/<string:task_id>")
def serial_result(task_id: str) -> str:
    """Define serial/result endpoint."""
    task1 = task_manager.get_task("serial")
    return task1.get_result(task_id)


@app.route("/parallel/result/<string:task_id>")
def parallel_result(task_id: str) -> str:
    """Define parallel/result endpoint."""
    task2 = task_manager.get_task("parallel")
    return task2.get_result(task_id)


if __name__ == "__main__":
    try:
        app.run(
            debug=True,
            passthrough_errors=True,
            use_debugger=True,
            use_reloader=False,
        )
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
