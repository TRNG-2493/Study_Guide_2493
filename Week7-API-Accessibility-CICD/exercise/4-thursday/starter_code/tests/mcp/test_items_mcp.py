"""Task 5: MCP tests with pytest-asyncio (marker: mcp). In-memory session, FakeSource, no network."""
import json

import pytest
from mcp.shared.memory import create_connected_server_and_client_session as connect

from mcp_server.items_mcp_server import build_server


class FakeSource:
    """Injectable stand-in for the Project 2 API."""
    ITEMS = [
        {"id": 1, "name": "Notebook", "price": 4.5, "category": "office", "stock": 100},
        {"id": 2, "name": "Desk Lamp", "price": 24.99, "category": "home", "stock": 15},
    ]

    def get_item(self, item_id):
        return next((dict(i) for i in self.ITEMS if i["id"] == item_id), None)

    def list_items(self, category=None):
        return [dict(i) for i in self.ITEMS if category in (None, i["category"])]


@pytest.fixture
def server():
    # Isolated in ONE fixture: `_mcp_server` is internal and may change in a future SDK.
    return build_server(FakeSource())._mcp_server


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_tools_list_schema(server):
    pytest.skip("TODO 1: list_tools(); assert the tool names, get_item's description is non-empty, and "
                "its inputSchema requires 'item_id' of type 'integer' (try jsonschema.validate too).")


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_get_item_success(server):
    pytest.skip("TODO 2: call_tool('get_item', {'item_id': 2}); assert isError is False and the payload "
                "(json.loads of content[0].text) has name 'Desk Lamp'.")


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_get_item_unknown_id_is_error_result(server):
    pytest.skip("TODO 3: call_tool('get_item', {'item_id': 999}); a tool failure is an isError RESULT, "
                "not a raised exception. Assert isError is True and 'not found' appears in the text.")


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_catalog_resource_read(server):
    pytest.skip("TODO 4: read_resource('items://catalog'); json.loads(contents[0].text) is a list of 2 items.")
