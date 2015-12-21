# -*- coding: utf-8 -*-

import json
import logging
import werkzeug.exceptions
import re

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT as DF
import time
import locale


_logger = logging.getLogger(__name__) 
 
parametros_list={'titulo':'',
            'url_boton_crear':'',
            'template':'',
            'icon_crear':'',
            'pie':'',
            'css':'info',
            'color_btn_crear':'primary',
                }
parametros_post={'titulo':'',
              'url_boton_list':'',
              'template':'',
              'js_enviar':'',
              'css':'info',
              'css_background':'',
              'css_btn_lista':'primary',
              'ico_btn_lista':'list-alt',
              'remover_btn_enviar':'no',
              'color_btn_enviar':'primary',
              'color_btn_lista':'primary',
              'id_enviar':'id_enviar',
              'id_form':'form1',
              'action':'/empty_action',
              'nombre_bt_accion':'Enviar'
                }


def panel_lista(datos={'parametros':'',}):
    conjunto_datos=set(datos['parametros']);
    conjunto_parametros=set(parametros_list);
    claves_dif=list(conjunto_parametros-conjunto_datos)
    for clave in conjunto_datos:
        try:
                parametros_list[clave]
        except Exception:
            msg = """Error en la clave en el parametro de parametros_list
                     coloco erroneamente %s:  %r los parametros para 
                     redireccionar a un panel de tipo lista son los 
                     siguientes: %s""" % (clave,request,parametros_list)
            _logger.error('%s ' , msg)
            raise werkzeug.exceptions.BadRequest(msg)
    for clave in claves_dif:
        datos['parametros'][clave]=parametros_list[clave]
    return http.request.website.render('website_apiform.template_lista', datos)


def panel_post(datos):
    conjunto_datos=set(datos['parametros']);
    conjunto_parametros=set(parametros_post);
    claves_dif=list(conjunto_parametros-conjunto_datos)
    for clave in conjunto_datos:
        try:
                parametros_post[clave]
        except Exception:
            msg = """Error en la clave en el parametro de parametros_crear
                     coloco erroneamente %s:  %r los parametros para 
                     redireccionar a un panel de tipo lista son los 
                     siguientes: %s""" % (clave,request,parametros_post)
            _logger.error('%s ' , msg)
            raise werkzeug.exceptions.BadRequest(msg)
    for clave in claves_dif:
        datos['parametros'][clave]=parametros_post[clave]
    return http.request.website.render('website_apiform.template_crear', datos)




def dict_keys_startswith(dictionary, string):
    '''Returns a dictionary containing the elements of <dict> whose keys start
    with <string>.

    .. note::
        This function uses dictionary comprehensions (Python >= 2.7)'''
    return {k: dictionary[k] for k in filter(lambda key: key.startswith(string), dictionary.keys())}

def dict_keys_startswith2(dictionary, string):
    '''devuelve un dict que contiene todas los valores cuyas claves terminen con un string <string>.

    .. note::
        This function uses dictionary comprehensions (Python >= 2.7)'''
    return {k: dictionary[k] for k in filter(lambda key: key.startswith(string,-1), dictionary.keys())}

