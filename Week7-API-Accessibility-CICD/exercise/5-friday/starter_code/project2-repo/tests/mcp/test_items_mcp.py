"""Task 5 (SOLUTION): MCP tests with pytest-asyncio. In-memory session, FakeSource, no network."""
import json

import jsonschema
import pytest
from mcp.shared.memory import create_connected_server_and_client_session as connect

from mcp_server.items_mcp_server import build_server


class FakeSource:
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
    return build_server(FakeSource())._mcp_server


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_tools_list_schema(server):
    async with connect(server) as session:
        tools = {t.name: t for t in (await session.list_tools()).tools}
    assert set(tools) == {"get_item", "search_items"}
    schema = tools["get_item"].inputSchema
    assert tools["get_item"].description
    assert schema["required"] == ["item_id"] and schema["properties"]["item_id"]["type"] == "integer"
    jsonschema.validate({"item_id": 2}, schema)                      # a valid call passes
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate({"item_id": "two"}, schema)               # wrong type is rejected
    assert "required" not in tools["search_items"].inputSchema or "category" not in tools["search_items"].inputSchema["required"]


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_get_item_success(server):
    async with connect(server) as session:
        res = await session.call_tool("get_item", {"item_id": 2})
    assert res.isError is False
    assert json.loads(res.content[0].text)["name"] == "Desk Lamp"


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_get_item_unknown_id_is_error_result(server):
    async with connect(server) as session:
        res = await session.call_tool("get_item", {"item_id": 999})
    assert res.isError is True                                        # a result, not a raised exception
    assert "not found" in res.content[0].text.lower()


@pytest.mark.mcp
@pytest.mark.asyncio
async def test_catalog_resource_read(server):
    async with connect(server) as session:
        res = await session.read_resource("items://catalog")
    items = json.loads(res.contents[0].text)
    assert [i["name"] for i in items] == ["Notebook", "Desk Lamp"]
