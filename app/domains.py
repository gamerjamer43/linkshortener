# this module provides a trusted domain list, allowing me to whitelist certain domains.
# if it"s not whitelisted you can still access it, but i have a page to confirm you actually want to go there.

from urllib.parse import urlparse, ParseResult # url parsing
from tldextract import extract, ExtractResult  # safe domain extraciton
from flask import jsonify, Response            # jsonify and the Response type (for mypy hinting)
from validators import url                     # url validator (cuz i will NOT roll my own)
from pathlib import Path                       # for trusted domains file its used once

# trusted domain map
TRUSTED_DOMAINS: set[str] = {
    line.strip() for line in Path("alloweddomains.txt").read_text().splitlines()  # read file and build a set from the lines
    if line.strip() and not line.startswith("#")                                  # strip empty lines and comments
}

# checks if a URL is a trusted domain
def trusted(target: str) -> bool:
    try:
        # parse and normalize host
        parsed: ParseResult = urlparse(target if "://" in target else "//" + target, scheme="http")
        host: str = parsed.hostname or ""
        if not host:
            return False

        # extract registered domain and suffix
        ex: ExtractResult = extract(host)
        if not ex.domain or not ex.suffix:
            return False

        # check if domain exactly matches a trusted domain
        domain: str = f"{ex.domain}.{ex.suffix}".lower()
        return domain in TRUSTED_DOMAINS

    except Exception:
        return False

# validates url and shortener, returns a response or the sanitized values
def validate(link: str, shortener: str) -> Response | tuple[str, str]:
    # required fields
    if not link or not shortener:
        return jsonify({"error": "URL and ending are required"}), 400

    # sanitize ending
    ending: str = shortener.strip("/")
    if not ending:
        return jsonify({"error": "Invalid ending after removing slashes"}), 400

    # validate URL format
    if not url(link):
        return jsonify({"error": "Invalid URL format"}), 400

    # banned words
    if "static" in ending.lower():
        return jsonify({"error": f'"{ending}" contains a banned word and cannot be used.'}), 400

    # invalid characters and traversal
    if ".." in ending or any(c in ending for c in ["<", ">", """, """]):
        return jsonify({"error": "Invalid characters in ending"}), 400

    return link, ending