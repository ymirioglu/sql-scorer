from sqlfluff.api.simple import Linter
from pathlib import Path
from typing import Dict

_linter = Linter(dialect="postgres")          

def lint_sql(sql_text: str) -> Dict[str, int]:
    """
    sqlfluff ile hataları say, 0‑100 arası okunaklılık skoru üret.
    Her ihlal 5 puan düşürür (örn. 4 ihlal ⇒ 80 /100).
    """
    result = _linter.lint_string(sql_text)
    violations = result.check_tuples()
    penalty = len(violations) * 5
    return {"lint_violations": len(violations),
            "lint_score": max(0, 100 - penalty)}
