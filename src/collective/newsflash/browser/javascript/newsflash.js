window.onload = function() {
    if ($('a#manage-newsflashes')[0] !== undefined){
        $('a#manage-newsflashes').prepOverlay(
            {
                subtype: 'ajax',
                formselector: '#form',
                noform: 'reload'
            }
        );
    }
}
