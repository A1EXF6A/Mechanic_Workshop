import sys
import os

import xmlrpc.client

url = 'http://localhost:8070'
db = 'odoo'
username = 'admin'
password = '123'

try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    print("UID:", uid)

    if uid:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        move_ids = models.execute_kw(db, uid, password, 'account.move', 'search', [[('move_type', '=', 'out_invoice')]], {'limit': 1, 'order': 'id desc'})

        if move_ids:
            move = models.execute_kw(db, uid, password, 'account.move', 'read', [move_ids[0]], {'fields': ['name', 'sri_xml_file', 'sri_xml_filename']})
            print("Move found:", move[0]['name'])
            xml = move[0].get('sri_xml_file')
            if xml:
                import base64
                with open('last_invoice.xml', 'wb') as f:
                    f.write(base64.b64decode(xml))
                print("Saved to last_invoice.xml")
            else:
                print("No XML")
except Exception as e:
    print(e)
