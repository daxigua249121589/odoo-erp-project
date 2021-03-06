# Copyright (C) 2021 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    mo_count = fields.Integer("# MOs", compute="_compute_mo_count")

    def _compute_mo_count(self):
        for ag_rec in self:
            ag_rec.mo_count = self.env["mrp.production"].search_count(
                [("agreement_id", "in", ag_rec.ids)]
            )
