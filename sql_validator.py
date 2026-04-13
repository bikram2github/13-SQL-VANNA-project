import re

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "EXEC",
    "GRANT", "REVOKE", "SHUTDOWN"
]

FORBIDDEN_PATTERNS = [
    r"\bxp_\w+",   
    r"\bsp_\w+",  
]

FORBIDDEN_TABLES = [
    "sqlite_master"
]


def validate_sql(query: str):
    q = query.strip().upper()


    if not q.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in q:
            return False, f"Forbidden keyword detected: {keyword}"


    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, q):
            return False, "Forbidden SQL pattern detected."


    for table in FORBIDDEN_TABLES:
        if table.upper() in q:
            return False, f"Access to system table '{table}' is not allowed."

    return True, "Query is safe."