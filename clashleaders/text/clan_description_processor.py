import re
from flask import escape

URL_LINK_REGEX = re.compile(r"(https?://)?([a-zA-Z0-9]+\.)?([a-zA-Z0-9]+\.(com|net|org|edu|uk|jp|ir|ru|us|ca|gg|ga|gl|ly|co|me|gd|xyz)[/\w-]*)",
                            flags=re.IGNORECASE)

REDDIT_LINK_REGEX = re.compile(r"((reddit.com)?(/r/\w+))", flags=re.IGNORECASE)


def transform_description(description):
    return " ".join([lookup(t) for t in description.split()])


def lookup(token):
    link = reddit_link(token)
    if link:
        return link

    link = regular_link(token)
    if link:
        return link

    return escape(token)


def reddit_link(token):
    if REDDIT_LINK_REGEX.match(token):
        return REDDIT_LINK_REGEX.sub(r'<a href="https://www.reddit.com\3/" target="_blank">\1</a>', token)

    return None


def regular_link(token):
    if URL_LINK_REGEX.match(token):
        return URL_LINK_REGEX.sub(regular_link_repl, token)

    return None


def regular_link_repl(match):
    if match.group(0).startswith('http'):
        return f"<a href=\"{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"
    else:
        return f"<a href=\"http://{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"
