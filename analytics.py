def pipeline_summary(df):

    if df.empty:
        return "No deals found."

    value_col = None

    for col in df.columns:
        c = col.lower()
        if "value" in c or "amount" in c or "revenue" in c or "deal" in c:
            value_col = col
            break

    if value_col is None:
        return "Could not detect deal value column."

    df[value_col] = df[value_col].replace(",", "", regex=True)

    try:
        df[value_col] = df[value_col].astype(float)
    except:
        return "Deal values are not numeric."

    total = df[value_col].sum()

    return f"Total pipeline value: ${total:,.0f}"