import json


def jsonl_to_markdown_table(json_line, table_number):
    obj = json.loads(json_line)
    rows = obj["table"]
    example_id = obj.get("example_id", "N/A")
    highlighted_cells = obj.get("highlighted_cells", [])

    md_lines = [f"Table {table_number}:", f"Example ID: {example_id}"]
    if highlighted_cells:
        hl = ", ".join(f"({r}, {c})" for r, c in highlighted_cells)
        md_lines.append(f"Highlighted Cells: {hl}")
    else:
        md_lines.append("Highlighted Cells: None")
    md_lines.append("")

    grid = []
    cell_map = {}

    for r_idx, row in enumerate(rows):
        col_pointer = 0
        while len(grid) <= r_idx:
            grid.append([])

        for cell in row:
            while (r_idx, col_pointer) in cell_map:
                col_pointer += 1

            val = cell["value"]
            col_span = int(cell.get("column_span", 1))
            row_span = int(cell.get("row_span", 1))

            for r_off in range(row_span):
                for c_off in range(col_span):
                    pos = (r_idx + r_off, col_pointer + c_off)
                    if r_off == 0 and c_off == 0:
                        cell_map[pos] = val
                    else:
                        cell_map[pos] = ""

            col_pointer += col_span

    max_row = max(r for r, _ in cell_map.keys()) + 1
    max_col = max(c for _, c in cell_map.keys()) + 1

    grid = []
    for r in range(max_row):
        row = []
        for c in range(max_col):
            row.append(cell_map.get((r, c), ""))
        grid.append(row)

    # --- Compute column widths ---
    col_widths = [0] * max_col
    for row in grid:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    # --- Format markdown table ---
    def fmt_row(row):
        return (
            "| "
            + " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            + " |"
        )

    md_lines.append(fmt_row(grid[0]))
    md_lines.append(
        "| " + " | ".join(":--".ljust(col_widths[i]) for i in range(max_col)) + " |"
    )
    for row in grid[1:]:
        md_lines.append(fmt_row(row))

    return "\n".join(md_lines)


with open("./datasets/dataset.jsonl", "r", encoding="utf-8") as infile, open(
    "output.txt", "w", encoding="utf-8"
) as outfile:

    table_number = 1
    for line in infile:
        markdown_table = jsonl_to_markdown_table(line, table_number)
        outfile.write(markdown_table + "\n\n")
        table_number += 1

    print("Complete")
