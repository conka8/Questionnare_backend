# -*- coding: utf-8 -*-
from urllib.parse import parse_qs, urlparse

from solana_actions.encode_url import (
    ActionRequestURLFields,
    BlinkURLFields,
    encode_url,
)


def test_action_request_url_without_params():
    link = "https://example.com/api/action"
    url = encode_url(ActionRequestURLFields(link=link))
    assert str(url) == f"solana-action:{link}"


def test_action_request_url_with_params():
    link = "https://example.com/api/action"
    label = "label"
    message = "message"
    url = encode_url(ActionRequestURLFields(link=link, label=label, message=message))
    assert str(url) == f"solana-action:{link}?label={label}&message={message}"


def test_action_request_url_with_query_params():
    link = "https://example.com/api/action?query=param"
    url = encode_url(ActionRequestURLFields(link=link))
    assert str(url) == f"solana-action:{(link)}"


def test_action_request_url_with_query_and_action_params():
    link = "https://example.com/api/action?query=param&amount=1337"
    label = "label"
    message = "message"
    url = encode_url(ActionRequestURLFields(link=link, label=label, message=message))
    assert str(url) == f"solana-action:{(link)}?label={label}&message={message}"


def test_blink_url_without_action_params():
    blink = "https://blink.com/"
    link = "https://action.com/api/action"
    url = encode_url(
        BlinkURLFields(blink=blink, action=ActionRequestURLFields(link=link))
    )
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    assert query_params["action"][0] == (f"solana-action:{link}")


def test_blink_url_with_action_params():
    blink = "https://blink.com/"
    link = "https://action.com/api/action?query=param"
    url = encode_url(
        BlinkURLFields(blink=blink, action=ActionRequestURLFields(link=link))
    )
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    assert query_params["action"][0] == (f"solana-action:{(link)}")


def test_blink_url_with_query_params_without_action_params():
    blink = "https://blink.com/?other=one"
    link = "https://action.com/api/action"
    url = encode_url(
        BlinkURLFields(blink=blink, action=ActionRequestURLFields(link=link))
    )
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    assert query_params["action"][0] == (f"solana-action:{link}")


def test_blink_url_with_query_params_and_action_params():
    blink = "https://blink.com/?other=one"
    link = "https://action.com/api/action?query=param"
    url = encode_url(
        BlinkURLFields(blink=blink, action=ActionRequestURLFields(link=link))
    )
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    assert query_params["action"][0] == (f"solana-action:{(link)}")
