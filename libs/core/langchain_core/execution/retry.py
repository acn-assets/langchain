"""Retry-based execution policy."""

from __future__ import annotations

from typing import Any, Callable

from langchain_core.execution.base import BaseExecutionPolicy


class RetryPolicy(BaseExecutionPolicy):
    """Execution policy that retries a callable on error up to a configured limit.

    Args:
        max_retries: Maximum number of retries after the first attempt. Must be
            non-negative.
    """

    def __init__(self, max_retries: int = 3) -> None:
        if max_retries < 0:
            msg = f"max_retries must be non-negative, got {max_retries!r}"
            raise ValueError(msg)
        self._max_retries = max_retries
        self._attempts: int = 0

    @property
    def timeout_seconds(self) -> float | None:
        return None

    def should_retry(self, attempt: int, error: Exception) -> bool:
        return attempt < self._max_retries

    def apply(
        self,
        func: Callable[..., Any],
        *,
        context: dict[str, Any] | None = None,
    ) -> Any:
        last_error: Exception | None = None
        for attempt in range(self._max_retries + 1):
            try:
                self._attempts += 1
                return func()
            except Exception as exc:
                last_error = exc
                if not self.should_retry(attempt, exc):
                    break
        raise last_error  # type: ignore[misc]
