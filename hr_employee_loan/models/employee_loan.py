# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import logging
import math
from datetime import timedelta
from werkzeug import url_encode

from odoo import api, fields, models
from odoo.exceptions import UserError, AccessError, ValidationError
from openerp.tools import float_compare
from odoo.tools.translate import _
from datetime import timedelta
from werkzeug import url_encode

from odoo import api, fields, models
from odoo.exceptions import UserError, AccessError, ValidationError
from openerp.tools import float_compare
from odoo.tools.translate import _
from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api
from openerp.exceptions import except_orm, Warning, RedirectWarning
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
import time

class account_move(models.Model):
	_inherit = 'account.move'
	
	vouch_id = fields.Many2one('employee.loan', string='Vouch')

class employee_loan(models.Model):

    _name = 'employee.loan'
    _description = 'employee loan'
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    
    @api.one        
    def _compute_amount(self):
        total_paid_amount = 0.00
        for loan in self:
            for line in loan.loan_line_ids:
                if line.paid == True:
                    total_paid_amount +=line.amount
            balance_amount =loan.amount - total_paid_amount
            self.total_amount = loan.amount
            self.balance_amount = balance_amount
            self.total_paid_amount = total_paid_amount

	

    name = fields.Char(string="Loan Name", default="/", readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    start_date = fields.Date(string="Date", default=fields.Date.today(), readonly=True)
    department_id = fields.Many2one('hr.department', related="employee_id.department_id", readonly=True, string="Department")
    job_id = fields.Many2one('hr.job', related="employee_id.job_id", readonly=True, string="Job")
    amount = fields.Float(string="Loan Amount", required=True)
    reason = fields.Text(string="Loan Reason")
	#move_ids = fields.Many2many('account.move', 'account_move_employee_loan_rel', 'employee_id', 'vouch_id', string='Tags')
    payment_method = fields.Many2one('loan.payments', string='Payment Methods', required=True)
    loan_end_date = fields.Date(string="Loan End Date", readonly=True)
    payment_start_date = fields.Date(string="Start Date of Payment", required=True)
    deduct_amount = fields.Float(string="Deduct Amount", required=True, default=False)
    total_amount = fields.Float(string="Total Amount", readonly=True, compute='_compute_amount')
    balance_amount = fields.Float(string="Remaining Balance", compute='_compute_amount')
    total_paid_amount = fields.Float(string="Deducted Amount", compute='_compute_amount')
    loan_line_ids = fields.One2many('employee.loan.line', 'loan_id', string="Loan Line", index=True)
    entry_count = fields.Integer(string="Entry Count", compute = 'compute_entery_count')
    state = fields.Selection([('draft', 'Draft'),('cancel', 'Cancel'), ('approved', 'Approved'),('editing','Editing')], string='Status', default='draft')
	#move = fields.One2many('account.move', 'ref', string='Moves')
	
	

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('employee.loan') or '/'
        vals['name'] = seq
        return super(employee_loan, self).create(vals)
    		
    #@api.model
    #def create(self, values):
       # values['name'] = self.env['ir.sequence'].get('employee.loan.seq') or  ' '
       # res = super(Loan, self).create(values)
       # return res
    
    @api.multi
    def compute_loan_line(self):
        loan_line = self.env['employee.loan.line']
        loan_line.search([('loan_id','=',self.id)]).unlink()
        for loan in self:
            date_start_str = fields.Datetime.from_string(loan.payment_start_date)
            counter = 0
            no_of_loop = int(loan.amount / loan.deduct_amount)
            remaining_amt = loan.amount % loan.deduct_amount
            amount_lon = 0
            for i in range(0, no_of_loop + 1):
                if no_of_loop == counter:
                    amount_lon = remaining_amt
                    loan.write({'loan_end_date':date_start_str})
                else:     
                    amount_lon = loan.deduct_amount
                
                if amount_lon > 0:
                    line_id = loan_line.create({
                        'discount_date':date_start_str, 
                        'amount': amount_lon,
                        #'employee_id': loan.employee_id.id,
                        'loan_id':loan.id})
                    #print "KKKKKKKKKKKKKKKKKKKK",line_id.amount
                counter += 1
                date_start_str = date_start_str + relativedelta(months = 1)
                
        return True
        
    @api.multi
    def button_reset_balance_total(self):
        total_paid_amount = 0.00
        for loan in self:
            for line in loan.loan_line_ids:
                if line.paid == True:
                    total_paid_amount +=line.amount
            balance_amt =loan.amount - total_paid_amount
            self.write({'total_paid_amount':total_paid_amount,'balance_amount':balance_amt})
            
    @api.multi
    def draft_loan(self):
        return self.write({'state':'draft'})
        
    #@api.model
    #@api.multi
    #def compute_entery_count(self):
    #    count = 0
     #   #entry_count = self.env['account.move'].search_count([('loan_id','=',self.id)])
     ##   entry_count = 0
     #   self.entry_count = entry_count
    
    @api.multi
    def approve_loan(self):
        if self.amount <= 0:
                raise except_orm('Warning', 'Please Set Loan Amount')
        if self.deduct_amount <= 0:
                raise except_orm('Warning', 'Please Set Deduct Amount Monthly')
        if not self.loan_line_ids:
            raise except_orm('Warning', 'You must Schedule Loan before Approve')                       
        equel = self.check_amount_totals()
        can_close = False
        loan_obj = self.env['employee.loan']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        currency_obj = self.env['res.currency']
        timenow = time.strftime('%Y-%m-%d')
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        for loan in self:
            
            company_currency = loan.employee_id.company_id.currency_id.id
            current_currency = self.env.user.company_id.currency_id.id
            amount = loan.amount
            loan_name = loan.employee_id.name
            reference = loan.name
            journal = loan.payment_method.journal_id.id

            move = {
                'narration': loan_name,
                'ref': reference,
                'journal_id': journal,
				'vouch_id': loan.id,
                'date': timenow,
                #'state': 'posted',
            }
            
            debit_account_id = loan.payment_method.debit_account_id.id
            credit_account_id = loan.payment_method.credit_account_id.id
            
            if debit_account_id:
                debit_line = (0, 0, {
                    'name': loan_name,
                    'account_id': debit_account_id,
                    'journal_id': journal,
                    'date': timenow,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            
            if credit_account_id:
                credit_line = (0, 0, {
                    'name': loan_name,
                    'account_id': credit_account_id,
                    'journal_id': journal,
                    'date': timenow,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                })
                line_ids.append(credit_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
            
            move.update({'line_ids': line_ids})
            move_id = move_obj.create(move)
            self.write({'move_id': move_id.id, 'state': 'approved'})
            move_id.post()
        return True
    	
    @api.multi
    def cancel_loan(self):
        can_close = False
        loan_obj = self.env['employee.loan']
        move_obj = self.env['account.move']
        move_line_obj = self.env['account.move.line']
        currency_obj = self.env['res.currency']
        timenow = time.strftime('%Y-%m-%d')
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        for loan in self:
            
            company_currency = loan.employee_id.company_id.currency_id.id
            current_currency = self.env.user.company_id.currency_id.id
            amount = loan.amount
            loan_name = loan.employee_id.name
            reference = loan.name
            journal = loan.payment_method.journal_id.id

            move = {
                'narration': _('Inverse: ')+loan_name,
                'ref': reference,
                'journal_id': journal,
				'vouch_id': loan.id,
                'date': timenow,
                'state': 'posted',
            }
            
            debit_account_id = loan.payment_method.debit_account_id.id
            credit_account_id = loan.payment_method.credit_account_id.id
            
            if debit_account_id:
                debit_line = (0, 0, {
                    'name': loan_name,
                    'account_id': credit_account_id,
                    'journal_id': journal,
                    'date': timenow,
                    'debit': amount > 0.0 and amount or 0.0,
                    'credit': amount < 0.0 and -amount or 0.0,
                })
                line_ids.append(debit_line)
                debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
            
            if credit_account_id:
                credit_line = (0, 0, {
                    'name': loan_name,
                    'account_id': debit_account_id,
                    'journal_id': journal,
                    'date': timenow,
                    'debit': amount < 0.0 and -amount or 0.0,
                    'credit': amount > 0.0 and amount or 0.0,
                })
                line_ids.append(credit_line)
                credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']
            
            move.update({'line_ids': line_ids})
            move_id = move_obj.create(move)
            
            return self.write({'move_id': move_id.id, 'state': 'cancel'})
            
        return True

    @api.multi
    def loan_reschedule(self):
        return self.write({'state':'editing'})
    	
    @api.multi
    def loan_reschedule_done(self):
        equel = self.check_amount_totals()
        return self.write({'state':'approved'})

    @api.multi
    def check_amount_totals(self):
        total_lines_amount = 0.0
        total_amount = 0.0
        for loan in self:
            for line in loan.loan_line_ids:
                total_lines_amount +=line.amount
                total_amount = loan.amount
        if total_amount != total_lines_amount:
            raise except_orm('Warning', 'Total of Loan Installments is not equal to Loan Amount')

employee_loan()
            

class employee_loan_line(models.Model):

    _name = 'employee.loan.line'
    _description = 'employee loan line'
    
    @api.one        
    def _compute_paid(self):
        #laon_paid = {}
        current_date = fields.Date.today()
        #print "CCCCCCCCCC", current_date
        for line in self:
            #laon_paid = {}
            if line.discount_date <= current_date:   
                line.paid = True
        #self.write({'paid':True})
    
    
    loan_id = fields.Many2one('employee.loan', string='Loan Ref.')
    discount_date = fields.Date(string='Payment Date', required=True)
    amount = fields.Float(string="Paid Amount", readonly=True)
    paid = fields.Boolean(string="Paid", compute='_compute_paid')

employee_loan_line()

class loan_payments(models.Model):
	_name = 'loan.payments'
	
	name = fields.Char(string="Name", required=True, help='Payment name')
	debit_account_id = fields.Many2one('account.account', string="Debit Account", required=True, help='Debit account for journal entry')
	credit_account_id = fields.Many2one('account.account', string="Credit Account", required=True, help='Credit account for journal entry')
	journal_id = fields.Many2one('account.journal', string="Journal", required=True, help='Journal for journal entry')
	analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic Account", help='Analytic account for journal entry')

loan_payments()


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    
    '''@api.multi
    def onchange_employee_id(self, date_from, date_to, employee_id=False, contract_id=False):
        res = super(hr_payslip,self).onchange_employee_id(date_from, date_to, employee_id=employee_id, contract_id=contract_id)
        employee_id = self.employee_id.id
        contract_data = self.env['hr.contract'].search([('employee_id', '=', employee_id)], order='id desc', limit=1)
        date_from = self.date_from
        date_to = self.date_to
        loan_obj = self.env['employee.loan']
        loan_line_obj = self.env['employee.loan.line']
        loan_ids = self.env['employee.loan'].search([('employee_id','=',employee_id),('state','=','approved')])
        loan_total = 0.0
        if loan_ids:
            for loan_id in loan_ids:
                line_ids = self.env['employee.loan.line'].search([('loan_id','=',loan_id.id),('discount_date','>=',date_from),('discount_date','<=',date_to)])
                print "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",line_ids
                if line_ids:
                    for loan in line_ids:
                        loan_total += loan.amount
                        print "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",loan_total
            vals = {'name': 'Loan', 'code': 'LOAN', 'amount': loan_total}
            res['value']['input_line_ids'].append(vals)
            #self.input_line_ids.create(vals)

        return res'''
        
        
    @api.model
    def get_inputs(self, contracts, date_from, date_to):
        res = []

        #contracts = self.env['hr.contract'].browse(contract_ids)
        structure_ids = contracts.get_all_structures()
        rule_ids = self.env['hr.payroll.structure'].browse(structure_ids).get_all_rules()
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]
        inputs = self.env['hr.salary.rule'].browse(sorted_rule_ids).mapped('input_ids')
		

        for contract in contracts:
            for input in inputs:
                input_data = {
                    'name': input.name,
                    'code': input.code,
                    'contract_id': contract.id,
                }
                res += [input_data]
            employee_id = self.employee_id.id
            contract_data = self.env['hr.contract'].search([('employee_id', '=', employee_id)], order='id desc', limit=1)
            date_from = self.date_from
            date_to = self.date_to
            loan_obj = self.env['employee.loan']
            loan_line_obj = self.env['employee.loan.line']
            loan_ids = self.env['employee.loan'].search([('employee_id','=',employee_id),('state','=','approved')])
            loan_total = 0.0
            if loan_ids:
                for loan_id in loan_ids:
                    line_ids = self.env['employee.loan.line'].search([('loan_id','=',loan_id.id),('discount_date','>=',date_from),('discount_date','<=',date_to)])
                    #print "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",line_ids
                    if line_ids:
                        for loan in line_ids:
                            loan_total += loan.amount
                            #print "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",loan_total
                vals = {'name': 'Loan', 'code': 'LOAN', 'amount': loan_total, 'contract_id': contract.id}
                
                res.append(vals)
        return res
        
hr_payslip()       
        
        
class hr_payslip_employees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    @api.multi
    def compute_sheet(self):
        payslips = self.env['hr.payslip']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.payslip.run'].browse(active_id).read(['date_start', 'date_end', 'credit_note'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
        for employee in self.env['hr.employee'].browse(data['employee_ids']):
            slip_data = self.env['hr.payslip'].onchange_employee_id(from_date, to_date, employee.id, contract_id=False)

            employee_id = employee.id
            #print"NNNNNNNNNNNNNNNNNNNNNNNNNNNN",employee.name
            date_from = run_data.get('date_start')
            #print"NNNNNNNNNNNNNNNNNNNNNNNNNNNN",date_from
            date_to = run_data.get('date_end')
            #print"NNNNNNNNNNNNNNNNNNNNNNNNNNNN",date_to
            loan_obj = self.env['employee.loan']
            loan_line_obj = self.env['employee.loan.line']
            loan_ids = self.env['employee.loan'].search([('employee_id','=',employee_id),('state','=','approved')])
            #print"LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL",loan_ids
            loan_total = 0.0
            if loan_ids:
                for loan_id in loan_ids:
                    line_ids = self.env['employee.loan.line'].search([('loan_id','=',loan_id.id),('discount_date','>=',date_from),('discount_date','<=',date_to)])
                    #print "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU",line_ids
                    if line_ids:
                        for loan in line_ids:
                            loan_total += loan.amount
                            #print "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",loan_total
                vals = {'name': 'Loan', 'code': 'LOAN', 'amount': loan_total, 'contract_id': slip_data['value'].get('contract_id')}
                #print"VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV",vals
                slip_data['value']['input_line_ids'].append(vals)
            res = {
                'employee_id': employee.id,
                'name': slip_data['value'].get('name'),
                'struct_id': slip_data['value'].get('struct_id'),
                'contract_id': slip_data['value'].get('contract_id'),
                'payslip_run_id': active_id,
                'input_line_ids': [(0, 0, x) for x in slip_data['value'].get('input_line_ids')],
                'worked_days_line_ids': [(0, 0, x) for x in slip_data['value'].get('worked_days_line_ids')],
                'date_from': from_date,
                'date_to': to_date,
                'credit_note': run_data.get('credit_note'),
                'company_id': employee.company_id.id,
            }

            payslips += self.env['hr.payslip'].create(res)
        payslips.compute_sheet()
        return {'type': 'ir.actions.act_window_close'}
hr_payslip_employees()
