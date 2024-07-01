from solana.transaction import Transaction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.commitment import Confirmed
from typing import List, Optional
from pydantic import BaseModel

from .types import ActionPostResponse, Reference
from .constants import MEMO_PROGRAM_ID
from .action_identity import (
    create_action_identifier_instruction,
    get_action_identity_from_env,
)


class CreatePostResponseError(Exception):
    pass


class CreateActionPostResponseArgs(BaseModel):
    fields: ActionPostResponse
    signers: Optional[List[Keypair]] = None
    action_identity: Optional[Keypair] = None
    reference: Optional[Reference] = None
    options: Optional[dict] = None


async def create_post_response(
    args: CreateActionPostResponseArgs,
) -> ActionPostResponse:
    transaction = args.fields.transaction

    if not transaction.recent_blockhash:
        transaction.recent_blockhash = "11111111111111111111111111111111"

    if not args.action_identity:
        try:
            args.action_identity = get_action_identity_from_env()
        except Exception:
            pass

    if len(transaction.instructions) <= 0:
        raise CreatePostResponseError("at least 1 instruction is required")

    if args.action_identity:
        instruction_data = create_action_identifier_instruction(
            args.action_identity, args.reference
        )
        transaction.add(instruction_data["instruction"])

        memo_id = Pubkey(MEMO_PROGRAM_ID)
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

    return ActionPostResponse(
        **args.fields.dict(), transaction=transaction.serialize().hex()
    )
