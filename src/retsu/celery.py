"""Retsu tasks with celery."""

from __future__ import annotations

from typing import Optional

import celery

from celery import chain, chord

from retsu.core import ParallelTask, SerialTask


class CeleryTask:
    """Celery Task class."""

    def task(self, *args, task_id: str, **kwargs) -> None:  # type: ignore
        """Define the task to be executed."""
        chord_tasks, chord_callback = self.get_chord_tasks(
            *args, task_id=task_id, **kwargs
        )
        chain_tasks = self.get_chain_tasks(*args, task_id=task_id, **kwargs)

        if chord_tasks:
            if chord_callback:
                workflow_chord = chord(chord_tasks, chord_callback)
            else:
                workflow_chord = chord(chord_tasks)
            workflow_chord.apply_async()

        if chain_tasks:
            workflow_chain = chain(chord_tasks)
            workflow_chain.apply_async()

    def get_chord_tasks(  # type: ignore
        self, *args, **kwargs
    ) -> tuple[list[celery.Signature], Optional[celery.Signature]]:
        """
        Run tasks with chord.

        Return
        ------
        tuple:
            list of tasks for the chord, and the task to be used as a callback
        """
        chord_tasks: list[celery.Signature] = []
        callback_task = None
        return (chord_tasks, callback_task)

    def get_chain_tasks(  # type: ignore
        self, *args, **kwargs
    ) -> list[celery.Signature]:
        """Run tasks with chain."""
        chain_tasks: list[celery.Signature] = []
        return chain_tasks


class ParallelCeleryTask(CeleryTask, ParallelTask):
    """Parallel Task for Celery."""

    ...


class SerialCeleryTask(CeleryTask, SerialTask):
    """Serial Task for Celery."""

    ...
