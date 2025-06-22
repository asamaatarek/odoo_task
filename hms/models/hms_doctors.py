from odoo import models, fields

class HMSDoctor(models.Model):
    _name = 'hms.doctors'
    _description = 'HMS Doctors'

    first_name = fields.Char(string="First Name")
    last_name = fields.Char(string="Last Name")
    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    
    department_id = fields.Many2one('hms.department')
