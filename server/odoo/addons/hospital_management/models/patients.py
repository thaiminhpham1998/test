from odoo import api,fields, models,_
from datetime import date
import random
from odoo.exceptions import ValidationError
class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit=['mail.thread','mail.activity.mixin']
    _description ='Hospital Patient'
    # _rec_name='references'
    
    ref = fields.Char(string='Ref')
    name = fields.Char(string='Name',required=True,tracking=True)
    reference = fields.Char(string='Reference',required=True,copy=False,readonly=True,default= lambda seft: _('New'))
    dob = fields.Date(string='Date of birth')
    
    date_of_birth=fields.Date(string="Date of birth")
    
    age = fields.Integer(string='Age',compute='_compute_age',search='_search_age',required=True,tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female')],string='Gender')
    image = fields.Image(string='Image')
    date_patient = fields.Date(string='Date')
    checkuptime = fields.Datetime(string='Check Up')
    father_name = fields.Char(string='Father name')
    partner_name = fields.Char(string='Partner name')
    marital_status = fields.Selection([('single','Single'),('married','Married')],string='Marital Status')
    #phone = fields.Char(string='Phone')
    #email = fields.Char(string='Email')
    active = fields.Boolean(string='Active', default= True)
    note = fields.Text(string='Description')
    stage = fields.Selection([('draft','Draft'),('confirm','Confirmed'),('done','Done'),('cancel','Cancel')],default='draft',string='Status')
    responsible=fields.Many2one('res.partner',string='Responsible')
    appointment_id = fields.Many2one('hospital.appointment',string='Appointments')
    booking_date = fields.Date(string='Book')
    doctor_id = fields.Many2one('res.users',string='Doctor')
    pharmacy_line = fields.One2many('patient.pharmacy.lines','patient_id',string='Pharmacy Lines')
    tag_ids = fields.Many2many('patient.tag',string = 'Tag')
    
    is_birthday = fields.Boolean(string='Birthday ?', compute='_compute_is_birthday')
    phone=fields.Char(string="Phone")
    email=fields.Char(string="email")
    website=fields.Char(string="Website")
    progress = fields.Integer(string='Progress', compute="_compute_progress")
    
    company_id =fields.Many2one('res.company','Company', default= lambda self: self.env.company)
    currency_id= fields.Many2one('res.currency', related='company_id.currency_id')
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth> fields.Date.today():
                raise ValidationError(_('The entered datei is not accept'))
    def action_confirm(seft):
        seft.stage ='confirm'
        
        return{
            'effect':{
                'fadeout':'slow',
                'message':'Click Successfull',
                'type':'rainbow_man'
            }
        }
    #url action
    # def action_done(seft):
    #     seft.stage ='done'
    #     return{
    #         'type':'ir.action.act_url',
    #         'target':'self',
    #         'url':'https://www.odoo.com'
    #     }
    def action_done(seft):
        seft.stage ='done'
        
    def action_draft(seft):
        seft.stage ='draft'
        
    def action_cancel(seft):
        seft.stage ='cancel' 
    @api.depends('date_of_birth')
    def _compute_age(self):
        
        for rec in self:
            today = date.today()
        # return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            if rec.date_of_birth:
                rec.age = today.year -rec.date_of_birth.year
            else:
                rec.age=0
    def _search_age(self,operator,value):
        return[('id','=',11)]
    @api.model
    def create(self,vals):
        if not vals.get('note'):
            vals['note']='New Patient'
        if vals.get('name',_('New')) == _('New'):
            vals['reference']=self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient,self).create(vals)
        return res
    
    
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today= date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday =True
            rec.is_birthday= is_birthday
    @api.depends('stage')
    def _compute_progress(self):
        for rec in self:
            if rec.stage =='draft':
                progress= random.randrange(0,25)
            elif rec.stage=='confirm':
                progress=random.randrange(25,99)
            elif rec.stage =='done':
                progress=100
            else:
                progress=0
            rec.progress =progress
            
    # # def create(self, vals):
    # #     if vals.get('name_seq', _('New')) == _('New'):
    # #         vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
    # #     result = super(HospitalPatient, self).create(vals)
    # #     return result
class PatientPharmacy(models.Model):
    _name = 'patient.pharmacy.lines'
    _description='Patient Pharmacy Lines'
    
    product_id= fields.Many2one('product.product')
    price_unit= fields.Integer(string='Price')
    qty=fields.Integer(string='Quantity')
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    # company_currency_id= fields.Many2one('res.currency', related='patient_id.currency_id')
    
    currency_id= fields.Many2one('res.currency', related='patient_id.currency_id')
    
    price_subtotal = fields.Monetary(string="Subtotal",compute='_compute_price_subtotal', 
                                    currency_field='currency_id')
    
    @api.depends('price_unit','qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal=rec.price_unit * rec.qty