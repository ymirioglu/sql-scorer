from sqlalchemy import create_engine, text
from time import perf_counter
import psutil
from pathlib import Path
from typing import Dict, Any

from config import DB_URI
from .analyzer import analyze_plan 
from .linter import lint_sql     

engine = create_engine(DB_URI, pool_pre_ping=True)

def run_sql(sql_text: str, sample_limit: int | None = None) -> Dict[str, Any]:
    """
    SQL'i çalıştır, EXPLAIN ANALYZE planını al, süre/CPU/RAM ölç.
    sample_limit verilirse gerçek çalıştırmada LIMIT eklenir.
    """
    sql_exec = f"{sql_text.rstrip(';')} LIMIT {sample_limit};" if sample_limit else sql_text

    t0 = perf_counter()
    process = psutil.Process()

    with engine.begin() as conn:
        plan_json = conn.execute(
            text(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {sql_exec}")
        ).scalar_one()
        rows = conn.execute(text(sql_exec)).fetchall()

    plan_metrics = analyze_plan(plan_json)
    lint_metrics = lint_sql(sql_text)

    elapsed_ms = (perf_counter() - t0) * 1000
    cpu_user = process.cpu_times().user
    mem_mb   = process.memory_info().rss / 1_048_576

    return {
        "elapsed_ms": round(elapsed_ms, 1),
        "cpu_sec":   round(cpu_user, 3),
        "mem_mb":    round(mem_mb, 2),
        "rows":      len(rows),
        **plan_metrics,
        **lint_metrics,
        "plan": plan_json,         
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m src.runner path/to/query.sql")
        sys.exit(1)

    sql_file = Path(sys.argv[1])
    stats = run_sql(sql_file.read_text(), sample_limit=1000)
    print(stats)
