from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from odoo import fields

class TestHelpdesk(TransactionCase):
    def setUp(self):
        super(TestHelpdesk, self).setUp()#EN CARPETA DATA
        self.ticket = self.env.ref('helpdesk_geyson.helpdesk_ticket_demo_01')
        self.tag = self.env.ref('helpdesk_geyson.helpdesk_ticket_tag_demo_01')
        self.ticket.tag_ids = [(6, 0, self.tag.ids)]

    def test_10_tag_assign(self):
        self.assertEqual(self.ticket.tag_ids, self.tag)

    def test_20_raise_Exception(self):
        self.ticket.dedicate_time=2
        self.assertEqual(self.ticket.dedicate_time, 2)
        with self.assertRaises(ValidationError):
            self.ticket.dedicate_time=-1

    def test_30_set_dedicated(self):
        values = {
            'name': "action",
            'date': fields.Date.today(),
            'ticket_id': self.ticket.id,
            'dedicate_time': 100,
        }
        self.ticket.action_ids += self.env['helpdesk.ticket.action'].create(values)
        self.ticket.dedicate_time = 40
        actions_total = sum(self.ticket.action_ids.mapped('dedicate_time'))

        self.assertEqual(self.ticket.dedicate_time, actions_total)

        

    


        

   