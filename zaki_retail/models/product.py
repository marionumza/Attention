# -*- coding: utf-8 -*-

from datetime import date
from odoo import api, models, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    print_cost_amount = fields.Float("Print Cost")
    region_ids = fields.One2many("product.region", inverse_name="product_id", string="Region",  )


class ProductRegion(models.Model):
    _name = 'product.region'

    product_id = fields.Many2one("product.template", string="Product")
    region_id = fields.Many2one("res.branch", string="Region")
    city_id = fields.Many2one("res.city", string="City")
    total_fees = fields.Float(string="Total Fees No.")
    face_uses = fields.Float(string="Fees in use")
    available = fields.Float(string="Available", compute="_compute_available")


    @api.one
    @api.depends('face_uses', 'total_fees')
    def _compute_available(self):
        for rec in self:
            rec.available = rec.total_fees - rec.face_uses




