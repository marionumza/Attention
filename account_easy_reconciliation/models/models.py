# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


import datetime
import logging
import json
_logger = logging.getLogger(__name__)


class AccountOutstandingCreditsDebits(models.TransientModel):
    _name = 'account.outstanding.lines'

    name = fields.Char('Title')
    line_id = fields.Many2one('account.move.line', 'Line')
    amount = fields.Float('Amount')
    invoice_id = fields.Many2one('account.invoice', 'Invoice', required = True)
    user_id = fields.Many2one('res.users', 'User')

class AccountInvoiceLine( models.Model ):
    _inherit = 'account.invoice.line'

    invoice_id = fields.Many2one('account.invoice', 'Invoice')

class EasyReconciliationLines(models.TransientModel):
    _name = 'easy.reconciliation.lines'


    easy_reconciliation_id = fields.Many2one('easy.reconciliation', 'Easy Reconciliation', required = True)
    invoice_id = fields.Many2one('account.invoice', 'Invoice', required = True , domain = "[('partner_id', '=', partner_id),('type', '=', 'out_invoice')]")
    amount_due = fields.Float('Amount Due', readonly = True)
    outstanding_line_id = fields.Many2one('account.outstanding.lines', 'Outstanding Credits/Debits', domain = "[('invoice_id', '=', invoice_id)]", required = True)
    outstanding_line_amount = fields.Float('Amount', readonly = True)

    amount_reconcile = fields.Float('Amount Reconcile', required = True)
    partner_id = fields.Many2one('res.partner',  'Partner', related = 'easy_reconciliation_id.partner_id')

    @api.onchange('outstanding_line_id')
    def on_outstanding_line_id(self):
        if self.outstanding_line_id:
            self.outstanding_line_amount = self.outstanding_line_id.amount

    @api.onchange('invoice_id')
    def on_invoice_id(self):
        if self.invoice_id:
            self.amount_due = self.invoice_id.residual            


