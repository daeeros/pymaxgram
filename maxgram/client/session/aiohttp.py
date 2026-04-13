from __future__ import annotations

import asyncio
import ssl
from collections.abc import AsyncGenerator, Iterable
from typing import TYPE_CHECKING, Any

import certifi
from aiohttp import BasicAuth, ClientError, ClientSession, FormData, TCPConnector
from aiohttp.hdrs import USER_AGENT
from aiohttp.http import SERVER_SOFTWARE
from typing_extensions import Self

from maxgram.__meta__ import __version__
from maxgram.exceptions import MaxNetworkError

from .base import BaseSession

if TYPE_CHECKING:
    from maxgram.client.bot import Bot
    from maxgram.methods import MaxMethod
    from maxgram.methods.base import MaxType
    from maxgram.types import InputFile

_ProxyBasic = str | tuple[str, BasicAuth]
_ProxyChain = Iterable[_ProxyBasic]
_ProxyType = _ProxyChain | _ProxyBasic


def _retrieve_basic(basic: _ProxyBasic) -> dict[str, Any]:
    from aiohttp_socks.utils import parse_proxy_url

    proxy_auth: BasicAuth | None = None

    if isinstance(basic, str):
        proxy_url = basic
    else:
        proxy_url, proxy_auth = basic

    proxy_type, host, port, username, password = parse_proxy_url(proxy_url)
    if isinstance(proxy_auth, BasicAuth):
        username = proxy_auth.login
        password = proxy_auth.password

    return {
        "proxy_type": proxy_type,
        "host": host,
        "port": port,
        "username": username,
        "password": password,
        "rdns": True,
    }


def _prepare_connector(chain_or_plain: _ProxyType) -> tuple[type[TCPConnector], dict[str, Any]]:
    from aiohttp_socks import ChainProxyConnector, ProxyConnector, ProxyInfo

    if isinstance(chain_or_plain, str) or (
        isinstance(chain_or_plain, tuple) and len(chain_or_plain) == 2  # noqa: PLR2004
    ):
        chain_or_plain = cast(_ProxyBasic, chain_or_plain)
        return ProxyConnector, _retrieve_basic(chain_or_plain)

    chain_or_plain = cast(_ProxyChain, chain_or_plain)
    infos: list[ProxyInfo] = [ProxyInfo(**_retrieve_basic(basic)) for basic in chain_or_plain]

    return ChainProxyConnector, {"proxy_infos": infos}


class AiohttpSession(BaseSession):
    def __init__(self, proxy: _ProxyType | None = None, limit: int = 100, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self._session: ClientSession | None = None
        self._connector_type: type[TCPConnector] = TCPConnector
        self._connector_init: dict[str, Any] = {
            "ssl": ssl.create_default_context(cafile=certifi.where()),
            "limit": limit,
            "ttl_dns_cache": 3600,
        }
        self._should_reset_connector = True
        self._proxy: _ProxyType | None = None

        if proxy is not None:
            try:
                self._setup_proxy_connector(proxy)
            except ImportError as exc:
                msg = (
                    "In order to use aiohttp client for proxy requests, install "
                    "https://pypi.org/project/aiohttp-socks/"
                )
                raise RuntimeError(msg) from exc

    def _setup_proxy_connector(self, proxy: _ProxyType) -> None:
        self._connector_type, self._connector_init = _prepare_connector(proxy)
        self._proxy = proxy

    @property
    def proxy(self) -> _ProxyType | None:
        return self._proxy

    @proxy.setter
    def proxy(self, proxy: _ProxyType) -> None:
        self._setup_proxy_connector(proxy)
        self._should_reset_connector = True

    async def create_session(self) -> ClientSession:
        if self._should_reset_connector:
            await self.close()

        if self._session is None or self._session.closed:
            self._session = ClientSession(
                connector=self._connector_type(**self._connector_init),
                headers={
                    USER_AGENT: f"{SERVER_SOFTWARE} maxgram/{__version__}",
                },
            )
            self._should_reset_connector = False

        return self._session

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
            await asyncio.sleep(0.25)

    async def make_request(
        self,
        bot: Bot,
        method: MaxMethod[MaxType],
        timeout: int | None = None,
    ) -> MaxType:
        session = await self.create_session()

        # Build URL from path
        path = method.build_request_path()
        url = self.api.api_url(path)

        # Authorization header
        headers = {"Authorization": bot.token}

        http_method = method.__http_method__
        request_timeout = self.timeout if timeout is None else timeout

        try:
            if http_method in ("POST", "PUT", "PATCH"):
                # Query params + JSON body
                query_params = method.build_query_params()
                body = method.build_request_body()
                async with session.request(
                    http_method,
                    url,
                    params=query_params or None,
                    json=body,
                    headers=headers,
                    timeout=request_timeout,
                ) as resp:
                    raw_result = await resp.text()
            else:
                # GET / DELETE - query params only
                query_params = method.build_query_params()
                async with session.request(
                    http_method,
                    url,
                    params=query_params or None,
                    headers=headers,
                    timeout=request_timeout,
                ) as resp:
                    raw_result = await resp.text()
        except asyncio.TimeoutError as e:
            raise MaxNetworkError(method=method, message="Request timeout error") from e
        except ClientError as e:
            raise MaxNetworkError(method=method, message=f"{type(e).__name__}: {e}") from e

        result = self.check_response(
            bot=bot,
            method=method,
            status_code=resp.status,
            content=raw_result,
        )
        return result

    async def upload_file(
        self,
        bot: Bot,
        upload_url: str,
        file_data: bytes,
        filename: str = "file",
    ) -> dict[str, Any]:
        """Upload file to the URL obtained from POST /uploads."""
        session = await self.create_session()

        form = FormData()
        form.add_field("data", file_data, filename=filename)

        try:
            async with session.post(upload_url, data=form) as resp:
                raw_result = await resp.text()
                return self.json_loads(raw_result)
        except ClientError as e:
            raise RuntimeError(f"File upload failed: {e}") from e

    async def stream_content(
        self,
        url: str,
        headers: dict[str, Any] | None = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        if headers is None:
            headers = {}

        session = await self.create_session()

        async with session.get(
            url,
            timeout=timeout,
            headers=headers,
            raise_for_status=raise_for_status,
        ) as resp:
            async for chunk in resp.content.iter_chunked(chunk_size):
                yield chunk

    async def __aenter__(self) -> Self:
        await self.create_session()
        return self
