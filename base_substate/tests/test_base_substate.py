# Copyright 2020 Akretion Mourad EL HADJ MIMOUNE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.tests import common, tagged


@tagged("-at_install", "post_install")
class TestBaseSubstate(common.SavepointCase, FakeModelLoader):
    @classmethod
    def setUpClass(cls):
        super(TestBaseSubstate, cls).setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import LineTest, SaleTest

        cls.loader.update_registry((SaleTest, LineTest))

        cls.substate_test_sale = cls.env["base.substate.test.sale"]
        cls.substate_test_sale_line = cls.env["base.substate.test.sale.line"]

        cls.base_substate = cls.env["base.substate.mixin"]
        cls.substate_type = cls.env["base.substate.type"]

        cls.substate_type._fields["model"].selection.append(
            ("base.substate.test.sale", "Sale Order")
        )

        cls.substate_type = cls.env["base.substate.type"].create(
            {
                "name": "Sale",
                "model": "base.substate.test.sale",
                "target_state_field": "state",
            }
        )

        cls.substate_val_quotation = cls.env["target.state.value"].create(
            {
                "name": "Quotation",
                "base_substate_type_id": cls.substate_type.id,
                "target_state_value": "draft",
            }
        )

        cls.substate_val_sale = cls.env["target.state.value"].create(
            {
                "name": "Sale order",
                "base_substate_type_id": cls.substate_type.id,
                "target_state_value": "sale",
            }
        )
        cls.substate_under_negotiation = cls.env["base.substate"].create(
            {
                "name": "Under negotiation",
                "sequence": 1,
                "target_state_value_id": cls.substate_val_quotation.id,
            }
        )

        cls.substate_won = cls.env["base.substate"].create(
            {
                "name": "Won",
                "sequence": 3,
                "target_state_value_id": cls.substate_val_quotation.id,
            }
        )

        cls.substate_wait_docs = cls.env["base.substate"].create(
            {
                "name": "Waiting for legal documents",
                "sequence": 4,
                "target_state_value_id": cls.substate_val_sale.id,
            }
        )

        cls.substate_valid_docs = cls.env["base.substate"].create(
            {
                "name": "To validate legal documents",
                "sequence": 5,
                "target_state_value_id": cls.substate_val_sale.id,
            }
        )

        cls.substate_in_delivering = cls.env["base.substate"].create(
            {
                "name": "In delivering",
                "sequence": 6,
                "target_state_value_id": cls.substate_val_sale.id,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def test_sale_order_substate(self):
        partner = self.env.ref("base.res_partner_1")
        so_test1 = self.substate_test_sale.create(
            {
                "name": "Test base substate to basic sale",
                "partner_id": partner.id,
                "line_ids": [
                    (0, 0, {"name": "line test", "amount": 120.0, "qty": 1.5})
                ],
            }
        )
        self.assertTrue(so_test1.state == "draft")
        self.assertTrue(so_test1.substate_id == self.substate_under_negotiation)

        # Test that validation of sale order change substate_id
        so_test1.button_confirm()
        self.assertTrue(so_test1.state == "sale")
        self.assertTrue(so_test1.substate_id == self.substate_wait_docs)

        # Test that substate_id is set to false if
        # there is not substate corresponding to state
        so_test1.button_cancel()
        self.assertTrue(so_test1.state == "cancel")
        self.assertTrue(not so_test1.substate_id)
