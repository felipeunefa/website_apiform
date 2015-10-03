(function ($) {
    'use strict';
    console.debug("[apiform_panel] Custom JS for apiform_panel is loading...");
         var apiform_panel = apiform_panel || {};
         apiform_panel.context=function(form_id){
             var datos=$(form_id).serializeArray();
             var destino=$(form_id).attr('action');
             var datos_post=$(form_id).serialize();
             return {datos:datos,destino:destino,datos_post:datos_post}
             }
         apiform_panel.ajax={
            enviar:function(destino,datos_post){
                  event.preventDefault();
                   $.ajax({
                            url :destino,
                            data :datos_post,
                            type : 'POST',
                            dataType : 'json',
                            success: function(response, status, xhr, wfe){
                                if (response['modal']){
                                    $.each(response['modal'], function( clave, valor ) {
                                        $('.'+clave).html(valor)
                                    });
                                     $('#AJAX_Modal').modal('show');
                                    }
                                if (response['mycontext']){
                                    $.each(response['mycontext'], function( clave, valor ) {
                                        $('.'+clave).html(valor)
                                    });
                                    }
                                
                                console.log('sfasdfsf voy bien '+response+' status'+status+' xhr'+xhr+' wfe'+wfe)
                                },
                            timeout: 5000,
                            error : function(jqXHR, textStatus, errorThrown) {
                                 $('#AJAXErrorModal').modal('show');
                            }
                        });
            }
             }
             
             
            $.fn.apiform_panel = function (options) {
                var $this = $(this), data = $this.data('apiform_panel')
                console.log(data);
                if (options== 'context') {
                    return apiform_panel.context($this);
                    }
                if (!data) {
                    console.log('gsgsdgsd');
                return apiform_panel
                }
                
                };
                
             
             
             
             
         
         $("#id_enviar").click( function( event ) {
             var context=apiform_panel.context('#form1');
             apiform_panel.ajax.enviar(context.destino,context.datos_post)
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
