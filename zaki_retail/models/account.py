# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from datetime import date, timedelta
import datetime
# from num2words import num2words


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    is_assets = fields.Boolean(string="assets", )
    discount_total = fields.Float('Total Discount', compute="_compute_total_discount")
    # total_in_words = fields.Char(compute="_total_amount_in_words")
    ref_number = fields.Char(string="Ref Number", )
    number = fields.Char(readonly=True, copy=False)
    number2 = fields.Char(readonly=True, copy=False)
    seq_number = fields.Char(string="Seq/Number", readonly=True, required=True, copy=False, default='New')

    @api.model
    def create(self, vals):
        if vals.get('seq_number', 'New') == 'New':
            vals['seq_number'] = self.env['ir.sequence'].next_by_code('account.invoice') or 'New'
        res = super(AccountInvoice, self).create(vals)
        if not vals['origin']:
            res.action_invoice_open()
            res.number = res.move_id.name
            res.number2 = res.move_id.name
            res.action_invoice_cancel()
            res.action_invoice_draft()
        return res

    def action_invoice_draft(self):
        res = super(AccountInvoice, self).action_invoice_draft()
        self.number = self.number2
        return res


    # @api.one
    # @api.depends('discount_total')
    # def _total_amount_in_words(self):
    #     for rec in self:
    #         rec.total_in_words = num2words(rec.amount_total)
    #         rec.total_in_words = num2words(rec.amount_total, lang='ar')

    @api.one
    @api.depends('invoice_line_ids')
    def _compute_total_discount(self):
        for rec in self:
            rec.discount_total = sum(x.gross_rate - x.net_cost for x in rec.invoice_line_ids if x.disc > 0)

    def _prepare_invoice_line_from_po_line(self, line):
        result = super(AccountInvoice, self)._prepare_invoice_line_from_po_line(line)
        new = {
            'account_id': line.categ_id.property_account_expense_categ_id.id,
            'region_id': line.region_id.id,
            'categ_id': line.categ_id.id,
            'city_id': line.city_id.id,
            # 'analytic_ids': [(6, 0, line.account_analytic_id.ids)],
        }
        result.update(new)
        return result

    # @api.multi
    # def action_invoice_open(self):
    #     res = super(AccountInvoice, self).action_invoice_open()
    #     total = 0.0
    #     amount_untaxed = 0.0
    #     for rec in self:
    #         for line in rec.invoice_line_ids:
    #             line.price_subtotal = (line.net_cost + line.printing_cost)
    #             line.prc_subtotal = (line.net_cost + line.printing_cost)
    #             amount_untaxed += line.prc_subtotal
    #             for tax in line.invoice_line_tax_ids:
    #                 total += line.price_subtotal * (tax.amount / 100)
    #         rec.amount_tax = total
    #         rec.amount_untaxed = amount_untaxed
    #         rec.amount_total = rec.amount_untaxed + rec.amount_tax
    #     return res

    # @api.constrains('invoice_line_ids', 'invoice_line_ids.tax_id' )
    # def _constrains_tax(self):
    #     total =0.0
    #     amount_untaxed = 0.0
    #     for rec in self:
    #         for line in rec.invoice_line_ids:
    #             line.price_subtotal = (line.net_cost + line.printing_cost)
    #             line.prc_subtotal = (line.net_cost + line.printing_cost)
    #             amount_untaxed += line.prc_subtotal
    #             for tax in line.invoice_line_tax_ids:
    #                 total += line.price_subtotal * (tax.amount /100)
    #         rec.amount_tax = total
    #         rec.amount_untaxed = amount_untaxed
    #         rec.amount_total = rec.amount_untaxed + rec.amount_tax


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    ref = fields.Char(string="Reference", )
    asset_category = fields.Char(string="Asset Category", required=False, )
    region_id = fields.Many2one("res.branch", string="Region")
    city_id = fields.Many2one("res.city", string="City")
    paid_faces = fields.Integer(string="Paid Faces")
    free_faces = fields.Integer(string="Free Faces")
    paid_weeks = fields.Integer(string="Paid Weeks")
    free_weeks = fields.Integer(string="Free Weeks")
    analytic_ids = fields.Many2many(comodel_name="account.analytic.account", relation="", string="Dimension", )
    # discount = fields.Float(string="Discount %")
    disc = fields.Float(string="Discount %")
    campaign_name = fields.Text(string="Campaign Name")
    prc_unit = fields.Float("Price Unit", )

    # company_name = fields.Text(string="Company Name")
    # categ_id = fields.Many2one('product.category',string="Category")
    start_date = fields.Date(string="start Date ", default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", compute='_compute_end_date')
    gross_rate = fields.Float(string="Gross Rate", )
    net_cost = fields.Float(string="Net cost", )
    printing_cost = fields.Float(string="Printing cost", store=1)
    categ_id = fields.Many2one('product.category', string="Category")
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', )
    value_ids = fields.Many2one('product.attribute.value',       string='Size (Frequency)')


    @api.onchange('pricelist_id')
    def _onchange_product(self):
        for rec in self:
            if rec.invoice_id.type == 'out_refund':
                rec.city_id = rec.pricelist_id.city_id.id
            for l in rec.pricelist_id.item_ids:
                if l.product_tmpl_id == rec.product_id.product_tmpl_id:
                    rec.print_cost_amount = l.printing_cost
                    rec.prc_unit = l.fixed_price

    # is_print = fields.Boolean(string="Printing cost?",  )
    # header_is_print = fields.Boolean(related="order_id.is_print",store=1, string="header printing" )
    # prc_subtotal = fields.Float("Subtotal")

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

    @api.depends('start_date')
    def _compute_end_date(self):
        for rec in self:
            if rec.paid_weeks:
                rec.end_date = rec.start_date + datetime.timedelta(days=rec.paid_weeks * 7)

    @api.onchange('categ_id')
    def _onchange_product_id(self):
        for rec in self:
            rec.account_id = rec.categ_id.property_account_income_categ_id.id

# class SaleAdvancePaymentInv(models.TransientModel):
#     _inherit = "sale.advance.payment.inv"
#
#     @api.multi
#     def create_invoices(self):
#         res = super(SaleAdvancePaymentInv, self).create_invoices()
#         print(">>>>>>>>>>>>Res<<<<<<<<<<<", res)
#         print(">>>>>>>>>>>>Res<<<<<<<<<<<", res['res_id'])
#         invoice_id = self.env['account.invoice'].browse(res['res_id'])
#         print(invoice_id)
#         invoice_id.action_invoice_open()
#         invoice_id.action_invoice_cancel()
#         invoice_id.action_invoice_draft()
#
#         return res
