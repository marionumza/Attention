# -*- coding: utf-8 -*-
from lxml import etree
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
import werkzeug
from werkzeug.urls import url_encode


class RecordApproval(models.Model):
    _name = "record.approval"

    @api.multi
    def get_user_name(self):
        for rec in self:
            name_list = [user_id.name for user_id in rec.user_ids]
            rec.user_name = ','.join(name_list)

    sale_order_id = fields.Many2one('sale.order', 'Sale Order')
    workflow_id = fields.Many2one('approval.workflow', 'Workflow')
    wfl_id = fields.Many2one('approval.workflow.line', 'Workflow Level')
    approved_user_id = fields.Many2one('res.users', 'Approved By')
    approved_date = fields.Datetime('Approved On')
    user_name = fields.Char(
        string="Users", compute="get_user_name", track_visibility='onchange')
    user_ids = fields.Many2many('res.users', 'record_approval_user_rel',
                                'approval_id', 'user_id', 'Users', track_visibility='always')
    status = fields.Selection(
        [('pending', 'Pending'), ('rejected', 'Rejected'), ('approved', 'Approved')], 'Status')
    level = fields.Selection([(1, 'First'), (2, 'Second'), (3, 'Third'), (4, 'Fourth'), (
        5, 'Fifth'), (6, 'Sixth'), (7, 'Seventh'), (8, 'Eighth'), (9, 'Ninth')], 'Approval Level')
    note = fields.Text('Note')
    job_id = fields.Many2one('hr.job', 'Job Position')




