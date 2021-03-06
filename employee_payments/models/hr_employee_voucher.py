from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools import float_is_zero, float_compare
from odoo.addons import decimal_precision as dp
import time
from datetime import datetime, timedelta
from dateutil import relativedelta
from datetime import datetime
import babel
import datetime
from dateutil.relativedelta import relativedelta
import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.addons import decimal_precision as dp

import datetime
from dateutil.relativedelta import relativedelta
import time

import time
from datetime import datetime, timedelta
from dateutil import relativedelta
import babel




class employee_voucher(models.Model):
    _name = "employee.voucher"
            
    def _compute_amount(self):
        res = {}
        grand_tot = []
        grand_tot_ded = []
        for payment_slip in self:
            
            if payment_slip.ticket_leave == True:
                ticket_1 = payment_slip.issue_amount_tickets
                grand_tot.append(ticket_1)
                
            if payment_slip.end_service == True:
                end_1 = payment_slip.paid_amount
                grand_tot.append(end_1)
                
            if payment_slip.deduct1 == True:
                deduct_1 = payment_slip.deduct1_amount
                grand_tot_ded.append(deduct_1)
                    
            if payment_slip.other == True:
                other_1 = payment_slip.other_amount
                grand_tot.append(other_1)
            
            gad_tot = grand_tot
            gad_tot_ded = grand_tot_ded
            tay = sum(gad_tot)-sum(gad_tot_ded)
            #print ("GGGGGGGGGGGGGGGGGGGGGGGGG"),tay
            self.grand_total = tay
        #return res
        
    def _sel_func(self):
        obj = self.env['hr.leave']
        ids = obj.search([])
        res = obj.read(['name', 'id'])
        res = [(r['id'], r['name']) for r in res]
        return res
    

    employee_id         = fields.Many2one('hr.employee',string='Employee', required=True, readonly=True, states={'draft':[('readonly',False)]})
    date                = fields.Date(string='Date', readonly=True, default=lambda *a: time.strftime('%Y-%m-%d'))
    company_id          = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    #voucher_ref         = fields.Char(string='Voucher Referance', required=True)
    journal_id          = fields.Many2one('account.journal', string='Journal', required=True, readonly=True, states={'draft':[('readonly',False)]})
    state               = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmation'), ('done', 'Done'), ('cancel', 'Cancel')], string='Status', default='draft')

    balance_laon        = fields.Float(string='Pending Loan Amount', readonly=True)
    ignore_loan         = fields.Boolean(string='Proceed if Pending Loan', states={'draft':[('invisible',True)],'done':[('readonly',True)]})
    balance_item        = fields.Boolean(string='Pending Employee Checklist', readonly=True)
    ignore_item       = fields.Boolean(string='Proceed if Pending Employee Checklist', states={'draft':[('invisible',True)],'done':[('readonly',True)]})

            ################# LEGAL LEAVES ##############################################

    move_id             = fields.Many2one('account.move',string='Journal Entry',help='Journal Entry for Employee voucher')
    #moves_ids           = fields.Many2many('account.move','account_move_employee_voucher_rel','employee_id','payment_id',string='Journal Entries',help='Journal entries related to this Employee Voucher')


    ######################## TICKETS ###################################################

    ticket_leave        = fields.Boolean(string='Employee Ticket', readonly=True, states={'draft':[('readonly',False)]})
    voucher_method2     = fields.Many2one('employee.voucher.line',string='Employee Payment Type2', readonly=True, default=lambda self: self.env['employee.voucher.line'].search([('pay_type','=','ticket')]))
    #allocated_tickets   = fields.Float(string='Allowed Empolyee Tickets', readonly=False)
    #allocated_amount_tickets= fields.Float(string='Allowed Employee Tickets Amount', readonly=False)
    issue_tickets       = fields.Float(string='Issue Employee Tickets', states={'done':[('readonly',True)]})
    issue_amount_tickets= fields.Float(string='Issue Employee Tickets Amount', required=True, states={'done':[('readonly',True)]})

    ######################### END OF SERVICE ########################################################

    end_service         = fields.Boolean(string='End of service', readonly=True, states={'draft':[('readonly',False)]})
    voucher_method3     = fields.Many2one('employee.voucher.line',string='Employee Payment Type3', readonly=True, default=lambda self: self.env['employee.voucher.line'].search([('pay_type','=','eos')]))
    whole_working       = fields.Float(string='Whole Working Days', readonly=True)
    total_unpaid        = fields.Float(string='Total Unpaid Leaves', readonly=True)
    actual_working      = fields.Float(string='Actual Working Days', readonly=True)
    paid_amount         = fields.Float(string='Pay Amount', required=True, states={'done':[('readonly',True)]})
    leave_reason        = fields.Selection([('endservice', 'End of Contract'),('termination','Termination'),('quit','Quit')], string='Job Leaving Reason', help="Reason of Employee job leaving", default='endservice')
    paid_eos_amount     = fields.Float(string='Paid EOS Amount', readonly=True)
    e_remain_eos_amount = fields.Float(string='EOS Remaining C-Amount', readonly=True)
    e_total_eos_amount  = fields.Float(string='EOS Total C-Amount', readonly=True)
    t_remain_eos_amount = fields.Float(string='EOS Remaining T-Amount', readonly=True)
    t_total_eos_amount  = fields.Float(string='EOS Total T-Amount', readonly=True)
    q_remain_eos_amount = fields.Float(string='EOS Remaining Q-Amount', readonly=True)
    q_total_eos_amount  = fields.Float(string='EOS Total Q-Amount', readonly=True)
    record_exit         = fields.Boolean(string='In Progress')
    period_year         = fields.Float(string='Contract Year', readonly=True)
    period_month        = fields.Float(string='Contract Month', readonly=True)
    period_day          = fields.Float(string='Contract Days', readonly=True)

    end_leave_reason    = fields.Char(string='Leave Reason', readonly=True)
    term_leave_reason   = fields.Char(string='Leave Reason', readonly=True)
    quit_leave_reason   = fields.Char(string='Leave Reason', readonly=True)
    end_years           = fields.Float(string='END of Service Years', readonly=True)
    first_end           = fields.Float(string='Upto 2 Years', readonly=True)
    second_end          = fields.Float(string='From 2 - 5 Years', readonly=True)
    third_end           = fields.Float(string='Above 5 Years', readonly=True)
    total_end           = fields.Float(string='EOS- Total', readonly=True)

    term_years          = fields.Float(string='END of Service Years', readonly=True)
    first_term          = fields.Float(string='Upto 2 Years', readonly=True)
    second_term         = fields.Float(string='From 2 - 5 Years', readonly=True)
    third_term          = fields.Float(string='Above 5 Years', readonly=True)
    total_term          = fields.Float(string='EOS- Total', readonly=True)

    quit_years          = fields.Float(string='END of Service Years', readonly=True)
    first_quit          = fields.Float(string='Upto 2 Years', readonly=True)
    second_quit         = fields.Float(string='From 2 - 5 Years', readonly=True)
    third_quit          = fields.Float(string='From 5 - 10 Years', readonly=True)
    fourth_quit         = fields.Float(string='Above 10 Years', readonly=True)
    total_quit          = fields.Float(string='EOS- Total', readonly=True)

    #################### EXIT / RE-ENTRY #########################


    deduct1             = fields.Boolean(string='Deduct', readonly=True, states={'draft':[('readonly',False)]})
    voucher_method5     = fields.Many2one('employee.voucher.line',string='Employee Payment Type5', readonly=True, default=lambda self: self.env['employee.voucher.line'].search([('pay_type','=','deduct')]))
    deduct1_amount      = fields.Float(string='Amount', required=True, states={'done':[('readonly',True)]})
    deduct1_desp        = fields.Text(string='Description', states={'done':[('readonly',True)]})

    other               = fields.Boolean(string='Other', readonly=True, states={'draft':[('readonly',False)]})
    voucher_method9     = fields.Many2one('employee.voucher.line',string='Employee Payment Type9', readonly=True, default=lambda self: self.env['employee.voucher.line'].search([('pay_type','=','other')]))
    other_amount        = fields.Float(string='Amount', required=True, states={'done':[('readonly',True)]})
    other_desp          = fields.Text(string='Description', states={'done':[('readonly',True)]})
    grand_total          = fields.Float(string="Total Amount", compute='_compute_amount')       

    
    def set_draft(self):
        self.write({'state':'draft'})
        return True
    
    def approve1_payment(self):
        ticket_amt = 0.0
        employee_id = self.employee_id.id
        if self.ticket_leave == True:
            self.write({'state':'confirm'})
        if self.ticket_leave == False:
            self.write({'issue_tickets':False,'issue_amount_tickets':False,'state':'confirm'})
        if self.end_service == True:
            if self.leave_reason == "endservice":
                if self.paid_amount > round(self.e_total_eos_amount-self.paid_eos_amount):
                    bal = round(self.e_total_eos_amount-self.paid_eos_amount)
                    raise UserError(_('Paying Amount is More than Remaining Balance Amount'))
            if self.leave_reason == "termination":
                if self.paid_amount > round(self.t_total_eos_amount-self.paid_eos_amount):
                    raise UserError(_('Paying Amount is More than Remaining Balance Amount'))
            if self.leave_reason == "quit":
                if self.paid_amount > round(self.q_total_eos_amount-self.paid_eos_amount):
                    raise UserError(_('Paying Amount is More than Remaining Balance Amount'))
            else:     
                self.write({'state':'confirm'})
        if self.end_service == False:
            self.write({'paid_amount':False,'state':'confirm'})
        else:        
            self.write({'state':'confirm'})
        return True
        
        