class validar():
    
    
    def construir_one_2_many(self,post,pivote,dict_principal):
        
        """Metodo para construir los one2many
           Este metodo recibe como parametros:
           
           - post= diccionarios con los valores de la vista
           - pivote= primer string de las claves del diccionario que representa el elemento comun
           - dict_principal  representa la estructura que se requiere para armar el one2many
           
        """
        datos_campos=dict_keys_startswith(post,pivote)
        datos_filtrados=datos_campos.keys()
        vals=[]
        datos_dicts=[]
        i=0
        datos_len=len(datos_filtrados)
        while i<=datos_len:
            if len(datos_filtrados)>0:
                dato=datos_filtrados[0].split('_')
                datos_dict=dict_keys_startswith2(datos_campos,dato[3])
                datos_dicts=datos_dict.keys()
                diccionario={}
                for dd in datos_dicts:
                    clave_tem=dd.split('_')
                    for dp in dict_principal:
                        clave_erp=dp.split('_')
                        if clave_tem[1]==clave_erp[0]:
                            diccionario[dp]=datos_campos[dd]
                datos_filtrados=list(set(datos_filtrados) - set(datos_dicts))
                vals.append([0,False,diccionario])
            i=i+1
        return vals
        
        
    def construir_one2many(self,post,pivote,dict_principal,dict_suplente):
        
        """Metodo para construir los one2many
           Este metodo recibe como parametros:
           
           - post= diccionarios con los valores de la vista
           - pivote= primer string de las claves del diccionario que representa el elemento comun
           - dict_principal y dict_sumplente representa la estructura que se requiere para armar el one2many
           
        """
        
       
        
        return vals
                
    
        
    
    def validar_one_2_many(self,post,pivote,datos_campos):
        
        """Metodo para validar los one2many
           Debe armar el nombre del input de la siguiente manera:
           
           pivote_nombredelcampo_tipoinput_numero
           
           ejemplo: equipo_tipo_text_1
                    equipo_cantidad_number_1
                    
           el nombre del input debe estar separado por el caracter especial "_"
           
           Este metodo recibe como parametro el post que representa el diccionario con todos los campos enviados desde el formulario,
           el pivote que representa  el string inicial que los campos tienen en comun,
           y la lista datos campos que representa una lista con valores previamente cargados desde el metodo principal
           
        """
        group=dict_keys_startswith(post,pivote)
       
        for campo in group.keys():
    
            campos=campo.split('_')
            datos_campos.append({'name':campo,
                                 'type':campos[2],
                                 'attr':campos[1].capitalize()+' de '+campos[0] },)
    
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
   
    def validar_file(self,campo,post):
        print campo
        print post
        errors = {}
        answer_candidates = dict_keys_startswith(post, campo['name'])
        dif=campo['cant']-len(answer_candidates)
        if not answer_candidates:
            errors.update({campo['attr']:' Es Obligatorio'})
        elif not dif == 0 :
            errors.update({campo['attr']:' Falta'+str(dif)+' archivo '})
        return errors
        
    def validar_img(self,campo,post):
        errors = {}
        answer_candidates = dict_keys_startswith(post, campo['name'])
        dif=campo['cant']-len(answer_candidates)
        if not answer_candidates:
            errors.update({campo['attr']:' Es Obligatorio'})
        elif not dif == 0 :
            errors.update({campo['attr']:' Falta '+str(dif)+' imagen '})
        return errors
        
    def validar_rif(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        if not answer:
            errors.update({campo['attr']:' es Obligatorio.'})
        if answer and campo.has_key('min') and campo.has_key('max'):
            if not (campo['min'] <= len(answer) <= campo['max']):
                errors.update({campo['attr']:'No Cumple el tamaño con lo requerido'})
        return errors
    
    def validar_number(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        if not answer:
            errors.update({campo['attr']:' es Obligatorio.'})
        if answer and campo.has_key('caracteres_minimo') and campo.has_key('caracteres_maximo'):
            if not (campo['caracteres_minimo'] <= len(answer) <= campo['caracteres_maximo']):
                errors.update({campo['attr']:'No Cumple el tamaño con lo requerido'})
        else:
            if answer and campo.has_key('caracteres_minimo'):
                if not (campo['caracteres_minimo'] <= len(answer)):
                    errors.update({campo['attr']:'No Cumple el tamaño con lo requerido'})
            else:
                if answer and campo.has_key('caracteres_maximo'):
                    if not (len(answer) <= campo['caracteres_maximo']):
                        errors.update({campo['attr']:'No Cumple el tamaño con lo requerido'})
        if answer and campo.has_key('cantidad_min') and campo.has_key('cantidad_max'):
            if not (campo['cantidad_min'] <= int(answer) <= campo['cantidad_max']):
                errors.update({campo['attr']:'El valor del campo esta fuera de los parametros permitidos'})
        else:
            if answer and campo.has_key('cantidad_min'):
                if not (campo['cantidad_min'] <= int(answer)):
                    errors.update({campo['attr']:'El valor del campo debe ser mayor a '+str(campo['cantidad_min'])})
            else:
                if answer and campo.has_key('cantidad_max'):
                    if not (int(answer) <= campo['cantidad_max']):
                         errors.update({campo['attr']:'El valor del campo debe ser menor a '+str(campo['cantidad_max'])})
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

    def validar_numerico(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        if not answer:
            errors.update({campo['attr']:'Campo Vacio'})
        # Checks if user input is a number
        if answer:
            try:
                answer=answer.replace(".","")
                answer=answer.replace(",",".")
                floatanswer = float(answer)
            except ValueError:
                errors.update({campo['attr']: 'Esto no es un Numero'})
        # Answer validation (if properly defined)
        if answer:
            # Answer is not in the right range
            try:
                floatanswer = float(answer)  # check that it is a float has been done hereunder
                if 'min' in campo and 'max' in campo:
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
                errors.update({campo['name']: ('No es un campo fecha')})
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
        
    def validar_date(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        # Empty answer to mandatory question
        if not answer:
            errors.update({campo['attr']: ' es Obligatorio'})
        # Checks if user input is a datetime
        if answer:
            try:
                print answer
                print DF
                dateanswer = time.strptime(answer,'%d-%m-%Y')
            except ValueError:
                errors.update({campo['attr']: ('No es un campo fecha')})
                return errors
        # Answer validation (if properly defined)
        return errors

    def validar_select(self,campo,post):
        errors = {}
        answer = post[campo['name']].strip()
        # Empty answer to mandatory question
        if not campo['name'] in post:
            errors.update({campo['attr']:'Es Obligatorio'})
        elif not len(answer):
            errors.update({campo['attr']: 'Es Obligatorio'})
        return errors
    
    
    def validar_radio(self,campo,post):
        errors = {}
        #~ answer = post[campo['name']].strip()
        # Empty answer to mandatory question
        if not campo['name'] in post:
            errors.update({campo['attr']:'Es Obligatorio'})
        else:
            answer = post[campo['name']].strip()
            if not len(answer):
                errors.update({campo['attr']: 'Es Obligatorio'})
        return errors

    def validar_checkbox(self,campo,post):
        errors = {}
        answer_candidates = dict_keys_startswith(post, campo['name'])
        if not answer_candidates:
            errors.update({campo['attr']:' Es Obligatorio'})
        return errors
        

