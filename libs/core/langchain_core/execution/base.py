"""Abstract base for execution policies."""

from __future__ import annotations

import abc
from typing import Any, Callable


class BaseExecutionPolicy(abc.ABC):
    """Abstract base class for execution policies applied during model invocation.

    Subclasses control timeout behavior and retry decisions.
    """

    @abc.abstractmethod
    def should_retry(self, attempt: int, error: Exception) -> bool:
        """Return True if the invocation should be retried.

        Args:
            attempt: Zero-based attempt index (0 = first attempt).
            error: The exception raised by the previous attempt.

        Returns:
            True if a retry should be attempted.
        """

    @property
    @abc.abstractmethod
    def timeout_seconds(self) -> float | None:
        """Timeout in seconds for a single invocation attempt, or None for no limit."""

    @abc.abstractmethod
    def apply(
        self,
        func: Callable[..., Any],
        *,
        context: dict[str, Any] | None = None,
    ) -> Any:
        """Execute *func* under this policy's constraints.

        Args:
            func: Callable to execute.
            context: Optional execution metadata passed through to the callable.

        Returns:
            The return value of *func*.
        """
