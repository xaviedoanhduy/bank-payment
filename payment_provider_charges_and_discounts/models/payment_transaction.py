# Copyright 2025 Trobz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"

    charge_amount = fields.Monetary(
        string="Charge",
        currency_field="currency_id",
        compute="_compute_fees",
        store=True,
        compute_sudo=True,
    )
    discount_amount = fields.Monetary(
        string="Discount",
        currency_field="currency_id",
        compute="_compute_fees",
        store=True,
        compute_sudo=True,
    )
    charge_breakdown = fields.Text(
        compute="_compute_fees",
        store=True,
        compute_sudo=True,
    )
    amount_total_charged = fields.Monetary(
        string="Total Charged",
        currency_field="currency_id",
        compute="_compute_fees",
        store=True,
        compute_sudo=True,
    )

    @api.depends(
        "amount",
        "currency_id",
        "partner_id",
        "company_id",
        "provider_id",
    )
    def _compute_fees(self):
        for tx in self:
            currency = tx.currency_id
            fee = 0.0
            disc = 0.0
            breakdown = {}

            if tx.provider_id and tx.amount and currency:
                res = tx.provider_id.compute_fees_to_apply(tx.amount, currency)
                fee = res.get("charge_amount", 0.0) or 0.0
                disc = res.get("discount_amount", 0.0) or 0.0
                breakdown = res.get("breakdown") or {}
                fee = currency.round(fee)
                disc = currency.round(disc)

            tx.charge_amount = fee
            tx.discount_amount = disc
            tx.charge_breakdown = breakdown
            tx.amount_total_charged = currency.round((tx.amount or 0.0) + fee - disc)
