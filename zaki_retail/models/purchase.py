# -*- coding: utf-8 -*-

import datetime as dt
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date
from odoo import api, models, fields, _
from datetime import datetime, date, timedelta


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_id = fields.Many2one(comodel_name="sale.order", string="Sale order")

    @api.onchange('sale_id')
    def change_sale_id(self):
        record = [(5, 0, 0)]
        if self.sale_id:
            for line in self.sale_id.order_line:
                start_date = datetime.now()
                if line.start_date:
                    start_date = line.start_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                record.append((0, 0, {
                                    'product_id': line.product_id.id,
                                    'region_id': line.region_id.id,
                                    'city_id': line.city_id.id,
                                    'taxes_id': [(6, 0, line.tax_id.ids)],
                                    'categ_id': line.categ_id.id,
                                    'name': line.name,
                                    'product_qty': line.product_uom_qty,
                                    'price_unit': line.price_unit,
                                    'product_uom': line.product_id.uom_id.id,
                                    'date_planned': start_date,
                                }))
        self.order_line = record
        self.partner_ref = self.sale_id.partner_id.name

    @api.onchange('partner_id')
    @api.constrains('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            stock_picking_type_id = self.env['stock.picking.type'].search([], limit=1)
            rec.picking_type_id = stock_picking_type_id.id


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    region_id = fields.Many2one("res.branch", string="Region")
    city_id = fields.Many2one("res.city", string="City")
    categ_id = fields.Many2one('product.category', string="Category")
    account_analytic_id = fields.Many2one('account.analytic.account', string="Analytic Account")

    start_date = fields.Date(string="start Date ", default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", )
    campaign_period = fields.Float(string="Campaign Period",  compute='_compute_end_date' )
    campaign = fields.Char(string="campaign", )

    @api.depends('start_date', 'end_date')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                date_format = '%Y-%m-%d'
                d11 = str(rec.start_date)
                d22 = str(rec.end_date)
                d1 = datetime.strptime(d11, date_format).date()
                d2 = datetime.strptime(d22, date_format).date()
                rec.campaign_period = relativedelta(d2, d1).days

    # @api.onchange('product_id', 'region_id', 'city_id')
    # def _onchange_product_id(self):
    #     for rec in self:
    #         res = {}
    #         city_ids = []
    #         if rec.region_id:
    #             for x in rec.region_id.city_ids:
    #                 city_ids.append(x.id)
    #             res['domain'] = {'city_id': [('id', 'in', city_ids)]}
    #         else:
    #             res['domain'] = {'city_id': []}
    #         return res
