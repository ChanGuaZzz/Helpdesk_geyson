from odoo import api, models, fields
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta

class HelpdeskTickets(models.Model):

    _name = "helpdesk.ticket"
    _description = "helpdesk Ticket"
    _inherit = ['mail.thread','mail.activity.mixin']

    def _default_user(self):
       return self.env.user
    
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    date = fields.Date(string="Date", default= fields.Date.today() )
    date_due= fields.Date(string="Date Due")
    dedicate_time = fields.Float(
        string="Time",
        compute='_compute_dedicate_time', 
        inverse='_set_dedicate_time', 
        search="_search_dedicate_time"
        
    )
    assigned = fields.Boolean('Assigned',compute='_compute_assigned', store=True)
    assigned_qty = fields.Integer(string='Assigned Qty', 
        compute='_compute_assigned_qty', store=True)
    
    corrective_action = fields.Html(
        help='Detail of corrective action after this issue'
    )
    preventive_action = fields.Html(
        help='Detail of preventive action after this issue'
    )

    
    state = fields.Selection(
        selection=[
            ('new','New'),
            ('assigned','Assigned'),
            ('in_progress','In Progress'),
            ('waiting','In Waiting'),
            ('done','Done'),
            ('cancel','Cancel'),
        ],
        compute='_compute_assigned',
        store=True,
        default='new',
        string='state',
        
    )

    def action_state(self):
        for record in self:
            if record.state == 'new':
                record.state='assigned'
            elif record.state == 'assigned':
                record.state='in_progress'
            elif record.state == 'in_progress':
                record.state='waiting'
            elif record.state == 'waiting':
                record.state='done'
            elif record.state == 'done':
                record.state='cancel'
            
    def action_cancel(self):
        for record in self:
            self.state='cancel'

    state_id= fields.Many2one(
        string='State',
        comodel_name='helpdesk.ticket.state',
    )

    user_id = fields.Many2one(
        string='Assigned to',
        comodel_name='res.users',
        
        default=_default_user#funcion para el usuario default
        
    )

    
    partner_id = fields.Many2one(string='Customer', comodel_name='res.partner')
    

    
    
    action_ids = fields.One2many(
        comodel_name="helpdesk.ticket.action", 
        inverse_name="ticket_id", 
        string='Actions'
    )
    
    tag_ids = fields.Many2many(
        string='tag',
        comodel_name='helpdesk.tag',
        relation='helpdesk_ticket_tag_rel',
        column1='ticket_id',
        column2='tag_id',
        domain=[('name','like','a')]
    )

    related_tag_ids= fields.Many2many(
        string='Related Tags',
        comodel_name='helpdesk.tag',
        compute='_compute_related_tag_ids',
    )
    new_tag_name = fields.Char(string='New Tag name')

    def create_new_tag_back(self):
        self.ensure_one()

        if self.new_tag_name:
            tag=self.env['helpdesk.tag'].create({
                'name': self.new_tag_name,
            })

            self.tag_ids +=tag
        

    def create_new_tag(self):
        self.ensure_one()
        action=self.env.ref("helpdesk_geyson.helpdesk_tag_new_action").read()[0]
        action['context'] = {
            'default_name': self.new_tag_name,
            'default_ticket_ids':self.ids,
           
        }
        return action

    
     



    def _search_dedicate_time(self, operator, value):

      #  action_ids= self.env['helpdesk.ticket.action'].search([('dedicate_time',operator,value)]).mapped('ticket_id').ids
        query_str = """select ticket_id from helpdesk_ticket_action group by ticket_id having sum(dedicate_time){} {}""".format(operator,value)

        self._cr.execute(query_str)
        res= self._cr.fetchall()
        return [('id','in',[r[0]for r in res])]
 



    def _set_dedicate_time(self):
        for record in self:
            computed_time= sum(record.action_ids.mapped('dedicate_time'))
            if self.dedicate_time != computed_time:
                values={
                    'name':"Auto time",
                    'date': fields.Date.today(),
                    'ticket_id': record.id,
                    'dedicate_time': self.dedicate_time - computed_time,

                }
                self.action_ids += self.env['helpdesk.ticket.action'].create(values)

        
    @api.depends('action_ids.dedicate_time')
    def _compute_dedicate_time(self):
        for record in self:
            record.dedicate_time = 0
            for action in record.action_ids:
                record.dedicate_time = sum(record.action_ids.mapped('dedicate_time'))


    @api.depends('user_id')
    def _compute_related_tag_ids(self):
        for record in self:
            user =record.user_id
            other_tickets= self.env["helpdesk.ticket"].search([('user_id','=',user.id)])
            all_tags=other_tickets.mapped('tag_ids')
            record.related_tag_ids = all_tags

    
    @api.depends('user_id')
    def _compute_assigned(self):
        for record in self:
            if record.user_id:
                record.assigned =True 
                record.state='assigned'
            else:
                record.state='new'
    
    @api.depends('user_id')
    def _compute_assigned_qty(self):
        for record in self:
            user =record.user_id
            other_tickets= self.env["helpdesk.ticket"].search([('user_id','=',user.id)])

            record.assigned_qty = len(other_tickets)


            
    @api.constrains("dedicate_time")#SE USA PARA RESTRICCIONES LOS CAMPOS CUANDO SE CAMBIAN ONCHANGE
    def _check_dedicate_time(self):
        for record in self:
            if record.dedicate_time <0:
                raise ValidationError('The dedicate time must be positive')
            
        


    @api.onchange("date")#Se ejecuta al cambiar el campo y hace la funcion que se le indica
    def _onchange_date_due(self):
        if self.date:
            if self.date < fields.Date.today():
                raise UserError('The date must be greater than today')

            date_datetime = fields.Date.from_string(self.date)
            self.date_due = date_datetime + timedelta(days=1)
        

   



    
