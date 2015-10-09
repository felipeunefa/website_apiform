(function () {
   
    'use strict';
    console.debug("[apiform_file] Custom JS for apiform_panel is loading...");

    var cont=0;
    var website = openerp.website,
    qweb = openerp.qweb;
   
    website.add_template_file('/website_apiform/static/src/xml/apiform_imagen.xml');
    website.cargaImagen = openerp.Widget.extend({
        template: 'cargaImagen',
        base646:'lolol',
        placeholder: "/website_apiform/static/src/images/3d_user.png",
        MAIN_TEMPLATE : '<a href="#"><div class="ejemplo_img" >\n' +
        '<img\n' +
                'css="story-small"\n' +
                'src="defaults.src"\n' +
                'height="defaults.height"\n' +
                'width="defaults.width"\n' +
                'id="defaults.id" />\n' +
        '   <div class="ejemplo_img_cont" style="top: defaults.top ; height: _height;width:_width ">\n' +
        '       <div class="oe_form_field_image_controls oe_edit_only">\n' +
        '       <i class="fa fa-pencil fa-1g pull-left col-md-offset-1 oe_form_binary_file_edit" id="defaults.id_file" title="Edit" />\n' +
        '       <i class="fa fa-trash-o fa-1g col-md-offset-5 oe_form_binary_file_clear"  id="defaults.id" title="Clear" />\n' +
        '       </div>\n' +
        '   </div>\n' +
        '</div></a>',
        start: function (input_file) {
            console.log(input_file.type);
            var self = this;
            if( ! window.FileReader ) {
                console.log('no soprta')
                alert('ERROR Disculpe: Usted debe actualizar su navegado \
                        para que el sistema funcione....');
                    return; // No soportado
                }
                if(input_file.type=='file'){
                    var defaults = self.val_defaults(input_file);
                    var TEMPLATE;
                    try {
                        TEMPLATE=qweb.render("apiform_imagen", {'defaults': defaults});
                        
                        }catch(e){
                    TEMPLATE=self.MAIN_TEMPLATE.replace('defaults.src',defaults.src).
                            replace('defaults.height', defaults.height).
                            replace('_height', defaults.height).
                            replace('defaults.top', defaults.height).
                            replace('defaults.width', defaults.width).
                            replace('_width', defaults.width).
                            replace('defaults.id', defaults.id).
                            replace('defaults.namehidden', defaults.namehidden).
                            replace('defaults.id_file', defaults.id_file)
                        }
                    $(input_file).after(TEMPLATE);
                    self.settings = $.extend({}, defaults);
                    self.do_render(self,input_file);
                    $(input_file).hide();
                    }
            },
        do_render: function(self,input_file) {
            $(".ejemplo_img").mouseenter(function() {
            var height=$(this).children('img').attr('height');
            height=height.replace('px','');
            height=height.replace('%','');
            var _top=(54*parseInt(height))/100
            console.log(_top);
            $(".ejemplo_img_cont", this).stop().animate({ top:_top+'px' },{ queue:false, duration:300 });  
            });  
            $(".ejemplo_img").mouseleave(function() {
                  var height=$(this).children('img').attr('height');
                  var width=$(this).children('img').attr('width');
                $(".ejemplo_img_cont", this).stop().animate({ top:height },{ queue:false, duration:300 });  
            });
            $('.oe_form_binary_file_edit').click(function(e){
                  if(input_file.id==$(this).attr('id')){
                  $('#'+input_file.id).click();
                  $('#'+input_file.id).change(function() {
                      self.readImage(this,self);
                  });
                  }
                 
                     });
            $('.oe_form_binary_file_clear').click(function(){
                 $(input_file).attr({ value: '' });
                 var id=$(input_file).attr('name')
                 $('#'+id).attr( "src", self.placeholder);
                })
            
            },
        readImage: function(input) {
            var self=this;
            var return_base64;
            if ( input.files && input.files[0] ) {
                var FR= new FileReader();
               FR.onload = function(e) {
                    var id=input.name;
                    return_base64=e.target.result;
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
                             $(input).attr('src',res[0].base64);
                            });
                };       
                FR.readAsDataURL(input.files[0]);
                }
              
            },
        val_defaults:function(input){
            var height= $(input).attr('height');
            if (!height){
               height= '128px';
               $(input).attr({'height':height});
                } 
            var id_file= $(input).attr('id');
            if (!id_file){
               id_file= 'id_file'+cont;
                $(input).attr({'id':id_file});
                } 
            var width= $(input).attr('width');
            if (!width){
               width= '128px';
               $(input).attr({'width':width});
                } 
            var src= $(input).attr('src');
            if (!src){
               src= this.placeholder;
                } 
            var id= $(input).attr('name');
            if (!id){
               id= 'idname'+cont;
               $(input).attr({'name':id});
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
