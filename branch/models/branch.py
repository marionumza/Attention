# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResBranch(models.Model):
    _name = 'res.branch'
    _description = 'Branch'

    name = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)
    telephone = fields.Char(string='Telephone No')
    address = fields.Text('Address')
    city_id=fields.Many2one('res.city',string='City')

class City(models.Model):
    _name = 'res.city'
    _rec_name='name'
    # _rec_name="name"

    branch_id = fields.Many2one(comodel_name="res.branch", string="Region", required=False, )
    name = fields.Char(string="Name",required=True)
