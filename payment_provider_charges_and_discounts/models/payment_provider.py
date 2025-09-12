# Copyright 2025 Trobz (https://trobz.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    charge_rule_ids = fields.One2many(
        "payment.charge.rule", "provider_id", string="Charge Rules"
    )
    discount_rule_ids = fields.One2many(
        "payment.discount.rule", "provider_id", string="Discount Rules"
    )

    def compute_fees_to_apply(self, amount, currency):
        """Return dict with fees, discounts and breakdown."""
        self.ensure_one()
        charges = 0.0
        discounts = 0.0
        charge_breakdown = []
        discount_breakdown = []
        charge_rule = self.charge_rule_ids.filtered(
            lambda r: r._match(amount, currency)
        )
        if charge_rule:
            rule = charge_rule[0]
            charges = rule._compute_amount(amount, currency)
            charge_breakdown.append({"rule_id": rule.id, "amount": charges})

        discount_rule = self.discount_rule_ids.filtered(
            lambda r: r._match(amount, currency)
        )
        if discount_rule:
            rule = discount_rule[0]
            discounts = rule._compute_amount(amount, currency)
            discount_breakdown.append({"rule_id": rule.id, "amount": discounts})
        return {
            "charge_amount": charges,
            "discount_amount": discounts,
            "breakdown": {
                "charges": charge_breakdown,
                "discounts": discount_breakdown,
            },
        }
