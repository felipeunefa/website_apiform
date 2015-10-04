# -*- coding: utf-8 -*-

import base64
import logging
import hashlib
import json

import openerp
from openerp.addons.web import http
from openerp.http import request, STATIC_CACHE

import werkzeug.exceptions

_logger = logging.getLogger(__name__)


class apiform_image(http.Controller):
    
    @http.route('/website_apiform/apiform_image/base64_size',type='json', auth="public", website=True)
    def image(self,image_base64,width,height, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        values = []
        headers = [('Content-Type', 'image/png')]
        hashed_session = hashlib.md5(request.session_id).hexdigest()
        retag = hashed_session
        etag = request.httprequest.headers.get('If-None-Match')
        image_base6 = openerp.tools.image_resize_image(
                                                    base64_source=image_base64,
                                                    size=(int(width),int(height)), 
                                                    encoding='base64', 
                                                    filetype='PNG')
        values.append({
                'base64':("data:image/png;base64,%s" % image_base6)
         });
        return  values

        
    def placeholder(self, image='placeholder.png'):
        addons_path = http.addons_manifest['web']['addons_path']
        return open(os.path.join(
                                addons_path, 
                                'website_apiform', 
                                'static', 
                                'src', 
                                'img', 
                                image), 
                                'rb').read()

