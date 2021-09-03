"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonreports.views import Connection


def completed_orders_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all products, with related user info.
            db_cursor.execute("""
                SELECT 
                    o.id,
                    u.first_name ||" "|| u.last_name AS NAME,
                    SUM(p.price) AS TOTAL_PRICE,
                    t.merchant_name AS PAYMENT_TYPE
                FROM bangazonapi_order o
                JOIN bangazonapi_payment t 
                    ON o.payment_type_id = t.id
                JOIN bangazonapi_customer c 
                    ON c.id = o.customer_id
                JOIN bangazonapi_orderproduct op 
                    ON op.order_id = o.id
                JOIN auth_user u 
                    ON u.id = c.user_id
                JOIN bangazonapi_product p 
                    ON p.id = op.product_id
            """)

            dataset = db_cursor.fetchall()

            completed_orders = {}

            for row in dataset:
                uid = row["id"]
                completed_orders[uid] = {}
                completed_orders[uid]["id"] = uid
                completed_orders[uid]["NAME"] = row["NAME"]
                completed_orders[uid]["TOTAL_PRICE"] = row["TOTAL_PRICE"]
                completed_orders[uid]["PAYMENT_TYPE"] = row["PAYMENT_TYPE"]

        # Get only the values from the dictionary and create a list from them
        list_of_completed_orders = completed_orders.values()

        # Specify the Django template and provide data context
        template = 'orders/list_of_completed_orders.html'
        context = {
            'completed_orders': list_of_completed_orders
        }

        return render(request, template, context)