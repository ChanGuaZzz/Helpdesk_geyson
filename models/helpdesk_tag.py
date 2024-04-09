from odoo import models, fields, api

class HelpdeskTag(models.Model):
    _name = "helpdesk.tag"
    _description = "helpdesk tag"

    name = fields.Char(string='name')
    ticket = fields.Boolean()
    action = fields.Boolean()
    ticket_ids = fields.Many2many(
        string='ticket',
        comodel_name='helpdesk.ticket',
        relation='helpdesk_ticket_tag_rel',
        column2='ticket_id',
        column1='tag_id',
            
    )
    @api.model#cron
    def _clean_tags_all(self):
        tags_to_delete= self.search([('ticket_ids','=',False)])
        tags_to_delete.unlink()