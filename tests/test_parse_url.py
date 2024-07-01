# -*- coding: utf-8 -*-
from urllib.parse import parse_qs, quote, urlparse

import pytest

from solana_actions.parse_url import (
    ActionRequestURLFields,
    BlinkURLFields,
    ParseURLError,
    parse_url,
)


def test_allow_solana_pay_protocol():
    url = "solana:https://example.com/api/action"
    result = parse_url(url)
    assert isinstance(result, ActionRequestURLFields)
    assert str(result.link) == "https://example.com/api/action"


def test_allow_solana_action_protocol():
    url = "solana-action:https://example.com/api/action"
    result = parse_url(url)
    assert isinstance(result, ActionRequestURLFields)
    assert str(result.link) == "https://example.com/api/action"


def test_parse_simple_action_url():
    url = "solana-action:https://example.com/api/action"
    result = parse_url(url)
    assert isinstance(result, ActionRequestURLFields)
    assert str(result.link) == "https://example.com/api/action"


def test_parse_action_url_with_action_params():
    url = "solana-action:https%3A%2F%2Fexample.com%2Fapi%2Faction%3Famount%3D1337%26another%3Dyes"
    result = parse_url(url)
    assert isinstance(result, ActionRequestURLFields)
    assert str(result.link) == "https://example.com/api/action?amount=1337&another=yes"


def test_parse_action_url_with_extra_action_params():
    url = "solana-action:https://example.com/api/action?label=Michael&message=Thanks%20for%20all%20the%20fish"
    result = parse_url(url)
    assert isinstance(result, ActionRequestURLFields)
    assert str(result.link) == "https://example.com/api/action"
    assert result.label == "Michael"
    assert result.message == "Thanks for all the fish"


def test_parse_action_url_with_query_params_and_action_params():
    url = "solana-action:https%3A%2F%2Fexample.com%2Fapi%2Faction%3Famount%3D1337%26another%3Dyes?label=Michael&message=Thanks%20for%20all%20the%20fish"
    result = parse_url(url)
    assert isinstance(result, ActionRequestURLFields)
    assert str(result.link) == "https://example.com/api/action?amount=1337&another=yes"
    assert result.label == "Michael"
    assert result.message == "Thanks for all the fish"


def test_parse_blinks_without_action_query_params():
    action_link = "https://action.com/api/action"
    action_url = f"solana-action:{quote(action_link)}"
    url = f"https://blink.com/?other=one&action={quote(action_url)}"

    result = parse_url(url)
    assert isinstance(result, BlinkURLFields)
    assert str(result.blink) == url
    assert parse_qs(urlparse(result.blink).query)["action"][0] == action_url
    assert str(result.action.link) == action_link


def test_parse_blinks_with_action_query_params():
    action_link = "https://action.com/api/action?query=param"
    action_url = f"solana-action:{quote(action_link)}?label=Michael&message=Thanks%20for%20all%20the%20fish"
    url = f"https://blink.com/?other=one&action={quote(action_url)}"

    result = parse_url(url)
    assert isinstance(result, BlinkURLFields)
    assert str(result.blink) == url
    assert parse_qs(urlparse(result.blink).query)["action"][0] == action_url
    assert str(result.action.link) == action_link
    assert result.action.label == "Michael"
    assert result.action.message == "Thanks for all the fish"


def test_error_on_invalid_length():
    url = "X" * 2049
    with pytest.raises(ParseURLError, match="length invalid"):
        parse_url(url)


def test_error_on_invalid_protocol():
    url = "eth:0xffff"
    with pytest.raises(ParseURLError, match="protocol invalid"):
        parse_url(url)


def test_error_on_missing_pathname():
    url = "solana-action:"
    with pytest.raises(ParseURLError, match="pathname missing"):
        parse_url(url)


def test_error_on_invalid_pathname():
    url = "solana-action:0xffff"
    with pytest.raises(ParseURLError, match="pathname invalid"):
        parse_url(url)


def test_error_on_invalid_blink_urls():
    url = "https://blink.com/?other=one&action="
    with pytest.raises(ParseURLError, match="invalid blink url"):
        parse_url(url)


def test_error_on_invalid_protocol_in_blink_action_param():
    url = "https://blink.com/?other=one&action=unknown-protocol%3Ahttps%253A%252F%252Faction.com%252Fapi%252Faction%253Fquery%253Dparam"
    with pytest.raises(ParseURLError, match="protocol invalid"):
        parse_url(url)


def test_error_on_invalid_link_in_blink_action_param():
    url = "https://blink.com/?other=one&action=solana-action%3Aftp%253A%252F%252Faction.com%252Fapi%252Faction%253Fquery%253Dparam"
    with pytest.raises(ParseURLError, match="link invalid"):
        parse_url(url)
