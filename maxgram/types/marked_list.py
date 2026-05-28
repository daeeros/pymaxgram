from __future__ import annotations

from typing import Generic, TypeVar

T = TypeVar("T")


class MarkedList(list, Generic[T]):
    """list with a pagination ``marker`` pointing to the next page (``None`` if no more pages)."""

    marker: int | None = None
