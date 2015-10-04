$(document).ready(function() {

        var element = $('input[widget=apiform_image]');
        if (element.length>0){
            element.each(function(){
                $(this).hide();
                });
         new openerp.website.cargaImagen(element);
        }
        $(".ejemplo_img").mouseenter(function() {  
            $(".ejemplo_img_cont", this).stop().animate({ top:'70px' },{ queue:false, duration:300 });  
            });  
            $(".ejemplo_img").mouseleave(function() {  
                $(".ejemplo_img_cont", this).stop().animate({ top:'128px' },{ queue:false, duration:300 });  
        });


});
