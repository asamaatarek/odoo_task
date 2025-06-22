from odoo import models, fields, api, exceptions
from odoo import models, fields, api
import re
from datetime import date
class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char()
    last_name = fields.Char()
    name = fields.Char(string="Name")
    birth_date = fields.Date()
    history = fields.Html()
    blood_type = fields.Selection(
        selection=[
            ('o', 'O'),
            ('a', 'A'),
            ('b', 'B'),
        ],
        string='Blood Type',
        default='o'
    )
    pcr = fields.Boolean()
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    cr_ratio = fields.Float()
    address = fields.Text()
    image = fields.Binary()
    state = fields.Selection(
        selection=[
            ('undetermined', 'Undetermined'),
            ('good', 'Good'),
            ('fair', 'Fair'),
            ('serious', 'Serious'),
        ],
        string='State',
        default='fair'
    )
    department_id = fields.Many2one('hms.department')
    
    email = fields.Char(string="Email", required=True)
    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)', 'Email must be unique.')
    ]
    doctors_id = fields.Many2many('hms.doctors')
    
    department_capacity = fields.Integer(related='department_id.capacity')
    related_customer_id = fields.One2many('res.partner', 'related_patient_id', string="Related Customers")

    level_logs = fields.One2many('hms.patient.log','patient_id')
    
    @api.onchange('age')
    def _onchange_age_auto_check_pcr(self):
        if self.age and self.age < 30 and not self.pcr:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Automatically Checked',
                    'message': 'PCR was automatically checked because age is less than 30.'
                }
            }
    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and record.cr_ratio is None:
                raise exceptions.ValidationError('CR Ratio is required when PCR is checked.')
    
    @api.model
    def create(self, vals):
        patient = super(HMSPatient, self).create(vals)  
        self.env['hms.patient.log'].create({
            'description': f'level changed to {patient.state}',
            'patient_id': patient.id,
            'created_by': self.env.user.id
            })
        return patient

    def write(self, vals):
        for record in self:
            old_state = record.state
            res = super(HMSPatient, record).write(vals)
            if 'state' in vals and vals['state'] != old_state:
                self.env['hms.patient.log'].create({
                    'patient_id': record.id,
                    'description': f"State changed to {vals['state']}",
                    'created_by' : self.env.uid
                })
        return res
    
    @api.constrains('email')
    def _check_valid_email(self):
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise exceptions.ValidationError("Email format is invalid.")

    
    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
            else:
                rec.age = 0
