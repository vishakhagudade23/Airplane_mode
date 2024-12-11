# Copyright (c) 2024, Vishakha Gudade and contributors
# For license information, please see license.txt


import frappe
import random
from frappe.model.document import Document

class AirplaneTicket(Document):
    
    def before_submit(self):
        if self.status != "Boarded":
            frappe.throw("Cannot submit Airplane Ticket document. Status must be 'Boarded'.")



    def before_insert(self):
        random_number = random.randint(1, 99)  
        random_letter = random.choice(['A', 'B', 'C', 'D', 'E'])  
        self.seat = f"{random_number}{random_letter}"



    def validate(self):
        flight = frappe.get_doc("Airplane Flight", self.flight)
        airplane = frappe.get_doc("Airplane", flight.airplane)

        capacity = airplane.capacity
        
        tickets_count = frappe.db.count('Airplane Ticket', filters={'flight': self.flight})
        
        if tickets_count >= capacity:
            frappe.throw(f"This flight is full. Cannot book more tickets for this flight.")



    def validate(self):

        total_addon_amount = 0
        for addon in self.add_ons:
            total_addon_amount += addon.amount

        self.total_amount = total_addon_amount + self.flight_price


        unique_add_ons = {}
        
        for item in self.add_ons:
            if item.item in unique_add_ons:
                frappe.throw("Add-on {0} has already been added. Duplicates are not allowed.".format(item.item))
            else:
                unique_add_ons[item.item] = item

        self.add_ons = list(unique_add_ons.values())
