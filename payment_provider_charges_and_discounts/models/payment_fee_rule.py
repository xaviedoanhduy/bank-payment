# Copyright 2025 Trobz (https://trobz.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class PaymentFeeRule(models.AbstractModel):
    """Abstract base for payment charge rules (fee or discount)."""

    _name = "payment.fee.rule"
    _inherit = "payment.charge.rule"
    _description = "Payment Fee Rule"

    sequence = fields.Integer(default=10)
    provider_id = fields.Many2one(
        "payment.provider",
        string="Provider",
        required=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="provider_id.company_id.currency_id",
        store=True,
    )
    account_id = fields.Many2one(
        "account.account",
        string="Account",
    )
    rule_type = fields.Selection(
        [("fixed", "Fixed Amount"), ("percent", "Percentage")],
        required=True,
    )
    value = fields.Float(string="Percent (%)")
    value_currency = fields.Monetary(
        string="Fixed Amount",
        currency_field="currency_id",
    )

    def _compute_amount(self, amount, currency):
        """Return charge amount based on rule type."""
        self.ensure_one()
        if self.rule_type == "fixed":
            return self.value_currency
        elif self.rule_type == "percent":
            return currency.round(amount * (self.value / 100.0))
        return 0.0

    def _match(self, amount, currency):
        """Optional hook: define condition to apply rule."""
        return True
