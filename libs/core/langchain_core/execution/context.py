"""Execution context passed to policies and invocation hooks."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExecutionContext:
    """Immutable bag of metadata threaded through an invocation.

    Attributes:
        tags: Arbitrary string labels attached to this invocation.
        metadata: Free-form key/value pairs for tracing and debugging.
        run_id: Optional unique identifier for the run, as a string.
    """

    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    run_id: str | None = None

    @classmethod
    def from_chat_model(cls, model: Any) -> "ExecutionContext":
        """Create an :class:`ExecutionContext` from a ``BaseChatModel`` instance.

        Surfaces the model-level fields that are most relevant to execution
        policies — rate limiting and streaming behaviour — as context metadata,
        without introducing an upward import from the ``execution`` package into
        ``language_models``.

        ``model`` is typed as :class:`~typing.Any` so that this module remains
        independent of the ``BaseChatModel`` class hierarchy; callers are
        expected to pass an actual ``BaseChatModel`` subclass instance.

        Args:
            model: A ``BaseChatModel`` instance (or any object that exposes
                ``disable_streaming`` and ``rate_limiter`` attributes).

        Returns:
            A new :class:`ExecutionContext` whose ``metadata`` contains
            ``"disable_streaming"`` and ``"has_rate_limiter"`` keys.
        """
        return cls(
            metadata={
                "disable_streaming": getattr(model, "disable_streaming", False),
                "has_rate_limiter": getattr(model, "rate_limiter", None) is not None,
            }
        )
