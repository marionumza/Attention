
import base64
import binascii
import os
import tempfile
import xlwt
import base64
from io import StringIO, BytesIO
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from xlsxwriter.workbook import Workbook
from PIL import Image
from odoo import models, fields, api, _
from datetime import datetime, date, timedelta

class GeneralLedgerReportWizard(models.TransientModel):
    _inherit = "general.ledger.report.wizard"

    partner_id = fields.Many2one('res.partner', string='Partners')

    @api.onchange('partner_id')
    def general_change_partner_id(self):
        if self.partner_id:
            self.partner_ids = [(6, 0, [self.partner_id.id])]
        else:
            self.partner_ids = [(6, 0, [])]
        self.onchange_partner_ids()
        self.onchange_type_accounts_only()

    @api.model
    def default_get(self, fields):
        res = super(GeneralLedgerReportWizard, self).default_get(fields)
        res['company_id'] = self.env.user.company_id.id
        return res

    @api.multi
    def button_export_xlsx_soa(self):
        model = self.env['report_general_ledger']
        report = model.create(self._prepare_report_general_ledger())
        report.compute_data_for_report()
        file = StringIO()
        workbook = xlwt.Workbook()
        format0 = xlwt.easyxf('font:height 230,bold True;align: wrap on, vert center, horiz center')
        format1 = xlwt.easyxf('font:height 190,bold True;align: horiz right')
        format11 = xlwt.easyxf('font:height 190,bold True;align: horiz center')
        format12 = xlwt.easyxf('font:height 190,bold True;align: wrap on, vert center, horiz center')
        format12.num_format_str = '#,##0.00'
        format2 = xlwt.easyxf('font:height 220,bold True;align: horiz center')
        format3 = xlwt.easyxf('font:height 250,bold True;align: wrap on, vert center, horiz center;borders: left thick, top thick, bottom thick;pattern: pattern solid, fore_colour gray25;')
        format4 = xlwt.easyxf('font:height 250,bold True;align: wrap on, vert center, horiz center;borders: top thick, bottom thick;pattern: pattern solid, fore_colour gray25;')
        format5 = xlwt.easyxf('font:height 250,bold True;align: wrap on, vert center, horiz center;borders: right thick, top thick, bottom thick;pattern: pattern solid, fore_colour gray25;')
        format6 = xlwt.easyxf('font:height 240;align: horiz center;')
        format7 = xlwt.easyxf('font:height 240;align: horiz center')
        format7.num_format_str = '#,##0.00'
        format8 = xlwt.easyxf('font:height 240,bold True;align: horiz center')
        format8.num_format_str = '#,##0.00'
        format9 = xlwt.easyxf('font:height 250,bold True;align: wrap on, vert center, horiz center;borders: top thick, bottom thick;pattern: pattern solid, fore_colour gray25;')
        format9.num_format_str = '#,##0.00'
        format10 = xlwt.easyxf('font:height 250,bold True;align: wrap on, vert center, horiz center;borders: right thick, top thick, bottom thick;pattern: pattern solid, fore_colour gray25;')
        format10.num_format_str = '#,##0.00'
        sheet_name = 'Customer SOA' if self.partner_id.customer else 'Vendor SOA'
        sheet = workbook.add_sheet(sheet_name)
        sheet.col(0).width = 256 * 20
        sheet.col(1).width = 256 * 20
        sheet.col(2).width = 256 * 20
        sheet.col(3).width = 256 * 30
        sheet.col(4).width = 256 * 20
        sheet.col(5).width = 256 * 20
        sheet.col(6).width = 256 * 20
        sheet.col(7).width = 256 * 20
        sheet.row(13).height_mismatch = True
        sheet.row(13).height = 256*2

        company_id = self.env.user.company_id
        binaryData = company_id.logo
        data = base64.b64decode(binaryData)
        # create a temporary file, and save the image
        fobj = tempfile.NamedTemporaryFile(delete=False)
        fname = fobj.name
        fobj.write(data)
        fobj.close()
        # open the image with PIL
        try:
            im = Image.open(fname)
            # do stuff here
        finally:
            pass
        image_parts = im.split()
        r = image_parts[0]
        g = image_parts[1]
        b = image_parts[2]
        img = Image.merge("RGB", (r, g, b))
        img = img.resize((280, 85), Image.ANTIALIAS)
        fo = BytesIO()
        img.save(fo, format='bmp')
        sheet.insert_bitmap_data(fo.getvalue(), 0, 0)
        sheet.write_merge(5, 6, 0, 1, 'Zaki Advertising Company', format0)
        sheet.write(1, 5, 'Printed Date :', format1)
        sheet.write(1, 6, datetime.now().date().strftime(DEFAULT_SERVER_DATE_FORMAT), format11)
        if self.partner_id.customer:
            sheet.write(8, 2, 'Customer Name: ', format1)
        elif self.partner_id.supplier:
            sheet.write(8, 2, 'Vendor Name: ', format1)
        else:
            sheet.write(8, 2, 'Name: ', format1)
        if self.partner_id.name and self.partner_id.ref:
            sheet.write_merge(8,8, 3,6, self.partner_id.name + ' - ' + self.partner_id.ref, format11)
        else:
            sheet.write_merge(8,8, 3,6, self.partner_id.name, format11)
        sheet.write(9, 2, 'Payment Terms: ', format1)
        days = 0
        if self.partner_id.customer and self.partner_id.property_payment_term_id:
            sheet.write(9, 3, self.partner_id.property_payment_term_id.name, format11)
            days = self.partner_id.property_payment_term_id.line_ids and self.partner_id.property_payment_term_id.line_ids[0].days
        elif self.partner_id.supplier and self.partner_id.property_supplier_payment_term_id:
            sheet.write(9, 3, self.partner_id.property_supplier_payment_term_id.name, format11)
            days = self.partner_id.property_supplier_payment_term_id.line_ids and self.partner_id.property_supplier_payment_term_id.line_ids[0].days
        else:
            sheet.write(9, 3, '', format1)
        current_date = datetime.now().date()
        outstanding_date = current_date - timedelta(days=days)
        sheet.write(10, 2, 'Period From :', format1)
        sheet.write(10, 3, ' %s - %s'%(self.date_from, self.date_to), format11)
        sheet.write(13, 0, 'Date', format3)
        sheet.write(13, 1, 'PO', format4)
        sheet.write(13, 2, 'Reference', format4)
        sheet.write(13, 3, 'Description', format4)
        sheet.write(13, 4, 'Debit', format4)
        sheet.write(13, 5, 'Credit', format4)
        sheet.write(13, 6, 'Balance', format5)
        row = 14
        debit = 0.0
        credit = 0.0
        final_balance = 0.0
        outstanding_balance = 0.0
        due_balance = 0.0
        for account in report.account_ids:
            for partner in account.partner_ids:
                sheet.write(row, 1, '', format6)
                sheet.write(row, 2, '', format6)
                sheet.write(row, 3, 'Initial balance', format6)
                sheet.write(row, 4, round(float(partner.initial_debit), 2), format7)
                sheet.write(row, 5, round(float(partner.initial_credit), 2), format7)
                sheet.write(row, 6, round(float(partner.initial_balance), 2), format8)
                debit += partner.initial_debit
                credit +=  partner.initial_credit
                final_balance += partner.initial_balance
                row += 1
                for line in partner.move_line_ids:
                    if line.date:
                        date = line.date.strftime('%d-%b-%y')
                        if line.date >= outstanding_date and line.date <= current_date and days > 0:
                            outstanding_balance += round(float(line.debit), 2)
                            due_balance += round(float(line.credit), 2)
                    else:
                        date =''
                    sheet.write(row, 0, date, format6)
                    if line.move_line_id.partner_id.customer:
                        bo = line.move_line_id.move_id.bo_number or ''
                        invocie_number = line.move_line_id.move_id.name or ''
                        if line.move_line_id.invoice_id.type in ['in_invoice', 'in_refund']:
                            bo = line.move_line_id.move_id.vendor_source_document or ''
                            invocie_number = line.move_line_id.move_id.vendor_invoice_number or ''
                    else:
                        bo = line.move_line_id.move_id.vendor_source_document or ''
                        invocie_number = line.move_line_id.move_id.vendor_invoice_number or ''
                    sheet.write(row, 1, bo, format6)
                    sheet.write(row, 2, invocie_number, format6)
                    sheet.write(row, 3, line.label, format6)
                    sheet.write(row, 4, round(float(line.debit), 2), format7)
                    sheet.write(row, 5, round(float(line.credit), 2), format7)
                    sheet.write(row, 6, round(float(line.cumul_balance), 2), format8)
                    debit += line.debit
                    credit +=  line.credit
                    balance = line.debit - line.credit
                    final_balance += balance
                    row += 1
        sheet.row(row).height_mismatch = True
        sheet.row(row).height = 256*2
        sheet.write_merge(row, row, 0, 3, 'Total & Balance', format3)
        sheet.write(row, 4, round(debit, 2), format9)
        sheet.write(row, 5, round(credit, 2), format9)
        sheet.write(row, 6, round(final_balance, 2), format10)
        outstanding_final_balance = round(final_balance - outstanding_balance, 2)
        due_final_balance = round(final_balance + due_balance, 2)
        if self.partner_id.customer:
            sheet.write(11, 2, 'Outstanding Balance :', format1)
            sheet.write(11, 3, outstanding_final_balance, format12)
        elif self.partner_id.supplier:
            sheet.write(11, 2, 'Due Balance :', format1)
            sheet.write(11, 3, due_final_balance, format12)
        filename = ('General Ledger.xls')
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodestring(file_data)
        export_id = self.env['soa.excel.report'].create({'file_name': filename, 'file_data': out})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'soa.excel.report',
           'view_mode': 'form',
           'view_type': 'form',
           'view_id': self.env.ref('soa_excel_report.soa_xls_report_wizard').id,
           'res_id': export_id.id,
           'target': 'new',
        }