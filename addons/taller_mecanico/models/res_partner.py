# -*- coding: utf-8 -*-
from odoo import models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def can_edit_vat(self):
        """
        Permitir editar el NIF/Cédula/RUC desde el portal web si el campo está vacío,
        incluso si ya existen facturas publicadas para este contacto.
        Esto evita el bloqueo donde el sistema exige el campo pero no permite escribirlo.
        """
        res = super(ResPartner, self).can_edit_vat()
        # Si el VAT está vacío en la base de datos, siempre permitimos escribirlo una primera vez
        if not self.vat:
            return True
        return res
