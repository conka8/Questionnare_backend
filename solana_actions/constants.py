# -*- coding: utf-8 -*-
from typing import Dict

SOLANA_PAY_PROTOCOL = "solana:"
SOLANA_ACTIONS_PROTOCOL = "solana-action:"
SOLANA_ACTIONS_PROTOCOL_PLURAL = "solana-actions:"
HTTPS_PROTOCOL = "https:"
MEMO_PROGRAM_ID = "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
BLINKS_QUERY_PARAM = "action"

ACTIONS_CORS_HEADERS: Dict[str, str] = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,PUT,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, Content-Encoding, Accept-Encoding",
    "Content-Type": "application/json",
}
