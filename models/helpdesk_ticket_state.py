from odoo import models, fields

class HelpdeskTicketState(models.Model):
    _name = "helpdesk.ticket.state"
    _description = "helpdesk State"

    name = fields.Char(string='name')
