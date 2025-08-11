import json

INPUT_FILE = "./datasets/dataset.jsonl"
OUTPUT_FILE = "tables.html"

CSS_STYLE = """
<style>
    table {
        border-collapse: collapse;
        margin-bottom: 20px;
        width: auto;
        font-family: Arial, sans-serif;
        font-size: 14px;
    }
    th, td {
        border: 1px solid #999;
        padding: 6px 10px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
    }
    .highlight {
        background-color: #ffeb3b; /* bright yellow */
    }
</style>
"""


def render_table_html(table, example_id, highlighted_cells):
    html = [f'<table id="{example_id}">']
    for r_idx, row in enumerate(table):
        html.append("<tr>")
        for c_idx, cell in enumerate(row):
            tag = "th" if cell.get("is_header") else "td"
            colspan = cell.get("column_span", 1)
            rowspan = cell.get("row_span", 1)

            classes = []
            if [r_idx, c_idx] in highlighted_cells:
                classes.append("highlight")

            class_attr = f' class="{" ".join(classes)}"' if classes else ""
            html.append(
                f'<{tag} colspan="{colspan}" rowspan="{rowspan}"{class_attr}>'
                f'{cell.get("value", "")}</{tag}>'
            )
        html.append("</tr>")
    html.append("</table>")
    return "\n".join(html)


def main():
    html_parts = ["<html><head>", CSS_STYLE, "</head><body>"]
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            table = data["table"]
            example_id = data["example_id"]
            highlighted_cells = data.get("highlighted_cells", [])
            html_parts.append(render_table_html(table, example_id, highlighted_cells))
    html_parts.append("</body></html>")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))


if __name__ == "__main__":
    main()
