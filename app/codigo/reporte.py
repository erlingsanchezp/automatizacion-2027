import csv
from pathlib import Path


def calcular(path):
    total = citas = 0
    with Path(path).open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            a, b = int(row["escribieron"]), int(row["agendaron"])
            if a < 0 or b < 0 or b > a:
                raise ValueError("Conteos no válidos")
            total += a
            citas += b
    return {"escribieron": total, "agendaron": citas,
            "conversion": round(100 * citas / total, 2) if total else 0}


if __name__ == "__main__":
    print(calcular(Path(__file__).resolve().parents[1] / "datos/reporte.csv"))
