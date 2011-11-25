window.onload = function() {
    $('a#manage-newsflashes').prepOverlay(
        {
            subtype: 'ajax',
            formselector: '#form',
            noform: 'reload'
        }
    );
}