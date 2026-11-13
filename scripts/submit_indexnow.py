#!/usr/bin/env python3
"""
==============================================================================
FILE: scripts/submit_indexnow.py
==============================================================================

PURPOSE:
Submits all canonical site URLs from sitemap.xml to the IndexNow Application
Programming Interface (API) so participating search engines (such as Microsoft
Bing, Yandex, Seznam, and AI search pipelines grounded by those indexes)
receive immediate crawl notifications after repository updates.

WHAT THIS FILE IS NOT FOR:
- Does not modify HTML, sitemap, or key files on disk.
- Does not require external Python packages outside the standard library.

INVARIANTS:
1. Reads the single 32-character hexadecimal IndexNow key file located at the
   repository root and confirms the file contents match the filename stem.
2. Reads canonical URLs strictly from sitemap.xml for the configured host.
3. Exits with status code 0 on dry-run or successful Hypertext Transfer
   Protocol (HTTP) 200/202 submission, and exits 1 on validation or network
   failure.
==============================================================================
"""

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Dict, List, Tuple
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

# Repository checkout root holding sitemap.xml and the IndexNow key file.
# Consumed by: locate_indexnow_key() and load_sitemap_urls().
REPO_ROOT = Path(__file__).resolve().parent.parent

# Canonical hostname registered with IndexNow (protocol prefix omitted per
# IndexNow API specification). Consumed by: build_payload().
CANONICAL_HOST = "itoldyouso.tech"

# Public Hypertext Transfer Protocol Secure (HTTPS) base URL matching the
# verification key location and sitemap entries. Consumed by: build_payload().
BASE_URL = f"https://{CANONICAL_HOST}"

# Shared IndexNow submission endpoint distributing URLs to all participating
# search engines. Value: https://api.indexnow.org/indexnow.
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"

# Maximum URLs allowed in a single IndexNow API request batch.
# Value: 10000 per protocol limit. Consumed by: submit_urls().
MAX_BATCH_URLS = 10000

# Regular expression matching a standard 32-hexadecimal-digit IndexNow key.
# Consumed by: locate_indexnow_key().
KEY_PATTERN = re.compile(r"^[0-9a-f]{32}$")

# HTTP request timeout in seconds to prevent hanging Continuous Integration
# (CI) workflow runners. Value: 30 seconds. Consumed by: post_indexnow_batch().
REQUEST_TIMEOUT_SECONDS = 30


def locate_indexnow_key(repo_root: Path) -> Tuple[str, Path]:
    """
    Locate and validate the 32-character IndexNow verification text file in the
    repository root directory.

    Args:
        repo_root: Absolute Path pointing to the repository root folder.

    Returns:
        Tuple of (key string, Path to key text file).

    Raises:
        RuntimeError: If zero or multiple candidate key files exist, or if file
        contents do not match the filename stem.
    """
    # 1. Scan repository root for *.txt files whose stem is 32 hex chars.
    candidates: List[Path] = []
    for txt_path in sorted(repo_root.glob("*.txt")):
        if KEY_PATTERN.match(txt_path.stem):
            candidates.append(txt_path)

    if len(candidates) != 1:
        raise RuntimeError(
            f"Expected exactly 1 IndexNow hex key file at repo root, "
            f"found {len(candidates)}."
        )

    # 2. Verify the key file contents match the filename without extension.
    key_path = candidates[0]
    expected_key = key_path.stem
    actual_content = key_path.read_text(encoding="utf-8").strip()
    if actual_content != expected_key:
        raise RuntimeError(
            f"Key file {key_path.name} contents do not match filename stem."
        )

    return expected_key, key_path


