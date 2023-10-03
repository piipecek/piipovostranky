from pathlib import Path

def piipuv_omnislovnik_path() -> Path:
    cwd = Path.cwd()
    return cwd / "piipuv_omnislovnik_k_3_10_2021.json"

def hadej_slova_db_path() -> Path:
    return Path.cwd() / "hadej_slova.json"

def tomiem_result_path() -> Path:
    return Path.cwd() / "tomiem_ipsum" / "result.txt"

def log_file_path() -> Path:
    return Path.cwd() / "data" / "logs.txt"

def multilang_path() -> Path:
    return Path.cwd() / "data" / "multilang.json"

def cernabila_getword_path() -> Path:
    return Path.cwd() / "cernabila" / "db.json"

def dotenv_path() -> Path:
    return Path.cwd() / ".env"