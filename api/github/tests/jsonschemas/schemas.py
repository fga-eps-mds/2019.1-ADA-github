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

create_issue_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties":{
            "title": {"type": "string"},
            "body": {"type": "string"},
            "html_url":{"type": "string"}
        },
    "required": ["title", "body", "html_url"]
}
