# Copyright 2025 Trobz (https://trobz.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Payment Provider Charges and Discounts",
    "version": "17.0.1.0.4",
    "category": "Banking addons",
    "license": "AGPL-3",
    "summary": "Add support for payment Charges and Discounts in Odoo Payment Framework.",
    "author": "Trobz, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/bank-payment",
    "depends": ["payment"],
    "data": [
        "security/ir.model.access.csv",
        "views/payment_fee_rule_views.xml",
    ],
    "auto_install": True,
    "installable": True,
    "application": False,
}
