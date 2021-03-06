# Copyright (C) 2019 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models


class StockPutawayRule(models.Model):
    _inherit = "stock.putaway.rule"

    @api.model
    def _get_putaway_options(self):
        res = super()._get_putaway_options()
        res.append(("vehicle", "Location of the vehicle"))
        return res

    @api.model
    def get_vehicle_location(self):
        if self.env.context.get("vehicle_id"):
            return (
                self.env["fsm.vehicle"]
                .browse(self.env.context.get("vehicle_id"))
                .inventory_location_id
            )
        return self.env["stock.location"]
