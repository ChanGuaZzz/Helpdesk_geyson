
{
    "name": "helpdesk geyson",
    "summary": "Helpdesk and tickets",
    "version": "13.0.1.0.0",
    "category": "Helpdesk",
    "descripcion":""" Helpdesk """,
    "website": "https://github.com/OCA/helpdesk",
    "author": "Geyson",
   
    "maintainers": ["ChanguaZzz"],
    "license": "AGPL-3",
    "application": True,
    "installable": True,
    "depends": [
        "base",
        "mail",
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "views/helpdesk_ticket_views.xml", 
        "wizards/new_ticket_from_tag_views.xml",
        "views/helpdesk_tag_views.xml",
        "views/helpdesk_action_views.xml",
        "data/helpdesk_data.xml",
        "reports/helpdesk_ticket_templates.xml",
       
    ],
    'demo': [
        'data/helpdesk_demo.xml',
    ],
}