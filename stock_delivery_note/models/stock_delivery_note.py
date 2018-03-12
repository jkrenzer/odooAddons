# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
from openerp.tools.translate import _

class stock_delivery_note(models.Model):
	_name = 'stock.delivery_note'
	_description = 'Delivery Note'
	_inherit = ['mail.thread', 'ir.needaction_mixin']
        _order = "name desc"

	@api.multi
	def _get_current_user(self):
        	return self.env.user

	@api.one
	@api.constrains('name')
	def _check_unique_constraint(self):
         if len(self.search([('name', '=', self.name)])) > 1:
             raise ValidationError("Name already exists and violates unique field constraint")

	STATE_SELECTION = [
                ('draft', 'Draft'),
                ('confirm', 'Confirm'),
                ('done', 'Done'),
                ('cancel', 'Cancelled')
        ]

	name = fields.Char(string="Name", default='/', required=True)
	notes = fields.Html(string="Additional Notes", help="Additional notes which should appear on the Delivery Note")
	pickings = fields.Many2many(string="Pickings", inverse_name="delivery_notes_ids", comodel_name="stock.picking", copy=True, readonly=False, help="Pickings documented by this delivery note")
        moves = fields.Many2many(string="Moves", compute="_compute_moves", comodel_name="stock.move", copy=False, store=False, readonly=True, help="All moves in the documented pickings")
        moves_count = fields.Integer(string="Number of moves", compute="_compute_moves_count", readonly=True)
        quants = fields.Many2many(string="Quants", compute="_compute_quants", search="_search_quants", comodel_name="stock.quant", copy=False, store=False, readonly=True, help="All quants moved or reserved in the documented pickings")
        quants_count = fields.Integer(string="Number of quants", compute="_compute_quants_count", readonly=True)
	date = fields.Datetime(string="Created", default=fields.Datetime.now, required=True)
	responsible = fields.Many2one(string="Responsible", comodel_name="res.users", required=True, default=_get_current_user)
	partner_id = fields.Many2one(string="Partner", comodel_name="res.partner", required=True)
	state = fields.Selection(STATE_SELECTION, 'Status', readonly=True, help="State of the delivery note. Draft marks a note being worked on, confirmed notes are filled appropiately. Notes marked as done have been sent or agreed upon by the recipient.", default='draft', select=True) 

        _sql_constraints = [('delivery_note_company_uniq', 'unique (name,company_id)', 'The Delivery Note reference number must be unique per company !')]


        @api.multi
        @api.depends('pickings','state')
        def _compute_moves(self):
            for rec in self:
                moves = self.env['stock.move'] #Get empty recordset
                for picking in rec.pickings:
                    moves += picking.move_lines
                rec.moves = moves
        
        @api.multi
        @api.depends('moves','pickings')
        def _compute_quants(self):
            for rec in self:
                quants = self.env['stock.quant'] #Get empty recordset
                for move in rec.moves:
                    quants += move.quant_ids or move.reserved_quant_ids
                rec.quants = quants

        @api.multi
        @api.depends('moves')
        def _compute_moves_count(self):
                for rec in self:
                        rec.moves_count = rec.moves and len(rec.moves) or 0
        @api.multi
        def view_moves(self):
                self.ensure_one() #Ensure we have only one object
                self._compute_moves()
                action = {
                        "type": "ir.actions.act_window",
                        "res_model": "stock.move",
                        "views": [[False, "tree"]],
                }
                if len(self.moves) > 1:
                        action['domain'] = "[('id','in',[" + ','.join(map(str, self.moves.ids)) + "])]"
                else:
                        action['views'] = [(False, 'form')]
                        action['res_id'] =  self.moves[0].id or False
                return action

        @api.multi
        @api.depends('quants')
        def _compute_quants_count(self):
                for rec in self:
                        rec.quants_count = rec.quants and len(rec.quants) or 0
        @api.multi
        def view_quants(self):
                self.ensure_one() #Ensure we have only one object
                self._compute_quants()
                action = {
                        "type": "ir.actions.act_window",
                        "res_model": "stock.quant",
                        "views": [[False, "tree"]],
                }
                if len(self.quants) > 1:
                        action['domain'] = "[('id','in',[" + ','.join(map(str, self.quants.ids)) + "])]"
                else:
                        action['views'] = [(False, 'form')]
                        action['res_id'] =  self.quants[0].id or False
                return action

        @api.multi
        def _search_quants(self, operator, value):
                quants = self.env['stock.quant'].search(['|',('product_id',operator,value),('lot_id',operator,value)])
                delivery_notes = self.env['stock.delivery_note']
                for quant in quants:
                        delivery_notes += quant.delivery_notes
                return [('id','in',delivery_notes.ids)]

	@api.model
	def create(self, vals):
		if vals.get('name', '/') == '/':
        		vals['name'] = self.env['ir.sequence'].get('stock.delivery_note')
        	if vals.get('responsible', '/') == '':
            		vals['responsible'] = self._get_current_user()
        	rec =  super(stock_delivery_note, self.with_context(mail_create_nolog=True)).create(vals)
                rec.message_post(body=_('Delivery Note <b>%s</b> created') % rec.name)
                return rec

	@api.multi
        def print_report(self):
                '''This function prints the delivery note'''
                for rec in self:
		    return rec.env['report'].render('report_delivery_note_view')

	#State functions

	@api.multi
	def _state_draft(self):
		'''This function marks the delivery note as draft'''
                for rec in self:
    		    if rec.state != 'draft':
			rec.write({'state': 'draft'})
			rec.message_post(body=_("Delivery Note marked as draft by %s") % rec.env.user.name, subtype="mail.mt_comment")
  		return True

        @api.multi
        def _state_confirm(self):
                '''This function marks the delivery note as confirmed'''
                for rec in self:
                    if rec.state != 'confirm':
                        rec.write({'state': 'confirm'})
                        rec.message_post(body=_("Delivery Note confirmed by %s") % rec.env.user.name, subtype="mail.mt_note")
                return True

        @api.multi
        def _state_done(self):
                '''This function marks the delivery note as done'''
                for rec in self:
                    if rec.state != 'done':
                        rec.write({'state': 'done'})
                        rec.message_post(body=_("Delivery Note marked done by %s") % rec.env.user.name, subtype="mail.mt_note")
                return True

        @api.multi
        def _state_cancel(self):
                '''This function marks the delivery note as cancelled'''
                for rec in self:
                    if rec.state != 'cancel':
                        rec.write({'state': 'cancel'})
                        rec.message_post(body=_("Delivery Note cancelled by %s") % rec.env.user.name, subtype="mail.mt_note")
                return True
