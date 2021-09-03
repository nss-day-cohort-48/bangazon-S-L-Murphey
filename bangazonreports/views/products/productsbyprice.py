"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def product_price_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all products, with related user info.
            db_cursor.execute("""
                SELECT
                    p.id,
                    p.name,
                    p.price
                FROM
                    bangazonapi_product p
                WHERE p.price >= 1000
            """)

            dataset = db_cursor.fetchall()

            products_by_price = {}

            for row in dataset:
                uid = row["id"]
                products_by_price[uid] = {}
                products_by_price[uid]["id"] = uid
                products_by_price[uid]["name"] = row["name"]
                products_by_price[uid]["price"]= row["price"]

        # Get only the values from the dictionary and create a list from them
        list_of_products_by_price = products_by_price.values()

        # Specify the Django template and provide data context
        template = 'products/list_of_products_by_price.html'
        context = {
            'product_by_price': list_of_products_by_price
        }

        return render(request, template, context)