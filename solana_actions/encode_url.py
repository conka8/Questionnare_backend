# -*- coding: utf-8 -*-
from typing import Union
from urllib.parse import urlencode

from .constants import BLINKS_QUERY_PARAM, SOLANA_ACTIONS_PROTOCOL
from .types import (
    ActionRequestURLFields,
    BlinkURLFields,
    SupportedProtocols,
)


class EncodeURLError(Exception):
    pass


def encode_url(
    fields: Union[ActionRequestURLFields, BlinkURLFields],
    protocol: SupportedProtocols = SOLANA_ACTIONS_PROTOCOL,
) -> str:
    if isinstance(fields, BlinkURLFields):
        return encode_blink_url(fields, protocol)
    return encode_action_request_url(fields, protocol)


def encode_action_request_url(
    fields: ActionRequestURLFields,
    protocol: SupportedProtocols = SOLANA_ACTIONS_PROTOCOL,
) -> str:

    # TODO: do we maybe need a urllib.parse.quote around this?
    pathname = str(fields.link).rstrip("/")
    print(protocol)
    url = f"{protocol}{pathname}"

    params = {}
    if fields.label:
        params["label"] = fields.label
    if fields.message:
        params["message"] = fields.message

    if params:
        url += "?" + urlencode(params)

    return url


def encode_blink_url(
    fields: BlinkURLFields, protocol: SupportedProtocols = SOLANA_ACTIONS_PROTOCOL
) -> str:
    blink_url = str(fields.blink)
    action_url = encode_action_request_url(fields.action, protocol)

    separator = "&" if "?" in blink_url else "?"
    # TODO: do we maybe need a urllib.parse.quote around action_url?
    return f"{blink_url}{separator}{BLINKS_QUERY_PARAM}={(action_url)}"
