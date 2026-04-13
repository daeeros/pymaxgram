from typing import Any
from urllib.parse import urlencode, urljoin

BASE_DOCS_URL = "https://docs.maxgram.dev/"
BRANCH = "dev-3.x"
BASE_PAGE_URL = f"{BASE_DOCS_URL}/en/{BRANCH}/"


def _format_url(url: str, *path: str, fragment_: str | None = None, **query: Any) -> str:
    url = urljoin(url, "/".join(path), allow_fragments=True)
    if query:
        url += "?" + urlencode(query)
    if fragment_:
        url += "#" + fragment_
    return url


def docs_url(*path: str, fragment_: str | None = None, **query: Any) -> str:
    return _format_url(BASE_PAGE_URL, *path, fragment_=fragment_, **query)


def create_max_user_link(user_id: int) -> str:
    """Create a MAX user mention link."""
    return f"max://user/{user_id}"
