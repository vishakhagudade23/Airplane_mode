# Copyright (c) 2024, Vishakha Gudade and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Shop(WebsiteGenerator):
    # Set default rent amount if rent_amount is 0
    def before_save(doc, method=None):
        if doc.rent_amount == 0:
            global_settings = frappe.get_single("Global Settings")
            default_rent_amount = global_settings.default_rent_amount

            if default_rent_amount:
                doc.rent_amount = default_rent_amount