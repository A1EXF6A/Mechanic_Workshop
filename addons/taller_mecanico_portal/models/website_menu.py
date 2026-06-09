from odoo import models, api

class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(WebsiteMenu, self).create(vals_list)
        self._ensure_es_ec_translations()
        return res

    def write(self, vals):
        res = super(WebsiteMenu, self).write(vals)
        self._ensure_es_ec_translations()
        return res

    @api.model
    def _ensure_es_ec_translations(self):
        try:
            # 1. Copiar traducción es_EC si no existe
            self.env.cr.execute("""
                UPDATE website_menu 
                SET name = name || jsonb_build_object('es_EC', name->>'en_US') 
                WHERE name->>'es_EC' IS NULL;
            """)

            # 2. Re-parentar menús personalizados al menú superior del sitio web 1
            root_menu = self.env['website.menu'].sudo().search([
                ('website_id', '=', 1),
                ('parent_id', '=', False)
            ], limit=1)
            if root_menu:
                xml_ids = [
                    'taller_mecanico_portal.menu_taller_home',
                    'taller_mecanico_portal.menu_taller_servicios',
                    'taller_mecanico_portal.menu_taller_nosotros',
                    'taller_mecanico_portal.menu_taller_contacto',
                    'taller_mecanico_portal.menu_taller_faq',
                    'taller_mecanico_portal.menu_taller_cita',
                    'taller_mecanico_portal.menu_taller_consulta',
                    'taller_mecanico_portal.menu_taller_productos',
                    'taller_mecanico_portal.menu_taller_carrito',
                    'taller_mecanico_portal.menu_taller_login'
                ]
                menu_ids = []
                for xml_id in xml_ids:
                    try:
                        record = self.env.ref(xml_id, raise_if_not_found=False)
                        if record:
                            menu_ids.append(record.id)
                    except Exception:
                        pass
                
                if menu_ids:
                    if len(menu_ids) == 1:
                        self.env.cr.execute("""
                            UPDATE website_menu
                            SET parent_id = %s, website_id = 1
                            WHERE id = %s AND (parent_id IS NULL OR parent_id != %s OR website_id IS NULL OR website_id != 1);
                        """, (root_menu.id, menu_ids[0], root_menu.id))
                    else:
                        self.env.cr.execute("""
                            UPDATE website_menu
                            SET parent_id = %s, website_id = 1
                            WHERE id IN %s AND (parent_id IS NULL OR parent_id != %s OR website_id IS NULL OR website_id != 1);
                        """, (root_menu.id, tuple(menu_ids), root_menu.id))
        except Exception:
            pass
