from groq import Groq
import os

client = Groq(api_key="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")


def ask_agent(question, deals_df, work_df):

    try:

        # Create summarized context
        context = f"""
        Business Data Summary

        Deals Board
        Total Deals: {len(deals_df)}

        Work Orders Board
        Total Work Orders: {len(work_df)}

        Deals Columns:
        {list(deals_df.columns)}

        Work Orders Columns:
        {list(work_df.columns)}

        Example Deals:
        {deals_df.head(3).to_string()}

        Example Work Orders:
        {work_df.head(3).to_string()}
        """

        prompt = f"""
You are a business intelligence assistant helping founders understand company data.

Use the provided monday.com board summary to answer the question.

If information is missing, explain possible limitations.

DATA CONTEXT:
{context}

USER QUESTION:
{question}

Provide clear business insights.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Agent error: {str(e)}"