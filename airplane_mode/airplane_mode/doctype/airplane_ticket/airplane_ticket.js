// Copyright (c) 2024, Vishakha Gudade and contributors
// For license information, please see license.txt


frappe.ui.form.on("Airplane Ticket", {
    refresh: function(frm) {
        frm.add_custom_button("Assign Seat",() => {
            let d = new frappe.ui.Dialog({
                title : "Select Seat",
                fields :[
                    {
                        label : "Seat Number",
                        fieldname : "seat_number",
                        fieldtype : "Data",
                        reqd: 1
                    }
                ],
                primary_action_label : "Assign",
                primary_action(values){
                    frm.set_value("seat",values.seat_number);
                    d.hide();
                }
            });
            d.show();
        },"Actions");
    }
});
           