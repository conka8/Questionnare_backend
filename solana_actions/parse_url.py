# -*- coding: utf-8 -*-
from typing import Union
from urllib.parse import parse_qs, unquote, urlparse

from pydantic import BaseModel

from .constants import (
    BLINKS_QUERY_PARAM,
    HTTPS_PROTOCOL,
    SOLANA_ACTIONS_PROTOCOL,
    SOLANA_ACTIONS_PROTOCOL_PLURAL,
    SOLANA_PAY_PROTOCOL,
)


class ParseURLError(Exception):
    pass


class ActionRequestURLFields(BaseModel):
    link: str
    label: str | None = None
    message: str | None = None


class BlinkURLFields(BaseModel):
    blink: str
    action: ActionRequestURLFields


def parse_url(url: str) -> Union[ActionRequestURLFields, BlinkURLFields]:
    if len(url) > 2048:
        raise ParseURLError("length invalid")

    parsed_url = urlparse(url)

    if parsed_url.scheme in ("http", "https"):
        return parse_blink_url(parsed_url)

    if parsed_url.scheme not in (
        SOLANA_PAY_PROTOCOL[:-1],
        SOLANA_ACTIONS_PROTOCOL[:-1],
        SOLANA_ACTIONS_PROTOCOL_PLURAL[:-1],
    ):
        raise ParseURLError("protocol invalid")

    if not parsed_url.path:
        raise ParseURLError("pathname missing")

    if not any(char in parsed_url.path for char in [":", "%"]):
        raise ParseURLError("pathname invalid")

    return parse_action_request_url(parsed_url)


def parse_action_request_url(parsed_url) -> ActionRequestURLFields:
    path = unquote(parsed_url.path)
    link = urlparse(path)
    if link.scheme != HTTPS_PROTOCOL[:-1]:
        raise ParseURLError("link invalid")

    query_params = parse_qs(parsed_url.query)

    return ActionRequestURLFields(
        link=path,
        label=query_params.get("label", [None])[0],
        message=query_params.get("message", [None])[0],
    )


def parse_blink_url(parsed_url) -> BlinkURLFields:
    query_params = parse_qs(parsed_url.query)
    link = query_params.get(BLINKS_QUERY_PARAM, [None])[0]

    if not link:
        raise ParseURLError("invalid blink url")

    return BlinkURLFields(blink=(parsed_url.geturl()), action=parse_url(link))
