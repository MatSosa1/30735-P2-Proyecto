import os
import hashlib
import sqlite3
import subprocess

# CWE-798: credenciales embebidas en el código
DB_PASSWORD = "SuperSecret123!"
api_key = "sk_live_4eC39HqLyjWDarjtT1zdp7dc"


def get_user(username):
    # CWE-89: SQL Injection por concatenación de strings
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()


def search_products(name):
    # CWE-89: SQL Injection con f-string
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name FROM products WHERE name = '{name}'")
    return cursor.fetchall()


def ping_host(host):
    # CWE-78: OS Command Injection
    os.system("ping -c 1 " + host)
    return subprocess.call("nslookup " + host, shell=True)


def run_code(expr):
    # CWE-95: Code Injection
    return eval(expr)


def hash_password(password):
    # CWE-327: criptografía débil
    return hashlib.md5(password.encode()).hexdigest()
