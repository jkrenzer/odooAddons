# -*- coding: utf-8 -*-

from openerp import models, fields, api

class quality_control_report_print_wizard(models.TransientModel):
     _name = 'qc.report.printwizard'

     @api.multi
     def _default_report(self):
        return self.env['qc.report'].browse(self._context.get('active_id'))


     @api.multi
     def print_report(self):
         '''
         Prints the report with the chosen template
         '''
         context = {'lang': self.language.code or 'en_US'}
         filename = "%s_%s" % (self.template.name, self.language.code)
         datas = {
           'ids': [self.report.id],
           'model': 'qc.report',
         }
         return {
           'type' : 'ir.actions.report.xml',
           'report_name' : self.template.report_name,
           'datas' : datas,
           'attachment_use': False,
           'name': filename,
           'attachment': filename,
           'context': context,
         }
     @api.multi
     def _get_language(self):
         user_lang_code = self.env.user.lang
         user_lang = user_lang_code and self.env['res.lang'].search([('code','=',user_lang_code)], limit=1) or self.env['res.lang'].search([('code','=','en_US')], limit=1)
         return user_lang

     report = fields.Many2one(comodel_name="qc.report", string="Report", default=_default_report, required=True)
     template = fields.Many2one(comodel_name="ir.actions.report.xml", string="Report Template", domain=[('model','=','qc.report')], required=True)
     language = fields.Many2one(comodel_name="res.lang", String="Printing Language", default=_get_language, required=True)

class quality_control_report_text_template(models.Model):
     _name = 'qc.report_text_template'
     
     name = fields.Char(string="Name", required=True)
     text = fields.Html(string="Description", translate=True, required=True)

class quality_control_report(models.Model):
     _name = 'qc.report'

     @api.multi
     def _get_current_user(self):
           return self.env.user.id


     name = fields.Char(string="Name", default='/', required=True)
     inspections = fields.Many2many(string="Inspections", comodel_name="qc.inspection", required=True)
     description = fields.Html(string="Description", translate=True)
     description_template = fields.Many2one(string="Use Template", comodel_name="qc.report_text_template")
     conclusion = fields.Html(string="Conclusion", translate=True)
     conclusion_template = fields.Many2one(string="Use Template", comodel_name="qc.report_text_template")
     date_written = fields.Datetime(string="Created", default=fields.Datetime.now, required=True)
     date_approved = fields.Datetime(string="Date approved")
     notes = fields.Text(string="Internal Notes")
     approver = fields.Many2one(string="Approver", comodel_name="res.users")
     writer = fields.Many2one(string="Responsible", comodel_name="res.users", default=_get_current_user)
     products = fields.Many2many(string="Products", comodel_name="product.product", compute="_get_products")
     lots = fields.Many2many(string="Serial/Lot-numbers", comodel_name="stock.production.lot", compute="_get_lots")
     productions = fields.Many2many(string="Productions", comodel_name="mrp.production", compute="_get_productions")
     pickings = fields.Many2many(string="Pickings", comodel_name="stock.picking", compute="_get_pickings")
     state = fields.Selection(
       [('draft', 'Draft'),
       ('confirm', 'Confirmed'),
       ('approve', 'Approved'),
       ('cancel', 'Cancelled')], string="State", readonly=True, default='draft')

     @api.multi
     @api.depends('inspections.lot')
     def _get_lots(self):
         for report in self:
             lot_set = set()
             for inspection in report.inspections:
                 if inspection.lot:
                    lot_set.add(inspection.lot.id)
             report.lots = list(lot_set)

     @api.multi
     @api.depends('inspections.production')
     def _get_productions(self):
         for report in self:
             prod_set = set()
             for inspection in report.inspections:
                 if inspection.production:
                    prod_set.add(inspection.production.id)
             report.productions = list(prod_set)

     @api.multi
     @api.depends('inspections.picking')
     def _get_pickings(self):
         for report in self:
             pick_set = set()
             for inspection in report.inspections:
                 if inspection.picking:
                    pick_set.add(inspection.picking.id)
             report.pickings = list(pick_set)

     @api.multi
     @api.depends('inspections.product')
     def _get_products(self):
         for report in self:
             prod_set = set()
             for inspection in report.inspections:
                 if inspection.product:
                    prod_set.add(inspection.product.id)
             report.products = list(prod_set)

     @api.one
     @api.constrains('name')
     def _check_unique_constraint(self):
         if len(self.search([('name', '=', self.name)])) > 1:
             raise ValidationError("Name already exists and violates unique field constraint")

#     @api.model
#     def load_template(self, field_name, template_name):
#         for report in self:
#             _field = getattr(report,field_name)
#             if _field:
#                #TODO
        

     @api.model
     def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].get('qc.report')
        if vals.get('writer', '/') == '':
            vals['writer'] = self._get_current_user()
        return super(quality_control_report, self).create(vals)

     @api.multi
     def print_report(self):
         '''
         Opens a wizard to print the report
         '''
         return quality_control_report_print_wizard()

     @api.multi
     def action_approve(self):
        '''
        Marks this report approved
        '''
        for report in self:
          report.state = 'approve'
          report.date_approved = fields.Datetime.now()
          report.approver = report._get_current_user()
          return True

     @api.multi
     def action_draft(self):
        '''
        Marks this report as draft
        '''
        for report in self:
          report.state = 'draft'
          return True

     @api.multi
     def action_confirm(self):
        '''
        Marks this report confirmed
        '''
        for report in self:
          report.state = 'confirm'
          if not report.writer:
            report.writer = report._get_current_user()
          return True

     @api.multi
     def action_cancel(self):
        '''
        Marks this report as cancelled
        '''
        for report in self:
          report.state = 'cancel'
          return True


