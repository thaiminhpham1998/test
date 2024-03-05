from typing import Dict, List
from odoo import api,fields, models, _
from odoo.exceptions import ValidationError
class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit=['mail.thread','mail.activity.mixin']
    _description ='Hospital Appointment'
    _rec_name='references'

    # names = fields.Char(string='Name',required=True,tracking=True)
    # references = fields.Char(string='Reference',required=True,copy=False,readonly=True,default= lambda seft: _('New'))
    references = fields.Char(string='Reference')
    dobs = fields.Date(string='Date of birth')
    patient_id= fields.Many2one('hospital.patient',string='Patient',required=True)
    age = fields.Integer(string='Age',required=True,tracking=True,related='patient_id.age')
    genders = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    images = fields.Image(string='Image')
    date_patients = fields.Date(string='Date')
    checkuptimes = fields.Datetime(string='Check Up')
    father_names = fields.Char(string='Father name')
    partner_names = fields.Char(string='Partner name')
    maritals_status = fields.Selection([('single','Single'),('married','Married')],string='Marital Status')
    phones = fields.Char(string='Phone')
    emails = fields.Char(string='Email')
    actives = fields.Boolean(string='Active', default= True)
    notes = fields.Text(string='Description')
    stages = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('done','Done'),('cancel','Cancel')],default='draft',string='Status')
    responsibles=fields.Many2one('res.partner',string='Responsible')
    prescripton = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
        ('4', 'Perfect'),
        ('5', 'Super'),
    ],string='Priority')
    def action_confirm(seft):
        seft.stages ='confirm'
    
    def action_done(seft):
        seft.stages ='done'
        
    def action_draft(seft):
        seft.stages ='draft'
        
    def action_cancel(seft):
        seft.stages ='cancel'
    def action_notification(seft):
        
        message="button click success"
        return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'message': message,
                'type':'success',
                'stcky':True
            }
        } 
    @api.model
    
    
    def create(self,vals):
        if not vals.get('notes'):
            vals['notes']='Done'
        # if vals.get('name',_('New')) == _('New'):
        #     vals['reference']=self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment,self).create(vals)
        return res
    def unlink(self):
        if self.stages != 'draft':
            raise ValidationError(_('you can  delete appointment with Draft status'))
        return super(HospitalAppointment,self).unlink()
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.references =self.patient_id.reference
        self.genders = self.patient_id.gender
        