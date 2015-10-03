(function () {
   
    'use strict';
    console.debug("[apiform_file] Custom JS for apiform_panel is loading...");
    var website = openerp.website,
    qweb = openerp.qweb;
    website.add_template_file('/website_apiform/static/src/xml/website.magenes.xml');
   
    website.cargaImagen = openerp.Widget.extend({
        template: 'cargaImagen',
        placeholder: "/website_apiform/static/src/images/3d_user.png",
        init: function (element) {
            this._super(element);
            var self = this;
            var url;
            if( ! window.FileReader ) {
                console.log('no soprta')
                    return; // No soportado
                }
            element.each(function(){
                if(this.type=='file'){
                    var defaults = self.val_defaults(this);
                    var cont=$(qweb.render('cargaImagen',{'defaults':defaults}));
                    $(this).after(cont);
                    self.settings = $.extend({}, defaults);
                    self.do_render(self,this);
                    $(this).hide();
                    }
               
                })
            },
        do_render: function(data,file) {
            $('.oe_form_binary_file_edit').click(function(){
                
                    
                 $(file).click();
                  $(file).change(function() {
                      data.readImage(this);
                  });
                     });
            $('.oe_form_binary_file_clear').click(function(){
                 $(file).attr({ value: '' });
                 var id=$(file).attr('name')
                 $('#'+id).attr( "src", data.placeholder);
                })
            
            },
        readImage: function(input) {
            console.log(input.name);
            if ( input.files && input.files[0] ) {
                var FR= new FileReader();
                FR.onload = function(e) {
                    var id=input.name;
                     $('#'+id).attr( "src", e.target.result );
                     $('input[name=hidden_'+id+']').val(e.target.result);
                };       
                FR.readAsDataURL( input.files[0] );
                }
            },
        val_defaults:function(input){
            var height= $(input).attr('height');
            if (!height){
               height= '128px';
                } 
            var width= $(input).attr('width');
            if (!width){
               width= '128px';
                } 
            var src= $(input).attr('src');
            if (!src){
               src= this.placeholder;
                } 
            var id= $(input).attr('name');
            if (!id){
               id= 'idname';
                }
            var namehidden='hidden_'+id;
            return {'height':height,'width':width,'src':src,'id':id,'namehidden':namehidden}
            }
        });
        
        $(document).ready(function() {
            var $element = $('input[widget=image]');
            var content = new website.cargaImagen($element);
        $(".ejemplo_img").mouseenter(function() {  
            $(".ejemplo_img_cont", this).stop().animate({ top:'70px' },{ queue:false, duration:300 });  
            });  
            $(".ejemplo_img").mouseleave(function() {  
                $(".ejemplo_img_cont", this).stop().animate({ top:'128px' },{ queue:false, duration:300 });  
        });
    });
        console.debug("[apiform_file] Custom JS for apiform_panel is loading...");

})();
//~ 
//~ (function () {
   //~ 
    //~ 'use strict';
    //~ console.debug("[apiform_file] Custom JS for apiform_panel is loading...");
    //~ var website = openerp.website,
    //~ qweb = openerp.qweb;
    //~ website.add_template_file('/website_apiform/static/src/xml/website_apiform.amagenes.xml');
    //~ website.carga_imagen = openerp.Widget.extend({
        //~ template: 'website.cargaImagen',
        //~ init: function(options) {
            //~ var self = this ;
            //~ self.discus_identifier;
            //~ var defaults = {
                //~ position: 'right',
                //~ post_id: $('.js_imagen').attr('name'),
                //~ content : false,
                //~ public_user: false,
            //~ };
            //~ self.settings = $.extend({}, defaults, options);
            //~ self.do_render(self);
        //~ },
        //~ do_render: function(data) {
            //~ var elt = $('.ejemplo_img');
            //~ console.log(elt);
            //~ console.log(elt);
            //~ elt.append(qweb.render("website.cargaImagen"));
            //~ },
        //~ });
        //~ new website.carga_imagen();
 //~ console.debug("[apiform_file] Custom JS for apiform_panel is loading...");
//~ 
//~ })();


//~ $(document).ready(function(){ 
    //~ 'use strict';
    //~ console.debug("[apiform_panel] Custom JS for apiform_panel is loading...");
        //~ var instance = openerp;
       //~ 
         //~ $(".ejemplo_img").mouseenter(function() {  
            //~ $(".ejemplo_img_cont", this).stop().animate({ top:'70px' },{ queue:false, duration:300 });  
            //~ });  
            //~ $(".ejemplo_img").mouseleave(function() {  
                //~ $(".ejemplo_img_cont", this).stop().animate({ top:'128px' },{ queue:false, duration:300 });  
        //~ });
        //~ $("#file-1").fileinput({
		//~ showUpload: false,
        //~ showCaption: false,
        //~ showPreview:false,
		//~ browseClass: "btn btn-primary btn-lg",
		//~ fileType: "any",
        //~ browseLabel:'Seleccionar',
	//~ });
    //~ console.debug("[apiform_panel] Custom JS for apiform_panel loaded!");
    //~ });
