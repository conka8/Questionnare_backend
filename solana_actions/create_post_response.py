# -*- coding: utf-8 -*-
import base64
from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from solders.keypair import Keypair
from solders.pubkey import Pubkey

from .action_identity import (
    create_action_identifier_instruction,
    get_action_identity_from_env,
)
from .constants import MEMO_PROGRAM_ID
from .types import ActionPostResponse, Reference


class CreatePostResponseError(Exception):
    pass


class CreateActionPostResponseArgs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    fields: ActionPostResponse
    signers: Optional[List[Keypair]] = None
    action_identity: Optional[Keypair] = None
    reference: Optional[Reference] = None
    options: Optional[dict] = None


def create_post_response(
    args: CreateActionPostResponseArgs,
) -> ActionPostResponse:
    transaction = args.fields.transaction

    if not transaction.recent_blockhash:
        transaction.recent_blockhash = "11111111111111111111111111111111"

    if not args.action_identity:
        try:
            args.action_identity = get_action_identity_from_env()
        except Exception:
            args.action_identity = None

    if len(transaction.instructions) <= 0:
        raise CreatePostResponseError("at least 1 instruction is required")

    if args.action_identity:
        instruction_data = create_action_identifier_instruction(
            args.action_identity, args.reference
        )
        transaction.add(instruction_data["instruction"])

        memo_id = Pubkey.from_string(MEMO_PROGRAM_ID)
        non_memo_index = next(
            (
                i
                for i, ix in enumerate(transaction.instructions)
                if ix.program_id != memo_id
            ),
            -1,
        )
        if non_memo_index == -1:
            raise CreatePostResponseError(
                "transaction requires at least 1 non-memo instruction"
            )

        transaction.instructions[non_memo_index].keys.extend(
            [
                {
                    "pubkey": args.action_identity.public_key,
                    "is_signer": False,
                    "is_writable": False,
                },
                {
                    "pubkey": instruction_data["reference"],
                    "is_signer": False,
                    "is_writable": False,
                },
            ]
        )

    if args.signers:
        for signer in args.signers:
            transaction.sign(signer)

    args.fields.transaction = base64.b64encode(bytes(transaction._solders)).decode(
        "ascii"
    )
    return ActionPostResponse(**args.fields.dict())
