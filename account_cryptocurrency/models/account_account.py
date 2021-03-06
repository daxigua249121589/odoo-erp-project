# Copyright 2021 ForgeFlow S.L.
# Copyright 2018 Fork Sand Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    @api.constrains("currency_id")
    def _check_inventory_account_id(self):
        for rec in self.filtered("currency_id"):
            currency = self.env["res.currency"].search(
                [
                    ("inventory_account_id", "=", rec.id),
                    ("id", "!=", rec.currency_id.id),
                ],
                limit=1,
            )
            if currency:
                raise exceptions.ValidationError(
                    _(
                        "You cannot change the account currency as it is "
                        "already being referenced to cryptocurrency %s as an "
                        "Inventory Account."
                    )
                    % currency.name
                )