class SaleOrder(models.Model):
    _inherit = "sale.order"

    activity_id = fields.Many2one('mail.activity', 'activity')

    @api.depends('approva_state', 'approval_user_ids', 'approval_level_ids')
    def _compute_user_approve(self):
        for rec in self:
            if rec.approval_level_ids:
                user_id = self.env.user.id
                allow_user = rec.approval_user_ids.filtered(
                    lambda r: r.id == user_id)
                if not allow_user:
                    rec.user_approve_boolean = True

            elif rec.approval_user_ids:
                user_id = self.env.user.id
                allow_user = rec.approval_user_ids.filtered(
                    lambda r: r.id == user_id)
                if not allow_user:
                    rec.user_approve_boolean = True

            else:
                rec.user_approve_boolean = False

    @api.multi
    @api.depends('check_user')
    def get_user(self):
        if SUPERUSER_ID == self._uid or self._uid == 2:
            self.check_user = True
        else:
            self.check_user = False

    approva_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending for Approval'),
        ('approved', 'Approved'),
    ], 'Approval Status', track_visibility='onchange', copy=False, default='draft')
    user_approve_boolean = fields.Boolean(
        'User Approved', compute='_compute_user_approve')
    approval_user_ids = fields.Many2many(
        'res.users', 'so_user_approval_rel', 'so_id', 'user_id', 'Approval Users', store=True)
    approval_level_ids = fields.One2many(
        'record.approval', 'sale_order_id', 'Sale Approval Levels')
    level_val = fields.Integer('Level value')
    check_user = fields.Boolean('Check', compute='get_user')

    def make_activity(self, user_group, note, summary):
        date_deadline = fields.Date.today()
        print(date_deadline)

        self.activity_id = self.sudo().activity_schedule(
            'mail.mail_activity_data_todo', date_deadline,
            note=note,
            user_id=user_group.id,
            res_id=self.id,
            summary=summary
        )

        # self.activity_id = x.id

    def action_send_for_approval(self):
        workflow_id = self.env['approval.workflow'].search(
            [('type', '=', 'sale_order'), ('active', '=', True)], limit=1)
        if workflow_id:
            if workflow_id.approval_line_ids:
                for rec in workflow_id.approval_line_ids:
                    if rec.level == 1:
                        employee_ids = self.env['hr.employee'].search(
                            [('job_id', '=', rec.job_id.id)])
                        print("employee_ids",employee_ids)

                        if employee_ids:
                            for emp_id in employee_ids:
                                print(",,,,,,,,",emp_id)
                                if emp_id.id == 231:
                                    print("<<<<<<<<<",emp_id)
                                    if emp_id.user_id:
                                        self.write({'approval_user_ids': [(4, emp_id.user_id.id)]})
                            workflow_id.write({
                                'level': 1,
                            })
                            print("rrrrrrrrr",self.approval_user_ids)
                            # mmmmmmmmmmmmmmmm
                            if self.approval_user_ids:
                                email_to = ''
                                for partner in self.approval_user_ids:
                                    email_to += partner.email + ','
                                if self.env.user and self.env.user.email:
                                    email_from = self.env.user.email
                                so_approval_template = workflow_id.mail_template_id
                                # so_approval_template = self.env.ref('evo_sales_approval.so_approval_wf_email_template2')

                                # so_approval_template = workflow_id.mail_template_id

                                if so_approval_template:
                                    mail_res = so_approval_template.with_context(email_from=email_from,
                                                                                 email_to=email_to).send_mail(self.id,
                                                                                                              force_send=True)
                                    print("Mail Sent===============", mail_res)
                                    print("partner",partner.name)
                                    mail_content = "  Hello  " + partner.name + ",<br>Sale Order #  " + \
                                                   self.name + ",<br> amounting = " + str(self.amount_total) +\
                                                   ".is waiting for your approval"
                                    self.make_activity(partner,mail_content,'SO Activity')
                                    # print("mail_activity",self.make_activity(partner,mail_content,'SO Activity'))
        self.write({
            'approva_state': 'pending',
            'level_val': 1,
        })


    # def action_send_for_approval(self):
    #     user_id = self.env.user.id
    #     workflow_id = self.env['approval.workflow'].search(
    #         [('type', '=', 'sale_order'), ('active', '=', True)], limit=1)
    #     if workflow_id:
    #         if workflow_id.approval_line_ids:
    #             for rec in workflow_id.approval_line_ids:
    #                 if rec.level == 1:
    #                     # employee_ids = self.env['hr.employee'].search(
    #                     #     [('job_id', '=', rec.job_id.id)])
    #                     # print("employee_ids",employee_ids)
    #                     employee_id = self.env['hr.employee'].search([('user_id.id', '=', user_id)])
    #                     print("emp_id", employee_id)
    #                     emp_id = employee_id.parent_id.id
    #                     if emp_id and emp_id == 231:
    #                     # if employee_ids:
    #                         if self.env['hr.employee'].browse(emp_id).user_id:
    #                             self.write({'approval_user_ids': [(4, self.env['hr.employee'].browse(emp_id).user_id.id)]})
    #                         workflow_id.write({
    #                             'level': 1,
    #                         })
    #                         if self.approval_user_ids:
    #                             email_to = ''
    #                             print("$$$$$$$$4",self.approval_user_ids)
    #                             # mmmmmmmmmmmm
    #                             for partner in self.approval_user_ids:
    #                                 email_to += partner.email + ','
    #                             if self.env.user and self.env.user.email:
    #                                 email_from = self.env.user.email
    #                             so_approval_template = workflow_id.mail_template_id
    #                             if so_approval_template and email_to and email_from:
    #                                 mail_res = so_approval_template.with_context(email_from=email_from,email_to=email_to).send_mail(self.id,force_send=True)
    #                                 print("Mail Sent===============", mail_res)
    #     self.write({
    #         'approva_state': 'pending',
    #         'level_val': 1,
    #     })

    def action_approve(self):
        view_id = self.env.ref('evo_sales_approval.wiz_update_approval_line_form')
        return {
            'name': 'Approve Quotation',
            'type': 'ir.actions.act_window',
            'res_model': 'update.approval.lines',
            'context': {
                'default_sale_order_id': self.id,
                'default_approve_check': True,
            },
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
        }
        # self.write({'state': 'approved'})

    def action_reject(self):
        view_id = self.env.ref(
            'evo_sales_approval.wiz_update_approval_line_form')
        return {
            'name': 'Reject Quotation',
            'type': 'ir.actions.act_window',
            'res_model': 'update.approval.lines',
            'context': {
                'default_sale_order_id': self.id,
                'default_reject_check': True,
            },
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': view_id.id,
            'target': 'new',
        }
        # self.write({'state': 'draft'})

    @api.multi
    def action_quotation_send(self):
        if self.approva_state != 'approved':
            raise ValidationError(
                _("Quotation is not approved yet. Email can't be send."))
        else:
            return super(SaleOrder, self).action_quotation_send()

    @api.multi
    def action_confirm(self):
        if self.approva_state != 'approved':
            raise ValidationError(
                _("Quotation is not approved yet. You cannot confirm the Order."))
        else:
            workflow_id = self.env['approval.workflow'].search(
                [('type', '=', 'sale_order'), ('active', '=', True)], limit=1)
            if workflow_id:
                if self.approval_user_ids:
                    email_to = ''
                    for partner in self.approval_user_ids:
                        email_to += partner.email + ','
                    if self.env.user and self.env.user.email:
                        email_from = self.env.user.email
                    # so_approval_template = workflow_id.mail_template_id
                    # so_approval_template = workflow_id.mail_template_id
                    so_approval_template = self.env.ref('evo_sales_approval.so_approval_wf_email_template2')

                    if so_approval_template:
                        mail_res = so_approval_template.with_context(email_from=email_from,
                                                                     email_to=email_to).send_mail(self.id,
                                                                                                  force_send=True)
                        print("Mail Sent===============", mail_res)
                        print("partner", partner.name)
                        mail_content = "  Hello  " + partner.name + ",<br>Sale Order #  " + \
                                       self.name + ",<br> amounting = " + str(self.amount_total) + \
                                       ".is confirmed"
                        # self.make_activity(partner, mail_content, 'SO Activity')
                return super(SaleOrder, self).action_confirm()

    @api.multi
    def print_quotation(self):
        if self.approva_state != 'approved':
            raise ValidationError(
                _("Quotation is not approved yet. You cannot print the Order."))
        else:
            return super(SaleOrder, self).print_quotation()

    @api.multi
    def get_full_url(self):
        self.ensure_one()
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        url_params = {
            'id': self.id,
            'view_type': 'form',
            'model': 'sale.order',
            'menu_id': self.env.ref('sale.menu_sale_quotations').id,
            'action': self.env.ref('sale.action_quotations_with_onboarding').id,
        }
        params = '/web?#%s' % url_encode(url_params)
        return base_url + params