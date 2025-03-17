from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class MdClaim(models.Model):
    _name = 'md.claim'
    _description = "Claim Management"
    _order = "claim_date desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', readonly=True, index='trigram', default=lambda self: _('New'))
    partner_id = fields.Many2one(comodel_name='res.partner', string="Customer", tracking=True)
    job_order = fields.Char(string="Job Order", tracking=True)
    plat_no = fields.Char(string="Plat No", tracking=True)
    responsible_id = fields.Many2one('res.users', string="Responsible", tracking=True)

    estimated_amount = fields.Float(string="Estimeted Amount", tracking=True)
    claim_to_company_id = fields.Many2one(comodel_name='res.company', string="Claim To Company", tracking=True)
    claim_type_id = fields.Many2one(comodel_name="claim.type", string="Claim Type", tracking=True)
    claim_description = fields.Text(string="Claim Description", tracking=True)
    claim_date = fields.Date(string="Claim Date", tracking=True)

    resolution_type_id = fields.Many2one(comodel_name="resouluation.type", string="Resolution Type", tracking=True)
    resolution_desc = fields.Text(string="Resolution Description ", tracking=True)
    resolution_date = fields.Date(string="Resolution Date", tracking=True)
    resolved_by_id = fields.Many2one(comodel_name='res.users', string="Resolved By", tracking=True)
    invoice_id = fields.Many2one(comodel_name='account.move', string="Invoice")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('start_investigation', 'Start Investigation'),
        ('resolved', 'Resolved'),
        ('close', 'Close'),
        ('cancelled', 'Cancelled'),
    ], default='draft', readonly=True, tracking=True)

    def action_start_investigation(self):
        for record in self:
            if not record.responsible_id or not record.claim_description or not record.claim_type_id:
                raise ValidationError(_("Please fill in Responsible Person, Claim Description, and Claim Type before starting the investigation."))
            record.write({'state' : 'start_investigation'})

    def action_resolved(self):
        for record in self:
            if not record.resolution_type_id or not record.resolution_desc:
                raise ValidationError(_("Please fill in Resolution Type and Resolution Description before marking as resolved."))
            record.write({'state': 'resolved', 'resolution_date': fields.Datetime.now(), 'resolved_by_id': self.env.uid})

    def action_close(self):
        self.write({'state': 'close'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].next_by_code('md.claim') or _("New")
        return super().create(vals_list)