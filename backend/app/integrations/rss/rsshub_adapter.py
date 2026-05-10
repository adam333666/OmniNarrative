from __future__ import annotations

from dataclasses import dataclass
import re
from xml.etree import ElementTree

import httpx


@dataclass(slots=True)
class RssHubFeedItem:
    title: str
    link: str
    description: str


class RssHubUnavailableError(RuntimeError):
    pass


class RssHubAdapter:
    def __init__(
        self,
        *,
        base_url: str,
        item_limit: int = 5,
        client_factory: type[httpx.Client] = httpx.Client,
    ) -> None:
        if not base_url.strip():
            raise RssHubUnavailableError("RSSHub base URL is empty")

        self.base_url = base_url.rstrip("/")
        self.item_limit = item_limit
        self.client_factory = client_factory

    def fetch_feed(self, route: str) -> list[RssHubFeedItem]:
        normalized_route = route if route.startswith("/") else f"/{route}"
        feed_url = f"{self.base_url}{normalized_route}"

        try:
            with self.client_factory(timeout=12.0, follow_redirects=True) as client:
                response = client.get(feed_url, headers={"Accept": "application/rss+xml, application/xml;q=0.9, */*;q=0.8"})
                response.raise_for_status()
        except Exception as exc:
            raise RssHubUnavailableError(str(exc)) from exc

        return self._parse_feed_items(response.text)

    def _parse_feed_items(self, payload: str) -> list[RssHubFeedItem]:
        try:
            root = ElementTree.fromstring(payload)
        except ElementTree.ParseError as exc:
            raise RssHubUnavailableError("RSSHub feed payload is not valid XML") from exc

        items: list[RssHubFeedItem] = []
        for element in root.iter():
            if not element.tag.endswith("item"):
                continue

            title = self._find_child_text(element, "title")
            link = self._find_child_text(element, "link")
            description = self._clean_html(self._find_child_text(element, "description"))
            if not title or not link:
                continue

            items.append(
                RssHubFeedItem(
                    title=title,
                    link=link,
                    description=description,
                )
            )
            if len(items) >= self.item_limit:
                break

        if not items:
            raise RssHubUnavailableError("RSSHub feed does not contain usable items")
        return items

    def _find_child_text(self, element: ElementTree.Element, child_name: str) -> str:
        for child in list(element):
            if child.tag.endswith(child_name):
                return (child.text or "").strip()
        return ""

    def _clean_html(self, value: str) -> str:
        without_tags = re.sub(r"<[^>]+>", " ", value)
        return " ".join(without_tags.split())
