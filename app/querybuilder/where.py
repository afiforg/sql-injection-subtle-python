"""
BuildCondition produces a SQL condition fragment for a single column.
Used by repository layer to construct WHERE clauses.

VULNERABLE: This function concatenates user-controlled value into SQL
without parameterization. The injection is not in the route or
repository—only here. Security tools must follow data flow from
HTTP input through service/repository to this module to detect it.
"""


def build_condition(column: str, value: str) -> str:
    if not value:
        return "1=1"
    return f"{column} = '{value}'"
