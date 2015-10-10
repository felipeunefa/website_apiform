# -*- coding: utf-8 -*-

import json
import logging
import werkzeug.exceptions
import re

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF


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
              'action':'/empty_action',
                }


def panel_lista(datos={'parametros':'',}):
    for clave in datos['parametros']:
        try:   
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




def dict_keys_startswith(dictionary, string):
    '''Returns a dictionary containing the elements of <dict> whose keys start
    with <string>.

    .. note::
        This function uses dictionary comprehensions (Python >= 2.7)'''
    return {k: dictionary[k] for k in filter(lambda key: key.startswith(string), dictionary.keys())}

class validar():
    
    def validacion_campos(self,campo,post):
        ''' validar campos del los formunlarios '''
        try:
            checker = getattr(self, 'validar_' + campo['type'])
        except AttributeError:
            _logger.warning(campo['type'] + ":Tipo de campo Incorrecto")
            return {}
        else:
            return checker(campo,post)
                
    def varios_campos(self,datos_campos,post):
        errors = {}
        for campo in datos_campos:
             errors.update(self.validacion_campos(campo,post))
        return errors
        
    def validar_textarea(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        if not answer:
            errors.update({campo['attr']: ' es obligatorio.'})
        return errors

    def validar_text(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        if not answer:
            errors.update({campo['attr']:' es Obligatorio.'})
        if answer and campo.has_key('min') and campo.has_key('max'):
            if not (campo['min'] <= len(answer) <= campo['max']):
                errors.update({campo['attr']:'No Cumple el tamaño con lo requerido'})
        return errors
        
    def validar_email(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        if not answer:
            errors.update({campo['attr']:'es Obligatorio.'})
        if answer and campo['type']=='email':
            if not re.match(r"[^@]+@[^@]+\.[^@]+", answer):
                errors.update({campo['attr']: (' El Formato no es de un Email.')})
        if answer and campo.has_key('min') and campo.has_key('max'):
            if not (campo['min'] <= len(answer) <= campo['max']):
                errors.update({campo['attr']:'No Cumple el tamaño requerido'})
        return errors

    def validar_numerical_text(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        if not answer:
            errors.update({campo['name']:'Campo Vacio'})
        # Checks if user input is a number
        if answer:
            try:
                floatanswer = float(answer)
            except ValueError:
                errors.update({campo['name']: 'Esto no es un Numero'})
        # Answer validation (if properly defined)
        if answer:
            # Answer is not in the right range
            try:
                floatanswer = float(answer)  # check that it is a float has been done hereunder
                if not (campo['min'] <= floatanswer <= campo['max']):
                    errors.update({campo['name']: 'No Cumple el tamaño con lo requerido'})
            except ValueError:
                pass
        return errors

    def validar_datetime(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        # Empty answer to mandatory question
        if not answer:
            errors.update({campo['name']: 'El campo de la fecha '+campo['name']+' es obligatorio'})
        # Checks if user input is a datetime
        if answer:
            try:
                dateanswer = datetime.datetime.strptime(answer, DF)
            except ValueError:
                errors.update({campo['name']: _('No es un campo fecha')})
                return errors
        # Answer validation (if properly defined)
        if answer and campo.has_key['fecha_min'] and campo.has_key['fecha_max']:
            # Answer is not in the right range
            try:
                dateanswer = datetime.datetime.strptime(answer, DF)
                if not (campo['fecha_min'] <= dateanswer <= campo['fecha_max']):
                    errors.update({campo['name']: 'La fecha esta Fuera del rango'})
            except ValueError:  # check that it is a datetime has been done hereunder
                pass
        return errors

    def validar_radio_select(self,campo,post):
        errors = {}
        campo = post[campo['name']].strip()
        # Empty answer to mandatory question
        if not campo['name'] in post:
            errors.update({campo['name']:'Campo vacio'})
        if  campo['name'] in post and post[campo['name']].strip() == '':
            errors.update({campo['name']: 'Campo vacio'})
        return errors

    def validar_checkbox(self,campo,post):
        errors = {}
        answer_candidates = dict_keys_startswith(post, campo['name'])
        if not answer_candidates:
            errors.update({campo['attr']:' Es Obligatorio'})
        return errors
        

