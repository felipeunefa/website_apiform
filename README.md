website_apiform para Odoo V8
====================
    Una colaboración del equipo de
Juventud Productiva Bicentenaria y el Consejo Federa de Gobierno
=========================

Este api para odoo es una combinación de varios plugins de bootstrap, jquery 
entre otros. Adaptados y configurado para ayudarte a ganar tiempo para tú diseño
de los formularios en la vista website. 


Las herramientas que le ofrece esta Api son las siguientes:

1- Rápida creación de una vista tree en la website, para mostrar los registos de su modelo. 

2- Rápida creación de los formularios en la website de los modelos.
    2.1- Fácil Validación de los campos del lado del cliente y del servidor.
    2.2- Mensaje de error y éxito de guardado de registro.
    3.3- Mensajes de alertas 

3- Botones para los campos checkbox y radio con Bootstrap Switch.
    3.1- Plugin en js que coloca el valor del Switch en el controlador.py una vez que sea pulsado.
    3.2- Pagina oficial de Bootstrap Switch http://www.bootstrap-switch.org/

4- Botones de carga de imágenes para los campos input file con Bootstrap Fileinput.
    4.1- widget apiform_image que simula el widget image del ERP.
        <input type="file" id="image1"  class="img-responsive" name="image"  widget="apiform_image" />
    4.2- Pagina oficial bootstrap-fileinput http://plugins.krajee.com/file-input, adicionalmente se le puede agregar
        la clase js_file_apiform para no tener que pulsar el boton upload para la cargar la imagen o imagenes por summit, 
        si no que sea un solo "botón guardar" que coloque todos los valoras de los input, select, radio, checkbox y textaria
        del formulario en en controlador.py por medio de openerp.jsonRpc().
         
        <input id="id"  name="nombre" multiple="1"  type="file" class="file-loading input-file js_file_apiform"/>

