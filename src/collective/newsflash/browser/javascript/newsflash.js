jQuery(document).ready(function($) {  
    if ($('#edit-newsflashes')[0] !== undefined){
        $('.manage-newsflashes').prepOverlay({
                subtype: 'ajax',
                formselector: '#form',
                noform: 'reload',
                config: {
                    onLoad : function (e) {
                        if(typeof init_rte == 'function') {
                            init_rte();
                        }
                        
                    }
                },
                afterpost: function(response, data_parent) {
                    if(typeof init_rte == 'function') {
                        init_rte();
                    }
                    return true;
                }
            });
    }
});
