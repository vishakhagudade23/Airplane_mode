frappe.ui.form.on("Airline", {
    refresh(frm) {
        let website = frm.doc.website;

        if (website) {
            frm.add_web_link(website, "Visit Website");
        }
    }
});