from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_create_claim(self):
        ctx = self.env.context.copy()
        action = self.env["ir.actions.act_window"]._for_xml_id("md_claim.action_claim_management")
        ctx.update({
            'default_partner_id': self.partner_id.id,
            'default_job_order': self.name,
            'default_claim_to_company_id': self.company_id.id,
        })
        action.update({
            'domain': [('partner_id', '=', self.partner_id.id)],
            'context': ctx,
            'view_mode': 'form',
            'target': 'current',
            'views': [(self.env.ref('md_claim.view_claim_management_form').id, 'form')],

        })

        return action