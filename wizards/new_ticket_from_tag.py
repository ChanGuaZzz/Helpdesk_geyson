from odoo import models, fields


class NewTicketFromTag(models.TransientModel):
    _name = 'new.ticket.from.tag'
    _description = 'New Ticket From Tag'

    def _get_default_tag(self):
        return self._context.get('active_id')
    

    name = fields.Char( string='name',required=True)
    date = fields.Date(string='date',  default=fields.Date.today())
    user_id = fields.Many2one(comodel_name='res.users',string='User')
    tag_id = fields.Many2one(comodel_name='helpdesk.tag',string='Tag', 
    default=_get_default_tag
    )

    def create_ticket(self):
        tag_id = self.tag_id.id
        values={
            'name': self.name,
            'date': self.date,
            'user_id': self.user_id.id,
            'tag_ids': [(6,0, [tag_id])],
        }
        ticket= self.env['helpdesk.ticket'].create(values)

        action= self.env.ref('helpdesk_geyson.helpdesk_ticket_action').read()[0]

        action['context']= {
            'res.id': ticket.id,
            'view_mode': 'form',
            } 
        action['context']= {
            'deafult_tag_ids': [(6,0, self.tag_id.ids)],
            } 
    
    
        action['views']=[(self.env.ref('helpdesk_geyson.helpdesk_ticket_view_form').id,'form')]
        action['res_id']= ticket.id
        return action
