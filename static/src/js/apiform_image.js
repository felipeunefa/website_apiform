(function () {
   
    'use strict';
    console.debug("[apiform_file] Custom JS for apiform_panel is loading...");
     var MAIN_TEMPLATE = '<div class="ejemplo_img" >\n' +
        '<img\n' +
                'css="story-small"\n' +
                'src="defaults.src"\n' +
                'height="defaults.height"\n' +
                'width="defaults.width"\n' +
                'id="defaults.id" />\n' +
        '   <input type="hidden" name="defaults.namehidden" value="" />\n' +
        '   <div class="ejemplo_img_cont" style="top: 128px;">\n' +
        '       <div class="oe_form_field_image_controls oe_edit_only">\n' +
        '       <i class="fa fa-pencil fa-1g pull-left col-md-offset-1 oe_form_binary_file_edit" id="defaults.id_file" title="Edit" />\n' +
        '       <i class="fa fa-trash-o fa-1g col-md-offset-5 oe_form_binary_file_clear"  id="defaults.id" title="Clear" />\n' +
        '       </div>\n' +
        '   </div>\n' +
        '</div>';
       
         var cont=0;
    var website = openerp.website,
    qweb = openerp.qweb;
   
    website.add_template_file('/website_apiform/static/src/xml/website.magenes.xml');
    website.cargaImagen = openerp.Widget.extend({
        template: 'cargaImagen',
        placeholder: "/website_apiform/static/src/images/3d_user.png",
        init: function (element) {
            //~ this._super(element);
            var self = this;
            var url;
            if( ! window.FileReader ) {
                console.log('no soprta')
                alert('ERROR Disculpe: Usted debe actualizar su navegado \
                        para que el sistema funcione....');
                    return; // No soportado
                }
            element.each(function(){
                if(this.type=='file'){
                    var defaults = self.val_defaults(this);
                    console.log(defaults.src)
                    MAIN_TEMPLATE=MAIN_TEMPLATE.replace('defaults.src',defaults.src).
                            replace('defaults.height', defaults.height).
                            replace('defaults.width', defaults.width).
                            replace('defaults.id', defaults.id).
                            replace('defaults.namehidden', defaults.namehidden).
                            replace('defaults.id_file', defaults.id_file)
                    $(this).after(MAIN_TEMPLATE);
                    self.settings = $.extend({}, defaults);
                    self.do_render(self,this);
                    $(this).hide();
                    }
               
                });
            },
        do_render: function(self,file) {
            $('.oe_form_binary_file_edit').click(function(e){
                console.log(file.id);
                  if(file.id==$(this).attr('id')){
                  $('#'+file.id).click();
                  $('#'+file.id).change(function() {
                      self.readImage(this,self);
                  });
                  }
                 
                     });
            $('.oe_form_binary_file_clear').click(function(){
                 $(file).attr({ value: '' });
                 var id=$(file).attr('name')
                 $('#'+id).attr( "src", self.placeholder);
                })
            
            },
        readImage: function(input,self) {
            if ( input.files && input.files[0] ) {
                var FR= new FileReader();
                FR.onload = function(e) {
                    var id=input.name;
                    var base64=e.target.result;
                    var defaults=self.val_defaults(input)
                    base64=base64.split(',')
                    var width=defaults.width.replace('px','');
                    var height=defaults.height.replace('px','');
                    width=width.replace('%','');
                    height=height.replace('%','');
                    openerp.jsonRpc("/website_apiform/apiform_image/base64_size", 'call', {
                        'image_base64': base64[1],
                        'width': width,
                        'height': height}).then(function(res){
                             $('#'+id).attr( "src", res[0].base64 );
                             $('input[name=hidden_'+id+']').val(base64);
                            });
                     
                };       
                FR.readAsDataURL(input.files[0]);
                }
            },
        val_defaults:function(input){
            var height= $(input).attr('height');
            if (!height){
               height= '128px';
                } 
            var id_file= $(input).attr('id');
            if (!id_file){
               id_file= 'id_file'+cont;
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
            return {'height':height,
                    'width':width,
                    'src':src,
                    'id':id,
                    'namehidden':namehidden,
                    'id_file':id_file
                    }
            },
        
        
        });
        console.debug("[apiform_file] Custom JS for apiform_panel is loading...");

})();
