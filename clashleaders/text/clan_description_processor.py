import re

from flask import escape, url_for

from clashleaders.clash.transformer import tag_to_slug

URL_LINK_REGEX = re.compile(
    r"(https?://)?([a-zA-Z0-9]+\.)?([a-zA-Z0-9]+\.(com|net|org|edu|uk|jp|ir|ru|us|ca|gg|ga|gl|ly|co|me|gd|xyz)[/\w-]*)",
    flags=re.IGNORECASE,
)

REDDIT_LINK_REGEX = re.compile(r"((reddit.com)?(/r/\w+))", flags=re.IGNORECASE)

TAG_REGEX = re.compile(r"(.*)(#[A-Z0-9]+)(.*)", flags=re.IGNORECASE)


def transform_description(description):
    return " ".join([lookup(t) for t in description.split()])


def lookup(token):
    if link := reddit_link(token):
        return link

    if link := regular_link(token):
        return link

    if link := clashleader_link(token):
        return link

    return escape(token)


def clashleader_link(token):
    if match := TAG_REGEX.match(token):
        if slug := tag_to_slug(match.group(2)):
            return f'{match.group(1)}<a href="{url_for("clan_detail_page", slug=slug)}">{match.group(2)}</a>{match.group(3)}'
        else:
            return f'{match.group(1)}<a href="{url_for("tagged_clans", tag=match.group(2).lower().lstrip("#"))}">{match.group(2)}</a>{match.group(3)}'

    return None


def reddit_link(token):
    if REDDIT_LINK_REGEX.match(token):
        return REDDIT_LINK_REGEX.sub(
            r'<a href="https://www.reddit.com\3/" target="_blank">\1</a>', token
        )

    return None


def regular_link(token):
    if URL_LINK_REGEX.match(token):
        return URL_LINK_REGEX.sub(regular_link_repl, token)

    return None


def regular_link_repl(match):
    if match.group(0).startswith("http"):
        return f'<a href="{match.group(0)}" target="_blank">{match.group(0)}</a>'
    else:
        return f'<a href="http://{match.group(0)}" target="_blank">{match.group(0)}</a>'