class EasyReconciliation(models.TransientModel):
    _name = 'easy.reconciliation'

    partner_id = fields.Many2one('res.partner', 'Partner', required = True)
    line_ids = fields.One2many('easy.reconciliation.lines', 'easy_reconciliation_id')
    journal_id = fields.Many2one('account.journal', 'Journal', required = True ) 



    @api.multi
    def make_reconciliations(self):
        if self.line_ids:
            account_move = self.env['account.move']
            account_move_line = self.env['account.move.line']
            widget_reconciliation = self.env['account.reconciliation.widget']
            account_invoice = self.env['account.invoice']
            outstanding_lines = self.env['account.outstanding.lines']

            line_ids = []
            payments = {}

            for record in self.line_ids:
                if not record.outstanding_line_id.line_id.id:
                    raise ValidationError('Please select a credit/debit for the invoice %s' % ( record.invoice_id.name ))

                if not record.amount_reconcile:
                    raise ValidationError('Please set the amount to reconcile for the invoice %s' % ( record.invoice_id.name ))

                if not record.outstanding_line_id.line_id.id in payments:            
                    payments.update({record.outstanding_line_id.line_id.id : {'line_ids' : [], 'remaining' : 0, 'move_id' : False, 'account_id' : record.invoice_id.account_id.id,
                    'account_id' : record.invoice_id.account_id.id,
                    'outstanding_line_amount' : record.outstanding_line_id.amount,
                    'outstanding_line_name' : record.outstanding_line_id.name,
                    'invoice_id' : record.invoice_id.id}})

                payments.get( record.outstanding_line_id.line_id.id ).get('line_ids').append( (0, 0, {'account_id' : record.invoice_id.account_id.id, 'partner_id' : record.partner_id.id, 'credit' : record.amount_reconcile, 'invoice_id' : record.invoice_id.id }) )
                payments.get( record.outstanding_line_id.line_id.id ).update({
                    'remaining' : payments.get( record.outstanding_line_id.line_id.id ).get('remaining') + record.amount_reconcile,
                    
                })

            _logger.info("Payments")
            _logger.info( payments ) 

            for payment_id in payments.keys(): 
                data = payments.get(  payment_id )
                account_id = data.get('account_id')
                outstanding_line_amount = data.get('outstanding_line_amount')
                remaining = data.get('remaining')
                invoice_id = data.get('invoice_id')
                outstanding_line_name = data.get('outstanding_line_name')

                payments.get( payment_id ).get('line_ids').append( (0, 0, {'account_id' : account_id, 'partner_id' : self.partner_id.id, 'debit' : outstanding_line_amount }) )  
                
                if remaining:
                    payments.get( payment_id ).get('line_ids').append( (0, 0, {'account_id' : account_id, 'partner_id' : self.partner_id.id, 'credit' : outstanding_line_amount - remaining }) )

                line_ids = payments.get( payment_id ).get('line_ids')
                move_id = account_move.create({
                    'journal_id' : self.journal_id.id,
                    'date' : datetime.datetime.now(),
                    'ref' : 'Split Move: %s' % ( outstanding_line_name ),
                    'line_ids' : line_ids
                })


                move_id.action_post() 
                payments.get( payment_id ).update({'move_id' : move_id.id})

                line_move_id = move_id.line_ids.search([('move_id', '=', move_id.id),('debit', '>', 0),('partner_id', '=', self.partner_id.id)])

                if line_move_id and payment_id:  
                    data = [{'mv_line_ids' : [line_move_id.id, payment_id], 'new_mv_line_dicts' : [], 'type' : 'partner', 'id' : self.partner_id.id }]              


                    widget_reconciliation.process_move_lines(data)

                else:
                    raise UserError('There is an error')                     

            for payment_id in payments.keys():
                line_ids = payments.get( payment_id ).get('line_ids')
                move_id = payments.get( payment_id ).get('move_id')

                for line in line_ids:
                    line = line[ 2 ]
                    invoice_id = line.get('invoice_id', False)
                    if invoice_id:

                        line_id = account_move_line.search([('partner_id', '=', self.partner_id.id),('credit', '=', line.get('credit')),
                            ('move_id', '=', move_id),('full_reconcile_id', '=', False),('invoice_id', '=', line.get('invoice_id'))])
                        invoice_id = account_invoice.browse( invoice_id )
                        invoice_id.assign_outstanding_credit( line_id.id )
                                                          


     

    @api.onchange('partner_id', 'journal_id')
    def on_partner_id(self):
        if self.partner_id and self.journal_id:
            outstanding_lines = self.env['account.outstanding.lines']
            if self.env.user:
                self.env.cr.execute('delete from easy_reconciliation_lines where outstanding_line_id in( select out.id from account_outstanding_lines out where out.user_id = %s )' % ( self.env.user.id ))
                self.env.cr.execute('delete from account_outstanding_lines where user_id = %s ' % ( self.env.user.id ))


            self.line_ids = False
            invoices_ids = self.env['account.invoice'].search([('state', 'in', ['open']),('partner_id', '=', self.partner_id.id),('journal_id', '=', self.journal_id.id),('type', '=', 'out_invoice')])
            if invoices_ids:
                self.line_ids = [ (0, 0, {'invoice_id' : invoice.id, 'amount_due' : invoice.residual}) for invoice in invoices_ids ]

            for invoice in invoices_ids:
                has_outstanding = invoice.has_outstanding
                if has_outstanding:
                    outstandings = json.loads(invoice.outstanding_credits_debits_widget).get('content')
                    title = json.loads(invoice.outstanding_credits_debits_widget).get('title') 
                    if title != 'Outstanding credits':
                        continue

                    outstanding_lines = self.env['account.outstanding.lines']

                    _logger.info( outstandings )

                    for outstanding in outstandings:
                        outstanding_lines.create({
                            'name' : outstanding.get('title'),
                            'invoice_id' : invoice.id,
                            'line_id' : outstanding.get('id'),
                            'amount' : outstanding.get('amount'),
                            'user_id' : self.env.user.id
                        })
                
        else:
            self.line_ids = False