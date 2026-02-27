from __future__ import annotations

from .types import ProjectionResult


def project_financials(payload: dict) -> ProjectionResult:
    years = int(payload["meta"]["years"])
    revenue_hist = [float(x) for x in payload["actuals"]["revenue"]]

    revenue_cagr = float(payload["assumptions"]["revenue_cagr"])
    ebitda_margin = float(payload["assumptions"]["ebitda_margin"])
    capex_pct = float(payload["assumptions"]["capex_pct_revenue"])
    nwc_pct = float(payload["assumptions"]["nwc_pct_revenue"])
    tax_rate = float(payload["assumptions"]["tax_rate"])

    revenue_proj: list[float] = []
    ebitda_proj: list[float] = []
    fcf_proj: list[float] = []

    prev_revenue = revenue_hist[-1]
    for _ in range(years):
        rev = prev_revenue * (1.0 + revenue_cagr)
        ebitda = rev * ebitda_margin

        # Simplified FCF proxy for v1.
        capex = rev * capex_pct
        delta_nwc = rev * nwc_pct
        ebit_proxy = ebitda * 0.85
        nopat = ebit_proxy * (1.0 - tax_rate)
        fcf = nopat - capex - delta_nwc

        revenue_proj.append(rev)
        ebitda_proj.append(ebitda)
        fcf_proj.append(fcf)

        prev_revenue = rev

    return ProjectionResult(revenue=revenue_proj, ebitda=ebitda_proj, fcf=fcf_proj)
