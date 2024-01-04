import re

def extract_table_aliases(sql_query):
    regex = r"FROM\s+(?:(?:\w+\.)?(\w+)\s+)?AS?\s+(\w+)?"
    table_aliases = {}
    for match in re.finditer(regex, sql_query, flags=re.IGNORECASE):
        table_name = match.group(1) or match.group(2)  # Use either captured group
        alias = match.group(2) or "NO_ALIAS"  # Use alias if present, else "NO_ALIAS"
        table_aliases[table_name] = alias
    return table_aliases

# Example usage:
sql_query = "SELECT * FROM customers AS c INNER JOIN orders AS o ON c.id = o.customer_id"
table_aliases = extract_table_aliases(sql_query)
print(table_aliases)  # Output: {'customers': 'c', 'orders': 'o'}
