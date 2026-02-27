from __future__ import annotations

from .types import DcfResult


def compute_dcf(payload: dict, fcf: list[float]) -> DcfResult:
    wacc = float(payload["assumptions"]["wacc"])
    terminal_growth = float(payload["assumptions"]["terminal_growth"])
    nfp = float(payload["actuals"].get("nfp", 0.0))

    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth for DCF.")

    pv_sum = 0.0
    for i, cash_flow in enumerate(fcf, start=1):
        pv_sum += cash_flow / ((1.0 + wacc) ** i)

    terminal_fcf = fcf[-1] * (1.0 + terminal_growth)
    terminal_value = terminal_fcf / (wacc - terminal_growth)
    terminal_pv = terminal_value / ((1.0 + wacc) ** len(fcf))

    enterprise_value = pv_sum + terminal_pv
    equity_value = enterprise_value - nfp
    return DcfResult(enterprise_value=enterprise_value, equity_value=equity_value)
