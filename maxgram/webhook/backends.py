from enum import Enum


class WebhookBackend(str, Enum):
    """HTTP backend for :meth:`Dispatcher.run_webhook` / :meth:`Dispatcher.start_webhook`.

    - :attr:`AIOHTTP` — default, built-in, no extra dependencies.
    - :attr:`FASTAPI` — FastAPI served by uvicorn (uvloop + httptools).
      Requires ``pip install pymaxgram[fastapi]``.
    - :attr:`SANIC` — Sanic with its own httptools-based server.
      Requires ``pip install pymaxgram[sanic]``.
    """

    AIOHTTP = "aiohttp"
    FASTAPI = "fastapi"
    SANIC = "sanic"
