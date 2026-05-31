import xmlrpc.client

url = 'http://localhost:8070'
db = 'host'
username = 'admin'
password = '123'

try:
    print("Connecting to Odoo...")
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    
    # Intentar obtener la lista de bases de datos
    try:
        dblist = common.list_db()
        print("Available databases:", dblist)
        if dblist and 'host' not in dblist:
            db = dblist[0]
            print(f"Switching database to: {db}")
    except Exception as dbe:
        print("Could not list databases:", dbe)

    uid = common.authenticate(db, username, password, {})
    print("Authenticated UID:", uid)

    if uid:
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        # Busquemos la vista portal.user_sign_in por su xml_id o por id=581 (como indica el error)
        view_id = models.execute_kw(db, uid, password, 'ir.ui.view', 'search', [[('xml_id', '=', 'portal.user_sign_in')]])
        print("View IDs found by xml_id:", view_id)
        if not view_id:
            view_id = [581] # El ID indicado en el traceback
        
        view_data = models.execute_kw(db, uid, password, 'ir.ui.view', 'read', [view_id[0]], {'fields': ['name', 'xml_id', 'arch_db', 'type', 'inherit_id']})
        print("\n=== VIEW DETAIL ===")
        print("Name:", view_data[0].get('name'))
        print("XML ID:", view_data[0].get('xml_id'))
        print("Inherit ID:", view_data[0].get('inherit_id'))
        print("Type:", view_data[0].get('type'))
        print("Arch:\n", view_data[0].get('arch_db'))
except Exception as e:
    print("Error:", e)
