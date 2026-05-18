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
