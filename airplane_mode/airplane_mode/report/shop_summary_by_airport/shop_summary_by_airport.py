# Copyright (c) 2024, Vishakha Gudade and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart_data(data)
    return columns, data, None, chart

def get_columns():
    return [
        {
            "fieldname": "airport",
            "label": _("Airport"),
            "fieldtype": "Link",
            "options": "Airport",
            "width": 180
        },
        {
            "fieldname": "total_shops",
            "label": _("Total Shops"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "available_shops",
            "label": _("Available Shops"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "occupied_shops",
            "label": _("Occupied Shops"),
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "occupancy_rate",
            "label": _("Occupancy Rate (%)"),
            "fieldtype": "Percent",
            "width": 150
        }
    ]

def get_data(filters):
    data = []
    
    conditions = ""
    if filters and filters.get("airport"):
        conditions = f" WHERE name = '{filters.get('airport')}'"
    
    airports = frappe.db.sql(f"""
        SELECT name 
        FROM tabAirport
        {conditions}
    """, as_dict=1)
    
    for airport in airports:
    
        total_shops = frappe.db.count("Shop",
            filters={"airport": airport.name})
            
        available_shops = frappe.db.count("Shop", 
            filters={
                "airport": airport.name,
                "lease_status": "Available"
            })
            
        occupied_shops = frappe.db.count("Shop", 
            filters={
                "airport": airport.name,
                "lease_status": "Occupied"
            })
            
    
        occupancy_rate = round((occupied_shops / total_shops * 100), 2) if total_shops else 0
            
        data.append({
            "airport": airport.name,
            "total_shops": total_shops,
            "available_shops": available_shops,
            "occupied_shops": occupied_shops,
            "occupancy_rate": occupancy_rate
        })
    
    return data

def get_chart_data(data):
    if not data:
        return None

    labels = []
    available_series = []
    occupied_series = []

    for entry in data:
        labels.append(entry.get("airport"))
        available_series.append(entry.get("available_shops"))
        occupied_series.append(entry.get("occupied_shops"))

    chart = {
        "data": {
            "labels": labels,
            "datasets": [
                {
                    "name": "Available Shops",
                    "values": available_series,
                    "chartType": "bar"
                },
                {
                    "name": "Occupied Shops",
                    "values": occupied_series,
                    "chartType": "bar"
                }
            ]
        },
        "type": "bar",
        "colors": ["#EA738DFF", "#CDB599FF"], 
        "barOptions": {
            "stacked": 0
        }
    }
    
    return chart