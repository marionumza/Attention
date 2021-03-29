# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from datetime import date, timedelta
import datetime


class AccountMove(models.Model):
    _inherit = 'account.move'
    inv_seq_number = fields.Char(string="Invoice Number", compute="_compute_inv_seq_number")

    @api.one
    @api.depends('name')
    def _compute_inv_seq_number(self):
        for rec in self:
            invoice_id = self.env['account.invoice'].search([('number', '=', rec.name)])
            rec.inv_seq_number = invoice_id.seq_number


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    city_id = fields.Many2one("res.city", string="City",)
    analytic_ids = fields.Many2many("account.analytic.account",string="Dimension")

    department_id = fields.Many2one('hr.department', 'Department',related="analytic_account_id.department_id")

    # @api.onchange('branch_id', 'city_id')
    # def _onchange_product_id(self):
    #     for rec in self:
    #         res = {}
    #         city_ids = []
    #         if rec.branch_id:
    #             for x in rec.branch_id.city_ids:
    #                 city_ids.append(x.id)
    #             res['domain'] = {'city_id': [('id', 'in', city_ids)]}
    #         else:
    #             res['domain'] = {'city_id': []}
    #         return res
