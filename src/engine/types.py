from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DcfResult:
    enterprise_value: float
    equity_value: float


@dataclass(frozen=True)
class MultiplesResult:
    enterprise_value: float | None
    equity_value: float | None


@dataclass(frozen=True)
class ProjectionResult:
    revenue: list[float]
    ebitda: list[float]
    fcf: list[float]


@dataclass(frozen=True)
class ValuationResult:
    projections: ProjectionResult
    dcf: DcfResult
    multiples: MultiplesResult
    football_field: dict[str, float]


def to_float_list(values: list[Any]) -> list[float]:
    return [float(v) for v in values]
