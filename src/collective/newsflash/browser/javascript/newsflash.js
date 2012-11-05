(function($){  
    if ($('#edit-newsflashes')[0] !== undefined){
        $('#edit-newsflashes').prepOverlay(
            {
                subtype: 'ajax',
                formselector: '#form',
                noform: 'reload'
            }
        );
    }
})(jQuery);
