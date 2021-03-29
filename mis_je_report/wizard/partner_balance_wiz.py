from odoo import api, fields, models, _
from io import BytesIO
import xlwt
from xlwt import easyxf
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime, timedelta

class PartnerBalanceWiz(models.TransientModel):
    _name = 'partner.balance.wiz'
    _description = 'Partner Balance Wiz'

    start_date = fields.Date(required=True, default=str(fields.Date.today().year) + '-01-01')
    end_date = fields.Date(required=True, default=fields.Date.today())
    partner_selection = fields.Selection(
        [('customers', 'Customers'),
         ('suppliers', 'Suppliers'),
        ],
        required=True,
        default='customers',
    )
    excel_file = fields.Binary("Excel File")
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries')],
                                   string='Target Moves',
                                   required=True,
                                   default='all')
    hide_partner_at_0 = fields.Boolean(default=True)

    @api.multi
    def action_open(self):
        res_partner_obj = self.env['res.partner']
        account_move_line_obj = self.env['account.move.line']
        open_bal_total = debit_amt_total = credit_amt_total = diff_amt_total = closing_amt_total = 0
        wiz_data = self[0]
        workbook = xlwt.Workbook()
        et_ws = workbook.add_sheet('Balance Sheet')
        title_style = easyxf('borders: right thin; font: name Arial, bold on, height 160; ')
        text_left = easyxf('font:name Calibri,height 220; align: wrap on,horiz left;')
        text_right = easyxf('font:name Calibri,height 220; align: wrap on,horiz right;', num_format_str='#,##0.00')
        text_right_bold = easyxf('font: name Calibri, bold on, height 160; align: horiz right;', num_format_str='#,##0.00')
        emp_txt_blue = easyxf(
            'borders: right thin; font: name Calibri, bold on, height 160, color blue; align: horiz right;')
        style_total_left = xlwt.easyxf(
            'borders: bottom thin, top thin, left_color black, right_color black, top_color black, bottom_color black; font: name Calibri, bold on, height 240, color black; align: wrap on, horiz left, vert center;'
            'pattern: pattern solid, pattern_fore_colour 44'
        )
        style_total = xlwt.easyxf(
            'borders: bottom thin, top thin, left_color black, right_color black, top_color black, bottom_color black; font: name Calibri, bold on, height 240, color black; align: wrap on, horiz center, vert center;'
            'pattern: pattern solid, pattern_fore_colour 44'
        )
        style_total_right = xlwt.easyxf(
            'borders: bottom thin, top thin, left_color black, right_color black, top_color black, bottom_color black; font: name Calibri, bold on, height 240, color black; align: wrap on, horiz right, vert center;'
            'pattern: pattern solid, pattern_fore_colour 44', num_format_str='#,##0.00'
        )
        style_total_center = xlwt.easyxf(
            'borders: bottom thin, top thin, left_color black, right_color black, top_color black, bottom_color black; font: name Calibri, bold on, height 240, color black; align: wrap on, horiz center, vert center;'
            'pattern: pattern solid, pattern_fore_colour 44', num_format_str='#,##0.00'
        )
        style_total1 = xlwt.easyxf(
            'borders: bottom thin, right thin, right thin, top thin, left_color black, right_color black, top_color black, bottom_color black; font: name Calibri, bold on, height 320, color black; align: wrap on, horiz left, vert center;')
        style_main_header = xlwt.easyxf(
            'borders: left_color black, right_color black, top_color black, bottom_color black,bottom thin, right thin, top thin, left thin; font: name Calibri, bold on, height 320, color black; align: wrap on, horiz left, vert center;')
        row = 0
        col = 0
#         et_ws.write_merge(row, row, 0, 6, '')
#         row += 1
        main_header = str(self.env.user.company_id.name)
        if wiz_data.partner_selection == 'customers':
            main_header += " - Customers Balance List"
        elif wiz_data.partner_selection == 'suppliers':
            main_header += " - Vendor Balance List"
