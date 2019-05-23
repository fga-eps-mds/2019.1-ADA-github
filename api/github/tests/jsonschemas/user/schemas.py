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

view_get_access_token_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"] 
}

view_get_repos_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "repositories": {"type": "array"}
    },
    "required": ["repositories"]
}

utils_get_user_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "github_username": {"type": "string"},
        "github_user_id":  {"type": "string"}
    },
    "required": ["github_username", "github_user_id"]
}

view_get_github_login_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "username": {"type": "string"}
    },
    "required": ["username"]
}

invalid_view_get_repos_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}


view_notfound_get_github_login_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "message": {"type": "string"}
    },
    "required": ["message"]
}

view_register_repository_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "status": {"type": "string"}
    },
    "required": ["status"]
}

view_notfound_register_repository_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "object",
    "properties": {
        "status": {"message": "string"}
    },
    "required": ["message"]
}