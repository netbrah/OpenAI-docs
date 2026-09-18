#!/usr/bin/env python3
"""Mirror OpenAI's first-party Markdown documentation."""

from __future__ import annotations

import concurrent.futures as cf
import pathlib
import re
import shutil
import sys
import urllib.parse
import urllib.request
from urllib.error import HTTPError

ROOT_INDEXES = ("https://developers.openai.com/llms.txt",)
ALLOWED_HOSTS = {"developers.openai.com", "learn.chatgpt.com"}
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
INDEXES_DIR = REPO_ROOT / "indexes"
LINK_RE = re.compile(r"\]\((https?://[^)\s]+)\)|(?<!\()(?P<bare>https?://[^\s<>`)]+)")
USER_AGENT = "OpenAI-docs-sync/1.0 (+https://github.com/netbrah/OpenAI-docs)"
TIMEOUT = 60
MAX_WORKERS = 12


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read()


def links(text: str) -> list[str]:
    found = []
    for match in LINK_RE.finditer(text):
        url = match.group(1) or match.group("bare")
        found.append(url.rstrip(".,;:"))
    return list(dict.fromkeys(found))


def local_path(root: pathlib.Path, url: str) -> pathlib.Path:
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lstrip("/") or "index"
    if parsed.query:
        destination = pathlib.PurePosixPath(path)
        query_suffix = "__" + "__".join(
            f"{key}-{value}" for key, value in urllib.parse.parse_qsl(parsed.query)
        )
        path = str(
            destination.with_name(
                f"{destination.stem}{query_suffix}{destination.suffix}"
            )
        )
    return root / parsed.netloc / path


def discover() -> tuple[dict[str, bytes], list[str]]:
    pending = list(ROOT_INDEXES)
    indexes: dict[str, bytes] = {}
    pages: set[str] = set()
    while pending:
        url = pending.pop(0)
        if url in indexes:
            continue
        try:
            data = fetch(url)
        except Exception as exc:  # noqa: BLE001
            if url in ROOT_INDEXES:
                raise
            print(f"! skipping unavailable nested index {url}: {exc}", file=sys.stderr)
            continue
        indexes[url] = data
        for candidate in links(data.decode("utf-8", errors="replace")):
            parsed = urllib.parse.urlparse(candidate)
            if parsed.netloc not in ALLOWED_HOSTS:
                continue
            if parsed.path.endswith("/llms.txt") and candidate not in indexes:
                pending.append(candidate)
            elif parsed.path.endswith(".md"):
                pages.add(candidate)
    return indexes, sorted(pages)


def sync_page(url: str) -> tuple[str, int]:
    try:
        data = fetch(url)
    except HTTPError as exc:
        if exc.code == 404:
            return url, -1
        raise
    destination = local_path(DOCS_DIR, url)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    return url, len(data)


def main() -> int:
    print("Discovering official OpenAI documentation indexes")
    indexes, pages = discover()
    print(f"Discovered {len(indexes)} indexes and {len(pages)} Markdown pages")

    shutil.rmtree(DOCS_DIR, ignore_errors=True)
    shutil.rmtree(INDEXES_DIR, ignore_errors=True)
    errors = []
    missing = []
    total = 0
    for url, data in indexes.items():
        destination = local_path(INDEXES_DIR, url)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)

    with cf.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(sync_page, url): url for url in pages}
        for future in cf.as_completed(futures):
            try:
                url, size = future.result()
                if size == -1:
                    missing.append(url)
                    print(f"! upstream index points to missing page {url}", file=sys.stderr)
                    continue
                total += size
            except Exception as exc:  # noqa: BLE001
                errors.append((futures[future], str(exc)))
                print(f"! {futures[future]}: {exc}", file=sys.stderr)

    missing_file = REPO_ROOT / "missing-pages.txt"
    if missing:
        missing_file.write_text(
            "# URLs advertised by official indexes but returning HTTP 404\n"
            + "".join(f"{url}\n" for url in sorted(missing)),
            encoding="utf-8",
        )
    elif missing_file.exists():
        missing_file.unlink()

    print(
        f"Wrote {len(pages) - len(errors) - len(missing)}/{len(pages)} pages "
        f"({total / 1048576:.1f} MiB); {len(missing)} upstream 404s"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
