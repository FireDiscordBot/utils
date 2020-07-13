"""
http
~~~~~~~~~~~~~~~~~~~~

A HTTP client
"""


from json.decoder import JSONDecodeError
from typing import Optional, Union
import aiohttp
import asyncio
import logging
import inspect
import json
import sys


logger = logging.getLogger('fire.http')


class UnexpectedContentType(Exception):
    def __init__(self, expected: str, received: str):
        self.expected = expected
        self.received = received
        super().__init__(self.__str__)

    def __str__(self):
        return f'Expected {self.expected} but got {self.received}'


class Route:
    def __init__(self, method: str = 'GET', path: str = '/', **kwargs):
        self.method = method.upper()
        self.path = path
        self.params: dict = kwargs.pop('params', {})
        self.cookies: Optional[dict] = kwargs.pop('cookies', None)
        self.headers: Optional[dict] = kwargs.pop('headers', None)
        self.expected_type = kwargs.pop('expected_type', None)

    def __repr__(self):
        return f'<Route method={self.method} path={self.path} params={self.params}>'


class HTTPClient:
    def __init__(self, base: str, **kwargs):
        self.BASE_URL: str = base
        self.format_base_url()
        loop = kwargs.pop('loop', None)
        self.logging = kwargs.pop('logging', True)
        self.loop = asyncio.get_event_loop() if not loop else loop
        user_agent = 'Python/{0[0]}.{0[1]} aiohttp/{1}'.format(sys.version_info, aiohttp.__version__)
        self.user_agent: str = kwargs.pop('user_agent', user_agent)
        self.headers: dict = kwargs.pop('headers', {})
        self.headers['User-Agent'] = self.user_agent
        self.params: dict = kwargs.pop('params', {})
        self.cookies: dict = kwargs.pop('cookies', {})
        self.raise_for_status: bool = kwargs.pop('raise_for_status', True)
        self.error_handlers: dict = kwargs.pop('error_handlers', {})
        self.middleware: list = kwargs.pop('middleware', [])
        self.session = aiohttp.ClientSession(
            loop=self.loop,
            headers=self.headers,
            raise_for_status=self.raise_for_status
        )

    def renew_session(self) -> aiohttp.ClientSession:
        if self.session.closed:
            if self.logging:
                logger.warn(f'[Session] Session is closed, renewing')
            session = aiohttp.ClientSession(
                loop=self.loop,
                headers=self.headers,
                raise_for_status=self.raise_for_status
            )
            return session
        return self.session

    def format_base_url(self):
        if self.BASE_URL.endswith('/'):
            self.BASE_URL = self.BASE_URL[:-1]
        if not self.BASE_URL.startswith('https://') and not self.BASE_URL.startswith('http://'):  # Lets hope it supports https lol
            self.BASE_URL = 'https://' + self.BASE_URL

    async def request(self, route: Route, **kwargs) -> Union[str, dict, bytes]:
        headers = self.headers.copy()
        params = self.params.copy()
        cookies = self.cookies.copy()

        if route.headers is not None:
            headers.update(route.headers)
        if route.params is not None:
            params.update(route.params)
        if route.cookies is not None:
            cookies.update(route.cookies)

        headers.update(kwargs.get('headers', {}))
        params.update(kwargs.get('params', {}))
        cookies.update(kwargs.get('cookies', {}))
        kwargs['headers'] = headers
        kwargs['params'] = params
        kwargs['cookies'] = cookies

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = json.dumps(
                kwargs.pop('json'),
                separators=(',', ':'),
                ensure_ascii=True
            )

        if self.error_handlers:
            self.session._raise_for_status = False

        method = route.method
        path = route.path
        url = self.BASE_URL + path

        self.session = self.renew_session()

        async with self.session.request(method, url, **kwargs) as r:
            if self.logging:
                logger.info(f'[Request] {method} {path} | {r.status}')
            if r.status in self.error_handlers:
                handler = self.error_handlers[r.status]
                if isinstance(handler, Exception):
                    raise handler
                if inspect.iscoroutinefunction(handler):
                    if inspect.getfullargspec(handler).args == 1:
                        return await handler(r)
                    return await handler()
                if inspect.getfullargspec(handler).args == 1:
                    return handler(r)
                return handler()
            self.session._raise_for_status = self.raise_for_status
            if self.raise_for_status:
                r.raise_for_status()
            for m in self.middleware:
                if inspect.iscoroutinefunction(m):
                    await m(r)
                else:
                    m(r)
            if route.expected_type:
                if r.headers.get('Content-Type', '') != route.expected_type:
                    if self.logging:
                        logger.debug(f'[Request] Received unexpected content type')
                    raise UnexpectedContentType(
                        route.expected_type,
                        r.headers.get('Content-Type', 'Unkown')
                    )

            if r.headers.get('Content-Type', '') == 'application/json':
                return await r.json()

            try:
                text = await r.text()
                try:
                    return json.loads(text)
                except JSONDecodeError:
                    return text
            except LookupError:
                return await r.read()
