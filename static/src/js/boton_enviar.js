(function ($) {
    'use strict';
    console.debug("[apiform_panel] Custom JS for apiform_panel is loading...");
         var apiform_panel = apiform_panel || {};
         apiform_panel.context=function(form_id){
             var datosfile;
             var datos_form=$(form_id).serializeArray();
             var destino=$(form_id).attr('action');
             var datos_post=$(form_id).serialize();
             $(form_id).find('input[type="file"]').each(function(input){
                 var cargaImagen=new openerp.website.cargaImagen();
                 var name,value;
                 if($(this).attr('widget')=='apiform_image'){
                     name=this.name
                     value=this.src
                     value=value.split(',');
                     console.log(value)
                     value=value[1]
                     datosfile={
                     'name':name,
                     'value':value
                     }
                    datos_post+='&'+name+'='+value;
                    datos_form.push(datosfile);
                     }
                 
                 });
                var datos= new Object();
                 $.each(datos_form,function(name,value){
                    var input;
                     datos[''+value.name+'']=value.value;
                     });
             return {datos:datos,destino:destino,datos_post:datos_post}
             }
         apiform_panel.ajax={
            enviar:function(destino,datos){
                  event.preventDefault();
                  openerp.jsonRpc(destino, 'call', datos).then(function (respuesta) {
                    if (respuesta['modal']){
                        $.each(respuesta['modal'], function( clave, valor ) {
                            $('.'+clave).html(valor)
                        });
                         $('#AJAX_Modal').modal('show');
                        }
                    if (respuesta['error_campos']){
                        console.log(respuesta['error_campos'])
                        var cuerpo=' ';
                        $.each(respuesta['error_campos'], function( clave, valor ) {
                            cuerpo+=clave+' '+valor+'<br>';
                        });
                        $('.cuerpo').html('<strong class="text-danger">'+cuerpo+'</strong>');
                        $('.titulo').html('<strong>Error de campos de Formularios.</strong>')
                         $('#AJAX_Modal').modal('show');
                        }
                    if (respuesta['mycontext']){
                        $.each(respuesta['mycontext'], function( clave, valor ) {
                            $('.'+clave).html(valor)
                        });
                            }
                }).fail(function (source, error) {
                   $('#error_server').html('<strong class="text-danger">Tipo de debug</strong>'+
                                            '<p>'+error.data.name+': '+error.data.message+'</p>'+
                                            '<strong class="text-danger">Debug</strong>'+
                                            '<p>'+error.data.debug+'</p>');
                    $('#AJAXErrorModal').modal('show');
                });
            }
             }
             
             
            $.fn.apiform_panel = function (options) {
                var $this = $(this), data = $this.data('apiform_panel');
                if (options== 'context') {
                    return apiform_panel.context($this);
                    }
                if (!data) {
                return apiform_panel
                }
                
                };
                
             
             
             
             
         
         $("#id_enviar").click( function( event ) {
             var context=apiform_panel.context('#form1');
             apiform_panel.ajax.enviar(context.destino,context.datos);
             });
         
    //~ Envio de checkbox bootstrapSwitch
    
    $('input[type="checkbox"]').on('switchChange.bootstrapSwitch', function(value, state) {
                   var auto_envio= $(this).attr('auto_envio')
                     if (auto_envio!=null){
                         var SI=$(this).attr('auto_envio').toUpperCase();
                         }
                     var auto_envio=$(this).attr('auto_envio')
                     if (SI=='SI' | SI=='1'){
                         var destino=$(this).attr('destino');
                         var datos_post={ id : $(this).val(),'state':state }
                         apiform_panel.ajax.enviar(destino,datos_post)
                         }
                    });
   
    console.debug("[apiform_panel] Custom JS for apiform_panel loaded!");
    })(jQuery);


//~ function botton_enviar(form,datos,action){
                //~ this.form=form;
                //~ this.datos=datos;
                //~ this.action=action;
                //~ }
        //~ botton_enviar.prototype.form_datos=function(){
            //~ return $(this.form).serializeArray();
        //~ }
        //~ botton_enviar.prototype.form_destino=function(){
                //~ console.log('hola mundo'+this.form_datos())
                //~ if (this.action==null){
                    //~ return $(this.form).attr('action');
                                    //~ }
                    //~ return this.action
                                    //~ }
        //~ 
        //~ botton_enviar.prototype.datos_post=function() {
                //~ if (this.datos==null){
                    //~ return $(this.form).serialize();
                                    //~ }
                    //~ return this.datos
                                    //~ 
            //~ }
        //~ botton_enviar.prototype.enviar=function() {
                        //~ event.preventDefault();
                      //~ console.log('dafjakjfjafljkl'+this.form_destino()+'ggsdg');
                       //~ $.ajax({
                                //~ url :this.form_destino(),
                                //~ data : this.datos_post(),
                                //~ type : 'POST',
                                //~ dataType : 'json',
                                //~ success: function(response, status, xhr, wfe){
                                    //~ },
                                //~ timeout: 5000,
                                //~ error : function(jqXHR, textStatus, errorThrown) {
                                     //~ $('#AJAXErrorModal').modal('show');
                                //~ }
                            //~ });
            //~ 
            //~ 
            //~ }
        //~ 
    //~ 
    //~ 
    //~ $("#id_enviar").click( function( event ) {
        //~ var enviar=new botton_enviar('#form1');
        //~ enviar.enviar();
        //~ });
