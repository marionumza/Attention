# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, models, fields, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    is_print = fields.Boolean(string="Is Print ?", )
    is_rent = fields.Boolean(string="Is Rent ?", )

