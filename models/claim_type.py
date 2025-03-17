from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ClaimType(models.Model):
    _name = 'claim.type'
    _description = "Claim Management"
    _rec_name = "claim_type"

    claim_type = fields.Char(string="Claim")