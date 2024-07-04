# -*- coding: utf-8 -*-
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict
from solana.transaction import Transaction
from solders.pubkey import Pubkey


# `reference` in the [Solana Actions spec](https://github.com/solana-labs/solana-pay/blob/master/SPEC.md#reference).
class Reference(Pubkey):
    ...


# `memo` in the [Solana Actions spec](https://github.com/solana-labs/solana-pay/blob/master/SPEC.md#memo
class Memo(str):
    ...


class ActionsJson(BaseModel):
    rules: List["ActionRuleObject"]


class ActionRuleObject(BaseModel):
    pathPattern: str
    apiPath: str


class ActionRequestURLFields(BaseModel):
    link: str
    label: Optional[str] = None
    message: Optional[str] = None


class BlinkURLFields(BaseModel):
    blink: str
    action: ActionRequestURLFields


class ActionParameter(BaseModel):
    name: str
    label: Optional[str] = None
    required: Optional[bool] = False


class LinkedAction(BaseModel):
    href: str
    label: str
    parameters: Optional[List[ActionParameter]] = None


class ActionError(BaseModel):
    message: str


class ActionGetResponse(BaseModel):
    icon: str
    title: str
    description: str
    label: str
    disabled: Optional[bool] = None
    links: Optional[dict] = None
    error: Optional[ActionError] = None


class ActionPostRequest(BaseModel):
    account: str


class ActionPostResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    transaction: Transaction | str
    message: Optional[str] = None


# Pydantic cannot use constants loaded from .constants here, unfortunately
SupportedProtocols: Optional[
    Literal["solana-actions://", "solana-action://", "solana://"]
] = None
ActionsJson.update_forward_refs()
