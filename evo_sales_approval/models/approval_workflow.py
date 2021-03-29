# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ApprovalWorkflow(models.Model):
    _name = "approval.workflow"
    _rec_name = 'type'

    _sql_constraints = [
        ('unique_object_workflow', 'UNIQUE (type)', 'Only one workflow allowed per Approval Type!')
    ]

    type = fields.Selection([('sale_order', 'Sale')], 'Approval Type', track_visibility='onchange', copy=False)
    active = fields.Boolean('Active', default=True)
    level = fields.Selection([
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5, 'Fifth'),
        (6, 'Sixth'),
        (7, 'Seventh'),
        (8, 'Eighth'),
        (9, 'Ninth')
    ], 'Approval Level')
    approval_line_ids = fields.One2many('approval.workflow.line', 'workflow_id', 'Approval Levels', copy=True, auto_join=True)
    mail_template_id = fields.Many2one('mail.template', 'Use template', copy=True, required=True)


class ApprovalWorkflowLine(models.Model):
    _name = "approval.workflow.line"

    _sql_constraints = [
        ('unique_level', 'CHECK(1=1)', 'Approval Level must be unique per workflow!')
    ]

    workflow_id = fields.Many2one('approval.workflow', 'Workflow', required=True, ondelete='cascade', copy=False,index=True)
    job_id = fields.Many2one('hr.job', 'Job Position')
    level = fields.Selection([
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5, 'Fifth'),
        (6, 'Sixth'),
        (7, 'Seventh'),
        (8, 'Eighth'),
        (9, 'Ninth')
    ], 'Approval Level')
