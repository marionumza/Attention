# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def action_invoice_data_move(self):
        invoice_ids = self.search([('move_id', '!=', False)])
        for invoice_id in invoice_ids:
            for invoice_line_id in invoice_id.invoice_line_ids:
                move_line_id = invoice_id.move_id.line_ids.filtered(lambda r:r.product_id.id == invoice_line_id.product_id.id)
                if move_line_id:
                    move_line_id.write({
                        'branch_id': invoice_line_id.region_id and invoice_line_id.region_id.id or False,
                        'city_id': invoice_line_id.city_id and invoice_line_id.city_id.id or False
                    })