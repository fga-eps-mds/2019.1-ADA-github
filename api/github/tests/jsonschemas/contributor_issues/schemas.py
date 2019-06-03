get_contributor_issues_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "User response schema",
    "type": "array",
    "properties": {
            "issue_number": {"type": "integer"},
            "title": {"type": "string"},
            "url": {"type": "string"}
        },
    "required": ["issue_number", "title", "url"]
}
