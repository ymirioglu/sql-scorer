from collections import Counter
from typing import Dict, Any, List

def _walk(node: Dict[str, Any], bag: List[Dict[str, Any]]):
    """Recursively flatten Plan tree into a list of nodes."""
    bag.append(node)
    for child in node.get("Plans", []):
        _walk(child, bag)

def flatten_plan(plan_json) -> List[Dict[str, Any]]:
    nodes: List[Dict[str, Any]] = []
    root = plan_json[0]["Plan"]  # JSON format
    _walk(root, nodes)
    return nodes

def analyze_plan(plan_json) -> Dict[str, Any]:
    nodes = flatten_plan(plan_json)

    ops = Counter(n["Node Type"] for n in nodes)
    seq_scans  = ops.get("Seq Scan", 0) + ops.get("Parallel Seq Scan", 0)
    index_scans = ops.get("Index Scan", 0) + ops.get("Index Only Scan", 0)
    total_cost = sum(n.get("Total Cost", 0) for n in nodes if "Total Cost" in n)


    top = plan_json[0]
    exec_ms = top.get("Execution Time", 0)
    plan_ms = top.get("Planning Time", 0)

    return {
        "seq_scans": seq_scans,
        "index_scans": index_scans,
        "total_cost": round(total_cost, 2),
        "execution_ms": round(exec_ms, 3),
        "planning_ms": round(plan_ms, 3),
    }

if __name__ == "__main__":
    import json, sys
    plan = json.loads(sys.stdin.read())
    print(analyze_plan(plan))
