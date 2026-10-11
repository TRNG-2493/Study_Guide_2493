from models.item import Item, ItemOut


class ItemsApi:
    """Everything the tests know about /items lives here (paths, verbs). Methods return raw responses."""

    PATH = "/items"

    def __init__(self, client):
        self.client = client

    def list(self, **params):
        return self.client.get(self.PATH, params=params)

    def get(self, item_id):
        return self.client.get(f"{self.PATH}/{item_id}")

    def create(self, payload):
        return self.client.post(self.PATH, json=payload)

    def create_raw(self, data, headers=None):
        return self.client.post(self.PATH, data=data, headers=headers)

    def replace(self, item_id, payload):
        return self.client.put(f"{self.PATH}/{item_id}", json=payload)

    def patch(self, item_id, payload):
        return self.client.patch(f"{self.PATH}/{item_id}", json=payload)

    def delete(self, item_id):
        return self.client.delete(f"{self.PATH}/{item_id}")

    def create_ok(self, payload):
        """Create and return a parsed ItemOut; fails loudly if the API did not answer 201."""
        r = self.create(payload)
        assert r.status_code == 201, f"create failed: {r.status_code} {r.text}"
        return ItemOut.model_validate(r.json())


__all__ = ["ItemsApi", "Item"]
