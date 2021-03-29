from odoo import models,fields,api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    vendor_invoice_number = fields.Char(string='Vendor Invoice Number',required=True)


class AccountMove(models.Model):
    _inherit = 'account.move'

    bo_number = fields.Char(string='Bo Number', compute='_get_bo_number')
    vendor_invoice_number = fields.Char(string='Vendor Invoice Number', compute='_get_vendor_invoice_number')
    vendor_source_document = fields.Char(string='Vendor Source Document', compute='_get_vendor_invoice_number')

    @api.multi
    def _get_vendor_invoice_number(self):
        for record in self:
            invoice_id = self.env['account.invoice'].search([('number', '=', record.name), ('type','=','in_invoice')], limit=1)
            if invoice_id:
                record.vendor_invoice_number = invoice_id.vendor_invoice_number
                record.vendor_source_document = invoice_id.origin
            else:
                record.vendor_invoice_number = ''
                record.vendor_source_document = ''

    @api.multi
    def _get_bo_number(self):
        for record in self:
            invoice_id = self.env['account.invoice'].search([('number', '=', record.name), ('type','=','out_invoice')], limit=1)
            if invoice_id:
                record.bo_number = invoice_id.ref_number
            else:
                record.bo_number = ''

