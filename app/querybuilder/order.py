"""
OrderBy builds an ORDER BY clause from column name and direction.
Direction is validated; column name is passed through from callers.

VULNERABLE: Column name is not validated. If callers pass user input
as the column, this can be used for second-order SQLi.
"""


def order_by(column: str, direction: str) -> str:
    d = "DESC" if direction and direction.upper() == "DESC" else "ASC"
    return f"ORDER BY {column} {d}"
