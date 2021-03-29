# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from copy import deepcopy

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('line_ids')
    def _onchange_line_ids(self):
        '''Compute additional lines corresponding to the taxes set on the line_ids.

        For example, add a line with 1000 debit and 15% tax, this onchange will add a new
        line with 150 debit.
        '''
        def _str_to_list(string):
            #remove heading and trailing brackets and return a list of int. This avoid calling safe_eval on untrusted field content
            string = string[1:-1]
            if string:
                return [int(x) for x in string.split(',')]
            return []

        def _build_grouping_key(line):
            #build a string containing all values used to create the tax line
            return str(line.tax_ids.ids) + '-' + str(line.analytic_tag_ids.ids) + '-' + (line.analytic_account_id and str(line.analytic_account_id.id) or '')

        def _parse_grouping_key(line):
            # Retrieve values computed the last time this method has been run.
            if not line.tax_line_grouping_key:
                return {'tax_ids': [], 'tag_ids': [], 'analytic_account_id': False}
            tax_str, tags_str, analytic_account_str = line.tax_line_grouping_key.split('-')
            return {
                'tax_ids': _str_to_list(tax_str),
                'tag_ids': _str_to_list(tags_str),
                'analytic_account_id': analytic_account_str and int(analytic_account_str) or False,
            }

        def _find_existing_tax_line(line_ids, tax, tag_ids, analytic_account_id, line):
            if tax.analytic:
                return line_ids.filtered(lambda x: x.tax_line_id == tax and x.analytic_tag_ids.ids == tag_ids and x.analytic_account_id.id == analytic_account_id)
            return line_ids.filtered(lambda x: x.tax_line_id == tax and x.tax_per_line_seq == line.tax_per_line_seq)

        def _get_lines_to_sum(line_ids, tax, tag_ids, analytic_account_id, line):
            if tax.analytic:
                return line_ids.filtered(lambda x: tax in x.tax_ids and x.analytic_tag_ids.ids == tag_ids and x.analytic_account_id.id == analytic_account_id)
            return line_ids.filtered(lambda x: tax in x.tax_ids and x.id == line.id)

        def _get_tax_account(tax, amount):
            if tax.tax_exigibility == 'on_payment' and tax.cash_basis_account_id:
                return tax.cash_basis_account_id
            if tax.type_tax_use == 'purchase':
                return tax.refund_account_id if amount < 0 else tax.account_id
            return tax.refund_account_id if amount >= 0 else tax.account_id

        # Cache the already computed tax to avoid useless recalculation.
        processed_taxes = self.env['account.tax']

        self.ensure_one()
        for line in self.line_ids.filtered(lambda x: x.recompute_tax_line):
            # Retrieve old field values.
            parsed_key = _parse_grouping_key(line)

            # Unmark the line.
            line.recompute_tax_line = False

            # Manage group of taxes.
            group_taxes = line.tax_ids.filtered(lambda t: t.amount_type == 'group')
            children_taxes = group_taxes.mapped('children_tax_ids')
            if children_taxes:
                line.tax_ids += children_taxes - line.tax_ids
                # Because the taxes on the line changed, we need to recompute them.
                processed_taxes -= children_taxes

            # Get the taxes to process.
            taxes = self.env['account.tax'].browse(parsed_key['tax_ids'])
            taxes += line.tax_ids.filtered(lambda t: t not in taxes)
            taxes += children_taxes.filtered(lambda t: t not in taxes)
            to_process_taxes = (taxes - processed_taxes).filtered(lambda t: t.amount_type != 'group')
            processed_taxes += to_process_taxes

            # Process taxes.
            for tax in to_process_taxes:
                if tax.price_include:
                    tax = tax.with_context(handle_price_include=False)
                tax_line = _find_existing_tax_line(self.line_ids, tax, parsed_key['tag_ids'], parsed_key['analytic_account_id'], line)
                lines_to_sum = _get_lines_to_sum(self.line_ids, tax, parsed_key['tag_ids'], parsed_key['analytic_account_id'], line)

                if not lines_to_sum:
                    # Drop tax line because the originator tax is no longer used.
                    self.line_ids -= tax_line
                    continue

                balance = sum([l.balance for l in lines_to_sum])

                # Compute the tax amount one by one.
                if self.company_id.tax_calculation_rounding_method == 'round_globally':
                    quantity = len(lines_to_sum) if tax.amount_type == 'fixed' else 1
                    taxes_vals = tax.compute_all(balance,
                        quantity=quantity, currency=line.currency_id, product=line.product_id, partner=line.partner_id)
                else:
                    taxes_vals_line = [
                        tax.compute_all(
                            lts.balance, quantity=1.0, currency=line.currency_id,
                            product=line.product_id, partner=line.partner_id
                        )
                        for lts in lines_to_sum
                    ]
                    taxes_vals = {
                        'base': 0.0,
                        'total_excluded': 0.0,
                        'total_included': 0.0,
                        'taxes': deepcopy(taxes_vals_line[0]['taxes']),
                    }
                    taxes_vals['taxes'][0]['base'] = 0.0
                    taxes_vals['taxes'][0]['amount'] = 0.0
                    for val in taxes_vals_line:
                        taxes_vals['base'] += val['base']
                        taxes_vals['total_excluded'] += val['total_excluded']
                        taxes_vals['taxes'][0]['base'] += sum([v['base'] for v in val['taxes']])
                        taxes_vals['taxes'][0]['amount'] += sum([v['amount'] for v in val['taxes']])

                if tax_line:
                    if len(tax_line) == 1:
                        # Update the existing tax_line.
                        if balance:
                            # Update the debit/credit amount according to the new balance.
                            if taxes_vals.get('taxes'):
                                amount = taxes_vals['taxes'][0]['amount']
                                account = _get_tax_account(tax, amount) or line.account_id
                                tax_line.debit = amount > 0 and amount or 0.0
                                tax_line.credit = amount < 0 and -amount or 0.0
                                tax_line.account_id = account
                        else:
                            # Reset debit/credit in case of the originator line is temporary set to 0 in both debit/credit.
                            tax_line.debit = tax_line.credit = 0.0
                elif taxes_vals.get('taxes'):
                    # Create a new tax_line.
                    if line.tax_per_line_seq:
                        tax_per_line_seq = line.tax_per_line_seq
                    else:
                        tax_per_line_seq = self.env['ir.sequence'].next_by_code('account.move.line.tax.per.line') #nirav
                    amount = taxes_vals['taxes'][0]['amount']
                    account = _get_tax_account(tax, amount) or line.account_id
                    tax_vals = taxes_vals['taxes'][0]

                    name = tax_vals['name']
                    line_vals = {
                        'account_id': account.id,
                        'name': name,
                        'tax_line_id': tax_vals['id'],
                        'partner_id': line.partner_id.id,
                        'debit': amount > 0 and amount or 0.0,
                        'credit': amount < 0 and -amount or 0.0,
                        'analytic_account_id': line.analytic_account_id.id if tax.analytic else False,
                        'analytic_tag_ids': line.analytic_tag_ids.ids if tax.analytic else False,
                        'move_id': self.id,
                        'tax_exigible': tax.tax_exigibility == 'on_invoice',
                        'company_id': self.company_id.id,
                        'company_currency_id': self.company_id.currency_id.id,
                        'tax_move_line_acc_id': line.account_id.id,#nirav
                        'tax_per_line_seq': tax_per_line_seq,
                    }
                    # N.B. currency_id/amount_currency are not set because if we have two lines with the same tax
                    # and different currencies, we have no idea which currency set on this line.
                    self.env['account.move.line'].new(line_vals)
                    if not line.tax_per_line_seq:
                        line.tax_per_line_seq = tax_per_line_seq
            # Keep record of the values used as taxes the last time this method has been run.
            line.tax_line_grouping_key = _build_grouping_key(line)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
 
 
    tax_move_line_acc_id = fields.Many2one('account.account', string='Ref for A/c taxesable line')
    tax_per_line_seq = fields.Char(string='Sequence per line')
