odoo.define('portal_orders.portal_quotation', function(require) {
	"use strict";
	var rpc = require('web.rpc');

	$(document).ready(function() {

		 
    
		$(".tag_ids").chosen({
				enable_search_threshold: 10
				
			});
			
		

$('#tag_ids').change (function () {
		var UserIds = $('#tag_ids').val();
		/*var ser_var=document.getElementById('tax_empty').value;
		ser_var = UserIds */
		 document.getElementById('tax_empty').value = UserIds
		console.log("assign",document.getElementById('tax_empty').value)
    });
		$('#add-line-btn').click(function() {

			$(".children_tax_ids").chosen({
				enable_search_threshold: 10
			});

		});
		
		
		$('.given_cust').change (function () {
		 var partner = document.getElementById("cust").value;
		 var crmId = ''
         if (partner != ' ')
        	 return rpc.query({
		            model: "sale.order",
		            method: 'pricce_list_change', 
		            args: [crmId,partner], 
		            context: {},
		        }).then(function (data) {
					
					const price = document.getElementById("price")
					price.value = data
            });
			});
	});
});