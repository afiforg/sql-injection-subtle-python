# Subtle SQL Injection (Python / FastAPI)

Intentionally vulnerable FastAPI service for **testing security and static analysis tools**. The SQL injection is not in a single file: user input flows through several isolated layers and is concatenated into SQL only in a dedicated querybuilder package.

## Why “subtle”?

- **No raw SQL in routes** – routes only read query parameters and call the service.
- **No SQL in the service layer** – the service forwards arguments to the repository.
- **Repository does not build value strings** – it calls `querybuilder.build_condition` / `querybuilder.order_by` and uses the returned string in a query.
- **Vulnerability is only in `app/querybuilder`** – `build_condition` and `order_by` concatenate user-controlled input into SQL.

Tools that only look for `execute(...)` or string formatting in the same file as the route will miss it. Detecting this requires **data-flow / taint analysis** from request params → route → service → repository → querybuilder.

## Layout

```
sql-injection-subtle-python/
├── app/
│   ├── main.py                    # FastAPI app, wiring only
│   ├── dependencies.py            # DB connection, get_user_service
│   ├── routes/
│   │   └── users.py               # reads q, username, sort, order
│   ├── services/
│   │   └── user_service.py        # passes through to repository
│   ├── repositories/
│   │   └── user_repository.py     # builds query via querybuilder, executes
│   ├── querybuilder/
│   │   ├── where.py               # build_condition(column, value) – concatenates value
│   │   └── order.py               # order_by(column, direction) – concatenates column
│   └── database/
│       └── schema.py              # safe DDL/seed only
├── requirements.txt
├── README.md
└── poc.py
```

## Vulnerable endpoints

| Endpoint | Source of taint | Sink |
|----------|-----------------|------|
| `GET /users/search?q=` or `?username=` | `q` or `username` | `querybuilder.build_condition("username", value)` |
| `GET /users?sort=&order=` | `sort`, `order` | `querybuilder.order_by(sort, order)` |

## Setup and run

```bash
cd sql-injection-subtle-python
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Server: `http://localhost:8080`.

## Proof of concept (for tool testing)

```bash
# Normal
curl "http://localhost:8080/users/search?q=alice"
curl "http://localhost:8080/users?username=admin"

# SQLi via search (WHERE clause)
curl "http://localhost:8080/users/search?q=alice' OR '1'='1"
curl "http://localhost:8080/users/search?username=admin'--"

# SQLi via sort (ORDER BY / second-order)
curl "http://localhost:8080/users?sort=id;(SELECT 1)--&order=asc"
```

Run the PoC script (starts server, sends requests, reports result):

```bash
python3 poc.py
```

## What a good security/SAST tool should do

1. **Taint from request** – treat query parameters as tainted.
2. **Follow calls** – route → service → repository → querybuilder.
3. **Flag sinks** – use of tainted data in:
   - `querybuilder.build_condition(_, value)` (second argument),
   - `querybuilder.order_by(column, _)` (first argument),
   - or any string concatenated into `conn.execute(...)`.

For security tooling evaluation only. Do not use in production.
