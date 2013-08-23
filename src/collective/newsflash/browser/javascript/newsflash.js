jQuery(document).ready(function($) {
	$('.manage-newsflashes').prepOverlay(
	    {
	        subtype: 'ajax',
	        formselector: '#form',
	        noform: 'reload',
	        filter: '#content'
	    }
	);
});
