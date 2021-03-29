# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, models
from datetime import datetime

class AgedPartnerBalanceXslx(models.AbstractModel):
    _name = 'report.a_f_r.report_aged_partner_balance_xlsx'
    _inherit = 'report.account_financial_report.abstract_report_xlsx'

    def _get_report_name(self, report):
        report_name = _('Aged Partner Balance')
        return self._get_report_complete_name(report, report_name)

    def _get_report_columns(self, report):
        if not report.show_move_line_details:
            year = str(datetime.now().year - 1)
            return {
                0: {'header': _('Partner'), 'field': 'partner', 'width': 70},
                1: {'header': _('Due'),
                    'field': 'amount_residual',
                    'field_footer_total': 'cumul_amount_residual',
                    'type': 'amount',
                    'width': 14},
                2: {'header': _('Not Due'),
                    'field': 'current',
                    'field_footer_total': 'cumul_current',
                    'field_footer_percent': 'percent_current',
                    'type': 'amount',
                    'width': 14},
                3: {'header': _('Total'),
                    'field': 'total',
                    'field_footer_total': 'cumul_total',
                    'field_footer_percent': 'percent_total',
                    'type': 'amount',
                    'width': 14},
                4: {'header': _('Payment terms'),
                    'field': 'payment_terms',
                    'field_footer_total': '',
                    'field_footer_percent': '',
                    'width': 14},
                5: {'header': _('Sales Person'),
                    'field': 'sales_person',
                    'field_footer_total': '',
                    'field_footer_percent': '',
                    'width': 14},
                6: {'header': _(u'January'),
                    'field': 'age_30_days',
                    'field_footer_total': 'cumul_age_30_days',
                    'field_footer_percent': 'percent_age_30_days',
                    'type': 'amount',
                    'width': 14},
                7: {'header': _(u'February'),
                    'field': 'age_60_days',
                    'field_footer_total': 'cumul_age_60_days',
                    'field_footer_percent': 'percent_age_60_days',
                    'type': 'amount',
                    'width': 14},
                8: {'header': _(u'March'),
                    'field': 'age_90_days',
                    'field_footer_total': 'cumul_age_90_days',
                    'field_footer_percent': 'percent_age_90_days',
                    'type': 'amount',
                    'width': 14},
                9: {'header': _(u'April'),
                    'field': 'age_120_days',
                    'field_footer_total': 'cumul_age_120_days',
                    'field_footer_percent': 'percent_age_120_days',
                    'type': 'amount',
                    'width': 14},
                10: {'header': _(u'May'),
                    'field': 'age_120_days',
                    'field_footer_total': 'cumul_age_150_days',
                    'field_footer_percent': 'percent_age_150_days',
                    'type': 'amount',
                    'width': 14},
                11: {'header': _(u'June'),
                     'field': 'age_180_days',
                     'field_footer_total': 'cumul_age_180_days',
                     'field_footer_percent': 'percent_age_180_days',
                     'type': 'amount',
                     'width': 14},
                12: {'header': _(u'July'),
                     'field': 'age_210_days',
                     'field_footer_total': 'cumul_age_210_days',
                     'field_footer_percent': 'percent_age_210_days',
                     'type': 'amount',
                     'width': 14},
                13: {'header': _(u'August'),
                     'field': 'age_240_days',
                     'field_footer_total': 'cumul_age_240_days',
                     'field_footer_percent': 'percent_age_240_days',
                     'type': 'amount',
                     'width': 14},
                14: {'header': _(u'September'),
                     'field': 'age_270_days',
                     'field_footer_total': 'cumul_age_270_days',
                     'field_footer_percent': 'percent_age_270_days',
                     'type': 'amount',
                     'width': 14},
                15: {'header': _(u'October'),
                     'field': 'age_300_days',
                     'field_footer_total': 'cumul_age_300_days',
                     'field_footer_percent': 'percent_age_300_days',
                     'type': 'amount',
                     'width': 14},
                16: {'header': _(u'November'),
                     'field': 'age_330_days',
                     'field_footer_total': 'cumul_age_330_days',
                     'field_footer_percent': 'percent_age_330_days',
                     'type': 'amount',
                     'width': 14},
                17: {'header': _(u'December'),
                     'field': 'age_360_days',
                     'field_footer_total': 'cumul_age_360_days',
                     'field_footer_percent': 'percent_age_360_days',
                     'type': 'amount',
                     'width': 14},
                18: {'header': _(year),
                     'field': 'older',
                     'field_footer_total': 'cumul_older',
                     'field_footer_percent': 'percent_older',
                     'type': 'amount',
                     'width': 14},
            }
        return {
            0: {'header': _('Date'), 'field': 'date', 'width': 11},
            1: {'header': _('Entry'), 'field': 'entry', 'width': 18},
            2: {'header': _('Journal'), 'field': 'journal', 'width': 8},
            3: {'header': _('Account'), 'field': 'account', 'width': 9},
            4: {'header': _('Partner'), 'field': 'partner', 'width': 25},
            5: {'header': _('Ref - Label'), 'field': 'label', 'width': 40},
            6: {'header': _('Due date'), 'field': 'date_due', 'width': 11},
            7: {'header': _('Residual'),
                'field': 'amount_residual',
                'field_footer_total': 'cumul_amount_residual',
                'field_final_balance': 'amount_residual',
                'type': 'amount',
                'width': 14},
            8: {'header': _('Current'),
                'field': 'current',
                'field_footer_total': 'cumul_current',
                'field_footer_percent': 'percent_current',
                'field_final_balance': 'current',
                'type': 'amount',
                'width': 14},
            9: {'header': _('Total'),
                'field': 'total',
                'field_footer_total': 'cumul_total',
                'field_footer_percent': 'percent_total',
                'type': 'amount',
                'width': 14},
            10: {'header': _('Payment terms'),
                 'field': 'payment_terms',
                 'field_footer_total': '',
                 'field_footer_percent': '',
                 'width': 14},
            11: {'header': _('Sales Person'),
                'field': 'sales_person',
                'field_footer_total': '',
                'field_footer_percent': '',
                'width': 14},
            12: {'header': _(u'Age ≤ 30 day'),
                 'field': 'age_30_days',
                 'field_footer_total': 'cumul_age_30_days',
                 'field_footer_percent': 'percent_age_30_days',
                 'field_final_balance': 'age_30_days',
                 'type': 'amount',
                 'width': 14},
            13: {'header': _(u'Age ≤ 60 day'),
                 'field': 'age_60_days',
                 'field_footer_total': 'cumul_age_60_days',
                 'field_footer_percent': 'percent_age_60_days',
                 'field_final_balance': 'age_60_days',
                 'type': 'amount',
                 'width': 14},
            14: {'header': _(u'Age ≤ 90 day'),
                 'field': 'age_90_days',
                 'field_footer_total': 'cumul_age_90_days',
                 'field_footer_percent': 'percent_age_90_days',
                 'field_final_balance': 'age_90_days',
                 'type': 'amount',
                 'width': 14},
            15: {'header': _(u'Age ≤ 120 day'),
                 'field': 'age_120_days',
                 'field_footer_total': 'cumul_age_120_days',
                 'field_footer_percent': 'percent_age_120_days',
                 'field_final_balance': 'age_120_days',
                 'type': 'amount',
                 'width': 14},
            16: {'header': _(u'Age ≤ 150 day'),
                 'field': 'age_120_days',
                 'field_footer_total': 'cumul_age_150_days',
                 'field_footer_percent': 'percent_age_150_days',
                 'field_final_balance': 'age_150_days',
                 'type': 'amount',
                 'width': 14},
            17: {'header': _(u'Age ≤ 180 day'),
                 'field': 'age_120_days',
                 'field_footer_total': 'cumul_age_180_days',
                 'field_footer_percent': 'percent_age_180_days',
                 'field_final_balance': 'age_180_days',
                 'type': 'amount',
                 'width': 14},
            18: {'header': _(u'Age ≤ 210 day'),
                 'field': 'age_210_days',
                 'field_footer_total': 'cumul_age_210_days',
                 'field_footer_percent': 'percent_age_210_days',
                 'field_final_balance': 'age_210_days',
                 'type': 'amount',
                 'width': 14},
            19: {'header': _(u'Age ≤ 240 day'),
                 'field': 'age_120_days',
                 'field_footer_total': 'cumul_age_240_days',
                 'field_footer_percent': 'percent_age_240_days',
                 'field_final_balance': 'age_240_days',
                 'type': 'amount',
                 'width': 14},
            20: {'header': _(u'Age ≤ 270 day'),
                 'field': 'age_270_days',
                 'field_footer_total': 'cumul_age_270_days',
                 'field_footer_percent': 'percent_age_270_days',
                 'field_final_balance': 'age_270_days',
                 'type': 'amount',
                 'width': 14},
            21: {'header': _(u'Age ≤ 300 day'),
                 'field': 'age_300_days',
                 'field_footer_total': 'cumul_age_300_days',
                 'field_footer_percent': 'percent_age_300_days',
                 'field_final_balance': 'age_300_days',
                 'type': 'amount',
                 'width': 14},
            22: {'header': _(u'Age ≤ 330 day'),
                 'field': 'age_240_days',
                 'field_footer_total': 'cumul_age_330_days',
                 'field_footer_percent': 'percent_age_330_days',
                 'field_final_balance': 'age_330_days',
                 'type': 'amount',
                 'width': 14},
            23: {'header': _(u'Age ≤ 360 day'),
                 'field': 'age_360_days',
                 'field_footer_total': 'cumul_age_360_days',
                 'field_footer_percent': 'percent_age_360_days',
                 'field_final_balance': 'age_360_days',
                 'type': 'amount',
                 'width': 14},
            24: {'header': _('Older'),
                 'field': 'older',
                 'field_footer_total': 'cumul_older',
                 'field_footer_percent': 'percent_older',
                 'field_final_balance': 'older',
                 'type': 'amount',
                 'width': 14},
        }

    def _get_report_filters(self, report):
        return [
            [_('Date at filter'), report.date_at],
            [_('Target moves filter'),
             _('All posted entries') if report.only_posted_moves else _(
                 'All entries')],
        ]

    def _get_col_count_filter_name(self):
        return 2

    def _get_col_count_filter_value(self):
        return 3

    def _get_col_pos_footer_label(self, report):
        return 0 if not report.show_move_line_details else 5

    def _get_col_count_final_balance_name(self):
        return 5

    def _get_col_pos_final_balance_label(self):
        return 5

    def _generate_report_content(self, workbook, report):
        if not report.show_move_line_details:
            # For each account
            for account in report.account_ids:
                # Write account title
                self.write_array_title(account.code + ' - ' + account.name)

                # Display array header for partners lines
                self.write_array_header(date_at=report.date_at)

                # Display partner lines
                for partner in account.partner_ids:
                    self.write_line(partner.line_ids)

                # Display account lines
                self.write_account_footer(report,
                                          account,
                                          _('Total'),
                                          'field_footer_total',
                                          self.format_header_right,
                                          self.format_header_amount,
                                          False)
                self.write_account_footer(report,
                                          account,
                                          _('Percents'),
                                          'field_footer_percent',
                                          self.format_right_bold_italic,
                                          self.format_percent_bold_italic,
                                          True)

                # 2 lines break
                self.row_pos += 2
        else:
            # For each account
            for account in report.account_ids:
                # Write account title
                self.write_array_title(account.code + ' - ' + account.name)

                # For each partner
                for partner in account.partner_ids:
                    # Write partner title
                    self.write_array_title(partner.name)

                    # Display array header for move lines
                    self.write_array_header(date_at=report.date_at)

                    # Display account move lines
                    for line in partner.move_line_ids:
                        self.write_line(line)

                    # Display ending balance line for partner
                    self.write_ending_balance(partner.line_ids)

                    # Line break
                    self.row_pos += 1

                # Display account lines
                self.write_account_footer(report,
                                          account,
                                          _('Total'),
                                          'field_footer_total',
                                          self.format_header_right,
                                          self.format_header_amount,
                                          False)
                self.write_account_footer(report,
                                          account,
                                          _('Percents'),
                                          'field_footer_percent',
                                          self.format_right_bold_italic,
                                          self.format_percent_bold_italic,
                                          True)

                # 2 lines break
                self.row_pos += 2

    def write_ending_balance(self, my_object):
        """
            Specific function to write ending partner balance
            for Aged Partner Balance
        """
        name = None
        label = _('Partner cumul aged balance')
        super(AgedPartnerBalanceXslx, self).write_ending_balance(
            my_object, name, label
        )

    def write_account_footer(self, report, account, label, field_name,
                             string_format, amount_format, amount_is_percent):
        """
            Specific function to write account footer for Aged Partner Balance
        """
        col_pos_footer_label = self._get_col_pos_footer_label(report)
        for col_pos, column in self.columns.items():
            date = report.date_at.strftime('%B')
            if col_pos == col_pos_footer_label or column.get(field_name):
                if col_pos == col_pos_footer_label:
                    value = label
                else:
                    value = getattr(account, column[field_name])
                cell_type = column.get('type', 'string')
                if cell_type == 'string' or col_pos == col_pos_footer_label:
                    self.sheet.write_string(self.row_pos, col_pos, value or '',
                                            string_format)
                elif cell_type == 'amount':
                    number = float(value)
                    if amount_is_percent:
                        number /= 100
                    self.sheet.write_number(self.row_pos, col_pos,
                                            number,
                                            amount_format)
            else:
                self.sheet.write_string(self.row_pos, col_pos, '',
                                        string_format)
            if date == column['header']:
                break
        self.row_pos += 1
