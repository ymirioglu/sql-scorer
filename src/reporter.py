import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

CRITICAL = [
    "score", "elapsed_ms", "cpu_sec", "mem_mb",
    "seq_scans", "index_scans", "total_cost", "lint_score"
]

def make_dataframe(stats_a: dict, stats_b: dict) -> pd.DataFrame:
    df = pd.DataFrame([stats_a, stats_b], index=["Query A", "Query B"])
    return df[CRITICAL]

CRITICAL = ["score", "computational", "optimization", "readability"]

def save_bar(df, out_png, winner_msg, stats_a, stats_b,
             alt_lines_a=None, alt_lines_b=None):
    import matplotlib.pyplot as plt
    df_cat = df[["computational", "optimization", "readability"]]

    plt.figure(figsize=(6, 4.8))
    ax = df_cat.plot(kind="bar", ax=plt.gca())
    ax.set_ylim(0, 100)
    ax.set_ylabel("Kategori Katkısı")
    plt.xticks(rotation=0)
    plt.tight_layout(rect=[0, 0.34, 1, 1])   # daha fazla alt boşluk

    # ana özet blok
    lines = [
        f"Query A → Comp:{stats_a['computational']:.1f}  Opt:{stats_a['optimization']:.1f}  Read:{stats_a['readability']:.1f}  Toplam:{stats_a['score']:.1f}",
        f"Query B → Comp:{stats_b['computational']:.1f}  Opt:{stats_b['optimization']:.1f}  Read:{stats_b['readability']:.1f}  Toplam:{stats_b['score']:.1f}",
        winner_msg,
    ]
    # alt-metrik katkıları
    if alt_lines_a and alt_lines_b:
        lines.append("Alt-metrik katkıları (0-100):")
        lines.append("A ➜ " + "  |  ".join(alt_lines_a))
        lines.append("B ➜ " + "  |  ".join(alt_lines_b))

    plt.figtext(0.5, 0.02, "\n".join(lines), ha="center", fontsize=8, wrap=True)
    plt.savefig(out_png, dpi=200)
    plt.close()

def cli(stats_a, stats_b, verbose=False):
    import rich.console, rich.table
    console = rich.console.Console()
    df = make_dataframe(stats_a, stats_b)
    tbl = rich.table.Table(show_header=True)
    tbl.add_column("Metric")
    tbl.add_column("Query A", justify="right")
    tbl.add_column("Query B", justify="right")

    for m in CRITICAL:
        tbl.add_row(m, f"{df.loc['Query A', m]:.3g}", f"{df.loc['Query B', m]:.3g}")
    console.print(tbl)

    if verbose:
        console.rule("[bold]Full JSON – Query A")
        console.print(stats_a)
        console.rule("[bold]Full JSON – Query B")
        console.print(stats_b)
