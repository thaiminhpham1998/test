from odoo import api,fields, models,_
from datetime import date
class PatientTag(models.Model):
    _name = 'patient.tag'
    _inherit=['mail.thread','mail.activity.mixin']
    
    name= fields.Char(string='Name')
    active=fields.Boolean(string='Active', default=True)
    color =fields.Integer(string='Color')
    color_add = fields.Char(string='Color Add')