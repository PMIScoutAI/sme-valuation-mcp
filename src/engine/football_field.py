from __future__ import annotations


def compute_football_field(dcf_equity_value: float, multiples_equity_value: float | None) -> dict[str, float]:
    points = [dcf_equity_value]
    if multiples_equity_value is not None:
        points.append(multiples_equity_value)

    points_sorted = sorted(points)
    low = points_sorted[0]
    high = points_sorted[-1]
    mid = sum(points_sorted) / len(points_sorted)

    return {
        "low": low,
        "mid": mid,
        "high": high,
    }
