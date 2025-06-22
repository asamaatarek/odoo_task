from odoo import models, fields

class ITIStudent(models.Model):
    _name = 'iti.student'
    _description = 'ITI Student'

    _rec_name = "age"
    name = fields.Char(string="Student Name")
    age = fields.Integer()
    salary = fields.Float()
    info = fields.Text()
    is_accepted = fields.Boolean()
    birth_date = fields.Date()
    image = fields.Binary()
    cv = fields.Char()
    is_working = fields.Boolean()

    track_id = fields.Many2one('iti.track')
    track_capacity = fields.Integer(related='track_id.capacity')
    track_is_opened = fields.Boolean(related='track_id.is_opened')