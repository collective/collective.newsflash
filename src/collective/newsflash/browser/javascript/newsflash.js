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
                    //XXX CUSTOM INIT_RTE                    
                    $.each(response.find(".rte-widget"), function(){
                        var $this = $(this);
                        $(this).rte({
                            content_css_url: "++resource++collective.z3cform.widgets/rte.css",
                            media_url: "++resource++collective.z3cform.widgets/rte/",
                            iframe_height: $this.data('iframe_height'),
                            format_block: $this.data('format_block'),
                            bold: $this.data('bold'),
                            italic: $this.data('italic'),
                            unordered_list: $this.data('unordered_list'),
                            link: $this.data('link'),
                            image: $this.data('image'),
                            allow_disable: $this.data('allow_disable')
                        });
                    });


                    return true;
                }
            });
        $('body').delegate('#add-newsflashes', 'click', function(e){
            e.preventDefault();
            $('#edit-newsflashes').click();
        });
    }
});
