# -*- coding: utf-8 -*-

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from solana.rpc.api import Client
from solana.transaction import Instruction, Transaction
from solders.compute_budget import set_compute_unit_price
from solders.instruction import AccountMeta
from solders.pubkey import Pubkey

from solana_actions.constants import MEMO_PROGRAM_ID
from solana_actions.create_post_response import (
    CreateActionPostResponseArgs,
    create_post_response,
)
from solana_actions.types import ActionPostResponse

SOLANA_API = "https://api.devnet.solana.com"


app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def ensure_cors_headers(request: Request, call_next):
    response = await call_next(request)
    # response.headers.update(ACTIONS_CORS_HEADERS)
    # response.content_type = "application/json"
    return response


@app.get("/actions.json")
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


@app.get("/api/actions/memo")
def get_actions_memo():
    return {
        "title": "Actions Example - Simple On-chain Memo",
        "icon": "/solana_devs.jpg",
        "description": "Send a message on-chain using a Memo",
        "label": "Send Memo",
    }


@app.post("/api/actions/memo")
async def post_actions_memo(request: Request):
    body = await request.json()
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
    uvicorn.run(app, port=5000)