################## Voucher Cancel Functions ############################################################
        
    def unlink(self):
        for vou in self:
            vouch_ids = self.env['account.move'].search([('payment_id', '=', vou.id)])
            #if expense.state in ['post', 'done']:
            if vouch_ids: 
                raise UserError(_('You Cant Delete Employee Voucher that have Journal Entries.'))
        super(employee_voucher, self).unlink()
        
    
    def draft_payment(self):
        self.write({'state':'draft'})
        return True
    
    def cancel_voucher(self):    
        move_pool = self.env['account.move']
        timenow = time.strftime('%Y-%m-%d')
        holiday_obj = self.env['hr.leave']
        for payment_slip in self:
            line_ids = []
            grand_tot = []
            grand_tot_ded = []
            # prepare account move data
            name = _('Inverse: Employee Voucher for ') + (payment_slip.employee_id.name)
            move = {
                'narration': name,
                'date': timenow,
                'payment_id': payment_slip.id,
                'journal_id': payment_slip.journal_id.id,
            }
            #print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",move
            amount2 = payment_slip.issue_amount_tickets
            debit_account_id2 = payment_slip.voucher_method2.debit_account_id.id or False
            credit_account_id2 = payment_slip.voucher_method2.credit_account_id.id or False        
            
            if payment_slip.ticket_leave == True:
                if payment_slip.voucher_method2.account_analytic_true == True:
                    ticket_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id2:
                        debit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id2,
                        'debit': 0.0,
                        'credit': amount2,
                        'analytic_account_id': ticket_analytic or False,
                    })
                        line_ids.append(debit_line2)

                    if credit_account_id2:
                        credit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id2,
                        'debit': amount2,
                        'credit': 0.0,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line2)
                else:
                    if debit_account_id2:
                        debit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id2,
                        'debit': 0.0,
                        'credit': amount2,
                        'analytic_account_id': False,
                    })
                        line_ids.append(debit_line2)

                    if credit_account_id2:
                        credit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id2,
                        'debit': amount2,
                        'credit': 0.0,
                        
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line2)        
               
            amount3 = payment_slip.paid_amount
            debit_account_id3 = payment_slip.voucher_method3.debit_account_id.id or False
            credit_account_id3 = payment_slip.voucher_method3.credit_account_id.id or False       
            
            if payment_slip.end_service == True:
                employee_id = payment_slip.employee_id.id
                emp_voucher_ids = self.env['employee.voucher'].search([('employee_id', '=', employee_id),('end_service', '=', True),('state','=','done')], order='id desc', limit=1)
             #   print "VOVOVOVOVOVOVVVOVOVOOVVO",emp_voucher_ids
                if payment_slip.id != emp_voucher_ids:
                    raise UserError(_('You cannot refuse paid EOS Employee voucher'))           
                
                if payment_slip.voucher_method3.account_analytic_true == True:
                    end_service_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id3:
                        debit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id3,
                        'debit': 0.0,
                        'credit': amount3,
                        'analytic_account_id': end_service_analytic or False,
                    })
                        line_ids.append(debit_line3)

                    if credit_account_id3:
                        credit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id3,
                        'debit': amount3,
                        'credit': 0.0,
                        
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line3)
                else:
                    if debit_account_id3:
                        debit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id3,
                        'debit': 0.0,
                        'credit': amount3,
                        'analytic_account_id': False,
                    })
                        line_ids.append(debit_line3)

                    if credit_account_id3:
                        credit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id3,
                        'debit': amount3,
                        'credit': 0.0,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line3)
                    
            amount5 = payment_slip.deduct1_amount
            debit_account_id5 = payment_slip.voucher_method5.debit_account_id.id or False
            credit_account_id5 = payment_slip.voucher_method5.credit_account_id.id or False
            
            if payment_slip.deduct1 == True:
                
                if payment_slip.voucher_method5.account_analytic_true == True:
                    deduct1_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id5:
                        debit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id5,
                        'debit': 0.0,
                        'credit': amount5,
                        #'analytic_account_id': analytic_account_id,
                    })
                        line_ids.append(debit_line5)

                    if credit_account_id5:
                        credit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id5,
                        'debit': amount5,
                        'credit': 0.0,  
                        'analytic_account_id': deduct1_analytic or False,
                    })
                        line_ids.append(credit_line5)
                else:
                    if debit_account_id5:
                        debit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id5,
                        'debit': 0.0,
                        'credit': amount5,
                        #'analytic_account_id': analytic_account_id,
                    })
                        line_ids.append(debit_line5)

                    if credit_account_id5:
                        credit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id5,
                        'debit': amount5,
                        'credit': 0.0,  
                        'analytic_account_id': False,
                    })
                        line_ids.append(credit_line5)
            
            amount9 = payment_slip.other_amount
            debit_account_id9 = payment_slip.voucher_method9.debit_account_id.id or False
            credit_account_id9 = payment_slip.voucher_method9.credit_account_id.id or False
            
            if payment_slip.other == True:
                
                if payment_slip.voucher_method9.account_analytic_true == True:
                    other_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id9:
                        debit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id9,
                        'debit': 0.0,
                        'credit': amount9,
                        'analytic_account_id': other_analytic or False,
                    })
                        line_ids.append(debit_line9)

                    if credit_account_id9:
                        credit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id9,
                        'debit': amount9,
                        'credit': 0.0,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line9)
                else:
                    if debit_account_id9:
                        debit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id9,
                        'debit': 0.0,
                        'credit': amount9,
                        'analytic_account_id': False,
                    })
                        line_ids.append(debit_line9)

                    if credit_account_id9:
                        credit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id9,
                        'debit': amount9,
                        'credit': 0.0,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line9)
                        
            move.update({'line_ids': line_ids})
            move_id = move_pool.create(move)
            #print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",move_id                                     
            self.write({'move_id': move_id.id, 'state': 'cancel'})
            move_id.post()
            return True
            
