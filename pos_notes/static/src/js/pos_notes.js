openerp.pos_notes = function(instance){
    var module = instance.point_of_sale;
    var QWeb = instance.web.qweb;
    var _t = instance.web._t;
    
	module.PaymentScreenWidget.include({
        show: function(){
            this._super();
			this.update_input();
		},
        update_input: function(){
            var self = this;
            var contents = this.$('.pos-order-note-div');
            contents.find('.pos-order-note').on('keyup',function(event){
					self.pos.get('selectedOrder').set_note(this.value);
                }); 
        },
	});
	
    module.Order = module.Order.extend({
        initialize: function(attributes){
            Backbone.Model.prototype.initialize.apply(this, arguments);
            this.pos = attributes.pos; 
            this.sequence_number = this.pos.pos_session.sequence_number++;
            this.uid =     this.generateUniqueId();
            this.set({
                creationDate:   new Date(),
                orderLines:     new module.OrderlineCollection(),
                paymentLines:   new module.PaymentlineCollection(),
                name:           _t("Order ") + this.uid,
                client:         null,
				note:          "",
            });
            this.selected_orderline   = undefined;
            this.selected_paymentline = undefined;
            this.screen_data = {};  // see ScreenSelector
            this.receipt_type = 'receipt';  // 'receipt' || 'invoice'
            this.temporary = attributes.temporary || false;
            return this;
        },
		
        export_as_JSON: function() {
            var orderLines, paymentLines;
            orderLines = [];
            (this.get('orderLines')).each(_.bind( function(item) {
                return orderLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            paymentLines = [];
            (this.get('paymentLines')).each(_.bind( function(item) {
                return paymentLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            return {
                name: this.getName(),
                amount_paid: this.getPaidTotal(),
                amount_total: this.getTotalTaxIncluded(),
                amount_tax: this.getTax(),
                amount_return: this.getChange(),
                lines: orderLines,
                statement_ids: paymentLines,
                pos_session_id: this.pos.pos_session.id,
                partner_id: this.get_client() ? this.get_client().id : false,
                user_id: this.pos.cashier ? this.pos.cashier.id : this.pos.user.id,
                uid: this.uid,
                sequence_number: this.sequence_number,
				note: this.get_note(),
            };
        },
		get_note: function(){
			return this.get('note');
		},
		set_note: function(note){
			this.set('note', note);
		},   
    });
}