def load_sitemap_urls(sitemap_path: Path, expected_base: str) -> List[str]:
    """
    Parse sitemap.xml and extract all ordered public URLs matching the site
    host.

    Args:
        sitemap_path: Path to sitemap.xml.
        expected_base: Expected URL prefix (e.g. https://itoldyouso.tech).

    Returns:
        List of canonical URL strings ready for IndexNow submission.

    Raises:
        RuntimeError: If sitemap.xml is missing, invalid XML, empty, or holds
        off-host entries.
    """
    # 1. Confirm sitemap.xml exists on disk.
    if not sitemap_path.is_file():
        raise RuntimeError(f"Missing sitemap file: {sitemap_path}")

    # 2. Parse Extensible Markup Language (XML) using sitemap namespace.
    try:
        tree = ET.parse(sitemap_path)
    except ET.ParseError as exc:
        raise RuntimeError(f"Invalid XML in {sitemap_path}: {exc}") from exc

    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls: List[str] = []

    # 3. Collect and validate every <loc> URL against expected host prefix.
    for loc in tree.getroot().findall("sm:url/sm:loc", ns):
        if not loc.text:
            continue
        url = loc.text.strip()
        if not url.startswith(f"{expected_base}/"):
            raise RuntimeError(f"Unexpected off-host URL in sitemap: {url}")
        urls.append(url)

    if not urls:
        raise RuntimeError("No URLs extracted from sitemap.xml.")

    return urls


def build_payload(host: str, key: str, urls: List[str]) -> Dict[str, object]:
    """
    Construct the JavaScript Object Notation (JSON) request body specified by
    the IndexNow API.

    Args:
        host: Canonical hostname without scheme (e.g. itoldyouso.tech).
        key: Verified 32-character IndexNow API key string.
        urls: Batch of absolute canonical URLs belonging to host.

    Returns:
        Dictionary serialisable as the IndexNow POST payload.
    """
    return {
        "host": host,
        "key": key,
        "keyLocation": f"https://{host}/{key}.txt",
        "urlList": urls,
    }


def post_indexnow_batch(
    endpoint: str, payload: Dict[str, object]
) -> Tuple[int, str]:
    """
    Send one JSON payload batch to the IndexNow API endpoint over HTTPS POST.

    Args:
        endpoint: Full IndexNow API URL.
        payload: Structured IndexNow request dictionary.

    Returns:
        Tuple of (HTTP status code, decoded response body text).

    Raises:
        RuntimeError: If IndexNow returns an error HTTP status or fails at the
        network layer.
    """
    # 1. Serialise payload dictionary as UTF-8 encoded JSON bytes.
    body_bytes = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        endpoint,
        data=body_bytes,
        method="POST",
        headers={"Content-Type": "application/json; charset=utf-8"},
    )

    # 2. Execute HTTP POST and handle expected 200 OK or 202 Accepted status.
    try:
        with urllib.request.urlopen(
            request, timeout=REQUEST_TIMEOUT_SECONDS
        ) as resp:
            status = resp.getcode()
            resp_text = resp.read().decode("utf-8", errors="replace").strip()
            return status, resp_text
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace").strip()
        raise RuntimeError(
            f"IndexNow HTTP error {exc.code}: {err_body or exc.reason}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"IndexNow network failure reaching {endpoint}: {exc.reason}"
        ) from exc


def main(argv: List[str] | None = None) -> int:
    """
    Locate key file, gather canonical sitemap URLs, and submit batches to the
    IndexNow API (or print payloads when --dry-run is passed).

    Args:
        argv: Optional CLI argument list for testability.

    Returns:
        0 on clean completion, or 1 when validation or submission fails.
    """
    # 1. Parse command-line options.
    parser = argparse.ArgumentParser(
        description="Submit itoldyouso.tech URLs to IndexNow."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate key and print IndexNow payload without sending.",
    )
    args = parser.parse_args(argv)

    # 2. Locate key file and load canonical URL list from sitemap.xml.
    try:
        key, key_path = locate_indexnow_key(REPO_ROOT)
        urls = load_sitemap_urls(REPO_ROOT / "sitemap.xml", BASE_URL)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Verified IndexNow key file: {key_path.name}")
    print(f"Loaded {len(urls)} canonical URL(s) from sitemap.xml.")

    # 3. Partition URLs into protocol-compliant batches and submit or print.
    for start in range(0, len(urls), MAX_BATCH_URLS):
        batch = urls[start : start + MAX_BATCH_URLS]
        payload = build_payload(CANONICAL_HOST, key, batch)

        if args.dry_run:
            print(json.dumps(payload, indent=2))
            continue

        try:
            status, body = post_indexnow_batch(INDEXNOW_ENDPOINT, payload)
        except RuntimeError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

        print(
            f"Submitted {len(batch)} URL(s) to {INDEXNOW_ENDPOINT} "
            f"-> HTTP {status}"
        )
        if body:
            print(f"Response: {body}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
