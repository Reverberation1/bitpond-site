"""Every served page must send visitors to kester.world, without JavaScript."""
from __future__ import annotations

import os
from html.parser import HTMLParser

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = "https://kester.world/"
PAGES = ["index.html", "paperless.html", "404.html"]


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.refresh: str | None = None
        self.canonical: str | None = None
        self.robots: str | None = None
        self.links: list[str] = []
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and (a.get("http-equiv") or "").lower() == "refresh":
            self.refresh = a.get("content")
        elif tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "a":
            self.links.append(a.get("href") or "")
        elif tag == "script":
            self.scripts += 1


def parse(name: str) -> HeadParser:
    p = HeadParser()
    with open(os.path.join(ROOT, name), encoding="utf-8") as f:
        p.feed(f.read())
    return p


def refresh_target(content: str) -> tuple[int, str]:
    delay, _, rest = content.partition(";")
    key, _, url = rest.strip().partition("=")
    assert key.strip().lower() == "url"
    return int(delay), url.strip()


@pytest.mark.parametrize("page", PAGES)
def test_page_redirects_immediately_to_kester_world(page):
    p = parse(page)
    assert p.refresh is not None, f"{page} has no meta refresh"
    assert refresh_target(p.refresh) == (0, TARGET)


@pytest.mark.parametrize("page", PAGES)
def test_page_is_canonical_noindex_with_fallback_link(page):
    p = parse(page)
    assert p.canonical == TARGET
    assert p.robots == "noindex"
    assert p.links == [TARGET]
    assert p.scripts == 0


def test_custom_domain_still_bound():
    # Removing CNAME would unbind bitpond.io instead of redirecting it.
    with open(os.path.join(ROOT, "CNAME"), encoding="utf-8") as f:
        assert f.read().strip() == "bitpond.io"


def test_retired_site_files_not_served():
    # Pages serves every tracked file, so the old site must not be in the tree.
    for path in ("deploy", "tools", "assets/fonts", "assets/fonts.css"):
        assert not os.path.exists(os.path.join(ROOT, path)), path
