"""JSON schemas for the Project 2 API (jsonschema, draft 7)."""
ITEM_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "price", "category", "stock"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "name": {"type": "string", "minLength": 1},
        "price": {"type": "number", "minimum": 0},
        "category": {"enum": ["office", "home", "electronics"]},
        "stock": {"type": "integer", "minimum": 0},
    },
    "additionalProperties": False,
}

ITEM_LIST_SCHEMA = {
    "type": "object",
    "required": ["total", "page", "limit", "items"],
    "properties": {
        "total": {"type": "integer", "minimum": 0},
        "page": {"type": "integer", "minimum": 1},
        "limit": {"type": "integer", "minimum": 1, "maximum": 50},
        "items": {"type": "array", "items": ITEM_SCHEMA},
    },
}
