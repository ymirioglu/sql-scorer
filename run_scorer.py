import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

def ask_file(title: str) -> str:
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title=title,
        filetypes=[("SQL files", "*.sql")],
    )
    root.destroy()
    if not path:
        sys.exit("İptal edildi.")
    return path

# ------------------------------------------------------------
if len(sys.argv) == 3:
    file_a, file_b = sys.argv[1], sys.argv[2]
else:
    print("🔍  Lütfen ilk SQL dosyasını seçin")
    file_a = ask_file("Select first SQL file")
    print("🔍  Lütfen ikinci SQL dosyasını seçin")
    file_b = ask_file("Select second SQL file")

print(f"\n▶️  Karşılaştırılıyor:\n  1) {file_a}\n  2) {file_b}\n")

subprocess.run(
    [sys.executable, "compare.py", file_a, file_b],   # venv'le aynı python
    check=True
)

print("\n🎉  Analiz tamam – 'report.png' dosyasına bakabilirsiniz.")
