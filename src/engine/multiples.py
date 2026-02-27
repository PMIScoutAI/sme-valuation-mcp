from __future__ import annotations

from .types import MultiplesResult


def compute_multiples(payload: dict, projected_ebitda: list[float]) -> MultiplesResult:
    multiples = payload.get("multiples") or {}
    nfp = float(payload["actuals"].get("nfp", 0.0))

    ev_ebitda_multiple = multiples.get("ev_ebitda_multiple")
    ev_ebit_multiple = multiples.get("ev_ebit_multiple")

    ev_candidates: list[float] = []
    last_ebitda = float(projected_ebitda[-1])
    last_ebit = last_ebitda * 0.85

    if ev_ebitda_multiple is not None:
        ev_candidates.append(float(ev_ebitda_multiple) * last_ebitda)
    if ev_ebit_multiple is not None:
        ev_candidates.append(float(ev_ebit_multiple) * last_ebit)

    if not ev_candidates:
        return MultiplesResult(enterprise_value=None, equity_value=None)

    enterprise_value = sum(ev_candidates) / len(ev_candidates)
    equity_value = enterprise_value - nfp
    return MultiplesResult(enterprise_value=enterprise_value, equity_value=equity_value)
