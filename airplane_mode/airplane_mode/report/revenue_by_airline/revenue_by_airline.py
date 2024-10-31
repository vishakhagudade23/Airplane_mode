# Copyright (c) 2024, Vishakha Gudade and contributors
# For license information, please see license.txt


import frappe
from frappe import _

def execute(filters=None):
    
    columns = [
        {
            "fieldname": "airline",
            "label": _("Airline"),
            "fieldtype": "Link",
            "options": "Airline",
            "width": 200
        },
        {
            "fieldname": "revenue",
            "label": _("Revenue"),
            "fieldtype": "Currency",
            "width": 150
        }
    ]

    airlines = frappe.get_all("Airline", fields=["name"])
    data = []

    for airline in airlines:
        total_revenue = 0
        airplanes = frappe.get_all("Airplane", filters={"airline": airline.name}, fields=["name"])
        
        for airplane in airplanes:
            flights = frappe.get_all("Airplane Flight", filters={"airplane": airplane.name}, fields=["name"])
            for flight in flights:
                tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight.name}, fields=["total_amount"])
                total_revenue += sum(ticket.total_amount for ticket in tickets)

        data.append({
            "airline": airline.name,
            "revenue": total_revenue
        })

    
    data.sort(key=lambda x: x["revenue"], reverse=True)

    airlines_list = [row["airline"] for row in data]
    revenue_list = [row["revenue"] for row in data]
    

    chart = {
        "type": "donut",
        "data": {
            "labels": airlines_list,
            "datasets": [{"name": "Revenue", "values": revenue_list}]
        }
    }

    summary = [{
        "label": _("Total Revenue"),
        "value": sum(revenue_list),
        "datatype": "Currency",
        "indicator": "green"
    }]

    return columns, data, None, chart, summary
