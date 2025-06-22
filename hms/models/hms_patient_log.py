from odoo import models, fields

class HMSPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log History'

    patient_id = fields.Many2one('hms.patient', required=True)
    description = fields.Text(required=True)
    created_by = fields.Many2one('res.users', string="Created By", default=lambda self: self.env.user)