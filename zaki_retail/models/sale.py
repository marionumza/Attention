# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from datetime import date, timedelta
import datetime
# from odoo.tools.misc import formatLang


# from num2words import num2words


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line')
    def _compute_total_print(self):
        for rec in self:
            x = 0.0
            for line in self.order_line:
                # print("22222222222222",line.order_id.name)
                # print("@@@@@@@@@@@",line.categ_id.name)
                print('self.order_line',line)
                if line.categ_id.is_print:
                    x += line.price_subtotal

            rec.total_print = x

    @api.depends('order_line')
    def _compute_total_rent(self):
        for rec in self:
            x = 0.0
            for line in rec.order_line:
                # print("33333333333",line.order_id.name)
                # print("&&&&&&&&&&&77",line.categ_id.name)
                if line.categ_id.is_rent:
                    x += line.price_subtotal

            rec.total_rent = x



    is_print = fields.Boolean(string="Printing cost?", )
    discount_total = fields.Float('Total Discount', compute="_compute_total_discount")

    total_in_words = fields.Char(compute="_total_amount_in_words")
    ref_number = fields.Char(string="Ref Number", )
    total_print = fields.Float('Production Cost', compute="_compute_total_print")
    total_rent = fields.Float('Total Rent', compute="_compute_total_rent")
    # attention_to = fields.Char(string="Attention To ",related='partner_id.attention_to' )

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create()
        invoice_ids = self.env['account.invoice'].browse(res)
        for rec in invoice_ids:
            rec.action_invoice_open()
            rec.number = rec.move_id.name
            rec.number2 = rec.move_id.name
            rec.action_invoice_cancel()
            rec.action_invoice_draft()
        return rec

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        new = {'ref_number': self.ref_number}
        res.update(new)

        return res

    # @api.multi
    # def _prepare_invoice(self):
    #     res = super(SaleOrder, self)._prepare_invoice()
    #     # print (">>>>>>>>>> ",res)
    #     new = {'ref_number': self.ref_number}
    #     res.update(new)
    #     # print (">>>>>>>>>> ",res)
    #
    #     return res

    @api.one
    @api.depends('discount_total')
    def _total_amount_in_words(self):
        for rec in self:
            pass
            # rec.total_in_words = num2words(rec.amount_total)
            # rec.total_in_words = num2words(rec.amount_total, lang='ar')

    @api.one
    @api.depends('order_line')
    def _compute_total_discount(self):
        for rec in self:
            rec.discount_total = sum(x.gross_rate - x.net_cost for x in rec.order_line if x.disc > 0)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_invoice_line(self, qty):
        new = {
            'region_id': self.region_id.id,
            'city_id': self.city_id.id,
            'categ_id': self.categ_id.id,
            'paid_faces': self.paid_faces,
            'free_faces': self.free_faces,
            'paid_weeks': self.paid_weeks,
            'free_weeks': self.free_weeks,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'gross_rate': self.gross_rate,
            'net_cost': self.net_cost,
            'prc_unit': self.prc_unit,
            'disc': self.disc,
            'pricelist_id': self.pricelist_id.id,
            'value_ids': self.value_ids.id,
            'campaign_name': self.campaign_name,
            'printing_cost': self.printing_cost,
            'account_id': self.categ_id.property_account_income_categ_id.id,
        }
        result = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        result.update(new)
        return result

    def _compute_allow(self):
        print("hi zaki ",self.env.user.discount_print_allow)
        for rec in self :
            if self.env.user.discount_print_allow:
                rec.is_allow =True


    region_id = fields.Many2one("res.branch",related="pricelist_id.city_id.branch_id", string="Region")
    city_id = fields.Many2one("res.city", related="pricelist_id.city_id", string="City")
    paid_faces = fields.Integer(string="Paid Faces")
    free_faces = fields.Integer(string="Free Faces")
    paid_weeks = fields.Integer(string="Paid Weeks")
    free_weeks = fields.Integer(string="Free Weeks")
    disc = fields.Float(string="Discount %")
    campaign_name = fields.Text(string="Campaign Name")
    start_date = fields.Date(string="start Date ", default=fields.Date.context_today)
    end_date = fields.Date(string="End Date", compute='_compute_end_date')
    gross_rate = fields.Float(string="Gross Rate", compute='_compute_gross_rate')
    net_cost = fields.Float(string="Net cost", compute='_compute_net')
    printing_cost = fields.Float(string="Printing Sale")
    is_print = fields.Boolean(string="print?", )
    is_rent = fields.Boolean(string="rent?", )
    header_is_print = fields.Boolean(related="order_id.is_print", string="header printing")
    prc_unit = fields.Float("Price Unit", )
    print_cost_amount = fields.Float(string="", required=False, )
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', )
    categ_id = fields.Many2one('product.category', string="Category")
    tot_discount = fields.Float(string="Total discount", compute="_compute_tot_discount" )
    value_ids = fields.Many2one('product.attribute.value',       string='Size (Frequency)')
    is_allow = fields.Boolean(string="is allow?",compute="_compute_allow" )

    def insert_line(self):
        self.ensure_one()
        vals = {

            'order_id': self.order_id.id,
            'product_id': self.product_id.id,
            'region_id': self.region_id.id,
            'city_id': self.city_id.id,
            'categ_id': self.categ_id.id,
            'paid_faces': self.paid_faces,
            'free_faces': self.free_faces,
            'paid_weeks': self.paid_weeks,
            'free_weeks': self.free_weeks,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'gross_rate': self.gross_rate,
            'net_cost': self.net_cost,
            'prc_unit': self.prc_unit,
            'price_unit': self.price_unit,
            'disc': self.disc,
            'tax_id': [(6, 0, [tax.id for tax in self.tax_id])]
        }
        self.copy(default=vals)
        # self.env['sale.order.line'].create(vals)

    @api.one
    @api.depends('price_unit', 'disc')
    def _compute_tot_discount(self):
        for rec in self:
            # if rec.categ_id.name == "Print" or rec.categ_id.complete_name == "Private - Printing":
            if rec.categ_id.is_print :
                rec.tot_discount = (rec.price_subtotal * (rec.disc/100))
                # rec.tot_discount = (rec.gross_rate * (rec.disc/100))
                print( 'kk',rec.tot_discount , (rec.disc/100) , rec.price_subtotal )
            # elif rec.categ_id.complete_name == "Rent" or rec.categ_id.complete_name == "Private – Renting":
            elif rec.categ_id.is_rent:
                rec.tot_discount = (rec.gross_rate * (rec.disc / 100))
                print( "mm",rec.tot_discount )
            elif rec.categ_id.complete_name == "Print And Rent":
                rec.tot_discount = ((rec.price_subtotal+rec.net_cost) * (rec.disc/100)) #XXXXXXXXX

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        for rec in self:
            # if rec.categ_id.complete_name == "Print" or rec.categ_id.complete_name == "Print and Rent":
            if rec.categ_id.is_print:
                rec.is_print = True
            else:
                rec.is_print = False
            if rec.categ_id.is_rent :
                rec.is_rent = True
            if rec.pricelist_id:
                for l in rec.pricelist_id.item_ids:
                    if l.applied_on == '1_product':
                        print("1111111111", rec.categ_id.complete_name, rec.categ_id.name)

                        if l.product_tmpl_id == rec.product_id.product_tmpl_id and rec.categ_id.is_print:
                            print("22222222222")
                            # rec.print_cost_amount = l.printing_cost
                            rec.prc_unit = l.printing_cost
                            rec.price_unit = rec.prc_unit
                        # elif l.product_tmpl_id == rec.product_id.product_tmpl_id and rec.categ_id.name == "Rent":
                        #     print("3333333333333")
                        #     rec.print_cost_amount = l.printing_cost
                        #     rec.prc_unit = l.fixed_price
                        #     rec.price_unit = rec.prc_unit
                        elif l.product_tmpl_id == rec.product_id.product_tmpl_id and rec.categ_id.is_rent:
                            print("printing_cost",l.printing_cost)
                            rec.print_cost_amount = l.printing_cost
                            print("fixed_price-------",l.fixed_price)
                            rec.prc_unit = l.fixed_price
                            print(",,,,,,,3333333", rec.prc_unit)
                            rec.price_unit = rec.prc_unit

                    if l.applied_on == '0_product_variant':
                        if rec.value_ids:
                            if l.value_ids == rec.value_ids and rec.categ_id.is_print:
                                rec.print_cost_amount = l.printing_cost
                                rec.prc_unit = l.printing_cost
                                rec.price_unit = rec.prc_unit
                            elif l.value_ids == rec.value_ids:
                                rec.print_cost_amount = l.printing_cost
                                rec.prc_unit = l.fixed_price
                                rec.price_unit = rec.prc_unit
                        else:
                            if l.product_id == rec.product_id and rec.categ_id.is_print:
                                rec.print_cost_amount = l.printing_cost
                                rec.prc_unit = l.printing_cost
                                rec.price_unit = rec.prc_unit
                            elif l.product_id == rec.product_id:
                                rec.print_cost_amount = l.printing_cost
                                rec.prc_unit = l.fixed_price
                                rec.price_unit = rec.prc_unit

    @api.depends('start_date', 'paid_weeks', 'free_weeks')
    def _compute_end_date(self):
        for rec in self:
            if rec.paid_weeks and rec.start_date:
                rec.end_date = rec.start_date + datetime.timedelta(days=rec.paid_weeks * 7) + datetime.timedelta(
                    days=rec.free_weeks * 7)

    @api.onchange('pricelist_id')
    def _onchange_product(self):
        for rec in self:
            for l in rec.pricelist_id.item_ids:
                if l.applied_on == '1_product':
                    print("1111111111",rec.categ_id.complete_name,rec.categ_id.name)

                    if l.product_tmpl_id == rec.product_id.product_tmpl_id and rec.categ_id.is_print:
                        print("22222222222")
                        # rec.print_cost_amount = l.printing_cost
                        rec.prc_unit = l.printing_cost
                        rec.price_unit = rec.prc_unit
                    # elif l.product_tmpl_id == rec.product_id.product_tmpl_id and rec.categ_id.name == "Rent":
                    #     print("3333333333333")
                    #     rec.print_cost_amount = l.printing_cost
                    #     rec.prc_unit = l.fixed_price
                    #     rec.price_unit = rec.prc_unit
                    elif l.product_tmpl_id == rec.product_id.product_tmpl_id and rec.categ_id.is_rent:
                        print("33333333333333")
                        rec.print_cost_amount = l.printing_cost
                        print("!!!!!!!",l.fixed_price)
                        rec.prc_unit = l.fixed_price
                        print(",,,,,,,",rec.prc_unit)
                        rec.price_unit = rec.prc_unit

                if l.applied_on == '0_product_variant':
                    if rec.value_ids:
                        if l.value_ids == rec.value_ids and rec.categ_id.is_print:
                            rec.print_cost_amount = l.printing_cost
                            rec.prc_unit = l.printing_cost
                            rec.price_unit = rec.prc_unit
                        elif l.value_ids == rec.value_ids :
                            rec.print_cost_amount = l.printing_cost
                            rec.prc_unit = l.fixed_price
                            rec.price_unit = rec.prc_unit
                    else:
                        if l.product_id == rec.product_id and rec.categ_id.is_print:
                            rec.print_cost_amount = l.printing_cost
                            rec.prc_unit = l.printing_cost
                            rec.price_unit = rec.prc_unit
                        elif l.product_id == rec.product_id:
                            rec.print_cost_amount = l.printing_cost
                            rec.prc_unit = l.fixed_price
                            rec.price_unit = rec.prc_unit

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

    @api.one
    @api.depends('paid_faces', 'prc_unit', 'free_faces', 'paid_weeks', 'free_weeks')
    def _compute_gross_rate(self):
        for rec in self:
            rec.gross_rate = (rec.paid_faces + rec.free_faces) * rec.prc_unit * (rec.paid_weeks + rec.free_weeks)

    # @api.one
    @api.depends('paid_faces', 'prc_unit', 'paid_weeks', 'disc', )
    def _compute_net(self):
        for rec in self:
            rec.net_cost = (((rec.paid_faces * rec.prc_unit) * rec.paid_weeks) - (
                    rec.paid_weeks * rec.paid_faces * rec.prc_unit) * (rec.disc / 100))

    @api.onchange('is_print', 'paid_faces', 'paid_weeks', 'disc',
                  'header_is_print', 'print_cost_amount',
                  'product_id', 'categ_id')
    def _compute_printing_cost(self):
        print("_compute_printing_cost")
        for rec in self:
            if rec.header_is_print == False:
                if rec.categ_id.name == "Print And Rent":
                    rec.printing_cost = (rec.paid_faces + rec.free_faces) * rec.print_cost_amount
                    rec.price_unit = rec.printing_cost + rec.net_cost
                elif rec.categ_id.is_print or rec.categ_id.name == "Private - Printing":
                    print("is_print",(rec.paid_faces + rec.free_faces) * rec.print_cost_amount)
                    print("44444",rec.paid_faces ,rec.free_faces , rec.print_cost_amount)
                    rec.printing_cost = (rec.paid_faces + rec.free_faces) * rec.print_cost_amount
                    rec.price_unit = rec.net_cost
                    # rec.price_unit = rec.printing_cost
                elif rec.categ_id.is_rent or rec.categ_id.name == "Private – Renting":
                    print("net_cost",rec.net_cost)
                    rec.price_unit = rec.net_cost
            else:
                print("rec.header_is_print")
                if rec.categ_id.name == "Print And Rent":
                    rec.printing_cost = (rec.paid_faces + rec.free_faces) * rec.print_cost_amount
                    rec.price_unit = rec.printing_cost + rec.net_cost
                elif rec.categ_id.is_print or rec.categ_id.name == "Private - Printing":
                    rec.printing_cost = (rec.paid_faces + rec.free_faces) * rec.print_cost_amount
                    # rec.price_unit = rec.printing_cost
                    rec.price_unit = rec.net_cost
                elif rec.categ_id.is_rent or rec.categ_id.name == "Private – Renting":
                    rec.price_unit = rec.net_cost

    @api.onchange('printing_cost')
    def _onchange_printing_cost(self):
        for rec in self:
            if rec.header_is_print == True:
                rec.price_unit = rec.printing_cost


class ProductPriceListItem(models.Model):
    _inherit = 'product.pricelist'

    city_id = fields.Many2one("res.city", string="City")


class ProductPriceListItem(models.Model):
    _inherit = 'product.pricelist.item'
    _rec_name = "printing_cost"

    printing_cost = fields.Float(string="", required=False, )
    value_ids = fields.Many2one('product.attribute.value', string='Size')
