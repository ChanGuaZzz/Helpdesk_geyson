from odoo import models, fields

class HelpdeskTicketAction(models.Model):
    _name = "helpdesk.ticket.action"
    _description = "helpdesk action"

    name = fields.Char(string='name')
    date = fields.Date(string='Date')
    ticket_id = fields.Many2one(
        comodel_name='helpdesk.ticket',
    )

    dedicate_time = fields.Float(string='Dedicated Time')