#         et_ws.write_merge(0, 0, 0, 1, 'Long Cell')
        et_ws.write_merge(row, row, 0, 7, main_header, style_main_header)
        #xlwt.add_palette_colour("custom_colour_0x21", et_ws)
#         workbook.set_colourRGB("light_blue_21", 0x21, 197, 217, 241)
        et_ws.col(0).width = 8000
        et_ws.row(row).height = 800
        row += 1
#         et_ws.write_merge(row, row, 0, 6, '')
#         row += 1
        date_header = " Start Date " + str(datetime.strptime(str(wiz_data.start_date), DEFAULT_SERVER_DATE_FORMAT).strftime('%d.%m.%Y')) + " End Date "  + str(datetime.strptime(str(wiz_data.end_date), DEFAULT_SERVER_DATE_FORMAT).strftime('%d.%m.%Y'))
        et_ws.write_merge(row, row, 0, 7, date_header, style_total1)
        et_ws.col(0).width = 8000
        et_ws.row(row).height = 600
        # row += 1
#         et_ws.write_merge(row, row, 0, 6, '')
        row += 1
        et_ws.row(row).height = 8000
        if wiz_data.partner_selection == 'customers':
            et_ws.write(row, col, str('Customer code'), style_total_left)
            et_ws.col(col).width = 3000

        elif wiz_data.partner_selection == 'suppliers':
            et_ws.write(row, col, str('Vendor Code'), style_total_left)
            et_ws.col(col).width = 3000
        col += 1
        if wiz_data.partner_selection == 'customers':
            et_ws.write(row, col, str('Customer Name'), style_total)
        elif wiz_data.partner_selection == 'suppliers':
            et_ws.write(row, col, str('Vendor Name'), style_total)
        et_ws.col(col).width = 4600
        if wiz_data.partner_selection == 'customers':
            col += 1
            et_ws.write(row, col, str('Saleperson'), style_total)
            et_ws.col(col).width = 5100
            et_ws.row(row).height = 600
        col += 1
        et_ws.write(row, col, str('Opening '), style_total)
        et_ws.col(col).width = 7100
        col += 1
        et_ws.write(row, col, str('Debit '), style_total)
        et_ws.col(col).width = 7100
        col += 1
        et_ws.write(row, col, str('Credit '), style_total)
        et_ws.col(col).width = 7100
        col += 1
        et_ws.write(row, col, str('Different'), style_total)
        et_ws.col(col).width = 5100
        col += 1
        et_ws.write(row, col, str('Closing '), style_total)
        et_ws.col(col).width = 7100
        et_ws.row(row).height = 600
        
        col = 0
        row += 1
        domain = [('customer', '=', True)]
        if wiz_data.partner_selection == 'suppliers':
            domain = [('supplier', '=', True)]
            domain += [('parent_id', '=', False)]
        domain += [('|')]
        domain += [('active', '=', True)]
        domain += [('active', '=', False)]
        res_partner_ids = res_partner_obj.search(domain)

        open_context = {
                'date_from': wiz_data.start_date,
                'initial_bal': True,
                'strict_range': True
        }
        move_context = {
            'company_id': self.env.user.company_id.id,
            'date_from': wiz_data.start_date,
            'date_to': wiz_data.end_date,
            'strict_range': True,
        }
        if wiz_data.target_move == 'posted':
            open_context.update({'state':'posted'})
            move_context.update({'state':'posted'})

        for res_partner in res_partner_ids:
#             open_debit = res_partner.with_context(open_context).debit
#             open_credit = res_partner.with_context(open_context).credit
#             open_bal = open_credit - open_debit
            open_bal = 0
            tables, where_clause, where_params = account_move_line_obj.with_context(open_context)._query_get()
            where_params = [tuple([res_partner.id])] + where_params
            if where_clause:
                where_clause = 'AND ' + where_clause
            if wiz_data.partner_selection == 'suppliers':
                where_clause += " AND act.type IN ('payable')"
            elif wiz_data.partner_selection == 'customers':
                where_clause += " AND act.type IN ('receivable')"
            self._cr.execute("""SELECT account_move_line.partner_id,SUM(account_move_line.debit) as debit ,SUM(account_move_line.credit) as credit 
                          FROM """ + tables + """
                          LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                          LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                          WHERE account_move_line.partner_id IN %s
                          --AND account_move_line.reconciled IS FALSE
                          """ + where_clause + """
                          GROUP BY account_move_line.partner_id
                          """, where_params)
            result_data = self._cr.fetchone()
            if result_data:
                open_bal = result_data[1] - result_data[2]
