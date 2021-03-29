# -*- coding: utf-8 -*-

import xlwt
import base64
from io import StringIO
from odoo import api, fields, models, _

class AccountProfitLossReport(models.TransientModel):
    _name = "account.profit.loss.excel.report"
    _description = 'Account Profit Loss Excel Report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    region_ids = fields.Many2many('res.branch', string='Region')
    city_ids = fields.Many2many('res.city', string='City')
    product_ids = fields.Many2many('product.product', string='Products')

    @api.multi
    def print_excel(self):
        file = StringIO()
        workbook = xlwt.Workbook()
        format0 = xlwt.easyxf('font:height 600,bold True;align: horiz left')
        format1 = xlwt.easyxf('font:bold True;align: horiz left')
        format2 = xlwt.easyxf('font:height 300,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;borders: left thin, right thin, top thin, bottom thin;')
        format3 = xlwt.easyxf('font:height 200,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;borders: left thin, right thin, top thin, bottom thin;')
        format4 = xlwt.easyxf('font:height 200,bold True;align: horiz center;borders: right thin, bottom thin;')
        format5 = xlwt.easyxf('font:height 200,bold True;align: horiz center;borders: right thin;')
        format6 = xlwt.easyxf('font:height 200,bold True;align: horiz center;borders: right thin, left thin;')
        format7 = xlwt.easyxf('font:height 200,bold True;align: horiz center;borders: right thin, left thin, bottom thin;')
        format8 = xlwt.easyxf('font:height 200,bold True,colour red;pattern: pattern solid, fore_colour light_green;align: horiz left;borders: left thin, right thin, top thin, bottom thin;')
        format9 = xlwt.easyxf('font:height 200;align: horiz left;borders: left thin, right thin, top thin, bottom thin;')
        format10 = xlwt.easyxf('font:height 200;align: horiz right;borders: left thin, right thin, top thin, bottom thin;')
        format11 = xlwt.easyxf('font:height 200,bold True;align: horiz right;borders: left thin, right thin, top thin, bottom thin;')
        format12 = xlwt.easyxf('font:height 200,bold True;align: horiz right;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour cyan_ega;')
        format13 = xlwt.easyxf('font:height 200,bold True;pattern: pattern solid, fore_colour gray25;align: horiz center;borders: left thin, right thin, top thin, bottom thin;')

        format14 = xlwt.easyxf('font:height 200,bold True;align: horiz right;borders: left thin, right thin, top thin, bottom thin;pattern: pattern solid, fore_colour orange;')
        format15 = xlwt.easyxf('font:height 200,bold True;pattern: pattern solid, fore_colour orange;align: horiz center;borders: left thin, right thin, top thin, bottom thin;')

        sheet = workbook.add_sheet('Project Profit & Loss Analysis')
        sheet.col(7).width = 256 * 20
        sheet.col(8).width = 256 * 20
        sheet.col(9).width = 256 * 20
        sheet.col(10).width = 256 * 20
        sheet.col(11).width = 256 * 18
        sheet.col(12).width = 256 * 20
        sheet.col(13).width = 256 * 20
        sheet.col(14).width = 256 * 20
        sheet.col(15).width = 256 * 20
        sheet.col(16).width = 256 * 18
        sheet.write_merge(0, 3, 0, 6, 'Zaki Advertising Company', format0)
        sheet.write_merge(4, 4, 0, 3, 'Project Profit & Loss Analysis', format1)
        sheet.write_merge(6, 8, 0, 3, 'Location', format2)
        sheet.write_merge(6, 8, 4, 6, 'Network', format2)
        sheet.write_merge(6, 6, 7, 8, 'Sales - Rent', format3)
        sheet.write(7, 7, '4100003', format5)
        sheet.write(7, 8, '4100005', format5)
        sheet.write(8, 7, 'Sales-Rent', format4)
        sheet.write(8, 8, 'Sales-Rent Prvt.', format4)
        sheet.write_merge(6, 6, 9, 10, 'Sales - Print', format3)
        sheet.write(7, 9, '4100002', format5)
        sheet.write(7, 10, '4100004', format5)
        sheet.write(8, 9, 'Sales-Print', format4)
        sheet.write(8, 10, 'Sales-Print Prvt.', format4)
        sheet.write_merge(6, 8, 11, 11, 'Total Sales', format2)
        sheet.write_merge(6, 6, 12, 13, 'COS - Rent', format3)
        sheet.write(7, 12, '5100003', format5)
        sheet.write(7, 13, '5100005', format5)
        sheet.write(8, 12, 'COS-Rent', format4)
        sheet.write(8, 13, 'COS-Rent Prvt.', format4)
        sheet.write_merge(6, 6, 14, 15, 'COS - Print', format3)
        sheet.write(7, 14, '5100002', format5)
        sheet.write(7, 15, '5100004', format5)
        sheet.write(8, 14, 'COS-Print', format4)
        sheet.write(8, 15, 'COS-Print Prvt.', format4)
        sheet.write_merge(6, 8, 16, 16, 'Total COS', format2)
        sheet.col(17).width = 256 * 3
        sheet.col(18).width = 256 * 20
        sheet.col(19).width = 256 * 20
        sheet.col(20).width = 256 * 20
        sheet.col(21).width = 256 * 20
        sheet.col(22).width = 256 * 20
        sheet.col(23).width = 256 * 20
        sheet.col(24).width = 256 * 20
        sheet.col(25).width = 256 * 20
        sheet.col(26).width = 256 * 20
        sheet.col(27).width = 256 * 20
        sheet.col(28).width = 256 * 18
        sheet.write_merge(6, 6, 18, 27, 'OH COS', format3)
        sheet.write(7, 18, '5200001', format6)
        sheet.write(7, 19, '5200002', format6)
        sheet.write(7, 20, '5200003', format6)
        sheet.write(7, 21, '5200004', format6)
        sheet.write(7, 22, '5200005', format6)
        sheet.write(7, 23, '5200006', format6)
        sheet.write(7, 24, '5200007', format6)
        sheet.write(7, 25, '5200008', format6)
        sheet.write(7, 26, '5200009', format6)
        sheet.write(7, 27, '5200010', format6)
        sheet.write(8, 18, 'Bank Chrgs', format7)
        sheet.write(8, 19, 'Maintenance', format7)
        sheet.write(8, 20, 'Assets Depr.', format7)
        sheet.write(8, 21, 'Rent & Rates', format7)
        sheet.write(8, 22, 'Buss. Travel', format7)
        sheet.write(8, 23, 'Sub-Allw.', format7)
        sheet.write(8, 24, 'Other Transpt', format7)
        sheet.write(8, 25, 'Sales Comm', format7)
        sheet.write(8, 26, 'Volume Rebate', format7)
        sheet.write(8, 27, 'Others', format7)
        sheet.write_merge(6, 8, 28, 28, 'Total OH COS', format3)
        sheet.col(29).width = 256 * 3
        sheet.col(30).width = 256 * 20
        sheet.col(31).width = 256 * 20
        sheet.col(32).width = 256 * 20
        sheet.col(33).width = 256 * 20
        sheet.write_merge(6, 6, 30, 33, 'Total', format3)
        sheet.write_merge(7, 8, 30, 30, 'Sales', format7)
        sheet.write_merge(7, 8, 31, 31, 'COS', format7)
        sheet.write_merge(7, 8, 32, 32, 'Total GP', format7)
        sheet.write_merge(7, 8, 33, 33, 'GP%', format7)
        final_data = []
        domain = [('date', '>=', self.start_date), ('date', '<=', self.end_date), 
                ('branch_id', '!=', False), ('city_id', '!=', False),
                ('account_id.code', 'in', ['5200001', '5200002', '5200003', '5200004', 
                '5200005', '5200006', '5200007', '5200008', '5200009', '5200010',
                '4100002', '4100003', '4100004', '4100005', '5100003', '5100005', '5100002', '5100004']), 
                ('product_id', '!=', False), ('account_id', '!=', False)]
        if self.region_ids:
            domain += [('branch_id', 'in', self.region_ids.ids)]
        if self.city_ids:
            domain += [('city_id', 'in', self.city_ids.ids)]
        if self.product_ids:
            domain += [('product_id', 'in', self.product_ids.ids)]
        move_line_ids = self.env['account.move.line'].search(domain)
        if move_line_ids:
            region_ids = self.region_ids if self.region_ids else self.env['res.branch'].search([])
            city_ids = self.city_ids if self.city_ids else self.env['res.city'].search([('branch_id', '!=', False), ('branch_id', 'in', region_ids.ids)])
            for region_id in region_ids:
                values = {'region': region_id}
                region_move_lines = move_line_ids.filtered(lambda r: r.branch_id.id == region_id.id)
                city_data = []
                if region_move_lines:
                    for city_id in city_ids.filtered(lambda r: r.branch_id.id == region_id.id):
                        city_move_lines = region_move_lines.filtered(lambda r:r.city_id.id == city_id.id)
                        for city_move_line_id in city_move_lines:
                            city_values = {
                                'product_id': city_move_line_id.product_id,
                                'debit_total': city_move_line_id.debit,
                                'credit_total': city_move_line_id.credit,
                                'code': city_move_line_id.account_id.code,
                                'city': city_id
                            }
                            city_data.append(city_values)
                other_data = []
                region_final_data = []
                if city_data:
                    for line in city_data:
                        if {'city': line.get('city'), 'product_id': line.get('product_id')} in other_data:
                            for temp in region_final_data:
                                if temp.get('city') and temp.get('product_id') and temp.get('city') == line.get('city') \
                                    and temp.get('product_id') == line.get('product_id'):
                                    dict1 = temp.get('code_data')
                                    if dict1.get(line.get('code')):
                                        dict1.get(line.get('code')).append({'deposit_amount': line.get('debit_total'), 'credit_amount': line.get('credit_total')})
                                    else:
                                        dict1[line.get('code')] = [{'deposit_amount': line.get('debit_total'), 'credit_amount': line.get('credit_total')}]
                                    temp['code_data'] = dict1
                        else:
                            other_data.append({'city': line.get('city'), 'product_id': line.get('product_id')})
                            region_final_data_values = {
                                'city': line.get('city'),
                                'product_id': line.get('product_id'),
                                'code_data': {line.get('code'): [{'deposit_amount': line.get('debit_total'), 'credit_amount': line.get('credit_total')}]}
                            }
                            region_final_data.append(region_final_data_values)
                values.update({
                    'lines_data': region_final_data
                })
                final_data.append(values)
        print (">>>>>>>", final_data)
        print (">>>>>>>\n\n")
        row = 9
        final_total_code_4100003 = 0.0
        final_total_code_4100005 = 0.0
        final_total_code_4100002 = 0.0
        final_total_code_4100004 = 0.0
        final_total_code_5100003 = 0.0
        final_total_code_5100005 = 0.0
        final_total_code_5100002 = 0.0
        final_total_code_5100004 = 0.0
        final_total_code_5200001 = 0.0
        final_total_code_5200002 = 0.0
        final_total_code_5200003 = 0.0
        final_total_code_5200004 = 0.0
        final_total_code_5200005 = 0.0
        final_total_code_5200006 = 0.0
        final_total_code_5200007 = 0.0
        final_total_code_5200008 = 0.0
        final_total_code_5200009 = 0.0
        final_total_code_5200010 = 0.0
        final_sales_total = 0.0
        final_purchase_total = 0.0
        final_difference_total = 0.0
        final_other_cos_total = 0.0
        final_gp_percent_total = 0.0
        for excel_data in final_data:
            print (">>>>>>>excel_data.get('region').name", excel_data.get('region').name)
            sheet.write_merge(row, row, 0, 3, excel_data.get('region').name, format8)
            sheet.write_merge(row, row, 4, 6, '', format8)
            sheet.write_merge(row, row, 7, 8, '', format8)
            sheet.write_merge(row, row, 9, 10, '', format8)
            sheet.write(row, 11, '', format8)
            sheet.write_merge(row, row, 12, 13, '', format8)
            sheet.write_merge(row, row, 14, 15, '', format8)
            sheet.write(row, 16, '', format8)
            sheet.write_merge(row, row, 18, 27, '', format8)
            sheet.write(row, 28, '', format8)
            sheet.write_merge(row, row, 30, 33, '', format8)
            row += 1
            city_names = []
            semi_total_code_4100003 = 0.0
            semi_total_code_4100005 = 0.0
            semi_total_code_4100002 = 0.0
            semi_total_code_4100004 = 0.0
            semi_total_code_5100003 = 0.0
            semi_total_code_5100005 = 0.0
            semi_total_code_5100002 = 0.0
            semi_total_code_5100004 = 0.0
            semi_total_code_5200001 = 0.0
            semi_total_code_5200002 = 0.0
            semi_total_code_5200003 = 0.0
            semi_total_code_5200004 = 0.0
            semi_total_code_5200005 = 0.0
            semi_total_code_5200006 = 0.0
            semi_total_code_5200007 = 0.0
            semi_total_code_5200008 = 0.0
            semi_total_code_5200009 = 0.0
            semi_total_code_5200010 = 0.0
            semi_sales_total = 0.0
            semi_purchase_total = 0.0
            semi_difference_total = 0.0
            semi_other_cos_total = 0.0
            semi_gp_percent_total = 0.0
            for excel_lines in excel_data.get('lines_data'):
                sheet.write_merge(row, row, 0, 3, excel_lines.get('city').name, format9)
                sheet.write_merge(row, row, 4, 6, excel_lines.get('product_id').name, format9)
                code_data = excel_lines.get('code_data')
                code_4100003 = 0.0
                code_4100005 = 0.0
                code_4100002 = 0.0
                code_4100004 = 0.0
                code_5100003 = 0.0
                code_5100005 = 0.0
                code_5100002 = 0.0
                code_5100004 = 0.0
                code_5200001 = 0.0
                code_5200002 = 0.0
                code_5200003 = 0.0
                code_5200004 = 0.0
                code_5200005 = 0.0
                code_5200006 = 0.0
                code_5200007 = 0.0
                code_5200008 = 0.0
                code_5200009 = 0.0
                code_5200010 = 0.0
                if code_data.get('4100003'):
                    deposit_amount_4100003 = sum([rec.get('deposit_amount') for rec in code_data.get('4100003')])
                    credit_amount_4100003 = sum([rec.get('credit_amount') for rec in code_data.get('4100003')])
                    code_4100003 = deposit_amount_4100003 - credit_amount_4100003
                if code_data.get('4100005'):
                    deposit_amount_4100005 = sum([rec.get('deposit_amount') for rec in code_data.get('4100005')])
                    credit_amount_4100005 = sum([rec.get('credit_amount') for rec in code_data.get('4100005')])
                    code_4100005 = deposit_amount_4100005 - credit_amount_4100005
                if code_data.get('4100002'):
                    deposit_amount_4100002 = sum([rec.get('deposit_amount') for rec in code_data.get('4100002')])
                    credit_amount_4100002 = sum([rec.get('credit_amount') for rec in code_data.get('4100002')])
                    code_4100002 = deposit_amount_4100002 - credit_amount_4100002
                if code_data.get('4100004'):
                    deposit_amount_4100004 = sum([rec.get('deposit_amount') for rec in code_data.get('4100004')])
                    credit_amount_4100004 = sum([rec.get('credit_amount') for rec in code_data.get('4100004')])
                    code_4100004 = deposit_amount_4100004 - credit_amount_4100004
                if code_data.get('5100003'):
                    deposit_amount_5100003 = sum([rec.get('deposit_amount') for rec in code_data.get('5100003')])
                    credit_amount_5100003 = sum([rec.get('credit_amount') for rec in code_data.get('5100003')])
                    code_5100003 = deposit_amount_5100003 - credit_amount_5100003
                if code_data.get('5100005'):
                    deposit_amount_5100005 = sum([rec.get('deposit_amount') for rec in code_data.get('5100005')])
                    credit_amount_5100005 = sum([rec.get('credit_amount') for rec in code_data.get('5100005')])
                    code_5100005 = deposit_amount_5100005 - credit_amount_5100005
                if code_data.get('5100002'):
                    deposit_amount_5100002 = sum([rec.get('deposit_amount') for rec in code_data.get('5100002')])
                    credit_amount_5100002 = sum([rec.get('credit_amount') for rec in code_data.get('5100002')])
                    code_5100002 = deposit_amount_5100002 - credit_amount_5100002
                if code_data.get('5100004'):
                    deposit_amount_5100004 = sum([rec.get('deposit_amount') for rec in code_data.get('5100004')])
                    credit_amount_5100004 = sum([rec.get('credit_amount') for rec in code_data.get('5100004')])
                    code_5100004 = deposit_amount_5100004 - credit_amount_5100004
                if code_data.get('5200001'):
                    deposit_amount_5200001 = sum([rec.get('deposit_amount') for rec in code_data.get('5200001')])
                    credit_amount_5200001 = sum([rec.get('credit_amount') for rec in code_data.get('5200001')])
                    code_5200001 = deposit_amount_5200001 - credit_amount_5200001
                if code_data.get('5200002'):
                    deposit_amount_5200002 = sum([rec.get('deposit_amount') for rec in code_data.get('5200002')])
                    credit_amount_5200002 = sum([rec.get('credit_amount') for rec in code_data.get('5200002')])
                    code_5200002 = deposit_amount_5200002 - credit_amount_5200002
                if code_data.get('5200003'):
                    deposit_amount_5200003 = sum([rec.get('deposit_amount') for rec in code_data.get('5200003')])
                    credit_amount_5200003 = sum([rec.get('credit_amount') for rec in code_data.get('5200003')])
                    code_5200003 = deposit_amount_5200003 - credit_amount_5200003
                if code_data.get('5200004'):
                    deposit_amount_5200004 = sum([rec.get('deposit_amount') for rec in code_data.get('5200004')])
                    credit_amount_5200004 = sum([rec.get('credit_amount') for rec in code_data.get('5200004')])
                    code_5200004 = deposit_amount_5200004 - credit_amount_5200004
                if code_data.get('5200005'):
                    deposit_amount_5200005 = sum([rec.get('deposit_amount') for rec in code_data.get('5200005')])
                    credit_amount_5200005 = sum([rec.get('credit_amount') for rec in code_data.get('5200005')])
                    code_5200005 = deposit_amount_5200005 - credit_amount_5200005
                if code_data.get('5200006'):
                    deposit_amount_5200006 = sum([rec.get('deposit_amount') for rec in code_data.get('5200006')])
                    credit_amount_5200006 = sum([rec.get('credit_amount') for rec in code_data.get('5200006')])
                    code_5200006 = deposit_amount_5200006 - credit_amount_5200006
                if code_data.get('5200007'):
                    deposit_amount_5200007 = sum([rec.get('deposit_amount') for rec in code_data.get('5200007')])
                    credit_amount_5200007 = sum([rec.get('credit_amount') for rec in code_data.get('5200007')])
                    code_5200007 = deposit_amount_5200007 - credit_amount_5200007
                if code_data.get('5200008'):
                    deposit_amount_5200008 = sum([rec.get('deposit_amount') for rec in code_data.get('5200008')])
                    credit_amount_5200008 = sum([rec.get('credit_amount') for rec in code_data.get('5200008')])
                    code_5200008 = deposit_amount_5200008 - credit_amount_5200008
                if code_data.get('5200009'):
                    deposit_amount_5200009 = sum([rec.get('deposit_amount') for rec in code_data.get('5200009')])
                    credit_amount_5200009 = sum([rec.get('credit_amount') for rec in code_data.get('5200009')])
                    code_5200009 = deposit_amount_5200009 - credit_amount_5200009
                if code_data.get('5200010'):
                    deposit_amount_5200010 = sum([rec.get('deposit_amount') for rec in code_data.get('5200010')])
                    credit_amount_5200010 = sum([rec.get('credit_amount') for rec in code_data.get('5200010')])
                    code_5200010 = deposit_amount_5200010 - credit_amount_5200010

                sales_total = code_4100002 + code_4100003 + code_4100004 + code_4100005

                sheet.write(row, 7, round(code_4100003, 2), format10)
                sheet.write(row, 8, round(code_4100005, 2), format10)
                sheet.write(row, 9, round(code_4100002, 2), format10)
                sheet.write(row, 10, round(code_4100004, 2), format10)
                sheet.write(row, 11, round(sales_total, 2), format11)

                semi_total_code_4100003 += code_4100003
                semi_total_code_4100005 += code_4100005
                semi_total_code_4100002 += code_4100002
                semi_total_code_4100004 += code_4100004
                semi_total_code_5100003 += code_5100003
                semi_total_code_5100005 += code_5100005
                semi_total_code_5100002 += code_5100002
                semi_total_code_5100004 += code_5100004
                semi_total_code_5200001 += code_5200001
                semi_total_code_5200002 += code_5200002
                semi_total_code_5200003 += code_5200003
                semi_total_code_5200004 += code_5200004
                semi_total_code_5200005 += code_5200005
                semi_total_code_5200006 += code_5200006
                semi_total_code_5200007 += code_5200007
                semi_total_code_5200008 += code_5200008
                semi_total_code_5200009 += code_5200009
                semi_total_code_5200010 += code_5200010

                semi_sales_total += sales_total

                purchase_total = code_5100002 + code_5100003 + code_5100004 + code_5100005

                semi_purchase_total += purchase_total

                sheet.write(row, 12, round(code_5100003, 2), format10)
                sheet.write(row, 13, round(code_5100005, 2), format10)
                sheet.write(row, 14, round(code_5100002, 2), format10)
                sheet.write(row, 15, round(code_5100004, 2), format10)
                sheet.write(row, 16, round(purchase_total, 2), format11)

                city_name = excel_lines.get('city').name
                sheet.write(row, 18, round(code_5200001, 2), format10)
                sheet.write(row, 19, round(code_5200002, 2), format10)
                sheet.write(row, 20, round(code_5200003, 2), format10)
                sheet.write(row, 21, round(code_5200004, 2), format10)
                sheet.write(row, 22, round(code_5200005, 2), format10)
                sheet.write(row, 23, round(code_5200006, 2), format10)
                sheet.write(row, 24, round(code_5200007, 2), format10)
                sheet.write(row, 25, round(code_5200008, 2), format10)
                sheet.write(row, 26, round(code_5200009, 2), format10)
                sheet.write(row, 27, round(code_5200010, 2), format10)

                other_cos_total = code_5200001 + code_5200002 + code_5200003 + code_5200004 + \
                                  code_5200005 + code_5200006 + code_5200007 + code_5200008 + \
                                  code_5200009 + code_5200010

                semi_other_cos_total += other_cos_total

                sheet.write(row, 28, round(other_cos_total, 2), format11)
                city_names.append(city_name)
                difference = sales_total - purchase_total
                if sales_total > 0:
                    gp_percent = (difference/sales_total)*100
                else:
                    gp_percent = 0

                semi_gp_percent_total += gp_percent
                semi_difference_total += difference

                sheet.write(row, 30, round(sales_total, 2), format10)
                sheet.write(row, 31, round(purchase_total, 2), format10)
                sheet.write(row, 32, round(difference, 2), format10)
                sheet.write(row, 33, round(gp_percent, 2), format10)
                row += 1
            sheet.write_merge(row, row, 0, 6, 'Total', format13)
            final_total_code_4100003 += semi_total_code_4100003
            final_total_code_4100005 += semi_total_code_4100005
            final_total_code_4100002 += semi_total_code_4100002 
            final_total_code_4100004 += semi_total_code_4100004 
            final_total_code_5100003 += semi_total_code_5100003 
            final_total_code_5100005 += semi_total_code_5100005 
            final_total_code_5100002 += semi_total_code_5100002 
            final_total_code_5100004 += semi_total_code_5100004 
            final_total_code_5200001 += semi_total_code_5200001
            final_total_code_5200002 += semi_total_code_5200002
            final_total_code_5200003 += semi_total_code_5200003
            final_total_code_5200004 += semi_total_code_5200004
            final_total_code_5200005 += semi_total_code_5200005
            final_total_code_5200006 += semi_total_code_5200006
            final_total_code_5200007 += semi_total_code_5200007
            final_total_code_5200008 += semi_total_code_5200008
            final_total_code_5200009 += semi_total_code_5200009
            final_total_code_5200010 += semi_total_code_5200010
            final_sales_total += semi_sales_total
            final_purchase_total += semi_purchase_total
            final_difference_total += semi_difference_total
            final_other_cos_total += semi_other_cos_total
            final_gp_percent_total += semi_gp_percent_total
            sheet.write(row, 7, round(semi_total_code_4100003, 2), format12)
            sheet.write(row, 8, round(semi_total_code_4100005, 2), format12)
            sheet.write(row, 9, round(semi_total_code_4100002, 2), format12)
            sheet.write(row, 10, round(semi_total_code_4100004, 2), format12)
            sheet.write(row, 11, round(semi_sales_total, 2), format12)
            sheet.write(row, 12, round(semi_total_code_5100003, 2), format12)
            sheet.write(row, 13, round(semi_total_code_5100005, 2), format12)
            sheet.write(row, 14, round(semi_total_code_5100002, 2), format12)
            sheet.write(row, 15, round(semi_total_code_5100004, 2), format12)
            sheet.write(row, 16, round(semi_purchase_total, 2), format12)
            sheet.write(row, 18, round(semi_total_code_5200001, 2), format12)
            sheet.write(row, 19, round(semi_total_code_5200002, 2), format12)
            sheet.write(row, 20, round(semi_total_code_5200003, 2), format12)
            sheet.write(row, 21, round(semi_total_code_5200004, 2), format12)
            sheet.write(row, 22, round(semi_total_code_5200005, 2), format12)
            sheet.write(row, 23, round(semi_total_code_5200006, 2), format12)
            sheet.write(row, 24, round(semi_total_code_5200007, 2), format12)
            sheet.write(row, 25, round(semi_total_code_5200008, 2), format12)
            sheet.write(row, 26, round(semi_total_code_5200009, 2), format12)
            sheet.write(row, 27, round(semi_total_code_5200010, 2), format12)
            sheet.write(row, 28, round(semi_other_cos_total, 2), format12)
            sheet.write(row, 30, round(semi_sales_total, 2), format12)
            sheet.write(row, 31, round(semi_purchase_total, 2), format12)
            sheet.write(row, 32, round(semi_difference_total, 2), format12)
            sheet.write(row, 33, round(semi_gp_percent_total, 2), format12)
            row += 1
        row += 1
        sheet.write_merge(row, row, 0, 6, 'Total', format15)
        sheet.write(row, 7, round(final_total_code_4100003, 2), format14)
        sheet.write(row, 8, round(final_total_code_4100005, 2), format14)
        sheet.write(row, 9, round(final_total_code_4100002, 2), format14)
        sheet.write(row, 10, round(final_total_code_4100004, 2), format14)
        sheet.write(row, 11, round(final_sales_total, 2), format14)
        sheet.write(row, 12, round(final_total_code_5100003, 2), format14)
        sheet.write(row, 13, round(final_total_code_5100005, 2), format14)
        sheet.write(row, 14, round(final_total_code_5100002, 2), format14)
        sheet.write(row, 15, round(final_total_code_5100004, 2), format14)
        sheet.write(row, 16, round(final_purchase_total, 2), format14)
        sheet.write(row, 18, round(final_total_code_5200001, 2), format14)
        sheet.write(row, 19, round(final_total_code_5200002, 2), format14)
        sheet.write(row, 20, round(final_total_code_5200003, 2), format14)
        sheet.write(row, 21, round(final_total_code_5200004, 2), format14)
        sheet.write(row, 22, round(final_total_code_5200005, 2), format14)
        sheet.write(row, 23, round(final_total_code_5200006, 2), format14)
        sheet.write(row, 24, round(final_total_code_5200007, 2), format14)
        sheet.write(row, 25, round(final_total_code_5200008, 2), format14)
        sheet.write(row, 26, round(final_total_code_5200009, 2), format14)
        sheet.write(row, 27, round(final_total_code_5200010, 2), format14)
        sheet.write(row, 28, round(final_other_cos_total, 2), format14)
        sheet.write(row, 30, round(final_sales_total, 2), format14)
        sheet.write(row, 31, round(final_purchase_total, 2), format14)
        sheet.write(row, 32, round(final_difference_total, 2), format14)
        sheet.write(row, 33, round(final_gp_percent_total, 2), format14)

        filename = ('Project Profit & Loss Analysis'+ '.xls')
        workbook.save(filename)
        file = open(filename, "rb")
        file_data = file.read()
        out = base64.encodestring(file_data)
        export_id = self.env['profit.loss.excel'].create({'file_name': filename, 'field_data': out})
        return {
           'type': 'ir.actions.act_window',
           'res_model': 'profit.loss.excel',
           'view_mode': 'form',
           'view_type': 'form',
           'view_id': self.env.ref('zaki_profit_loss_excel_report.account_profit_loss_report_excel_wizard').id,
           'res_id': export_id.id,
           'target': 'new',
        }