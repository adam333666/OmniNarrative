from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class CrawlDocument:
    source_url: str
    title: str
    markdown: str


class Crawl4AIUnavailableError(RuntimeError):
    pass


class Crawl4AIAdapter:
    def __init__(self) -> None:
        try:
            from crawl4ai import AsyncWebCrawler, CrawlerRunConfig  # type: ignore
        except Exception as exc:  # pragma: no cover - depends on optional runtime dependency
            raise Crawl4AIUnavailableError(str(exc)) from exc

        self._crawler_cls = AsyncWebCrawler
        self._config_cls = CrawlerRunConfig

    async def fetch_document(self, source_url: str) -> CrawlDocument:
        async with self._crawler_cls() as crawler:
            config = self._config_cls(word_count_threshold=40)
            result = await crawler.arun(source_url, config=config)

        markdown = getattr(result, "markdown", None) or getattr(result, "cleaned_html", None) or getattr(result, "html", None)
        if not getattr(result, "success", False) or markdown is None:
            raise Crawl4AIUnavailableError(f"Unable to collect usable content from {source_url}")

        title = getattr(result, "metadata", {}).get("title") if getattr(result, "metadata", None) else None
        return CrawlDocument(
            source_url=source_url,
            title=title or source_url,
            markdown=str(markdown),
        )
