# -*- coding: utf-8 -*-
import functools

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from solana.rpc.api import Client
from solana.transaction import Instruction, Transaction
from solders.compute_budget import set_compute_unit_price
from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from solana_actions.constants import (
    ACTIONS_CORS_HEADERS,
    MEMO_PROGRAM_ID,
)
from solana_actions.create_post_response import (
    CreateActionPostResponseArgs,
    create_post_response,
)
from solana_actions.types import ActionPostResponse

SOLANA_API = "https://api.devnet.solana.com"


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def return_json(f):
    @functools.wraps(f)
    def inner(**kwargs):
        ret = f(**kwargs)
        response = make_response(jsonify(ret))
        response.headers.update(ACTIONS_CORS_HEADERS)
        response.content_type = "application/json"
        response.status_code = 200
        return response

    return inner


@app.route("/actions.json", methods=["GET", "OPTIONS"])
@return_json
def actions_json():
    return {
        "rules": [
            # map all root level routes to an action
            {
                "pathPattern": "/*",
                "apiPath": "/api/actions/*",
            },
            # idempotent rule as the fallback
            {
                "pathPattern": "/api/actions/**",
                "apiPath": "/api/actions/**",
            },
        ],
    }


@app.route("/api/actions/memo", methods=["GET", "OPTIONS"])
@return_json
def get_actions_memo():
    return {
        "title": "Actions Example - Simple On-chain Memo",
        "icon": "/solana_devs.jpg",
        "description": "Send a message on-chain using a Memo",
        "label": "Send Memo",
    }


@app.route("/api/actions/memo", methods=["POST"])
@return_json
def post_actions_memo():
    body = request.get_json(force=True)
    # NOTE: you may want to do validation here

    account = Pubkey.from_string(body["account"])
    # NOTE: do some basic validation and exception handling

    connection = Client(SOLANA_API)
    latest_block_hash = connection.get_latest_blockhash()
    transaction = Transaction(
        recent_blockhash=latest_block_hash.value.blockhash, fee_payer=account
    ).add(
        set_compute_unit_price(
            micro_lamports=1000,
        ),
        Instruction(
            program_id=Pubkey.from_string(MEMO_PROGRAM_ID),
            data=b"this is a simple memo message2",
            accounts=[AccountMeta(account, is_signer=True, is_writable=True)],
        ),
    )

    actions_args: ActionPostResponse = ActionPostResponse(
        transaction=transaction,
        message="Post this memo on-chain",
    )
    payload: ActionPostResponse = create_post_response(
        args=CreateActionPostResponseArgs(
            fields=actions_args,
            # no additional signers are required for this transaction
            signers=None,
        )
    )
    return payload.model_dump()


if __name__ == "__main__":
    app.run(port=5000)
