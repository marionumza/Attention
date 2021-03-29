# -*- coding: utf-8 -*-

from odoo import fields, models


class SOAExcelReport(models.TransientModel):
    _name = "soa.excel.report"
    _description = 'SOA Excel Report'

    file_name = fields.Char('Name', size=256)
    file_data = fields.Binary('Account Excel Report', readonly=True)
