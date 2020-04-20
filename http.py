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
        self.loop = asyncio.get_event_loop() if not loop else loop
        user_agent = 'Python/{0[0]}.{0[1]} aiohttp/{1}'.format(sys.version_info, aiohttp.__version__)
        self.user_agent: str = kwargs.pop('user_agent', user_agent)
        self.headers: dict = kwargs.pop('headers', {})
        self.headers['User-Agent'] = self.user_agent
        self.cookies: dict = kwargs.pop('cookies', {})
        self.raise_for_status: bool = kwargs.pop('raise_for_status', True)
        self.session = aiohttp.ClientSession(
            loop=self.loop,
            headers=self.headers,
            raise_for_status=self.raise_for_status
        )

    def renew_session(self) -> aiohttp.ClientSession:
        if self.session.closed:
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
        if not self.BASE_URL.startswith('https://'):
            self.BASE_URL = 'https://' + self.BASE_URL

    async def request(self, route: Route, **kwargs) -> Union[str, dict, bytes]:
        headers = self.headers.copy()
        cookies = self.cookies.copy()

        if route.headers is not None:
            headers.update(route.headers)
        if route.cookies is not None:
            cookies.update(route.cookies)

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = json.dumps(
                kwargs.pop('json'),
                separators=(',', ':'),
                ensure_ascii=True
            )

        method = route.method
        path = route.path
        url = self.BASE_URL + path

        self.session = self.renew_session()

        async with self.session.request(method, url, **kwargs) as r:
            logger.info(f'[Request] {method} {path} | {r.status}')
            if route.expected_type:
                if r.headers.get('Content-Type', '') != route.expected_type:
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
