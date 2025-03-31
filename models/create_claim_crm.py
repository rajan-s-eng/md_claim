from odoo import models, fields, api

class ClaimCreateCrm(models.Model):
    _inherit = 'crm.lead'

    crm_count = fields.Integer("Claims", compute='_compute_crm_count')

    def action_claim_create(self):
        self.ensure_one()
        ctx = self.env.context.copy()
        action = self.env["ir.actions.act_window"]._for_xml_id("md_claim.action_claim_management")
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_lead_id': self.id,
            'default_claim_to_company_id': self.company_id.id,
            'default_claim_date' : self.date_deadline,
            'default_estimated_amount' : self.expected_revenue,
            'default_responsible_id' : self.user_id.id,
            'default_claim_description' : self.name,
        })
        action.update({
            'domain': [('lead_id', '=', self.id)],
            'context': ctx,
            'view_mode': 'form',
            'target': 'current',
            'views': [(self.env.ref('md_claim.view_claim_management_form').id, 'form')],

        })
        return action

    def view_crm(self):
        self.ensure_one()
        action = self.env["ir.actions.act_window"]._for_xml_id("md_claim.action_claim_management")
        ctx = self.env.context.copy()
        ctx.update({
            'default_partner_id': self.partner_id.id,
        })
        action.update({
            'domain': [('lead_id', '=', self.id)],
            'context': ctx
        })
        return action

    def _compute_crm_count(self):
        for move in self:
            move.crm_count = self.env['md.claim'].search_count([('lead_id', '=', move.id)])