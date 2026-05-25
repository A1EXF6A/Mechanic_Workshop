move = env['account.move'].search([('move_type', '=', 'out_invoice')], limit=1, order='id desc')
if move:
    print('Last move:', move.name)
    xml = move.sri_xml_file
    if xml:
        import base64
        with open('/tmp/last_invoice.xml', 'wb') as f:
            f.write(base64.b64decode(xml))
        print('Saved to /tmp/last_invoice.xml')
    else:
        print('No XML found for this move')
else:
    print('No move found')
