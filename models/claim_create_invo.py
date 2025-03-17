from odoo import models, fields, api

class ClaimCreateInvo(models.Model):
    _inherit = 'account.move'

    claim_count = fields.Integer("Claims", compute='_compute_invoice_count')

    def action_claim_create(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        action = self.env["ir.actions.act_window"]._for_xml_id("md_claim.action_claim_management")
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_job_order': self.name,
            'default_claim_to_company_id': self.company_id.id,
            'default_invoice_id': self.id
        })
        action.update({
            'domain': [('partner_id', '=', self.partner_id.id)],
            'context': ctx,
            'view_mode': 'form',
            'target': 'current',
            'views': [(self.env.ref('md_claim.view_claim_management_form').id, 'form')],

        })
        return action

    def view_invoice(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("md_claim.action_claim_management")
        ctx = self.env.context.copy()
        ctx.update({
            'default_partner_id': self.partner_id.id,
        })
        action.update({
            'domain': [('invoice_id', '=', self.id)],
            'context': ctx
        })
        return action

    def _compute_invoice_count(self):
        for move in self:
            move.claim_count = self.env['md.claim'].search_count([('invoice_id', '=', move.id)])