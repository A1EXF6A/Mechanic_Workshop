# Script de sincronización rápida de marcas y modelos para el taller
print("Iniciando sincronización de marcas populares en Odoo...")
marca_model = env['taller.marca']

# 1. Sincronizar marcas populares desde la API de la NHTSA
print("Descargando marcas de la API...")
env['taller.marca'].action_sync_makes()
env.cr.commit()
print("Sincronización de marcas populares finalizada y guardada.")

# 2. Sincronizar modelos de las 10 marcas más importantes en Ecuador para ahorrar tiempo de API
marcas_ecuador = ['toyota', 'chevrolet', 'hyundai', 'kia', 'nissan', 'suzuki', 'great wall', 'chery', 'ford', 'volkswagen']
marcas_a_sincronizar = env['taller.marca'].search([]) # Buscar marcas populares creadas
marcas_filtradas = marcas_a_sincronizar.filtered(lambda m: m.name.lower() in marcas_ecuador)

print(f"Sincronizando modelos para las marcas top de Ecuador: {[m.name for m in marcas_filtradas]}")
for marca in marcas_filtradas:
    try:
        marca.action_sync_models()
        env.cr.commit() # Commit after each model sync to save progress
        print(f"-> Modelos de {marca.name} sincronizados con éxito.")
    except Exception as e:
        print(f"-> Error al sincronizar modelos de {marca.name}: {str(e)}")

print("¡Proceso de sincronización completado con éxito y guardado en la base de datos!")
