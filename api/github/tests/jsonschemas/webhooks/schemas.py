
set_webhook_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "Webhook response schema",
    "type": "object",
    "properties": {
        "success": {"type": "string"}
    },
    "required": ["success"]
}

not_found_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
            "message": {"type": "string"},
            "status_code": {"type": "integer"}
        },
    "required": ["message", "status_code"]
}
