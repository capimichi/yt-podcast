"""Base command abstractions for the ytpodcast CLI."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable

import click


class AbstractCommand(ABC):
    """Base class for Click-backed application commands."""

    command_name: str = "command"

    def register_options(self, function: Callable[..., Any]) -> Callable[..., Any]:
        """Register Click options for the command callback."""
        return function

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> None:
        """Execute the command implementation."""
        raise NotImplementedError

    def to_click_command(self) -> click.Command:
        """Convert the command object into a Click command."""

        @click.command(name=self.command_name, help=(self.run.__doc__ or "").strip())
        @self.register_options
        def command(**kwargs: Any) -> None:
            self.run(**kwargs)

        return command
