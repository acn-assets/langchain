"""Composite execution policy combining timeout and retry."""

from __future__ import annotations

from typing import Any, Callable

from langchain_core.execution.base import BaseExecutionPolicy
from langchain_core.execution.retry import RetryPolicy
from langchain_core.execution.timeout import TimeoutPolicy


class CompositePolicy(BaseExecutionPolicy):
    """Execution policy that applies a :class:`TimeoutPolicy` and a
    :class:`RetryPolicy` in sequence.

    The timeout governs each individual attempt; the retry logic decides whether
    to repeat after a failure. Both constituent policies remain independently
    configurable and usable on their own.

    Args:
        timeout: Policy controlling the per-attempt time limit.
        retry: Policy controlling how many times a failed attempt is repeated.
    """

    def __init__(self, timeout: TimeoutPolicy, retry: RetryPolicy) -> None:
        self._timeout = timeout
        self._retry = retry

    @property
    def timeout_seconds(self) -> float | None:
        return self._timeout.timeout_seconds

    def should_retry(self, attempt: int, error: Exception) -> bool:
        return self._timeout.should_retry(attempt, error)

    def apply(
        self,
        func: Callable[..., Any],
        *,
        context: dict[str, Any] | None = None,
    ) -> Any:
        return self._retry.apply(
            lambda: self._timeout.apply(func, context=context),
            context=context,
        )
