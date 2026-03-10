import pandas as pd
import json

def board_to_dataframe(data):

    if "data" not in data or len(data["data"]["boards"]) == 0:
        return pd.DataFrame()

    items = data["data"]["boards"][0]["items_page"]["items"]

    rows = []

    for item in items:

        row = {"Item": item["name"]}

        for col in item["column_values"]:

            title = col["column"]["title"]

            value = col.get("text")

            if not value:
                try:
                    raw = json.loads(col.get("value") or "{}")
                    value = list(raw.values())[0] if raw else ""
                except:
                    value = ""

            row[title] = value

        rows.append(row)

    return pd.DataFrame(rows)