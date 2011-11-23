window.onload = function() {
    $('a#add-newsflash').prepOverlay(
        {
            subtype: 'ajax',
            formselector: '#form',
            noform: 'close'
        }
    );
}