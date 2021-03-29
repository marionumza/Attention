# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def action_analytic_data_move(self):
        move_line_ids = self.search([('analytic_ids', '!=', False)])
        for record in move_line_ids:
            record.analytic_account_id = record.analytic_ids and record.analytic_ids[0].id