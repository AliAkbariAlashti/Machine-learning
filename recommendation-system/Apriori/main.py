import pandas as pd
import pyodbc
import pandas as pd
from math import sqrt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
from itertools import combinations
from collections import defaultdict
from mlxtend.frequent_patterns import apriori, association_rules
import requests
from flask import Flask, request, jsonify
# test api
app = Flask(__name__)

@app.route('/test-api', methods=['POST'])
def test_api():
    data = request.get_json()
    
    required_keys = ["BuyerId", "antecedents", "consequents", "support", "confidence", "lift"]
    if not all(key in data for key in required_keys):
        return jsonify({"error": "Missing required parameters!"}), 400

    # اگر antecedents از نوع frozenset باشد، آن را به list تبدیل کن
    if isinstance(data["antecedents"], frozenset):
        data["antecedents"] = list(data["antecedents"])

    print("Received Data:", data)  # نمایش داده‌های دریافتی در کنسول
    
    # افزودن هدر به پاسخ
    response = jsonify({"message": "Data received successfully!", "data": data})
    response.headers["Custom-Header"] = "This is a custom header"
    response.headers["Content-Type"] = "application/json"
    
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # اجرا روی پورت 5000





sql_query = """
SELECT 
    ProductId,
    BuyerId,
    BuyerName,
    ProductName,
    PriceWithoutVat / Count AS ItemPrice,
    PersianDate,
    CreateDate,
    Count
FROM viewSellReport
WHERE
    Count > 0
    AND PersianDate >= '1403/01/01'
ORDER BY 
    ResellerOrderId;
"""

def read_data_from_sql():
    
    server = ""
    database = ""
    username = ""
    password = ""

    try:
        # Connection string
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )
        
        # Connect to the SQL Server
        connection = pyodbc.connect(conn_str)
        
        # Execute the query and load the result into a DataFrame
        df = pd.read_sql(sql_query, connection)
        
        # Close the connection
        connection.close()
        
        return df
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
data = read_data_from_sql()

data["PersianDate"] = data["PersianDate"].str.split("/").str[1] + data["PersianDate"].str.split("/").str[2]
grouped = data.groupby(["PersianDate", "BuyerId"])["ProductId"].apply(list).reset_index()
buyerid_list = grouped['BuyerId'].unique()



for i in buyerid_list:
    ap_df = grouped[grouped['BuyerId'] == i]
    transactions = ap_df['ProductId'].tolist()

    all_products = sorted(set(item for sublist in transactions for item in sublist))
    onehot_encoded_data = []
    for transaction in transactions:
        onehot_encoded_data.append([1 if product in transaction else 0 for product in all_products])

    onehot_df = pd.DataFrame(onehot_encoded_data, columns=all_products)

    frequent_itemsets = apriori(onehot_df, min_support=0.05, use_colnames=True)

    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
    rules['antecedents'] = rules['antecedents'].apply(lambda x: list(x))
    rules['consequents'] = rules['consequents'].apply(lambda x: list(x))

    url = "http://127.0.0.1:5000/test-api"  # آدرس API لوکال
    headers = {
        "Content-Type": "application/json",
        "Custom-Request-Header": "Test Header"
    }

    
    for index, row in rules.iterrows():
        params = {
            "BuyerId": i ,  
            "antecedents": row['antecedents'],
            "consequents": row['consequents'],  
            "support": row['support'],  
            "confidence": row['confidence'],  
            "lift": row['lift']
        }
        

        # Send the GET request
        response = requests.get(url, headers=headers, params=params)

        # Print the response
        print(f"Status Code: {response.status_code}")
        try:
            print(f"Response: {response.json()}")
        except ValueError:
            print("Response is not valid JSON")
            print(response.text)
    

    
