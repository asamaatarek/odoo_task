from odoo import models, fields

class ITITrack(models.Model):
    _name = 'iti.track'
    _description = 'ITI Track'

    name = fields.Char(string="Track Name")
    capacity = fields.Integer()
    is_opened = fields.Boolean()

    student_id = fields.One2many('iti.student','track_id')