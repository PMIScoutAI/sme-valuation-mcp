from __future__ import annotations

from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

from src.mcp_server import mcp


async def health(_: object) -> JSONResponse:
    return JSONResponse({"ok": True})


if mcp is None:
    async def mcp_unavailable(_: object) -> JSONResponse:
        return JSONResponse(
            {"ok": False, "error": "mcp package not installed on server"},
            status_code=500,
        )

    app = Starlette(
        routes=[
            Route("/health", health, methods=["GET"]),
            Route("/mcp", mcp_unavailable, methods=["GET", "POST"]),
        ]
    )
else:
    mcp_http_app = mcp.streamable_http_app()

    @asynccontextmanager
    async def lifespan(_: Starlette):
        async with mcp_http_app.session_manager.run():
            yield

    app = Starlette(
        lifespan=lifespan,
        routes=[
            Route("/health", health, methods=["GET"]),
            Mount("/mcp", app=mcp_http_app),
        ],
    )
