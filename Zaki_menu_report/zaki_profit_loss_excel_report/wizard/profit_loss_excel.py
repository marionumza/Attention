# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProfitLossExcel(models.TransientModel):
    _name = "profit.loss.excel"
    _description = 'Profit Loss Excel'

    field_data = fields.Binary(string='Excel File', readonly=True)
    file_name = fields.Char(size=256)