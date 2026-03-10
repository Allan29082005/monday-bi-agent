import requests

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYzMTAwNjMyNCwiYWFpIjoxMSwidWlkIjoxMDA4MTI2MzgsImlhZCI6IjIwMjYtMDMtMTBUMDU6NDU6NTEuMDAwWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MTUzMzA1LCJyZ24iOiJhcHNlMiJ9.yjrjcuFkcW2KHyh0uu441U9IzkdwJtu_uxRSUorVurM"

url = "https://api.monday.com/v2"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

def get_board_data(board_id):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page(limit: 500) {{
          items {{
            name
            column_values {{
              column {{
                title
              }}
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        url,
        json={"query": query},
        headers=headers,
        verify=False
    )

    return response.json()