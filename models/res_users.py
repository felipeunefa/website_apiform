# -*- coding: utf-8 -*-
##############################################################################
#
# 
#    Modulo Desarrollado por Juventud Productiva (Felipe Villamizar)
#    Visitanos en http://juventudproductivabicentenaria.blogspot.com/
#    Nuestro Correo juventudproductivabicentenaria@gmail.com
#
#############################################################################

from openerp.osv import osv, fields
from openerp.addons.website_apiform.controladores import panel, base_tools

#~ esta clase le hereda los siguientes metodos a res_users los metodos son los 
#~ siguientes:
     #~ 
     #~ adicionar_groups_id => este metodo nos devuelve los ids de los grupos 
                        #~ pasandole una lista con los nombre del grupo

class res_users(osv.osv):
    _name = 'res.users'
    _inherit="res.users"
    
    def buscar_groups_id(self, cr, uid,name_rols,context=None):
        res_groups_obj=self.pool.get('res.groups')
        res_groups_ids=res_groups_obj.search(cr,uid,[('name','in',name_rols)])
        return res_groups_ids
        
        
        
    def raise_groups_id(self, cr, uid, context=None):
        grupos=' '
        res_groups_obj=self.pool.get('res.groups')
        groups_data=res_groups_obj.browse(cr,uid,context['only_groups_id'])
        for groups in groups_data:
            grupos+=groups.name+' \n'
        raise osv.except_osv(('Error de asignación grupo'),
            (u'''El grupo que le esta asignando no corresponde con 
            los autorizados para esta interfaz. Por esta enterfaz soló
            puede asignarle los siguientes grupos:\n %s 
            NOTA:Si desea crear un usuario con los grupos que esta asignando,
            debe comunnicarse con el administrador. , ''' % (grupos)))
        return True

    def default_groups_id(self, cr, uid, vals, context=None):
        #~ aplicamos teoria de conjuntos de lo que ponen por defecto
        #~ y lo que el usuario selecciono...
        adicionar=self.buscar_groups_id( cr, uid,['Employee'])
        groups_id= set(vals['groups_id'][0][2])
        default_groups_id= set(context['only_groups_id'])
        union=groups_id & default_groups_id;
        diferencia1= groups_id - default_groups_id;
        diferencia2=diferencia1-set(adicionar)
        if len(diferencia2)>0:
            self.raise_groups_id(cr, uid,context)
        #~ self.raise_groups_id(cr, uid,context)
        for group in adicionar:
            if not group in vals['groups_id'][0][2]:
                vals['groups_id'][0][2].append(group)
        return vals
        
    def create(self, cr, uid, vals, context=None):
        if context.has_key('only_groups_id'):
            vals=self.default_groups_id(cr,uid,vals,context)
            print vals
        user_id = super(res_users, self).create(cr, uid, vals, context=context)
        return user_id
        
    def write(self, cr, uid, ids, vals, context=None):
        if context.has_key('only_groups_id') and vals.has_key('groups_id'):
            vals=self.default_groups_id(cr,uid,vals,context=context)
        res = super(res_users, self).write(cr, uid, ids, vals, context=context)
        return res
