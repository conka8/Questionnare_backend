# -*- coding: utf-8 -*-
import pytest
from solana.rpc.async_api import AsyncClient
from solders.keypair import Keypair
from solders.pubkey import Pubkey

from solana_actions.find_reference import (
    FindReferenceError,
    find_reference,
)


@pytest.fixture
def mock_connection():
    reference = Keypair().pubkey
    signatures_for_address = {str(reference): [{"signature": "signature"}]}

    class MockConnection(AsyncClient):
        async def get_signatures_for_address(self, reference: Pubkey, **kwargs):
            return signatures_for_address.get(str(reference), [])

    return MockConnection("http://localhost:8899"), reference


@pytest.mark.asyncio
async def test_find_reference_returns_last_signature(mock_connection):
    connection, reference = mock_connection
    found = await find_reference(connection, reference)
    assert found == {"signature": "signature"}


@pytest.mark.asyncio
async def test_find_reference_throws_error_on_signature_not_found(mock_connection):
    connection, _ = mock_connection
    reference = Keypair().pubkey

    with pytest.raises(FindReferenceError, match="not found"):
        await find_reference(connection, reference)
