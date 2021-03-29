from odoo import api, models, fields, _
from datetime import date, timedelta
import datetime


class AccountMoveLine(models.Model):
    _inherit = 'hr.employee'

    code=fields.Char('Code')

class AccountUserinfo(models.Model):
    _inherit = 'res.users'

    discount_print_allow =fields.Boolean(string="allow discount")