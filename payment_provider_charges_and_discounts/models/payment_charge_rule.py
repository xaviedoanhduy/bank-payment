# Copyright 2025 Trobz (https://trobz.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PaymentChargeRule(models.Model):
    _name = "payment.charge.rule"
    _inherit = "payment.fee.rule"
    _description = "Payment Charge Rule"
