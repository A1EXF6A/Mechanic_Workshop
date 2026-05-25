import xmlrpc.client

url = 'http://localhost:8070'
db = 'host'
username = 'admin'
password = '123'

try:
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    if uid:
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        move_ids = models.execute_kw(db, uid, password, 'account.move', 'search', [[('move_type', '=', 'out_invoice')]], {'limit': 1, 'order': 'id desc'})

        if move_ids:
            move = models.execute_kw(db, uid, password, 'account.move', 'read', [move_ids[0]], {'fields': ['name', 'amount_untaxed', 'amount_tax', 'amount_total', 'invoice_line_ids']})[0]
            print("Move:", move['name'])
            print(f"Untaxed: {move['amount_untaxed']} Tax: {move['amount_tax']} Total: {move['amount_total']}")
            
            lines = models.execute_kw(db, uid, password, 'account.move.line', 'read', [move['invoice_line_ids']], {'fields': ['name', 'display_type', 'price_subtotal', 'price_total', 'tax_ids']})
            for line in lines:
                if not line['display_type']:
                    taxes = []
                    if line['tax_ids']:
                        taxes = models.execute_kw(db, uid, password, 'account.tax', 'read', [line['tax_ids']], {'fields': ['amount']})
                    print(f"Line: Subtotal={line['price_subtotal']} Total={line['price_total']} Taxes={[t['amount'] for t in taxes]}")
except Exception as e:
    print(e)
