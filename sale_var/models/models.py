# -*- coding: utf-8 -*-

from odoo import models, fields, api


class mmmmmm(models.Model):
    _inherit = 'sale.order.line'

    product_template = fields.Many2one(comodel_name="product.template", string="Size", required=False, )

    # attribute_id = fields.Many2one('product.attribute', 'Attribute')
    # value_ids = fields.Many2one('product.attribute.value', string='Size')

    @api.onchange('product_template')
    def onchange_product_varient(self):
        for rec in self:
            return {'domain': {'product_id':[('product_tmpl_id', '=' , rec.product_template.id)]}}


# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"
#     @api.onchange('product_id')
#     def _onchange_cust_categ_id(self):
#         return {'domain': {'value_ids': [('id', '=', self.product_id.id)]}}


    # @api.onchange('product_id')
    #     def onchange_product_id(self):
    #       if self.order_id.pricelist_id:
    #         product_template_ids = self.env['product.template'].search([]).filtered(
    #             lambda x: self.order_id.pricelist_id.id in x.item_ids.mapped('pricelist_id').ids)
    #         product_ids = self.env['product.product'].search([('product_tmpl_id', 'in', product_template_ids.ids)])
    #         return {'domain': {'product_id': [('id', 'in', product_ids.ids)]}}
