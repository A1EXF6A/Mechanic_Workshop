# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import io
import zipfile
import base64

class SriDownloadController(http.Controller):

    @http.route('/sri/download_xml_zip', type='http', auth='user')
    def download_xml_zip(self, ids, **kw):
        """
        Genera un archivo comprimido .zip con todos los XMLs autorizados del SRI
        correspondientes a las facturas proporcionadas.
        """
        if not ids:
            return request.not_found()

        try:
            move_ids = [int(x) for x in ids.split(',')]
        except ValueError:
            return request.not_found()

        moves = request.env['account.move'].browse(move_ids)
        
        # Filtrar solo facturas con XML guardado
        valid_moves = moves.filtered(lambda m: m.sri_xml_file)
        if not valid_moves:
            return request.not_found("Ninguna de las facturas tiene archivos XML del SRI válidos.")

        # Crear el archivo ZIP en memoria
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for move in valid_moves:
                xml_data = base64.b64decode(move.sri_xml_file)
                filename = move.sri_xml_filename or f"{move.sri_clave_acceso or move.name}.xml"
                zip_file.writestr(filename, xml_data)

        zip_buffer.seek(0)
        zip_content = zip_buffer.getvalue()
        zip_buffer.close()

        headers = [
            ('Content-Type', 'application/zip'),
            ('Content-Disposition', 'attachment; filename="xml_sri_autorizados.zip"'),
            ('Content-Length', str(len(zip_content)))
        ]
        return request.make_response(zip_content, headers=headers)
