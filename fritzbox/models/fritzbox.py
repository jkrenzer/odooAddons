# -*- coding: utf-8 -*-

from openerp import models, api, fields, osv, exceptions
from openerp.tools.translate import _

import logging
_logger = logging.getLogger(__name__)

from fritzconnection import FritzConnection, FRITZ_IGD_DESC_FILE, FRITZ_TR64_DESC_FILE, FRITZ_IP_ADDRESS, FRITZ_TCP_PORT, FRITZ_USERNAME

class FritzBox(models.Model):
    _name = 'fritzbox.fritzbox'
    
    company_id = fields.Many2one(comodel_name='res.company', string='Company', readonly=False, copy=False)
    name = fields.Char(string='Name', copy=True, help='Name of FritzBox')
    address = fields.Char(string='Address', copy=True, help='IP or DNS-Name of FritzBox', default='169.254.1.1')
    port = fields.Integer(string='Port', copy=True, help='Portnumber of FritzBox Remote Access Service', default='49000')
    user = fields.Char(string='User', copy=True, help='Username used to login to FritzBox', default='dslf-config')
    password = fields.Char(string='Password', copy=True, help='Password used to login to FritzBox', default='')
    model = fields.Char(string='Model', copy=False, help='Model of FritzBox', default='', readonly=True)
    services = fields.Text(string="JSON Service description", help="Description of all services in JSON", copy=False, default='', readonly=True)
    initialized = fields.Boolean(compute='is_initialized')
    
    @api.one
    def get_connection(self):
        if self.services == '':
            return FritzConnection(address=self.address, port=self.port, user=self.user, password=self.password, protocol='https', path='tr064/', descfiles=['tr64desc.xml'])
        else:
            return FritzConnection(address=self.address, port=self.port, user=self.user, password=self.password, protocol='https', path='tr064/', descfiles=['tr64desc.xml'], services_jason=self.services)

    @api.one    
    def call_action(self, serviceName, actionName, **kwargs):
        return self.get_connection.call_action(serviceName,actionName,kwargs)

    @api.one
    @api.depends('services')
    def is_initialized(self):
        if services != '':
            self.initialized = True
        else:
            self.initialized = False

    @api.one
    def init_connection(self):
        connection = self.get_connection()
        modelName = connection[0].get_modelname()
        services = connection[0].get_services_json()
        if modelName:
            self.write({'model': modelName,
                        'services': services})
        else:
            self.write({'model': 'Unknown'})

    @api.multi
    def action_init_connection(self, args):
        self.write({'model': '',
                    'services': ''})
        self.init_connection()
    
#        fxp = FritzXmlParser(address=None,port=None,filename=result['NewPhonebookURL'])
#        nodes = fxp.root.iterfind('.//contact')
#        for node in nodes:
#            print('#%s %s: %s' % (node.find('uniqueid').text, node.find('person/realName').text, node.find('telephony/number').text))
