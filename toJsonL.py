import json
import re

INPUT_PATH = "output.txt"
OUTPUT_PATH = "./datasets/tableToJsonl.jsonl"


def flush_table(current, results):
    cols = current["columns"] or []
    norm_data = []
    for row in current["data"]:
        if len(row) < len(cols):
            row += [""] * (len(cols) - len(row))
        elif len(row) > len(cols):
            row = row[: len(cols)]
        norm_data.append(row)
    results.append(
        {
            "id": current["id"] or f"table_{len(results)+1}",
            "qtype": "",
            "qsubtype": "",
            "table": {"columns": cols, "data": norm_data},
            "question": "",
            "answer": "",
        }
    )


with open(INPUT_PATH, "r", encoding="utf-8") as f:
    lines = [ln.rstrip("\n") for ln in f]

results = []
current = {"id": None, "columns": None, "data": []}

for ln in lines:
    s = ln.strip()

    if (
        not s
        or s.startswith("**Table ")
        or s.lower().startswith(("example id:", "id:"))
    ):
        if current["columns"] is not None:
            flush_table(current, results)
            current = {"id": None, "columns": None, "data": []}

        if s.lower().startswith(("example id:", "id:")):
            current["id"] = s.split(":", 1)[1].strip()
        continue

    if s.lower().startswith("highlighted cells:"):
        continue

    if "|" in ln:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
            continue
        if current["columns"] is None:
            current["columns"] = cells
        else:
            current["data"].append(cells)

if current["columns"] is not None or current["id"]:
    flush_table(current, results)

with open(OUTPUT_PATH, "w", encoding="utf-8") as out:
    for obj in results:
        out.write(json.dumps(obj, ensure_ascii=False) + "\n")
