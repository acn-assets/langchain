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
    def from_runnable_config(cls, config: dict[str, Any]) -> "ExecutionContext":
        """Create an :class:`ExecutionContext` from a ``RunnableConfig`` dict.

        Bridges the standard Runnable-layer config (as produced by
        :func:`langchain_core.runnables.config.ensure_config`) into an
        :class:`ExecutionContext` so execution policies can be driven by the
        same metadata that flows through the Runnable graph.

        Args:
            config: A ``RunnableConfig``-shaped dict containing at least the
                keys ``tags``, ``metadata``, and ``run_id``.  Missing keys are
                treated as empty / absent.

        Returns:
            A new :class:`ExecutionContext` populated from *config*.
        """
        return cls(
            tags=list(config.get("tags") or []),
            metadata=dict(config.get("metadata") or {}),
            run_id=config.get("run_id"),
        )
