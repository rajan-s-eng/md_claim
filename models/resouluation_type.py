from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResouluationType(models.Model):
    _name = 'resouluation.type'
    _description = "Claim Management"
    _rec_name = "resouluation_type"

    resouluation_type = fields.Char(string="Resouluation Type")