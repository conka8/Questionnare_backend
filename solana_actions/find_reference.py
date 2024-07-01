# -*- coding: utf-8 -*-
from typing import Any, Dict

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey


class FindReferenceError(Exception):
    pass


async def find_reference(
    connection: AsyncClient, reference: Pubkey, options: Dict[str, Any] = {}
):
    finality = options.pop("finality", Confirmed)

    signatures = await connection.get_signatures_for_address(
        reference,
        limit=options.get("limit", 1000),
        before=options.get("before"),
        until=options.get("until"),
        commitment=finality,
    )

    if not signatures:
        raise FindReferenceError("not found")

    oldest = signatures[-1]

    if len(signatures) < options.get("limit", 1000):
        return oldest

    try:
        return await find_reference(
            connection,
            reference,
            {
                "finality": finality,
                **options,
                "before": oldest.signature,
            },
        )
    except FindReferenceError:
        return oldest
