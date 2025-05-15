from pathlib import Path
import sys, json
from rich.console import Console
from rich.table   import Table

from src.runner   import run_sql
from src.scorer   import compute_score
from src.reporter import make_dataframe, save_bar, cli

console = Console()
if len(sys.argv) < 3:
    console.print("[bold red]Usage:[/] python compare.py A.sql B.sql [--verbose]")
    sys.exit(1)

sql_a, sql_b = Path(sys.argv[1]).read_text(), Path(sys.argv[2]).read_text()
stats_a, stats_b = run_sql(sql_a), run_sql(sql_b)

num = {k for k, v in stats_a.items() if isinstance(v, (int, float))}
mins = {k: min(stats_a[k], stats_b[k]) for k in num}
maxs = {k: max(stats_a[k], stats_b[k]) for k in num}

overall_a, cat_a, detail_a = compute_score(stats_a, mins, maxs)
overall_b, cat_b, detail_b = compute_score(stats_b, mins, maxs)

stats_a.update(score=overall_a, **cat_a)
stats_b.update(score=overall_b, **cat_b)

df = make_dataframe(stats_a, stats_b)
cli(stats_a, stats_b, verbose="--verbose" in sys.argv)

# -------- alt-metrik tablosu terminale ---------
t = Table(title="Alt-Metrik Katkıları (0-100)", show_header=True)
t.add_column("Metric")
t.add_column("Query A", justify="right")
t.add_column("Query B", justify="right")
for m in sorted(detail_a):
    t.add_row(m, f"{detail_a[m]:.2f}", f"{detail_b[m]:.2f}")
console.print(t)

# -------- sonuç mesajı ---------
if overall_a > overall_b:
    winner_msg = "Sonuç: Query A daha iyi bir seçenek."
elif overall_b > overall_a:
    winner_msg = "Sonuç: Query B daha iyi bir seçenek."
else:
    winner_msg = "Sonuç: İkisi de eşit"

console.print(f"\nSonuç: [bold green]{winner_msg}[/]\n")

console.print("✅  report.png güncellendi.")

alt_lines_a = [
    f"CPU süresi (sn): {detail_a['cpu_sec']:.2f}",
    f"Çalışma süresi (ms): {detail_a['elapsed_ms']:.2f}",
    f"Bellek (MB): {detail_a['mem_mb']:.2f}",
    f"Sıralı tarama sayısı: {detail_a['seq_scans']:.2f}",
    f"İndeks tarama sayısı: {detail_a['index_scans']:.2f}",
    f"Tahmini maliyet: {detail_a['total_cost']:.2f}",
    f"Okunaklılık puanı: {detail_a['lint_score']:.2f}",
]

alt_lines_b = [
    f"CPU süresi (sn): {detail_b['cpu_sec']:.2f}",
    f"Çalışma süresi (ms): {detail_b['elapsed_ms']:.2f}",
    f"Bellek (MB): {detail_b['mem_mb']:.2f}",
    f"Sıralı tarama sayısı: {detail_b['seq_scans']:.2f}",
    f"İndeks tarama sayısı: {detail_b['index_scans']:.2f}",
    f"Tahmini maliyet: {detail_b['total_cost']:.2f}",
    f"Okunaklılık puanı: {detail_b['lint_score']:.2f}",
]

save_bar(df,
         "report.png",
         winner_msg,
         stats_a,
         stats_b,
         alt_lines_a,
         alt_lines_b)