################## Voucher Cancel Functions ############################################################

    def approve2_payment(self):    
        move_pool = self.env['account.move']
        timenow = time.strftime('%Y-%m-%d')
        holiday_obj = self.env['hr.leave']
        for payment_slip in self:
            employee_id = payment_slip.employee_id.id
            if payment_slip.balance_laon != 0.0 and payment_slip.ignore_loan == False:
                raise ValidationError(_('This Employee has Balance Loan Amount, You cannot confirm this Voucher')) 
            if payment_slip.balance_item == True and payment_slip.ignore_item == False:
                raise ValidationError(_('This Employee has Pending Checklist Items, You cannot confirm this Voucher'))               
            line_ids = []
            grand_tot = []
            grand_tot_ded = []
           
            # prepare account move data
            name = _('Employee Voucher for ') + (payment_slip.employee_id.name)
            move = {
                'narration': name,
                'date': timenow,
                'payment_id': payment_slip.id,
                'journal_id': payment_slip.journal_id.id,
            }
            #print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",move
                    
            amount2 = payment_slip.issue_amount_tickets
            debit_account_id2 = payment_slip.voucher_method2.debit_account_id.id or False
            credit_account_id2 = payment_slip.voucher_method2.credit_account_id.id or False        
            
            if payment_slip.ticket_leave == True:
                ticket_1 = payment_slip.issue_amount_tickets
                grand_tot.append(ticket_1)
                if payment_slip.voucher_method2.account_analytic_true == True:
                    ticket_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id2:
                        debit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id2,
                        'debit': amount2,
                        'credit': 0.0,
                        'analytic_account_id': ticket_analytic or False,
                    })
                        line_ids.append(debit_line2)

                    if credit_account_id2:
                        credit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id2,
                        'debit': 0.0,
                        'credit': amount2,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line2)
                else:
                    if debit_account_id2:
                        debit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id2,
                        'debit': amount2,
                        'credit': 0.0,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(debit_line2)

                    if credit_account_id2:
                        credit_line2 = (0, 0, {
                        'name': payment_slip.voucher_method2.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id2,
                        'debit': 0.0,
                        'credit': amount2,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line2)        
                
            
            amount3 = payment_slip.paid_amount
            debit_account_id3 = payment_slip.voucher_method3.debit_account_id.id or False
            credit_account_id3 = payment_slip.voucher_method3.credit_account_id.id or False       
            
            if payment_slip.end_service == True:
                end_1 = payment_slip.paid_amount
                grand_tot.append(end_1)
                if payment_slip.voucher_method3.account_analytic_true == True:
                    end_service_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id3:
                        debit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id3,
                        'debit': amount3,
                        'credit': 0.0,
                        'analytic_account_id': end_service_analytic or False,
                    })
                        line_ids.append(debit_line3)

                    if credit_account_id3:
                        credit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id3,
                        'debit': 0.0,
                        'credit': amount3,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line3)
                        
                else:
                    if debit_account_id3:
                        debit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id3,
                        'debit': amount3,
                        'credit': 0.0,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(debit_line3)

                    if credit_account_id3:
                        credit_line3 = (0, 0, {
                        'name': payment_slip.voucher_method3.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id3,
                        'debit': 0.0,
                        'credit': amount3,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line3)
                    
            amount5 = payment_slip.deduct1_amount
            debit_account_id5 = payment_slip.voucher_method5.debit_account_id.id or False
            credit_account_id5 = payment_slip.voucher_method5.credit_account_id.id or False
            
            if payment_slip.deduct1 == True:
                deduct_1 = payment_slip.deduct1_amount
                grand_tot_ded.append(deduct_1)
                if payment_slip.voucher_method5.account_analytic_true == True:
                    deduct1_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id5:
                        debit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id5,
                        'debit': amount5,
                        'credit': 0.0,
                        #'analytic_account_id': analytic_account_id,
                    })
                        line_ids.append(debit_line5)

                    if credit_account_id5:
                        credit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id5,
                        'debit': 0.0,
                        'credit': amount5,
                        'analytic_account_id': deduct1_analytic or False,
                    })
                        line_ids.append(credit_line5)
                else:
                    if debit_account_id5:
                        debit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id5,
                        'debit': amount5,
                        'credit': 0.0,
                        #'analytic_account_id': analytic_account_id,
                    })
                        line_ids.append(debit_line5)

                    if credit_account_id5:
                        credit_line5 = (0, 0, {
                        'name': payment_slip.voucher_method5.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id5,
                        'debit': 0.0,
                        'credit': amount5,
                        'analytic_account_id': False,
                    })
                        line_ids.append(credit_line5)
            
                    
            amount9 = payment_slip.other_amount
            debit_account_id9 = payment_slip.voucher_method9.debit_account_id.id or False
            credit_account_id9 = payment_slip.voucher_method9.credit_account_id.id or False
            
            if payment_slip.other == True:
                other_1 = payment_slip.other_amount
                grand_tot.append(other_1)
                if payment_slip.voucher_method9.account_analytic_true == True:
                    other_analytic = payment_slip.employee_id.analytic_account_id and payment_slip.employee_id.analytic_account_id.id or False
                    if debit_account_id9:
                        debit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id9,
                        'debit': amount9,
                        'credit': 0.0,
                        'analytic_account_id': other_analytic or False,
                    })
                        line_ids.append(debit_line9)

                    if credit_account_id9:
                        credit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id9,
                        'debit': 0.0,
                        'credit': amount9,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line9)
                else:
                    if debit_account_id9:
                        debit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': debit_account_id9,
                        'debit': amount9,
                        'credit': 0.0,
                        'analytic_account_id': False,
                    })
                        line_ids.append(debit_line9)

                    if credit_account_id9:
                        credit_line9 = (0, 0, {
                        'name': payment_slip.voucher_method9.pay_type,
                        'date': timenow,
                        'partner_id': payment_slip.employee_id.address_home_id.id,
                        'account_id': credit_account_id9,
                        'debit': 0.0,
                        'credit': amount9,
                        #'analytic_account_id': False,
                    })
                        line_ids.append(credit_line9)
                        
                
            move.update({'line_ids': line_ids})
            move_id = move_pool.create(move)
            #print "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",move_id
            gad_tot = grand_tot
            gad_tot_ded = grand_tot_ded
            tay = sum(gad_tot)-sum(gad_tot_ded)
            #print "GGGGGGGGGGGGGGGGGGGGGGGGG",gad_tot                                 
            self.write({'move_id': move_id.id, 'state': 'done', 'grand_total':tay})
            move_id.post()
            return True
              

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        employee_id = self.employee_id.id
        contract_data = self.env['hr.contract'].search([('employee_id', '=', employee_id)], order='id desc', limit=1)
        print ("555555555555555555555555555555555555555",contract_data)
        ticket_year = contract_data.ticket
        #print "DDDDD1111111111111:",ticket_year
        ticket_money = contract_data.ticket_amount*ticket_year
        #print "DDDDD1111111111111:",ticket_money
        
        bal_loan = 0.0
        emp_loan_ids = self.env['employee.loan'].search([('employee_id', '=', employee_id),('state','=','approved')])
        #print ("GGGGGGGGGGGGGGGGGGGGGGGGG",emp_loan_ids)
        for loan_data in emp_loan_ids:
            bal_loan += loan_data.balance_amount
            #print ("GGGGGGGGGGGGGGGGGGGGGGGGG",bal_loan)
            
        bal_item = False
        emp_item_ids = self.env['employee.item'].search([('employee_id', '=', employee_id),('state','=','checkin')])
        #print ("GGGGGGGGGGGGGGGGGGGGGGGGG",emp_loan_ids)
        if emp_item_ids:
            bal_item = True
            #print ("GGGGGGGGGGGGGGGGGGGGGGGGG",bal_item)
                
        emp_holidays_ids = self.env['hr.leave'].search([('employee_id', '=', employee_id),('state','=','validate'),('holiday_status_id.name', '=', 'Unpaid')])
        #print "SSSSSSSSSSSSSSSSSSSS",emp_holidays_ids
        res = []
        emp_holidays_legal_ids = self.env['hr.leave'].search([('employee_id', '=', employee_id),('state','=','validate'),('holiday_status_id.name', '=', 'LegalLeaves')], order='id desc', limit=1)
        #print "1111111111111111111111111111111111111111111",emp_holidays_legal_ids

        res = emp_holidays_legal_ids
        val = 0.0
        for hai in emp_holidays_ids:
            total_paid_amount = 0.0
            val +=hai.number_of_days
         #   print "UUUUUUUUUUUUUUUUUUUU",val
        emp_voucher_data = self.env['employee.voucher'].search([('employee_id', '=', employee_id),('end_service', '=', True),('state','=','done')], order='id desc', limit=1)
        #print "VOVOVOVOVOVOVVVOVOVOOVVO",emp_voucher_data
        
        emp_eos = 0.0
        emp_tot_eos = 0.0

        emp_eos = emp_voucher_data.paid_amount
        emp_paid_eos = emp_voucher_data.paid_eos_amount
        emp_detail = emp_voucher_data.leave_reason

        emp_tot_e_eos = emp_voucher_data.e_total_eos_amount
        emp_tot_t_eos = emp_voucher_data.t_total_eos_amount
        emp_tot_q_eos = emp_voucher_data.q_total_eos_amount

        date_format = '%Y-%m-%d'  
        
        start_date = contract_data.date_start
        end_date = contract_data.date_end
        if start_date:
            current_date = fields.datetime.now().strftime(date_format)
            
            d1 = fields.Datetime.from_string(start_date)
         #   print "STSSTSTSTSTSTSTTSTST",d1
            
            d2 = fields.Datetime.from_string(current_date)
          #  print "CDCDCDCDCDCDCDCDCDCDC",d2

            if end_date:
                d3 = fields.Datetime.from_string(end_date)
           #     print "ENEENENENENENENENNENE",d3
                if val > 0.0:
                    tab = d1 + relativedelta.relativedelta(days=val)
                    #print ("VACAGVACAVCACAGACAVACAAVACAVACA",tab)
                    r = relativedelta.relativedelta(d3,tab)
                    delta = d3 - tab
                    period_days = delta.days
                #    print "VACAGVACAVCACAGACAVACAAVACAVACA",period_days
                    whole_days = r.days
                 #   print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_days
                    whole_months = r.months
                  #  print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_months
                    whole_years = r.years
                   # print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_years
                    #cap = d1 + relativedelta.relativedelta(months=12)
                    #print"CPCPCPCPCPCPCPC",cap
                else:
                    r = relativedelta.relativedelta(d3,d1)
                    delta = d3 - d1
                    period_days = delta.days
                #    print "VACAGVACAVCACAGACAVACAAVACAVACA",period_days
                    whole_days = r.days
                 #   print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_days
                    whole_months = r.months
                  #  print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_months
                    whole_years = r.years
                   # print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_years
                    #cap = d1 + relativedelta.relativedelta(months=12)
                    #print"CPCPCPCPCPCPCPC",cap
                
                emp_net = contract_data.total_salary
                print ("PPPPPPPPPPPPPPPP",emp_net)
                day_salary = emp_net/30
                #print "PPPPPPPPPPPPPPPP",day_salary
                actual_work_days = period_days-val
                #print "PPPPPPPPPPPPPPPP",actual_work_days
          ########### Calculation of Employee END of service  #############
                        
                end_first = 0.0
                end_second = 0.0
                end_third = 0.0
                
                eos_end_years = actual_work_days/365
                #print "qqqqqqqqqqqqqq",eos_end_years
                if eos_end_years < 2 :
                    end_first = eos_end_years*emp_net/2
                    #print "E1E1E1E1E1E1EE1E1",end_first
                
                elif eos_end_years < 5 and eos_end_years >= 2:                    
                    end_first = 2*emp_net/2
                    second_year_sly = emp_net/2
                    second_month_sly = second_year_sly/12
                    second_days_sly = second_month_sly/30
                    end_second = ((whole_years - 2) * second_year_sly) + (whole_months * second_month_sly) + (whole_days * second_days_sly)
                    #print "E2E2EE22E2E2E2E2EE2",end_second
                
                elif eos_end_years >= 5 :
                    end_rem_val = eos_end_years - 5
                    #print "R1R1R1R1R1R1R1R1R1R",end_rem_val
                    end_first = 2*emp_net/2
                    end_second = 3*emp_net/2
                    third_year_sly = emp_net
                    third_month_sly = third_year_sly/12
                    third_days_sly = third_month_sly/30
                    end_third = ((whole_years - 5) * third_year_sly) + (whole_months * third_month_sly) + (whole_days * third_days_sly)
                    #print "E3E3E3E3E3E3E3E3E3E3",end_third
                    
                    
      ########### Calculation of Employee TERMINATION #############      
                
                term_first = 0.0
                term_second = 0.0
                term_third = 0.0
                
                eos_term_years = actual_work_days/365
                #print "qqqqqqqqqqqqqq",eos_end_years
                if eos_term_years < 2 :                    
                    first_year_sly = emp_net/2
                    first_month_sly = first_year_sly/12
                    first_days_sly = first_month_sly/30
                    term_first = (whole_years * first_year_sly) + (whole_months * first_month_sly) + (whole_days * first_days_sly)
                    #print "T1T1T1T1T1T1T1T1T1T1",term_first
                
                elif eos_term_years < 5 and eos_end_years >= 2:
                    term_first = 2*emp_net/2
                    second_year_sly = emp_net/2
                    second_month_sly = second_year_sly/12
                    second_days_sly = second_month_sly/30
                    term_second = ((whole_years - 2) * second_year_sly) + (whole_months * second_month_sly) + (whole_days * second_days_sly)
                    #print "T2T2T2TT2T2T2T2T2T2T2",term_second
                
                elif eos_term_years >= 5 :
                    term_rem_val = eos_term_years - 5
                    #print "R2R2RR22R2R2R2RR2R2RR2",term_rem_val
                    term_first = 2*emp_net/2
                    term_second = 3*emp_net/2
                    third_year_sly = emp_net
                    third_month_sly = third_year_sly/12
                    third_days_sly = third_month_sly/30
                    term_third = ((whole_years - 5) * third_year_sly) + (whole_months * third_month_sly) + (whole_days * third_days_sly)
                    #print "T3T3T3T3T3T3TT3T33T3T3T",term_third
                    
                    
      ########### Calculation of Employee QUIT #############      
                    
                quit_first = 0.0
                quit_second = 0.0
                quit_third = 0.0
                quit_fourth = 0.0
                
                eos_quit_years = actual_work_days/365
                #print "qqqqqqqqqqqqqq",eos_end_years
                if eos_quit_years < 2 :
                    quit_first = 0.0
                    #print "Q1Q1Q1Q1Q1Q1Q1Q1Q1Q1Q1",quit_first
                
                elif eos_quit_years < 5 and eos_end_years >= 2:
                    quit_second = (eos_quit_years*emp_net/2)*1/3
                    #print "Q2Q2Q2Q2Q2Q22Q2Q2Q2Q2Q2Q2",quit_second
                    
                    quit_first = (2*emp_net/2)*1/3
                    second_year_sly = (emp_net/2)*1/3
                    second_month_sly = second_year_sly/12
                    second_days_sly = second_month_sly/30
                    quit_second = ((whole_years - 2) * second_year_sly) + (whole_months * second_month_sly) + (whole_days * second_days_sly)
                
                elif eos_quit_years < 10 and eos_end_years >= 5:
                    quit_first = (2*emp_net/2)*2/3
                    quit_second = (3*emp_net/2)*2/3
                    third_year_sly = (emp_net)*2/3
                    third_month_sly = third_year_sly/12
                    third_days_sly = third_month_sly/30
                    quit_third = ((whole_years - 5) * third_year_sly) + (whole_months * third_month_sly) + (whole_days * third_days_sly)
                    #print "Q3Q3Q3Q3Q3Q3Q3Q3Q3Q3Q3Q3",quit_third
                    
                elif eos_quit_years >= 10:
                    quit_first = 2*emp_net/2
                    quit_second = 3*emp_net/2
                    quit_third = 5*emp_net
                    fourth_year_sly = emp_net
                    fourth_month_sly = fourth_year_sly/12
                    fourth_days_sly = fourth_month_sly/30
                    quit_fourth = ((whole_years - 10) * fourth_year_sly) + (whole_months * fourth_month_sly) + (whole_days * fourth_days_sly)
                    #print "Q4Q4Q4Q4Q4Q4Q4Q4Q4Q44Q4Q4Q4",quit_fourth
                    
                if emp_voucher_data:
                    result = {'value': {
                                #'allocated_tickets':ticket_year,
                                #'allocated_amount_tickets':ticket_money,
                                'issue_tickets':ticket_year,
                                'issue_amount_tickets':ticket_money,
                                
                                'period_year': whole_years,
                                'period_month': whole_months,
                                'period_day': whole_days,
                                'whole_working':period_days,
                                'total_unpaid':val,
                                'actual_working':actual_work_days,
                                'balance_laon':bal_loan,
                                'balance_item':bal_item,
                                'end_leave_reason': 'END OF CONTRACT',
                                'end_years': eos_end_years, 
                                'first_end': end_first,
                                'second_end': end_second,
                                'third_end': end_third,
                                'total_end': end_first+end_second+end_third,
                                
                                'term_leave_reason': 'TERMINATION',
                                'term_years': eos_term_years,
                                'first_term': term_first,
                                'second_term': term_second,
                                'third_term': term_third,
                                'total_term': term_first+term_second+term_third,
                                
                                'quit_leave_reason': 'QUIT',
                                'quit_years': eos_quit_years,
                                'first_quit': quit_first,
                                'second_quit': quit_second,
                                'third_quit': quit_third,
                                'fourth_quit': quit_fourth,
                                'total_quit': quit_first+quit_second+quit_third+quit_fourth,

                                'e_total_eos_amount': emp_tot_e_eos,
                                't_total_eos_amount': emp_tot_t_eos,
                                'q_total_eos_amount': emp_tot_q_eos,
                                'paid_eos_amount': emp_paid_eos+emp_eos,
                                'leave_reason': emp_detail,
                                'record_exit': True,
                                }}
                                
                else:
                    result = {'value': {
                                #'allocated_tickets':ticket_year,
                                #'allocated_amount_tickets':ticket_money,
                                'issue_tickets':ticket_year,
                                'issue_amount_tickets':ticket_money,
                                
                                'period_year': whole_years,
                                'period_month': whole_months,
                                'period_day': whole_days,
                                'whole_working':period_days,
                                'total_unpaid':val,
                                'actual_working':actual_work_days,
                                'balance_laon':bal_loan,
                                'balance_item':bal_item,
                                'end_leave_reason': 'END OF CONTRACT',
                                'end_years': eos_end_years, 
                                'first_end': end_first,
                                'second_end': end_second,
                                'third_end': end_third,
                                'total_end': end_first+end_second+end_third,
                                
                                'term_leave_reason': 'TERMINATION',
                                'term_years': eos_term_years,
                                'first_term': term_first,
                                'second_term': term_second,
                                'third_term': term_third,
                                'total_term': term_first+term_second+term_third,
                                
                                'quit_leave_reason': 'QUIT',
                                'quit_years': eos_quit_years,
                                'first_quit': quit_first,
                                'second_quit': quit_second,
                                'third_quit': quit_third,
                                'fourth_quit': quit_fourth,
                                'total_quit': quit_first+quit_second+quit_third+quit_fourth,

                                'e_total_eos_amount': end_first+end_second+end_third,
                                'e_remain_eos_amount': end_first+end_second+end_third,
                                't_total_eos_amount': term_first+term_second+term_third,
                                't_remain_eos_amount': term_first+term_second+term_third,
                                'q_total_eos_amount': quit_first+quit_second+quit_third+quit_fourth,
                                'q_remain_eos_amount': quit_first+quit_second+quit_third+quit_fourth,
                                }}
            else:
                if val > 0.0:
                    tab = d1 + relativedelta.relativedelta(days=val)
                    #print ("VACAGVACAVCACAGACAVACAAVACAVACA",tab)
                    r = relativedelta.relativedelta(d2,tab)
                    delta = d2 - tab
                    period_days = delta.days
                #    print "VACAGVACAVCACAGACAVACAAVACAVACA",period_days
                    whole_days = r.days
                 #   print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_days
                    whole_months = r.months
                  #  print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_months
                    whole_years = r.years
                   # print "VACAGVACAVCACAGACAVACAAVACAVACA",whole_years
                    #cap = d1 + relativedelta.relativedelta(months=12)
                    #print"CPCPCPCPCPCPCPC",cap
                else:
                    r = relativedelta.relativedelta(d2,d1)
                    delta = d2 - d1
                    period_days = delta.days
                    #print "LELELELELLELELELELELELELELELELELELELELELELELLELELELE",period_days
                    whole_days = r.days
                #    print "LELELELELLELELELELELELELELELELELELELELELELELLELELELE",whole_days
                    whole_months = r.months
                 #   print "LELELELELLELELELELELELELELELELELELELELELELELLELELELE",whole_months
                    whole_years = r.years
                  #  print "LELELELELLELELELELELELELELELELELELELELELELELLELELELE",whole_years
                    #cap = d1 + relativedelta.relativedelta(months=12)
                    #print"CPCPCPCPCPCPCPC",cap
                
                emp_net = contract_data.total_salary
                print ("LELELELELLELELELELELELELELELELELELELELELELELLELELELE",emp_net)
                day_salary = emp_net/30
                #print "LELELELELLELELELELELELELELELELELELELELELELELLELELELE",day_salary

                actual_work_days = period_days-val
               # print "LELELELELLELELELELELELELELELELELELELELELELELLELELELE",actual_work_days    


          ########### Calculation of Employee END of service  #############
                        
                end_first = 0.0
                end_second = 0.0
                end_third = 0.0
                
                eos_end_years = actual_work_days/365
                #print "qqqqqqqqqqqqqq",eos_end_years
                if eos_end_years < 2 :
                    end_first = 0.0
                    #print "E1E1E1E1E1E1EE1E1",end_first
                
                elif eos_end_years < 5 and eos_end_years >= 2:                    
                    end_first = 2*emp_net/2
                    second_year_sly = emp_net/2
                    second_month_sly = second_year_sly/12
                    second_days_sly = second_month_sly/30
                    end_second = ((whole_years - 2) * second_year_sly) + (whole_months * second_month_sly) + (whole_days * second_days_sly)
                    #print "E2E2EE22E2E2E2E2EE2",end_second
                
                elif eos_end_years >= 5 :
                    end_rem_val = eos_end_years - 5
                    #print "R1R1R1R1R1R1R1R1R1R",end_rem_val
                    end_first = 2*emp_net/2
                    end_second = 3*emp_net/2
                    third_year_sly = emp_net
                    third_month_sly = third_year_sly/12
                    third_days_sly = third_month_sly/30
                    end_third = ((whole_years - 5) * third_year_sly) + (whole_months * third_month_sly) + (whole_days * third_days_sly)
                    #print "E3E3E3E3E3E3E3E3E3E3",end_third
                    
                    
      ########### Calculation of Employee TERMINATION #############      
                
                term_first = 0.0
                term_second = 0.0
                term_third = 0.0
                
                eos_term_years = actual_work_days/365
                #print "qqqqqqqqqqqqqq",eos_end_years
                if eos_term_years < 2 :                    
                    first_year_sly = emp_net/2
                    first_month_sly = first_year_sly/12
                    first_days_sly = first_month_sly/30
                    term_first = (whole_years * first_year_sly) + (whole_months * first_month_sly) + (whole_days * first_days_sly)
                    #print "T1T1T1T1T1T1T1T1T1T1",term_first
                
                elif eos_term_years < 5 and eos_end_years >= 2:
                    term_first = 2*emp_net/2
                    second_year_sly = emp_net/2
                    second_month_sly = second_year_sly/12
                    second_days_sly = second_month_sly/30
                    term_second = ((whole_years - 2) * second_year_sly) + (whole_months * second_month_sly) + (whole_days * second_days_sly)
                    #print "T2T2T2TT2T2T2T2T2T2T2",term_second
                
                elif eos_term_years >= 5 :
                    term_rem_val = eos_term_years - 5
                    #print "R2R2RR22R2R2R2RR2R2RR2",term_rem_val
                    term_first = 2*emp_net/2
                    term_second = 3*emp_net/2
                    third_year_sly = emp_net
                    third_month_sly = third_year_sly/12
                    third_days_sly = third_month_sly/30
                    term_third = ((whole_years - 5) * third_year_sly) + (whole_months * third_month_sly) + (whole_days * third_days_sly)
                    #print "T3T3T3T3T3T3TT3T33T3T3T",term_third
                    
                    
      ########### Calculation of Employee QUIT #############      
                    
                quit_first = 0.0
                quit_second = 0.0
                quit_third = 0.0
                quit_fourth = 0.0
                
                eos_quit_years = actual_work_days/365
                #print "qqqqqqqqqqqqqq",eos_end_years
                if eos_quit_years < 2 :
                    quit_first = 0.0
                    #print "Q1Q1Q1Q1Q1Q1Q1Q1Q1Q1Q1",quit_first
                
                elif eos_quit_years < 5 and eos_end_years >= 2:
                    quit_second = (eos_quit_years*emp_net/2)*1/3
                    #print "Q2Q2Q2Q2Q2Q22Q2Q2Q2Q2Q2Q2",quit_second
                    
                    quit_first = (2*emp_net/2)*1/3
                    second_year_sly = (emp_net/2)*1/3
                    second_month_sly = second_year_sly/12
                    second_days_sly = second_month_sly/30
                    quit_second = ((whole_years - 2) * second_year_sly) + (whole_months * second_month_sly) + (whole_days * second_days_sly)
                
                elif eos_quit_years < 10 and eos_end_years >= 5:
                    quit_first = (2*emp_net/2)*2/3
                    quit_second = (3*emp_net/2)*2/3
                    third_year_sly = (emp_net)*2/3
                    third_month_sly = third_year_sly/12
                    third_days_sly = third_month_sly/30
                    quit_third = ((whole_years - 5) * third_year_sly) + (whole_months * third_month_sly) + (whole_days * third_days_sly)
                    #print "Q3Q3Q3Q3Q3Q3Q3Q3Q3Q3Q3Q3",quit_third
                    
                elif eos_quit_years >= 10:
                    quit_first = 2*emp_net/2
                    quit_second = 3*emp_net/2
                    quit_third = 5*emp_net
                    fourth_year_sly = emp_net
                    fourth_month_sly = fourth_year_sly/12
                    fourth_days_sly = fourth_month_sly/30
                    quit_fourth = ((whole_years - 10) * fourth_year_sly) + (whole_months * fourth_month_sly) + (whole_days * fourth_days_sly)
                    #print "Q4Q4Q4Q4Q4Q4Q4Q4Q4Q44Q4Q4Q4",quit_fourth
                    
                    
                    
                if emp_voucher_data:
                    result = {'value': {
                                #'allocated_tickets':ticket_year,
                                #'allocated_amount_tickets':ticket_money,
                                'issue_tickets':ticket_year,
                                'issue_amount_tickets':ticket_money,
                                
                                'period_year': whole_years,
                                'period_month': whole_months,
                                'period_day': whole_days,
                                'whole_working':period_days,
                                'total_unpaid':val,
                                'actual_working':actual_work_days,
                                'balance_laon':bal_loan,
                                'balance_item':bal_item,
                                'end_leave_reason': 'END OF CONTRACT',
                                'end_years': eos_end_years, 
                                'first_end': end_first,
                                'second_end': end_second,
                                'third_end': end_third,
                                'total_end': end_first+end_second+end_third,
                                
                                'term_leave_reason': 'TERMINATION',
                                'term_years': eos_term_years,
                                'first_term': term_first,
                                'second_term': term_second,
                                'third_term': term_third,
                                'total_term': term_first+term_second+term_third,
                                
                                'quit_leave_reason': 'QUIT',
                                'quit_years': eos_quit_years,
                                'first_quit': quit_first,
                                'second_quit': quit_second,
                                'third_quit': quit_third,
                                'fourth_quit': quit_fourth,
                                'total_quit': quit_first+quit_second+quit_third+quit_fourth,
                                'e_total_eos_amount': emp_tot_e_eos,
                                't_total_eos_amount': emp_tot_t_eos,
                                'q_total_eos_amount': emp_tot_q_eos,
                                'paid_eos_amount': emp_paid_eos+emp_eos,
                                'leave_reason': emp_detail,
                                'record_exit': True,
                                }}
                                
                else:
                    result = {'value': {
                                #'allocated_tickets':ticket_year,
                                #'allocated_amount_tickets':ticket_money,
                                'issue_tickets':ticket_year,
                                'issue_amount_tickets':ticket_money,
                                
                                'period_year': whole_years,
                                'period_month': whole_months,
                                'period_day': whole_days,
                                'whole_working':period_days,
                                'total_unpaid':val,
                                'actual_working':actual_work_days,
                                'balance_laon':bal_loan,
                                'balance_item':bal_item,
                                'end_leave_reason': 'END OF CONTRACT',
                                'end_years': eos_end_years, 
                                'first_end': end_first,
                                'second_end': end_second,
                                'third_end': end_third,
                                'total_end': end_first+end_second+end_third,
                                
                                'term_leave_reason': 'TERMINATION',
                                'term_years': eos_term_years,
                                'first_term': term_first,
                                'second_term': term_second,
                                'third_term': term_third,
                                'total_term': term_first+term_second+term_third,
                                
                                'quit_leave_reason': 'QUIT',
                                'quit_years': eos_quit_years,
                                'first_quit': quit_first,
                                'second_quit': quit_second,
                                'third_quit': quit_third,
                                'fourth_quit': quit_fourth,
                                'total_quit': quit_first+quit_second+quit_third+quit_fourth,
                                
                                'e_total_eos_amount': end_first+end_second+end_third,
                                'e_remain_eos_amount': end_first+end_second+end_third,
                                't_total_eos_amount': term_first+term_second+term_third,
                                't_remain_eos_amount': term_first+term_second+term_third,
                                'q_total_eos_amount': quit_first+quit_second+quit_third+quit_fourth,
                                'q_remain_eos_amount': quit_first+quit_second+quit_third+quit_fourth,
                                }}
            return result
            
