print("Sincronizando modelos faltantes...")
nombres_faltantes = ['Byd', 'Mazda', 'Peugeot', 'Renault']
marcas = env['taller.marca'].search([('name', 'in', nombres_faltantes)])

for marca in marcas:
    try:
        marca.action_sync_models()
        env.cr.commit()
        print(f"-> Modelos de {marca.name} sincronizados con éxito.")
    except Exception as e:
        print(f"-> Error al sincronizar {marca.name}: {e}")
