from __future__ import annotations

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from src.mcp_server import mcp


async def root(_: object) -> JSONResponse:
    return JSONResponse(
        {
            "ok": True,
            "service": "sme-valuation-mcp",
            "mcp_endpoint": "/mcp",
            "health_endpoint": "/health",
        }
    )


async def health(_: object) -> JSONResponse:
    return JSONResponse({"ok": True})

middlewares = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


if mcp is None:
    async def mcp_unavailable(_: object) -> JSONResponse:
        return JSONResponse(
            {"ok": False, "error": "mcp package not installed on server"},
            status_code=500,
        )

    app = Starlette(
        middleware=middlewares,
        routes=[
            Route("/", root, methods=["GET"]),
            Route("/health", health, methods=["GET"]),
            Route("/mcp", mcp_unavailable, methods=["GET", "POST"]),
        ]
        )
else:
    try:
        mcp_http_app = mcp.streamable_http_app()
    except Exception as exc:  # pragma: no cover
        error_message = f"mcp init failed: {exc}"

        async def mcp_init_error(_: object) -> JSONResponse:
            return JSONResponse(
                {"ok": False, "error": error_message},
                status_code=500,
            )

        app = Starlette(
            middleware=middlewares,
            routes=[
                Route("/", root, methods=["GET"]),
                Route("/health", health, methods=["GET"]),
                Route("/mcp", mcp_init_error, methods=["GET", "POST"]),
            ]
        )
    else:
        app = Starlette(
            middleware=middlewares,
            routes=[
                Route("/", root, methods=["GET"]),
                Route("/health", health, methods=["GET"]),
                Mount("/mcp", app=mcp_http_app),
            ],
        )
