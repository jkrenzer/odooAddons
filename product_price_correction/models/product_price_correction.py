# -*- coding: utf-8 -*-

from openerp import models, fields, api

class CorrectionProductCostLine(models.Model):
    _name="product.price.correction"
    _description = 'Product Price Correction'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _order = "id desc"


    STATES = [
        ('draft','Draft'),
        ('undone','Undone'),
        ('done','Done'),
    ]

    MASTERS = [
        ('purchase', 'Purchase Line'),
        ('template_history', 'Template History'),
        ('product_history', 'Product History'),
        ('quant','Quant'),
    ]

    STRATEGIES = [
        ('nothing', 'Do nothing'),
        ('only_bigger', 'Change bigger than master'),
        ('only smaller' , 'Change smaller than master'),
        ('null' , 'Change zero prices only'),
        ('all' , 'Apply to all'),
    ]

    @api.multi
    def _default_purchase_line(self):
        for rec in self:
            if rec.move.purchase_line_id:
               return rec.move.purchase_line_id
            else:
               qualified_lines = rec.purchase_lines.filtered(lambda l: l.date_order <= rec.move.date)
               return qualified_lines[-1]

    @api.multi
    def _default_purchase_line(self):
        for rec in self:
            if rec.move.purchase_line_id:
               return rec.move.purchase_line_id
            else:
               qualified_lines = rec.purchase_lines.filtered(lambda l: l.date_order <= rec.move.date)
               return qualified_lines[-1]

    @api.multi
    def _default_product_template_historic_line(self):
        for rec in self:
            qualified_lines = rec.product_template_historic_line.filtered(lambda l: l.datetime <= rec.move.date)
            return qualified_lines[-1]

    @api.multi
    def _default_product_historic_line(self):
        for rec in self:
            qualified_lines = rec.product_historic_line.filtered(lambda l: l.datetime <= rec.move.date)
            return qualified_lines[-1]

    @api.multi
    def _default_product_historic_line(self):
        for rec in self:
            return rec.move.quant_ids[0]

    
    
    move = fields.Many2one(string="Stock Move", comodel_name="stock.move",required=True, help="Stock move whose costs should be corrected.")
    date = fields.Datetime(string="Movement Date", related="move.date", readonly=True, help="Date on which the movement which is to be revaluated was made.")
    product_template = fields.Many2one(string="Product Template", comodel_name="product.template",compute="_get_product_template", store=True, help="Product template involved in the move.")
    product = fields.Many2one(string="Product", comodel_name="product.product",compute="_get_product", store=True, help="Product involved in the move.")
    
    purchase_lines = fields.One2many(string="Purchase Lines", comodel_name="purchase.order.line", compute="_get_purchase_lines", store=False, help="Lines in purchase orders.")
    purchase_line = fields.Many2one(string="Applicable Purchase", comodel_name="purchase.order.line", default=_default_purchase_line, help="Applicable purchase line")
    purchase_line_cost = fields.Float(string="Price on Purchase", related="purchase_line.price_unit", store=True)
    old_purchase_line_cost = fields.Float(string="Old Purchase Cost", default=-1.0)
    
    product_template_history_lines = fields.One2many(string="Product Template History Prices", comodel_name="product.price.history", compute="_get_product_template_history_lines", store=False, help="Historic product template prices.")
    product_template_historic_line = fields.Many2one(string="Applicable Historic Template Price", comodel_name="product.price.history", default=_default_product_template_historic_line, help="Cost from product template price history")
    product_template_historic_cost = fields.Float(string="Historic Template Price", related="product_template_historic_line.cost", store=True)
    old_product_template_historic_cost = fields.Float(string="Old Template History Cost", default=-1.0)
  
    product_history_lines = fields.One2many(string="Product History Prices", comodel_name="product.price.history.product", compute="_get_product_history_lines", store=False, help="Historic product prices.")
    product_historic_line = fields.Many2one(string="Applicable Historic Price", comodel_name="product.price.history.product", default=_default_product_historic_line, help="Cost from product price history")
    product_historic_cost = fields.Float(string="Historic Product Price", related="product_historic_line.cost", store=True)
    old_product_historic_cost = fields.Float(string="Old Product History Cost", default=-1.0)
    
    quants = fields.One2many(string="Quants", comodel_name="stock.quant", compute="_get_quants", store=False, help="Quants")
    quant = fields.Many2one(string="Applicable Quant Cost", comodel_name="stock.quant", help="Applicable quant")
    quant_cost = fields.Float(string="Cost from Quant", related="quant.cost", store=True)
    old_quant_cost = fields.Float(string="Old Quant Cost", default=-1.0)

    change_purchase_line = fields.Boolean(String="Change Purchase Line")
    change_template_historic_line = fields.Boolean(String="Change Template History")
    change_historic_line = fields.Boolean(String="Change Product History")
    change_quant = fields.Boolean(String="Change Quant")

    master = fields.Selection(string="Master Cost Object", required=True, selection=MASTERS, help="Decide which object gives the master price to which the other ones are corrected.")
    master_cost = fields.Float(string="Correct Cost", compute="_get_master_cost", help="The cost to which the other objects will be corrected, if their checkbox is set.")
    strategy = fields.Selection(string="Strategy", default='nothing', selection=STRATEGIES, help="With which price should be applied as correct master to the other cost-variables?")
    state = fields.Selection(string="State", selection=STATES, help="State of correction")
    
    @api.multi
    @api.depends('master','product_template_historic_cost','product_historic_cost','quant_cost','purchase_line_cost')
    def _get_master_cost(self):
        for rec in self:
            if rec.master == 'template_history':
               rec.master_cost = product_template_historic_cost                  
            elif rec.master == 'product_history':
               rec.master_cost = product_historic_cost
            elif rec.master == 'quant':
               rec.master_cost = quant_cost
            else:
               rec.master_cost = purchase_line_cost

    @api.multi
    def action_apply(self):
        for rec in self:
           try:
               if rec.change_purchase_line:
                  rec.old_purchase_line_cost = rec.purchase_line.price_unit
                  rec.purchase_line.price_unit = rec.master_cost
               if rec.change_template_historic_line:
                  rec.old_product_template_historic_cost = rec.product_template_historic_line.cost
                  rec.product_template_historic_line.cost = rec.master_cost
               if change_historic_line:
                  rec.old_product_historic_cost = rec.product_historic_line.cost
                  rec.product_historic_line.cost = rec.master_cost
               if change_quant:
                  rec.old_quant_cost = rec.quant.cost
                  rec.quant.cost = rec.master_cost
           except:
               raise
           else:
               rec.state = 'done'

    @api.multi
    def action_undo(self):
        for rec in self:
            try:
                if rec.old_purchase_line_cost >= 0:
                   rec.purchase_line.price_unit = rec.old_purchase_line_cost
                if rec.old_product_template_historic_cost >= 0:
                   rec.product_template_historic_line.cost = rec.old_product_template_historic_cost
                if rec.old_product_historic_cost >= 0:
                   rec.product_historic_line.cost = rec.old_product_historic_cost
                if rec.old_quant_cost >= 0:
                   rec.quant.cost = rec.old_quant_cost
            except:
                raise
            else:
                rec.state = 'undone'

    @api.multi  
    @api.depends('move')
    def _get_product(self):
        for rec in self:
            rec.product = rec.move.product_id

    @api.multi  
    @api.depends('move')
    def _get_product_template(self):
        for rec in self:
            rec.product_template = rec.move.product_id.product_tmpl_id

    @api.multi  
    @api.depends('product')
    def _get_purchase_lines(self):
        for rec in self:
            product = rec.product
            domain = [
                ('product_id','=',product.id),
            ]
            order = "date_order asc, product_qty asc"
            rec.purchase_lines = self.env['purchase.order.line'].search(args=domain,order=order)

    @api.multi  
    @api.depends('product_template')
    def _get_product_template_history_lines(self):
        for rec in self:
            product_template = rec.product_template
            domain = [
                ('product_template_id','=',product_template.id),
            ]
            order = "datetime asc"
            rec.product_template_history_lines = self.env['product.price.history'].search(args=domain,order=order)

    @api.multi
    @api.depends('product_template')
    def _get_product_history_lines(self):
        for rec in self:
            product = rec.product
            domain = [
                ('product_id','=',product.id),
            ]
            order = "datetime asc"
            rec.product_history_lines = self.env['product.price.history.product'].search(args=domain,order=order)

    @api.multi  
    @api.depends('move')
    def _get_quants(self):
        for rec in self:
            move = rec.move
            rec.quants = move.quant_ids



            
