jQuery(document).ready(function($) {
    if ($('#edit-newsflashes')[0] !== undefined){
        $('.manage-newsflashes').prepOverlay(
            {
                subtype: 'ajax',
                formselector: '#form',
                noform: 'reload',
                filter: '#content'
            }
        );
    }
});
