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
    "properties": {
            "title": {"type": "string"},
            "body": {"type": "string"},
            "html_url": {"type": "string"}
        },
    "required": ["title", "body", "html_url"]
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

not_found_user_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
            "status_code": {"type": "integer"}
        },
    "required": ["status_code"]
}

comment_issue_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
            "body": {"type": "string"}
        },
    "required": ["body"]
}
