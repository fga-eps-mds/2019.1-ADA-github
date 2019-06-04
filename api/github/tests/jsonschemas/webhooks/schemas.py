ping_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "status": {"type": "string"}
    },
    "required": ["message", "status"]
}

set_webhook_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Webhook response schema",
    "type": "object",
    "properties": {
        "success": {"type": "string"}
    },
    "required": ["success"]
}