#                 open_bal = result_data[2] - result_data[1]
#                 if wiz_data.partner_selection == 'suppliers':
#                     open_bal = result_data[1] - result_data[2]
            debit_amt = credit_amt = 0
            tables, where_clause, where_params = account_move_line_obj.with_context(move_context)._query_get()
            where_params = [tuple([res_partner.id])] + where_params
            if where_clause:
                where_clause = 'AND ' + where_clause
            if wiz_data.partner_selection == 'suppliers':
                where_clause += " AND act.type IN ('payable')"
            elif wiz_data.partner_selection == 'customers':
                where_clause += " AND act.type IN ('receivable')"
            self._cr.execute("""SELECT account_move_line.partner_id,SUM(account_move_line.debit) as debit ,SUM(account_move_line.credit) as credit 
                          FROM """ + tables + """
                          LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                          LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                          WHERE account_move_line.partner_id IN %s
                          --AND account_move_line.reconciled IS FALSE
                          """ + where_clause + """
                          GROUP BY account_move_line.partner_id
                          """, where_params)
            result_data = self._cr.fetchone()
            if result_data:
                debit_amt = result_data[1]
                credit_amt = result_data[2]
            diff_amt = debit_amt - credit_amt
            closing_amt = open_bal + diff_amt
            et_ws.row(row).height = 400
            if wiz_data.hide_partner_at_0:
                if open_bal or debit_amt or credit_amt or diff_amt or closing_amt:
                    et_ws.write(row, col, res_partner.ref or '', text_left)
                    et_ws.write(row, col + 1, res_partner.name, text_left)
                    et_ws.col(col+1).width = 12000
                    et_ws.write(row, col + 2, res_partner.user_id and res_partner.user_id.name or '', text_left)
                    et_ws.col(col+2).width = 12000
                    et_ws.write(row, col + 3, open_bal or '-', text_right)
                    et_ws.write(row, col + 4, debit_amt or '-', text_right)
                    et_ws.write(row, col + 5, credit_amt or '-', text_right)
                    et_ws.write(row, col + 6, diff_amt or '-', text_right)
                    et_ws.write(row, col + 7, closing_amt or '-', text_right)
                    row += 1
            else:
                et_ws.write(row, col, res_partner.ref or '', text_left)
                et_ws.write(row, col + 1, res_partner.name, text_left)
                et_ws.col(col+1).width = 12000
                et_ws.write(row, col + 2, res_partner.user_id and res_partner.user_id.name or '', text_left)
                et_ws.col(col+2).width = 12000
                et_ws.write(row, col + 3, open_bal or '-', text_right)
                et_ws.write(row, col + 4, debit_amt or '-', text_right)
                et_ws.write(row, col + 5, credit_amt or '-', text_right)
                et_ws.write(row, col + 6, diff_amt or '-', text_right)
                et_ws.write(row, col + 7, closing_amt or '-', text_right)
                row += 1
            
            
            open_bal_total += open_bal
            debit_amt_total += debit_amt
            credit_amt_total += credit_amt
            diff_amt_total += diff_amt
            closing_amt_total += closing_amt
