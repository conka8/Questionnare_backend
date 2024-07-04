# -*- coding: utf-8 -*-
from typing import List, Optional, Union

import base58
import nacl.signing
from pydantic import BaseModel
from solana.rpc.api import Client
from solana.transaction import Instruction
from solders.keypair import Keypair
from solders.pubkey import Pubkey

from .constants import MEMO_PROGRAM_ID, SOLANA_ACTIONS_PROTOCOL
from .find_reference import find_reference
from .types import Reference


class ActionsIdentitySchema(BaseModel):
    separator: str = ":"
    protocol: str = SOLANA_ACTIONS_PROTOCOL.replace(":", "")
    scheme: dict = {
        "protocol": 0,
        "identity": 1,
        "reference": 2,
        "signature": 3,
    }


ACTIONS_IDENTITY_SCHEMA = ActionsIdentitySchema()


class ActionIdentifierError(Exception):
    pass


def create_action_identifier_memo(identity: Keypair, reference: Reference) -> str:
    signature = nacl.signing.SigningKey(identity.secret_key()).sign(
        reference.to_bytes()
    )[:64]

    identifier = [""] * len(ACTIONS_IDENTITY_SCHEMA.scheme)
    identifier[
        ACTIONS_IDENTITY_SCHEMA.scheme["protocol"]
    ] = ACTIONS_IDENTITY_SCHEMA.protocol
    identifier[ACTIONS_IDENTITY_SCHEMA.scheme["identity"]] = str(identity.public_key)
    identifier[ACTIONS_IDENTITY_SCHEMA.scheme["reference"]] = str(reference)
    identifier[ACTIONS_IDENTITY_SCHEMA.scheme["signature"]] = base58.b58encode(
        signature
    ).decode()

    return ACTIONS_IDENTITY_SCHEMA.separator.join(identifier)


def validate_action_identifier_memo(
    identity: Pubkey, memos: Union[str, List[str], None]
) -> Union[bool, dict]:
    if not memos:
        return False

    if isinstance(memos, str):
        memos = memos.split(";")

    for memo in memos:
        try:
            memo = memo.strip()
            if memo.startswith("[") and "] " in memo:
                memo = memo.split("] ", 1)[1].strip()

            if not memo.count(":") >= 2:
                raise ActionIdentifierError("invalid memo formatting")

            identifier = memo.split(ACTIONS_IDENTITY_SCHEMA.separator)
            if len(identifier) != len(ACTIONS_IDENTITY_SCHEMA.scheme):
                raise ActionIdentifierError("invalid memo length")

            try:
                memo_identity = Pubkey.from_string(
                    identifier[ACTIONS_IDENTITY_SCHEMA.scheme["identity"]]
                )
            except ValueError:
                raise ActionIdentifierError("malformed memo identity")

            if not memo_identity:
                raise ActionIdentifierError("invalid memo identity")
            if str(memo_identity) != str(identity):
                raise ActionIdentifierError("identity mismatch")

            verified = nacl.signing.VerifyKey(bytes(identity)).verify(
                base58.b58decode(
                    identifier[ACTIONS_IDENTITY_SCHEMA.scheme["reference"]]
                ),
                base58.b58decode(
                    identifier[ACTIONS_IDENTITY_SCHEMA.scheme["signature"]]
                ),
            )

            if verified:
                return {
                    "verified": True,
                    "reference": identifier[
                        ACTIONS_IDENTITY_SCHEMA.scheme["reference"]
                    ],
                }
        except Exception:
            return False
    return False


def verify_signature_info_for_identity(
    connection: Client, identity: Keypair, sig_info: dict
) -> bool:
    try:
        validated = validate_action_identifier_memo(
            identity.public_key, sig_info.get("memo")
        )
        if not validated:
            return False

        confirmed_sig_info = find_reference(
            connection, Pubkey.from_string(validated["reference"])
        )

        if confirmed_sig_info["signature"] == sig_info["signature"]:
            return True
    except Exception:
        return False
    return False


def create_action_identifier_instruction(
    identity: Keypair, reference: Optional[Pubkey] = None
) -> dict:
    if reference is None:
        reference = Keypair().public_key

    memo = create_action_identifier_memo(identity, reference)

    return {
        "memo": memo,
        "reference": reference,
        "instruction": Instruction(
            program_id=Pubkey.from_string(MEMO_PROGRAM_ID),
            data=memo.encode("utf-8"),
            keys=[],
        ),
    }


def get_action_identity_from_env(env_key: str = "ACTION_IDENTITY_SECRET") -> Keypair:
    import json
    import os

    try:
        if env_key not in os.environ:
            raise ValueError("missing env key")
        return Keypair.from_secret_key(bytes(json.loads(os.environ[env_key])))
    except Exception:
        raise ValueError(f"invalid identity in env variable: '{env_key}'")
