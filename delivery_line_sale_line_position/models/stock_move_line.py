# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    position_sale_line = fields.Char(
        related="move_id.position_sale_line", string="Position"
    )
