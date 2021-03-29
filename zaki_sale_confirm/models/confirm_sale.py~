from odoo import api, models, fields, _
from datetime import date, timedelta


class Partner(models.Model):
    _inherit = 'res.partner'


    multi_user_id = fields.Many2many('res.users', 'res_partner_res_users_rel', 'partner_id', 'user_id', string='Add Multiple Sale Persons', copy=False, create=False)