employee_voucher()            


class employee_voucher_line(models.Model):
    _name = "employee.voucher.line"

    pay_type               = fields.Selection([('ticket', 'Employee Ticket'), ('eos', 'End of Service'), ('deduct', 'Deduct'), ('other', 'Other')], string='Payment Type', default='draft')
    company_id          = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    debit_account_id     = fields.Many2one('account.account',string='Debit Account', required=True,help='Debit account for journal entry')
    credit_account_id    = fields.Many2one('account.account',string='Credit Account', required=True,help='Credit account for journal entry')
    account_analytic_true= fields.Boolean(string='Pick Analytic Account from Employee screen')
    
    @api.constrains('pay_type')
    def _validate_pay_type(self):
        
        for record in self:
            tab = self.env['employee.voucher.line'].search([('pay_type', '=', record.pay_type)]) 
            if len(tab) > 1:
                #print ("GGGGGGGGGGGGGGGGGGGGGGGGG",len(tab))
                raise ValidationError(_("This Payment Types is Already created"))
    
employee_voucher_line()

class hr_contract(models.Model):

    _inherit = "hr.contract"


    vacation = fields.Float('Annual Vacation Days', required=True)
    ticket = fields.Float('Eligible Employee Tickets', required=True)
    ticket_amount = fields.Float('Amount per Ticket', required=True)
    contract_years = fields.Integer('No of Years Contract', required=True)
    total_salary = fields.Float('Total Salary', required=True)
    
    transport_allow = fields.Float('Transport Allowance')
    housing_allow = fields.Float('Housing Allowance')
    mobile_allow = fields.Float('Mobile Allowance')
    fuel_allow = fields.Float('Fuel Allowance')
    other_allow = fields.Float('Other Allowance')
   
hr_contract()


class account_move(models.Model):
    
    _inherit='account.move'

    payment_id  = fields.Many2one('employee.voucher', string='Employee Payment')
  

account_move()


class hr_employee(models.Model):
    _inherit = 'hr.employee'

    analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account')

hr_employee()
