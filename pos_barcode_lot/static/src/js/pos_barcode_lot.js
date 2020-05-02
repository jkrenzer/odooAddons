/*
    POS Payment With Sumup App
*/

odoo.define("pos_barcode_lot.pos_barcode_lot", function(require) { 
"use strict";

  var screens = require('point_of_sale.screens');
  var popups = require('point_of_sale.popups');
  var chrome = require("point_of_sale.chrome");
  var core = require('web.core');
  var _t = core._t;

  popups.include(
  {
    
      
    barcode_callbacks: {},

    show: function(options) {
      self = this;
      this._super(options);
      if (this.pos.barcode_reader)
      {
        var callbacks = Object.keys(this.barcode_callbacks)
        if(callbacks.length > 0) {
          console.log("Adding barcode-callback(s) for popup.");
          callbacks.forEach( function (type) {
            self.barcode_callbacks[type] = _.bind(self.barcode_callbacks[type], self);
          });
          this.pos.barcode_reader.set_action_callback(this.barcode_callbacks);
        }
      }
      else 
      {
        console.log("No barcode-reader, not adding barcode-callback(s) for popup.");
      }
    },

    close: function() 
    {
      if (this.pos.barcode_reader) 
      {
        this.pos.barcode_reader.reset_action_callbacks(); 
      }
      this._super();
    } 
  });
    
  screens.ScreenWidget.include(
  { 
    show: function() 
    { 
      this._super(); 
      this.pos.barcode_reader.set_action_callback(
      { 
        'lot': function(){ console.log("LOT SCANNED");} 
      });
      var packlotline = this.gui.popup_instances.packlotline;
      packlotline.barcode_callbacks = 
      {
        'lot': function(code)
          {
            console.log("Sanned lot/serial " + code.code + " into the popup.");
            this.$('.packlot-line-input').val(code.code);
            this.click_confirm();
          },
        'product': function(code)
          {
            var self = this;
            this.gui.show_popup('error', {
              'title': _t('Product Scanned'),
              'body': _t('The scanned barcode \"' + code.code + '\" is a product-barcode. Please scan a valid barcode for a lot- or serial-number.'),
              cancel: function() 
               {
                 this.gui.show_popup('packlotline', self.options);
               }
            });
          },
        'discount': function(code)
          {
            var self = this;
            this.gui.show_popup('error', {
              'title': _t('Discount Scanned'),
              'body': _t('The scanned barcode \"' + code.code + '\" is a discount-barcode. Please scan a valid barcode for a lot- or serial-number.'),
              cancel: function()  
               {
                 this.gui.show_popup('packlotline', self.options);
               }
            });
          },
        'prize': function(code)
          {
            var self = this;
            this.gui.show_popup('error', {
              'title': _t('Prize Scanned'),
              'body': _t('The scanned barcode \"' + code.code + '\" is a prize-barcode. Please scan a valid barcode for a lot- or serial-number.'),
              cancel: function()  
               {
                 this.gui.show_popup('packlotline', self.options);
               }
            });
          },
        'weight': function(code)
          {
            var self = this;
            this.gui.show_popup('error', {
              'title': _t('Weight Scanned'),
              'body': _t('The scanned barcode \"' + code.code + '\" is a weight-barcode. Please scan a valid barcode for a lot- or serial-number.'),
              cancel: function()  
               {
                 this.gui.show_popup('packlotline', self.options);
               }
            });
          },
        'cashier': function(code)
          {
            var self = this;
            this.gui.show_popup('error', {
              'title': _t('Cashier Change Not Allowed'),
              'body': _t('Please scan a valid barcode for a lot- or serial-number or close this popup to perform a change of cashier.'),
              cancel: function()  
               {
                 this.gui.show_popup('packlotline', self.options);
               }
            });
          },
        'error': function(code)
          {
            var self = this;
            this.gui.show_popup('error', {
              'title': _t('Invalid Barcode'),
              'body': _t('The scanned barcode \"' + code.code + '\" is invalid. Please scan a valid barcode for a lot- or serial-number.'),
              cancel: function()  
               {
                 this.gui.show_popup('packlotline', self.options);
               }
            });
          } 
      }  
    }
  }); 
});
