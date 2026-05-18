"""Timeout-based execution policy."""

from __future__ import annotations

from typing import Any, Callable

from langchain_core.execution.base import BaseExecutionPolicy


class TimeoutPolicy(BaseExecutionPolicy):
    """Execution policy that enforces a wall-clock timeout per invocation attempt.

    Args:
        seconds: Maximum seconds allowed per invocation attempt. ``None`` disables
            the limit.
    """

    def __init__(self, seconds: float | None = None) -> None:
        self._seconds = seconds

    @property
    def timeout_seconds(self) -> float | None:
        return self._seconds

    def should_retry(self, attempt: int, error: Exception) -> bool:
        return False

    def apply(
        self,
        func: Callable[..., Any],
        *,
        context: dict[str, Any] | None = None,
    ) -> Any:
        if self._seconds is None:
            return func()
        raise NotImplementedError(
            "Platform-specific timeout enforcement is not yet implemented."
        )
