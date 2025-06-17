from odoo import models, fields, api, exceptions

class HMSPatient(models.Model):
    _name = 'hms.patient'
    _description = 'HMS Patient'

    first_name = fields.Char()
    last_name = fields.Char()
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
    age = fields.Integer()
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
    doctors_id = fields.Many2many('hms.doctors')
    
    department_capacity = fields.Integer(related='department_id.capacity')

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and record.cr_ratio is None:
                raise exceptions.ValidationError('CR Ratio is required when PCR is checked.')
