# -*- coding: utf-8 -*-

import json
import logging
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
import werkzeug.exceptions

_logger = logging.getLogger(__name__) 

parametros_list={'titulo':'',
            'url_boton_crear':'',
            'template':'',
            'icon_crear':'',
            'pie':'',
            'css':'info',
            'color_btn_crear':'primary',
                }
parametros_crear={'titulo':'',
              'url_boton_list':'',
              'template':'',
              'js_enviar':'',
              'css':'info',
              'css_btn_lista':'primary',
              'ico_btn_lista':'list-alt',
              'remover_btn_enviar':'no',
              'color_btn_enviar':'primary',
              'color_btn_lista':'primary',
              'id_enviar':'id_enviar',
                }


def panel_lista(datos={'parametros':'',}):
    for clave in datos['parametros']:
        try:   
                 parametros_list[clave]
                 parametros_list[clave]=datos['parametros'][clave]
        except Exception:
            msg = """Error en la clave en el parametro de parametros_list
                     coloco erroneamente %s:  %r los parametros para 
                     redireccionar a un panel de tipo lista son los 
                     siguientes: %s""" % (clave,request,parametros_list)
            _logger.error('%s ' , msg)
            raise werkzeug.exceptions.BadRequest(msg)
    datos['parametros']=parametros_list
    return http.request.website.render('website_apiform.template_lista', datos)

def panel_crear(datos={'parametros':'',}):
    for clave in datos['parametros']:
        try:
                parametros_crear[clave]=datos['parametros'][clave]
        except Exception:
            msg = """Error en la clave en el parametro de parametros_crear
                     coloco erroneamente %s:  %r los parametros para 
                     redireccionar a un panel de tipo lista son los 
                     siguientes: %s""" % (clave,request,parametros_crear)
            _logger.error('%s ' , msg)
            raise werkzeug.exceptions.BadRequest(msg)
    datos['parametros']=parametros_crear
    return http.request.website.render('website_apiform.template_crear', datos)

