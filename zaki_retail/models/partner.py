# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from datetime import date, timedelta
import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    attention_to = fields.Char(string="Attention To ",  required=False, )
