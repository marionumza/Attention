# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        sequence = None
        if vals.get('customer') :
            sequence = self.env['ir.sequence'].search(
                [('code', '=', 'customer')])
        if vals.get('supplier') :
            sequence = self.env['ir.sequence'].search(
                [('code', '=', 'vendor')])
        if sequence:
            vals['ref'] = sequence[0].next_by_id() or '/'
        return super(ResPartner, self).create(vals)