#         et_ws.write_merge(row, row, 0, 6, '')

        #undefine Partner
        no_partner_debit_amt = no_partner_credit_amt = no_partner_open_bal = 0
        tables, where_clause, where_params = account_move_line_obj.with_context(open_context)._query_get()
        if where_clause:
            where_clause = 'AND ' + where_clause
        if wiz_data.partner_selection == 'suppliers':
            where_clause += " AND act.type IN ('payable')"
        elif wiz_data.partner_selection == 'customers':
            where_clause += " AND act.type IN ('receivable')"
        self._cr.execute("""SELECT account_move_line.partner_id,SUM(account_move_line.debit) as debit ,SUM(account_move_line.credit) as credit 
                      FROM """ + tables + """
                      LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                      LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                      WHERE account_move_line.partner_id is null
                      --AND account_move_line.reconciled IS FALSE
                      """ + where_clause + """
                      GROUP BY account_move_line.partner_id
                      """, where_params)
        result_data = self._cr.fetchone()
        if result_data:
            no_partner_open_bal = result_data[1] - result_data[2]
#             no_partner_open_bal = result_data[2] - result_data[1]
#             if wiz_data.partner_selection == 'suppliers':
#                 no_partner_open_bal = result_data[1] - result_data[2]
        tables, where_clause, where_params = account_move_line_obj.with_context(move_context)._query_get()
        if where_clause:
            where_clause = 'AND ' + where_clause
        if wiz_data.partner_selection == 'suppliers':
            where_clause += " AND act.type IN ('payable')"
        elif wiz_data.partner_selection == 'customers':
            where_clause += " AND act.type IN ('receivable')"
        self._cr.execute("""SELECT account_move_line.partner_id,SUM(account_move_line.debit) as debit ,SUM(account_move_line.credit) as credit 
                      FROM """ + tables + """
                      LEFT JOIN account_account a ON (account_move_line.account_id=a.id)
                      LEFT JOIN account_account_type act ON (a.user_type_id=act.id)
                      WHERE account_move_line.partner_id is null
                      --AND account_move_line.reconciled IS FALSE
                      """ + where_clause + """
                      GROUP BY account_move_line.partner_id
                      """, where_params)
        result_data = self._cr.fetchone()
        if result_data:
            no_partner_debit_amt = result_data[1]
            no_partner_credit_amt = result_data[2]
        no_partner_diff_amt = no_partner_debit_amt - no_partner_credit_amt
        no_partner_closing_amt = no_partner_open_bal + no_partner_diff_amt
        et_ws.write(row, col, '', text_left)
        et_ws.write(row, col + 1, 'No Partner', text_left)
        et_ws.write(row, col + 2, no_partner_open_bal or '-', text_right)
        et_ws.write(row, col + 3, no_partner_debit_amt or '-', text_right)
        et_ws.write(row, col + 4, no_partner_credit_amt or '-', text_right)
        et_ws.write(row, col + 5, no_partner_diff_amt or '-', text_right)
        et_ws.write(row, col + 6, no_partner_closing_amt or '-', text_right)
        et_ws.write(row, col + 7, '', text_left)
        open_bal_total += no_partner_open_bal
        debit_amt_total += no_partner_debit_amt
        credit_amt_total += no_partner_credit_amt
        diff_amt_total += no_partner_diff_amt
        closing_amt_total += no_partner_closing_amt
        #END

        row += 1
        #et_ws.write_merge(row, row, 0, 1, "Total", style_total_right)
        et_ws.write(row, col, '', style_total_right)
        et_ws.write(row, col + 1, 'Total', style_total_center)
        et_ws.col(0).width = 8000
        et_ws.row(row).height = 600
        et_ws.write(row, col + 2, '', style_total_right)
        et_ws.write(row, col + 3, open_bal_total or '-', style_total_right)
        et_ws.write(row, col + 4, debit_amt_total or '-', style_total_right)
        et_ws.write(row, col + 5, credit_amt_total or '-', style_total_right)
        et_ws.write(row, col + 6, diff_amt_total or '-', style_total_right)
        et_ws.write(row, col + 7, closing_amt_total or '-', style_total_right)
        #et_ws.write(row, col + 7, '-', style_total_right)
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})
        if self.excel_file:
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=partner.balance.wiz&download=\
                    true&field=excel_file&id=%s&filename=%s' % (self.ids[0], 'PartnerBalanceSheet.xls'),
                'target': 'new',
            }
