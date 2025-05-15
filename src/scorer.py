import yaml
from pathlib import Path
from typing import Dict

WEIGHTS = yaml.safe_load(Path("weights.yaml").read_text())

def normalize(val, lo, hi, smaller_is_better=True):
    if hi == lo:
        return 1.0
    score = (hi - val) / (hi - lo) if smaller_is_better else (val - lo) / (hi - lo)
    return max(0, min(score, 1))

def compute_score(metrics: dict, mins: dict, maxs: dict):
    overall   = 0.0
    cat_tot   = {"computational": 0.0, "optimization": 0.0, "readability": 0.0}
    metric_ct = {}   # her metrik katkısı

    for k, cfg in WEIGHTS.items():
        if k not in metrics:
            continue
        w   = cfg["weight"] if isinstance(cfg, dict) else cfg
        sib = cfg.get("smaller_is_better", True) if isinstance(cfg, dict) else True
        cat = cfg.get("category", "misc")
        sc  = normalize(metrics[k], mins[k], maxs[k], smaller_is_better=sib)
        contrib = w * sc * 100        # 0-100 ölçeğine
        overall   += contrib
        cat_tot[cat] += contrib
        metric_ct[k] = round(contrib, 2)

    return round(overall, 2), {k: round(v, 2) for k, v in cat_tot.items()}, metric_ct


