"""Items MCP server skeleton (MCP SDK 1.x: `pip install "mcp<2"`).

Exposes the Project 2 items to an AI client:
  tool      get_item(item_id: int)            -> one item as a dict; unknown id => error
  tool      search_items(category: str|None)  -> {"total": n, "items": [...]}
  resource  items://catalog                   -> JSON text of ALL items

The data comes from an injectable "source" so tests never need the real API:
  build_server(source=FakeSource())   # tests
  build_server()                      # real: ApiItemsSource -> http://127.0.0.1:8000

RULE: never print() to stdout in a stdio server (it corrupts the JSON-RPC stream).
Run for real (stdio):  python -m mcp_server.items_mcp_server
"""
import json
import os

import requests
from mcp.server.fastmcp import FastMCP


class ApiItemsSource:
    """Reads items from the Project 2 API. Provided; you do not need to change it."""

    def __init__(self, base_url=None, timeout=5):
        self.base_url = (base_url or os.getenv("BASE_URL", "http://127.0.0.1:8000")).rstrip("/")
        self.timeout = timeout

    def get_item(self, item_id):
        """Return the item dict, or None when the API answers 404."""
        r = requests.get(f"{self.base_url}/items/{item_id}", timeout=self.timeout)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def list_items(self, category=None):
        params = {"limit": 50}
        if category:
            params["category"] = category
        r = requests.get(f"{self.base_url}/items", params=params, timeout=self.timeout)
        r.raise_for_status()
        return r.json()["items"]


def build_server(source=None) -> FastMCP:
    src = source or ApiItemsSource()
    mcp = FastMCP("project2-items")

    @mcp.tool()
    def get_item(item_id: int) -> dict:
        """Return one Project 2 item by its numeric id."""
        # TODO 1: call src.get_item(item_id); return the dict.
        #         If it returns None, raise ValueError(f"Item {item_id} not found")
        #         (FastMCP turns an exception into an isError result, not a crash).
        raise NotImplementedError("TODO 1: implement get_item")

    @mcp.tool()
    def search_items(category: str | None = None) -> dict:
        """List items, optionally filtered by category (office, home, electronics)."""
        # TODO 2: items = src.list_items(category); return {"total": len(items), "items": items}
        raise NotImplementedError("TODO 2: implement search_items")

    @mcp.resource("items://catalog")
    def catalog() -> str:
        """The full item catalogue as JSON text."""
        # TODO 3: return json.dumps(src.list_items())
        raise NotImplementedError("TODO 3: implement the catalog resource")

    return mcp


if __name__ == "__main__":
    build_server().run()  # stdio transport
