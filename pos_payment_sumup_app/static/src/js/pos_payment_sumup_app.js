/*
    POS Payment With Sumup App
*/

odoo.define('pos_payment_sumup_app.pos_payment_sumup_app', function (require) {
"use strict";

    var screens = require('point_of_sale.screens');
    var devices = require('point_of_sale.devices');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var gui = require("point_of_sale.gui")
    var _t = core._t;
    var QWeb = core.qweb;
    
    function get_next_sumup_payment_line(lines) {
        for ( var i = 0; i < lines.length; i++ ) {
            console.log("DEBUG: Payment-mode:" + lines[i].cashregister.journal.payment_mode);
            if (lines[i].cashregister.journal.payment_mode == "sumup_app_url" && !lines[i].sumup_app_payment_success) {
                return lines[i];
            }
        }
        return false;
    }

    models.load_fields('account.journal','payment_mode');

    models.Paymentline.sumup_app_payment_success = false;

    screens.PaymentScreenWidget.include({

        validate_order: function(force_validation) {
            var self = this;
            var lines = this.pos.get_order().get_paymentlines();
            if (get_next_sumup_payment_line(lines) === false) {
                self._super(force_validation);
            }
            else {
                    this.gui.show_popup('confirm', {
                        'title': _t('Open Sumup Payments'),
                        'body': _t('There seem to be open Sumup transactions! Are you sure the payments were already sucessfully processed? If you are in doubt, please press abort.'),
                        confirm: function() {
                            self._super(force_validation);
                        }
                    });
            }
        },
 
        pos_payment_sumup_app_start: function(currency_ios, currency_decimals){
            var line;
            var lines = this.pos.get_order().get_paymentlines();
            console.log("DEBUG: Found " + lines.length + " payment-lines.");
            line = get_next_sumup_payment_line(lines);
            if (typeof line === 'undefined') {
                this.gui.show_popup('error', {
                'title': _t('No Sumup Payment'),
                'body': _t('There was no payment found in the list which is associated with a payment-type supporting Sumup transactions. Please choose an appropriate payment-type and try again.')
                }
               );
            }
            else {
                //TODO Read values from pos.config
                var title = line.order.name;
                var affiliate_key = this.pos.config.sumup_app_affiliate_key;
                var app_id = this.pos.config.sumup_app_application_identifier;
                var callback = this.pos.config.sumup_app_callback;
                var url = 'sumupmerchant://pay/1.0?total=' + line.get_amount() + '&currency=' + this.pos.currency.name  + '&affiliate-key=' + affiliate_key + '&app-id=' + app_id + '&title=' + title + '&callback=' + callback;
                window.open(url);
                this.gui.show_popup('confirm',{
                    'title': _t('Verify External Payment Success'),
                    'body':  _t('Please confirm the success of payment in the Sumup app or abort.'),
                    confirm: function(){
                        line.sumup_app_payment_success = true;
                    },
}               );
            }
        },

        renderElement: function(){
            this._super.apply(this, arguments);
            var self  = this;
            this.$('.js_payment_sumup_app_start').click(function(event){
            console.log(event.target);
            self.pos_payment_sumup_app_start(self.pos.currency.name, self.pos.currency.decimals);
            });
        }

    });
});
