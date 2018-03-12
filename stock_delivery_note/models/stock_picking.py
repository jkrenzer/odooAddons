from openerp import models, api, fields, osv, exceptions
#from openerp.osv import fields, osv
from openerp.tools.translate import _

class StockPicking(models.Model):
        _inherit = 'stock.picking'
        _name = 'stock.picking'
	
	backorders_ids = fields.One2many('stock.picking', 'backorder_id', 'Backorders', readonly=True, copy=False)	
        delivery_notes_count = fields.Integer(string='Number of References', compute="_delivery_notes_count",  help="Number of Delivery Notes referencing this picking.", readonly=True, copy=False)
	delivery_notes_ids = fields.Many2many(comodel_name='stock.delivery_note', inverse_name='pickings', string='Delivery Notes', help="All DNs mentioning this picking")

        @api.multi
        @api.depends('delivery_notes_ids')
        def _delivery_notes_count(self):
                for rec in self:
                        rec.delivery_notes_count = rec.delivery_notes_ids and len(rec.delivery_notes_ids) or 0
        @api.multi
        def view_delivery_notes(self):
                self.ensure_one() #Ensure we have only one object
                action = {
                        "type": "ir.actions.act_window",
                        "res_model": "stock.delivery_note",
                        "views": [[False, "tree"]],
                }
                if len(self.delivery_notes_ids) > 1:
                        action['domain'] = "[('id','in',[" + ','.join(map(str, self.delivery_notes_ids.ids)) + "])]"
                else:
                        action['views'] = [(False, 'form')]
                        action['res_id'] =  self.delivery_notes_ids[0].id or False

                return action

        @api.multi
        def create_delivery_note(self):
                serialnumbers = self.env['ir.sequence']
                name = serialnumbers.next_by_code('stock.delivery_note')
                values = {
                         'name': name,
                }
                delivery_note = self.env['stock.delivery_note'].create(values)
                delivery_note.pickings = self
                delivery_note.partner_id = self[0].partner_id or self.env['res.partner']
                action = {
                          "type": "ir.actions.act_window",
                          "res_model": "stock.delivery_note",
                          "views": [[False, "form"]],
                          "res_id": delivery_note.id,
                }
                return action
