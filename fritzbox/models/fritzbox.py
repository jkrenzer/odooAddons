# -*- coding: utf-8 -*-

from openerp import models, api, fields, osv, exceptions
from openerp.tools.translate import _

from fritzconnection.fritzconnection import (FritzXmlParser, FritzConnection)

class FritzBox(models.Model)
    _name = 'fritzbox'
    
    company_id = fields.Many2one(comodel_name='res.company', string='Company', readonly=false, copy=False)
    name = fields.Char(string='Name', copy=True, help='Name of FritzBox')
    address = field.Char(string='Address', copy=True, help='IP or DNS-Name of FritzBox', default='169.254.1.1')
    port = field.Integer(string='Port', copy=True, help='Portnumber of FritzBox Remote Access Service', default='49000')
    user = field.Char(string='User', copy=True, help='Username used to login to FritzBox', default='dslf-config')
    password = field.Char(string='Password', copy=True, help='Password used to login to FritzBox', default='')
    model = field.Char(string='Model', copy=False, help='Model of FritzBox', default='', readonly=True)

    def get_connection()
        return FritzConnection(address=self.address, port=self.port, user=self.user, password=self.password)
        
    def call_action(serviceName, actionName, **kwargs)
        return get_connection.call_action(serviceName,actionName,kwargs)
    
    def test_connection()
        modelName = get_connection().modelname
        if modelName:
            self.write({model: modelName})
        else:
            self.write({model: ''})
    
#        fxp = FritzXmlParser(address=None,port=None,filename=result['NewPhonebookURL'])
#        nodes = fxp.root.iterfind('.//contact')
#        for node in nodes:
#            print('#%s %s: %s' % (node.find('uniqueid').text, node.find('person/realName').text, node.find('telephony/number').text))
