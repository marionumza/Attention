# -*- coding: utf-8 -*-

import xlwt
import base64
from datetime import datetime, date, timedelta
from io import StringIO
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

class AgedPartnerExcel(models.TransientModel):
    _name = "aged.partner.excel"
    _description = 'Aged Partner Excel'

    date = fields.Date(string='Date')
    partner_ids = fields.Many2many('res.partner', string='Partners')
    field_data = fields.Binary(string='Excel File', readonly=True)
    file_name = fields.Char(size=256)


    @api.multi
    def print_excel(self):
        file = StringIO()
        workbook = xlwt.Workbook()
        format0 = xlwt.easyxf('font:name Angsana New, height 400, colour red,bold True;align: horiz left;borders: left thin, right thin, top thin, bottom thin;')
        format1 = xlwt.easyxf('font:name Angsana New, height 300, bold True;align: horiz center;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour pale_blue;')
        format2 = xlwt.easyxf('font:name Angsana New, height 250;align: horiz center;borders: left thin, right thin, top thin, bottom thin;')
        format3 = xlwt.easyxf('font:name Angsana New, height 250;align: horiz left;borders: left thin, right thin, top thin, bottom thin;')
        format4 = xlwt.easyxf('font:name Angsana New, height 250;align: horiz right;borders: left thin, right thin, top thin, bottom thin;')
        format4.num_format_str = '#,##0.00'
        format5 = xlwt.easyxf('font:name Angsana New, height 300,bold True;align: horiz right;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour pale_blue;')
        format5.num_format_str = '#,##0.00'
        format6 = xlwt.easyxf('font:name Angsana New, height 300, bold True;align: horiz center;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour ivory;')
        format7 = xlwt.easyxf('font:name Angsana New, height 250, bold True;align: horiz center;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour ivory;')
        sheet = workbook.add_sheet('Aged Partner Excel')
        sheet.col(0).width = 256 * 20
        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 256 * 2
        sheet.col(1).width = 256 * 40
        sheet.col(2).width = 256 * 40
        sheet.row(2).height_mismatch = True
        sheet.row(2).height = 256 * 2
        sheet.col(3).width = 256 * 20
        sheet.row(3).height_mismatch = True
        sheet.row(3).height = 256 * 2
        sheet.col(4).width = 256 * 20
        sheet.col(5).width = 256 * 20
        sheet.col(6).width = 256 * 20
        sheet.col(7).width = 256 * 20
        sheet.col(8).width = 256 * 20
        sheet.col(9).width = 256 * 20
        sheet.col(10).width = 256 * 20
        sheet.col(11).width = 256 * 20
        sheet.col(12).width = 256 * 20
        sheet.col(13).width = 256 * 20
        sheet.col(14).width = 256 * 20
        sheet.col(15).width = 256 * 20
        sheet.col(16).width = 256 * 20
        sheet.col(17).width = 256 * 20
        sheet.col(18).width = 256 * 20
        sheet.col(19).width = 256 * 20
        date = self.date.strftime('%d %b %Y')
        sheet.write_merge(0, 1, 0, 6, 'Zaki Advertising Company Ageing Report As ' + date, format0)
        sheet.write_merge(2, 3, 0, 0,'Account', format1)
        sheet.write_merge(2, 3, 1, 1,'Customer Name', format1)
        sheet.write_merge(2, 3, 2, 2,"Seller's Name", format1)
        sheet.write_merge(2, 3, 3, 3,'Due', format1)
        sheet.write_merge(2, 3, 4, 4,'Not Due', format1)
        sheet.write_merge(2, 3, 5, 5,'Total', format1)
        sheet.write_merge(2, 3, 6, 6,'Payment Terms', format6)
        months = int(self.date.strftime('%m'))
        sheet.write_merge(2, 2, 7, 7+months-1, self.date.strftime('%Y'), format1)
        previous_year = self.date.year - 1
        sheet.write_merge(2, 3, 7+months, 7+months, previous_year, format1)
        col = 7
        months_total = {}
        for rec in range(1, months+1):
            months_total.update({rec: []})
            sheet.write(3, col, self.date.replace(month=rec).strftime('%b'), format1)
            col += 1
        partner_ids = self.env['res.partner'].search(['|', ('customer', '=', True), ('supplier', "=", True)]) if not self.partner_ids else self.partner_ids
        row = 4
        total_due_amount = 0.0
        total_notdue_amount = 0.0
        final_amount = 0.0
        final_amount_previous_year = 0.0
        for partner_id in partner_ids:
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 156 * 3
            sheet.write(row, 0, partner_id.ref if partner_id.ref else '', format2)
            sheet.write(row, 1, partner_id.name, format3)
            sheet.write(row, 2, partner_id.user_id.name if partner_id.user_id else '', format3)
            payment_term = ''
            days = 0
            if partner_id.customer and partner_id.property_payment_term_id:
                payment_term = partner_id.property_payment_term_id.name
                days = partner_id.property_payment_term_id.line_ids and partner_id.property_payment_term_id.line_ids[0].days
            elif partner_id.supplier and partner_id.property_supplier_payment_term_id:
                payment_term = partner_id.property_supplier_payment_term_id.name
                days = partner_id.property_supplier_payment_term_id.line_ids and partner_id.property_supplier_payment_term_id.line_ids[0].days
            sheet.write(row, 6, payment_term, format7)
            total_amount = 0.0
            col = 7
            for month in range(1, months+1):
                start_date = datetime.now().replace(day=1, month=month)
                next_month = start_date.replace(day=28) + timedelta(days=4)
                end_date = next_month - timedelta(days=next_month.day)
                invoice_ids = self.env['account.invoice'].search([('date_invoice', '!=', False), 
                            ('date_invoice', '>=', start_date.strftime(DEFAULT_SERVER_DATE_FORMAT)), 
                            ('date_invoice', '<=', end_date.strftime(DEFAULT_SERVER_DATE_FORMAT)),
                            ('partner_id', '=', partner_id.id), ('state', 'in', ('open','paid'))
                            ])
                amount_due = sum(invoice_ids.mapped('residual'))
                total_amount += amount_due
                months_total.get(month).append(amount_due)
                sheet.write(row, col, amount_due, format4)
                col += 1
            final_year = datetime.now().year - 1
            final_date = datetime.now().replace(day=31, month=12, year=final_year)
            account_move_id = self.env['account.move'].search([('date', '=', final_date), ('journal_id.code', '=', 'OPEJ'), ('journal_id.type', '=', 'situation')], limit=1)
            if account_move_id:
                account_move_partner_lines = account_move_id.line_ids.filtered(lambda r:r.partner_id.id == partner_id.id)
                debit_amount = sum(account_move_partner_lines.mapped('debit'))
                credit_amount = sum(account_move_partner_lines.mapped('credit'))
                balance = debit_amount - credit_amount
            sheet.write(row, col, balance, format4)
            final_amount_previous_year += balance
            notdue_amount = 0.0
            if days > 0:
                start_date = datetime.now().replace(day=1, month=months)
                next_month = start_date.replace(day=28) + timedelta(days=4)
                notdue_end_date = next_month - timedelta(days=next_month.day)
                notdue_start_date = notdue_end_date - timedelta(days=days)
                invoice_ids = self.env['account.invoice'].search([('date_invoice', '!=', False), 
                            ('date_invoice', '>=', notdue_start_date.strftime(DEFAULT_SERVER_DATE_FORMAT)), 
                            ('date_invoice', '<=', notdue_end_date.strftime(DEFAULT_SERVER_DATE_FORMAT)),
                            ('partner_id', '=', partner_id.id), ('state', 'in', ('open','paid'))
                            ])
                notdue_amount = sum(invoice_ids.mapped('residual'))
            due_amount = total_amount - notdue_amount
            total_due_amount += due_amount
            total_notdue_amount += notdue_amount
            final_amount += total_amount
            sheet.write(row, 3, due_amount, format4)
            sheet.write(row, 4, notdue_amount, format4)
            sheet.write(row, 5, total_amount, format4)
            row += 1
        sheet.row(row).height_mismatch = True
        sheet.row(row).height = 156 * 3
        sheet.write_merge(row, row, 0, 2, 'Total', format1)
        sheet.write(row, 3, total_due_amount, format5)
        sheet.write(row, 4, total_notdue_amount, format5)
        sheet.write(row, 5, final_amount, format5)
        sheet.write(row, 6, '', format6)
        col = 7
        for rec in range(1, months+1):
            sheet.write(row, col, sum(months_total.get(rec)), format5)
            col += 1
        sheet.write(row, col, final_amount_previous_year, format5)
        filename = ('Aged Partner'+ '.xls')
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodestring(file_data)
        export_id = self.env['aged.partner.excel'].create({'file_name': filename, 'field_data': out})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'aged.partner.excel',
           'view_mode': 'form',
           'view_type': 'form',
           'view_id': self.env.ref('aged_partner_xls.account_aged_partner_report_excel_wizard').id,
           'res_id': export_id.id,
           'target': 'new',
        }