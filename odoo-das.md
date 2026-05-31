# Añadir datos a módulo Odoo Ventas

**Session ID:** ses_20a39dcd9ffeyBO9dCrIhsIXEJ
**Created:** 5/4/2026, 8:34:56 PM
**Updated:** 5/4/2026, 10:07:08 PM

---

## User

oye tu puedes meterle datos a un modulo de odoo?, osea por ejemplo el modulo de odoo de ventas

---

## Assistant (Build · GPT-5.2-Codex · 3.3s)

_Thinking:_

**Requesting clarification**

I'm asking in Spanish whether they want to import data or create records, if they need access, and which version and method they are using.

Sí, puedo ayudarte. Para hacerlo bien, dime lo siguiente (una sola respuesta está bien):

- ¿Qué versión de Odoo usas y cómo accedo (UI, XML‑RPC/JSON‑RPC, CSV, o directo a la base de datos)?
- ¿Qué datos quieres cargar en Ventas exactamente (clientes, productos, cotizaciones, pedidos, líneas, precios, etc.)?
- ¿Tienes ya el archivo origen (CSV/Excel) o hay que generarlo desde cero?

Con eso te digo el mejor método y te preparo los pasos.

---

## User

es un modulo nativo osea yo levanto el odoo, lo instale y ya nada mas

---

## Assistant (Build · GPT-5.2-Codex · 2.5s)

_Thinking:_

**Requesting specifics for UI import**

I need to ask which version and method are being used and what data and source file the user wants to import to provide tailored native module UI import steps.

Perfecto. Puedo guiarte con la carga desde la UI nativa de Odoo.

Solo necesito esto para darte los pasos exactos:
- ¿Qué datos quieres cargar en Ventas (clientes, productos, cotizaciones, pedidos, precios, etc.)?
- ¿Tienes los datos en CSV/Excel o todavía no?

Si no tienes archivo, te puedo dar una plantilla base.

---

## User

Todo lo que pueda es odoo 18, es que necesito lo siguiente, todas las aplicaciones del proyecto configuradas, son las siguientes: sitio web, inventario, compras, ventas, empleados, necesito como minimo 10 registros para cada uno, todos deben estar configurados, con nombre de la empresa, moneda, logo, etc, el sitio web debe tener al menos 3 paginas relevantes al negocio, probar un flujo completo de de extremo a extremo demostrable (ejemplo: cliente navega el sitio → realiza una compra → se genera la factura). El negocio es un negocio de una mecanica, el nombre de la empresa es Terrabyte EC, el logo esta en este mismo directorio llamado logo.jpeg, todos los datos inventatelos porque no tengo nada

---

## Assistant (Build · GPT-5.2-Codex · 3.6s)

_Thinking:_

**Clarifying access and permissions**

I need to confirm if the user wants instructions for instance access or if I should proceed directly, and whether admin access can be provided.

Puedo hacerlo, pero necesito acceso a tu instancia de Odoo para cargar y configurar todo. ¿Prefieres que te deje un plan paso a paso para hacerlo tú en la UI, o puedo conectarme y hacerlo directamente?

Si quieres que lo haga yo, dime:
- URL de tu Odoo 18
- Usuario admin y contraseña (o crea un usuario temporal)
- Confirmación de que el logo está en el servidor en `/home/alexander/Desktop/das/Mechanic_Workshop/logo.jpeg` o indícame la ruta real dentro del host de Odoo.

---

## User

el odoo es local por docker aqui mismo tienes el compose el usuario que tengo es: admin@gmail.com -> admin123, y la imagen si existe, puedes verlo pero con todo la url es: http://localhost:8070/

---

## Assistant (Build · GPT-5.2-Codex · 10.6s)

_Thinking:_

**Drafting import plan and data generation**

I'll prepare CSV templates with 10 records each for key modules and company setup instructions in Spanish, plus a plan for data import and module installation, asking only to confirm the database name before proceeding.

_Thinking:_

**Planning CSV creation and inventory guidance**

I'm preparing CSV templates for contacts, products, employees, sales, and purchase orders, plus guidance to set product quantities manually via the Odoo UI. Next, I'll check the repo for a logo file to include in the company config.

**Tool: read**

**Input:**
```json
{
  "filePath": "/home/alexander/Desktop/das/Mechanic_Workshop"
}
```

**Output:**
```
<path>/home/alexander/Desktop/das/Mechanic_Workshop</path>
<type>directory</type>
<entries>
.env
.env.example
.env.linux-selinux.example
.env.windows.example
.git/
.gitignore
addons/
config/
docker-compose.yml
logo.jpeg
README.md

(11 entries)
</entries>
```

---

## Assistant (Build · GPT-5.2-Codex · 3.1s)

_Thinking:_

**Requesting clarification on access**

I can't access the UI directly but can provide step-by-step guidance and generate data files like CSVs; I'll ask if that approach works before proceeding.

No puedo abrir un navegador desde aquí para entrar a `http://localhost:8070/` y cargar datos en la UI, pero sí puedo dejarte todo listo para que solo importes en Odoo: plantillas CSV completas (clientes, productos, proveedores, empleados, etc.), más una guía paso a paso para configurar empresa, moneda, logo, web con 3 páginas y el flujo de compra → factura.

Si te sirve, dime:
- ¿Quieres que genere los CSV con 10+ registros por app y la guía de importación?
- ¿Usas moneda USD (por defecto en Ecuador) o prefieres otra?

Con eso preparo todo en este repo y te indico exactamente dónde importar cada archivo.

---

## User

Yaya hazlo, los registros que sean alrededor de 30,  si la moneda por defecto, dime todo lo que debo hacer

---

## Assistant (Build · GPT-5.2-Codex · 16.7s)

_Thinking:_

**Planning CSV and content generation**

I'll create a data folder with CSV files for 30 records each of customers, vendors, products, employees, sales orders, purchase orders, and inventory adjustments, plus 3 website pages in HTML. Also, I'll prepare README instructions detailing import fields, external IDs, and setup steps.

_Thinking:_

**Setting up import data directory**

I'll verify the import data directory exists using bash and create it if missing to prepare for CSV file placement.

**Tool: bash**

**Input:**
```json
{
  "command": "ls",
  "description": "Lists files in current directory"
}
```

**Output:**
```
addons
config
docker-compose.yml
logo.jpeg
README.md

```

---

## Assistant (Build · GPT-5.2-Codex · 35.0s)

_Thinking:_

**Planning Odoo CSV data and setup guide**

I'm outlining creation of CSV files (around 30 records each) for key Odoo models like contacts, products, employees, orders, and inventory in a data_import directory, plus a setup guide with configuration steps and sample website pages to support an end-to-end eCommerce flow.

_Thinking:_

**Detailing CSV structure and setup guide content**

I'm defining CSV file names, record counts, and fields for customers, vendors, products, employees, orders, and inventory adjustments, plus the structure of a Spanish ASCII-only setup guide with step-by-step import and configuration instructions including website pages and payment setup.

**Tool: bash**

**Input:**
```json
{
  "command": "mkdir data_import",
  "description": "Creates data_import directory"
}
```

**Output:**
```
(no output)
```

---

## Assistant (Build · GPT-5.2-Codex · 78.3s)

_Thinking:_

**Planning CSV data generation**

I'm defining data needs for each app module: around 30 records per module, including contacts (vendors/customers), products, inventory adjustments, sales and purchase orders, and employees; website pages only need 3. Next, I'll create ASCII CSV files with proper Odoo 18 import fields and prepare README instructions.

_Thinking:_

**Finalizing CSV structure and import fields**

I've detailed the specific fields and data formats for contacts, products, inventory adjustments, sales and purchase orders, and employees aligned with Odoo 18 import requirements, deciding to create separate ASCII CSVs for each. Next, I'll generate consistent records including 30 products, 60 contacts (customers and vendors), and 30 orders per sales and purchases, then create a single patch adding all CSV files with proper content and instructions.

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/contacts_customers.csv\n+Name,Email,Phone,Mobile,Street,City,Country,Company Type,Customer Rank,Supplier Rank\n+Cliente 01,cliente01@terrabyteec.com,022900001,0999000001,Av. Principal 101,Quito,Ecuador,Company,1,0\n+Cliente 02,cliente02@terrabyteec.com,022900002,0999000002,Calle 10 #202,Guayaquil,Ecuador,Company,1,0\n+Cliente 03,cliente03@terrabyteec.com,022900003,0999000003,Av. Central 303,Cuenca,Ecuador,Company,1,0\n+Cliente 04,cliente04@terrabyteec.com,022900004,0999000004,Calle Norte 404,Manta,Ecuador,Company,1,0\n+Cliente 05,cliente05@terrabyteec.com,022900005,0999000005,Av. Sur 505,Ambato,Ecuador,Company,1,0\n+Cliente 06,cliente06@terrabyteec.com,022900006,0999000006,Av. Sierra 606,Quito,Ecuador,Company,1,0\n+Cliente 07,cliente07@terrabyteec.com,022900007,0999000007,Calle Costa 707,Guayaquil,Ecuador,Company,1,0\n+Cliente 08,cliente08@terrabyteec.com,022900008,0999000008,Av. Andes 808,Cuenca,Ecuador,Company,1,0\n+Cliente 09,cliente09@terrabyteec.com,022900009,0999000009,Calle 9 #909,Portoviejo,Ecuador,Company,1,0\n+Cliente 10,cliente10@terrabyteec.com,022900010,0999000010,Av. Taller 1010,Quito,Ecuador,Company,1,0\n+Cliente 11,cliente11@terrabyteec.com,022900011,0999000011,Calle 11 #1111,Guayaquil,Ecuador,Company,1,0\n+Cliente 12,cliente12@terrabyteec.com,022900012,0999000012,Av. 12 1212,Cuenca,Ecuador,Company,1,0\n+Cliente 13,cliente13@terrabyteec.com,022900013,0999000013,Calle 13 #1313,Manta,Ecuador,Company,1,0\n+Cliente 14,cliente14@terrabyteec.com,022900014,0999000014,Av. 14 1414,Ambato,Ecuador,Company,1,0\n+Cliente 15,cliente15@terrabyteec.com,022900015,0999000015,Calle 15 #1515,Quito,Ecuador,Company,1,0\n+Cliente 16,cliente16@terrabyteec.com,022900016,0999000016,Av. 16 1616,Guayaquil,Ecuador,Company,1,0\n+Cliente 17,cliente17@terrabyteec.com,022900017,0999000017,Calle 17 #1717,Cuenca,Ecuador,Company,1,0\n+Cliente 18,cliente18@terrabyteec.com,022900018,0999000018,Av. 18 1818,Manta,Ecuador,Company,1,0\n+Cliente 19,cliente19@terrabyteec.com,022900019,0999000019,Calle 19 #1919,Ambato,Ecuador,Company,1,0\n+Cliente 20,cliente20@terrabyteec.com,022900020,0999000020,Av. 20 2020,Quito,Ecuador,Company,1,0\n+Cliente 21,cliente21@terrabyteec.com,022900021,0999000021,Calle 21 #2121,Guayaquil,Ecuador,Company,1,0\n+Cliente 22,cliente22@terrabyteec.com,022900022,0999000022,Av. 22 2222,Cuenca,Ecuador,Company,1,0\n+Cliente 23,cliente23@terrabyteec.com,022900023,0999000023,Calle 23 #2323,Manta,Ecuador,Company,1,0\n+Cliente 24,cliente24@terrabyteec.com,022900024,0999000024,Av. 24 2424,Ambato,Ecuador,Company,1,0\n+Cliente 25,cliente25@terrabyteec.com,022900025,0999000025,Calle 25 #2525,Quito,Ecuador,Company,1,0\n+Cliente 26,cliente26@terrabyteec.com,022900026,0999000026,Av. 26 2626,Guayaquil,Ecuador,Company,1,0\n+Cliente 27,cliente27@terrabyteec.com,022900027,0999000027,Calle 27 #2727,Cuenca,Ecuador,Company,1,0\n+Cliente 28,cliente28@terrabyteec.com,022900028,0999000028,Av. 28 2828,Manta,Ecuador,Company,1,0\n+Cliente 29,cliente29@terrabyteec.com,022900029,0999000029,Calle 29 #2929,Ambato,Ecuador,Company,1,0\n+Cliente 30,cliente30@terrabyteec.com,022900030,0999000030,Av. 30 3030,Quito,Ecuador,Company,1,0\n*** Add File: data_import/contacts_vendors.csv\n+Name,Email,Phone,Mobile,Street,City,Country,Company Type,Customer Rank,Supplier Rank\n+Proveedor 01,proveedor01@terrabyteec.com,042800001,0988000001,Av. Industrial 101,Guayaquil,Ecuador,Company,0,1\n+Proveedor 02,proveedor02@terrabyteec.com,042800002,0988000002,Calle Bodega 202,Guayaquil,Ecuador,Company,0,1\n+Proveedor 03,proveedor03@terrabyteec.com,042800003,0988000003,Av. Logistica 303,Quito,Ecuador,Company,0,1\n+Proveedor 04,proveedor04@terrabyteec.com,042800004,0988000004,Calle Taller 404,Quito,Ecuador,Company,0,1\n+Proveedor 05,proveedor05@terrabyteec.com,042800005,0988000005,Av. Repuestos 505,Cuenca,Ecuador,Company,0,1\n+Proveedor 06,proveedor06@terrabyteec.com,042800006,0988000006,Calle Motor 606,Cuenca,Ecuador,Company,0,1\n+Proveedor 07,proveedor07@terrabyteec.com,042800007,0988000007,Av. Lubricantes 707,Manta,Ecuador,Company,0,1\n+Proveedor 08,proveedor08@terrabyteec.com,042800008,0988000008,Calle Filtros 808,Manta,Ecuador,Company,0,1\n+Proveedor 09,proveedor09@terrabyteec.com,042800009,0988000009,Av. Frenos 909,Ambato,Ecuador,Company,0,1\n+Proveedor 10,proveedor10@terrabyteec.com,042800010,0988000010,Calle Electricos 1010,Ambato,Ecuador,Company,0,1\n+Proveedor 11,proveedor11@terrabyteec.com,042800011,0988000011,Av. Suspensiones 1111,Quito,Ecuador,Company,0,1\n+Proveedor 12,proveedor12@terrabyteec.com,042800012,0988000012,Calle Neumaticos 1212,Quito,Ecuador,Company,0,1\n+Proveedor 13,proveedor13@terrabyteec.com,042800013,0988000013,Av. Baterias 1313,Guayaquil,Ecuador,Company,0,1\n+Proveedor 14,proveedor14@terrabyteec.com,042800014,0988000014,Calle Enfriamiento 1414,Guayaquil,Ecuador,Company,0,1\n+Proveedor 15,proveedor15@terrabyteec.com,042800015,0988000015,Av. Accesorios 1515,Cuenca,Ecuador,Company,0,1\n+Proveedor 16,proveedor16@terrabyteec.com,042800016,0988000016,Calle Herramientas 1616,Cuenca,Ecuador,Company,0,1\n+Proveedor 17,proveedor17@terrabyteec.com,042800017,0988000017,Av. Sensores 1717,Manta,Ecuador,Company,0,1\n+Proveedor 18,proveedor18@terrabyteec.com,042800018,0988000018,Calle Electronica 1818,Manta,Ecuador,Company,0,1\n+Proveedor 19,proveedor19@terrabyteec.com,042800019,0988000019,Av. Iluminacion 1919,Ambato,Ecuador,Company,0,1\n+Proveedor 20,proveedor20@terrabyteec.com,042800020,0988000020,Calle Pintura 2020,Ambato,Ecuador,Company,0,1\n+Proveedor 21,proveedor21@terrabyteec.com,042800021,0988000021,Av. Correas 2121,Quito,Ecuador,Company,0,1\n+Proveedor 22,proveedor22@terrabyteec.com,042800022,0988000022,Calle Rodamientos 2222,Quito,Ecuador,Company,0,1\n+Proveedor 23,proveedor23@terrabyteec.com,042800023,0988000023,Av. Escape 2323,Guayaquil,Ecuador,Company,0,1\n+Proveedor 24,proveedor24@terrabyteec.com,042800024,0988000024,Calle Direccion 2424,Guayaquil,Ecuador,Company,0,1\n+Proveedor 25,proveedor25@terrabyteec.com,042800025,0988000025,Av. Transmision 2525,Cuenca,Ecuador,Company,0,1\n+Proveedor 26,proveedor26@terrabyteec.com,042800026,0988000026,Calle Insumos 2626,Cuenca,Ecuador,Company,0,1\n+Proveedor 27,proveedor27@terrabyteec.com,042800027,0988000027,Av. Refrigeracion 2727,Manta,Ecuador,Company,0,1\n+Proveedor 28,proveedor28@terrabyteec.com,042800028,0988000028,Calle Autoelectricos 2828,Manta,Ecuador,Company,0,1\n+Proveedor 29,proveedor29@terrabyteec.com,042800029,0988000029,Av. Limpieza 2929,Ambato,Ecuador,Company,0,1\n+Proveedor 30,proveedor30@terrabyteec.com,042800030,0988000030,Calle Quimicos 3030,Ambato,Ecuador,Company,0,1\n*** Add File: data_import/products.csv\n+Name,Internal Reference,Sales Price,Cost,Product Type,Product Category,Can be Sold,Can be Purchased\n+Aceite 5W30 1L,P-001,12.50,8.20,Storable Product,Lubricantes,TRUE,TRUE\n+Aceite 10W40 1L,P-002,11.90,7.80,Storable Product,Lubricantes,TRUE,TRUE\n+Filtro de aceite A1,P-003,6.50,3.80,Storable Product,Repuestos,TRUE,TRUE\n+Filtro de aire A2,P-004,8.20,4.60,Storable Product,Repuestos,TRUE,TRUE\n+Bujia NGK BKR6E,P-005,9.90,6.10,Storable Product,Repuestos,TRUE,TRUE\n+Pastillas de freno delanteras,P-006,35.00,22.00,Storable Product,Repuestos,TRUE,TRUE\n+Pastillas de freno traseras,P-007,32.00,20.50,Storable Product,Repuestos,TRUE,TRUE\n+Disco de freno 280mm,P-008,45.00,30.00,Storable Product,Repuestos,TRUE,TRUE\n+Bateria 12V 60Ah,P-009,120.00,90.00,Storable Product,Repuestos,TRUE,TRUE\n+Neumatico 195/65R15,P-010,85.00,60.00,Storable Product,Repuestos,TRUE,TRUE\n+Neumatico 205/55R16,P-011,95.00,68.00,Storable Product,Repuestos,TRUE,TRUE\n+Amortiguador delantero,P-012,78.00,52.00,Storable Product,Repuestos,TRUE,TRUE\n+Amortiguador trasero,P-013,74.00,49.00,Storable Product,Repuestos,TRUE,TRUE\n+Correa de distribucion,P-014,55.00,37.00,Storable Product,Repuestos,TRUE,TRUE\n+Correa auxiliar,P-015,25.00,16.00,Storable Product,Repuestos,TRUE,TRUE\n+Liquido de frenos DOT4,P-016,7.50,4.20,Consumable,Lubricantes,TRUE,TRUE\n+Liquido refrigerante 1L,P-017,6.80,3.90,Consumable,Lubricantes,TRUE,TRUE\n+Filtro de combustible C1,P-018,10.50,6.70,Storable Product,Repuestos,TRUE,TRUE\n+Limpiaparabrisas 22in,P-019,12.00,7.50,Storable Product,Accesorios,TRUE,TRUE\n+Lampara H4 60/55W,P-020,5.50,3.10,Storable Product,Accesorios,TRUE,TRUE\n+Kit de embrague,P-021,180.00,130.00,Storable Product,Repuestos,TRUE,TRUE\n+Alternador 90A,P-022,210.00,160.00,Storable Product,Repuestos,TRUE,TRUE\n+Motor de arranque,P-023,190.00,140.00,Storable Product,Repuestos,TRUE,TRUE\n+Sensor de oxigeno,P-024,65.00,45.00,Storable Product,Repuestos,TRUE,TRUE\n+Bobina de encendido,P-025,48.00,31.00,Storable Product,Repuestos,TRUE,TRUE\n+Radiador compacto,P-026,135.00,95.00,Storable Product,Repuestos,TRUE,TRUE\n+Termostato 88C,P-027,18.00,11.00,Storable Product,Repuestos,TRUE,TRUE\n+Kit de afinamiento,P-028,60.00,40.00,Storable Product,Repuestos,TRUE,TRUE\n+Aditivo limpiainyectores,P-029,9.50,5.20,Consumable,Lubricantes,TRUE,TRUE\n+Grasa multiproposito 500g,P-030,7.80,4.10,Consumable,Lubricantes,TRUE,TRUE\n*** Add File: data_import/inventory_adjustments.csv\n+Product,Location,Counted Quantity\n+Aceite 5W30 1L,WH/Stock,40\n+Aceite 10W40 1L,WH/Stock,35\n+Filtro de aceite A1,WH/Stock,60\n+Filtro de aire A2,WH/Stock,50\n+Bujia NGK BKR6E,WH/Stock,80\n+Pastillas de freno delanteras,WH/Stock,25\n+Pastillas de freno traseras,WH/Stock,25\n+Disco de freno 280mm,WH/Stock,20\n+Bateria 12V 60Ah,WH/Stock,12\n+Neumatico 195/65R15,WH/Stock,18\n+Neumatico 205/55R16,WH/Stock,16\n+Amortiguador delantero,WH/Stock,22\n+Amortiguador trasero,WH/Stock,22\n+Correa de distribucion,WH/Stock,30\n+Correa auxiliar,WH/Stock,45\n+Liquido de frenos DOT4,WH/Stock,70\n+Liquido refrigerante 1L,WH/Stock,65\n+Filtro de combustible C1,WH/Stock,40\n+Limpiaparabrisas 22in,WH/Stock,55\n+Lampara H4 60/55W,WH/Stock,90\n+Kit de embrague,WH/Stock,10\n+Alternador 90A,WH/Stock,8\n+Motor de arranque,WH/Stock,7\n+Sensor de oxigeno,WH/Stock,18\n+Bobina de encendido,WH/Stock,20\n+Radiador compacto,WH/Stock,9\n+Termostato 88C,WH/Stock,28\n+Kit de afinamiento,WH/Stock,15\n+Aditivo limpiainyectores,WH/Stock,50\n+Grasa multiproposito 500g,WH/Stock,55\n*** Add File: data_import/sales_orders.csv\n+Customer,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Cliente 01,2026-04-01,Aceite 5W30 1L,2,12.50\n+Cliente 02,2026-04-02,Filtro de aceite A1,3,6.50\n+Cliente 03,2026-04-03,Pastillas de freno delanteras,1,35.00\n+Cliente 04,2026-04-04,Disco de freno 280mm,2,45.00\n+Cliente 05,2026-04-05,Bateria 12V 60Ah,1,120.00\n+Cliente 06,2026-04-06,Neumatico 195/65R15,2,85.00\n+Cliente 07,2026-04-07,Amortiguador delantero,2,78.00\n+Cliente 08,2026-04-08,Correa de distribucion,1,55.00\n+Cliente 09,2026-04-09,Liquido de frenos DOT4,4,7.50\n+Cliente 10,2026-04-10,Liquido refrigerante 1L,3,6.80\n+Cliente 11,2026-04-11,Filtro de aire A2,2,8.20\n+Cliente 12,2026-04-12,Limpiaparabrisas 22in,2,12.00\n+Cliente 13,2026-04-13,Lampara H4 60/55W,4,5.50\n+Cliente 14,2026-04-14,Kit de embrague,1,180.00\n+Cliente 15,2026-04-15,Alternador 90A,1,210.00\n+Cliente 16,2026-04-16,Motor de arranque,1,190.00\n+Cliente 17,2026-04-17,Sensor de oxigeno,1,65.00\n+Cliente 18,2026-04-18,Bobina de encendido,2,48.00\n+Cliente 19,2026-04-19,Radiador compacto,1,135.00\n+Cliente 20,2026-04-20,Termostato 88C,2,18.00\n+Cliente 21,2026-04-21,Kit de afinamiento,1,60.00\n+Cliente 22,2026-04-22,Aditivo limpiainyectores,3,9.50\n+Cliente 23,2026-04-23,Grasa multiproposito 500g,4,7.80\n+Cliente 24,2026-04-24,Correa auxiliar,2,25.00\n+Cliente 25,2026-04-25,Neumatico 205/55R16,2,95.00\n+Cliente 26,2026-04-26,Filtro de combustible C1,2,10.50\n+Cliente 27,2026-04-27,Pastillas de freno traseras,1,32.00\n+Cliente 28,2026-04-28,Aceite 10W40 1L,2,11.90\n+Cliente 29,2026-04-29,Bujia NGK BKR6E,4,9.90\n+Cliente 30,2026-04-30,Amortiguador trasero,2,74.00\n*** Add File: data_import/purchase_orders.csv\n+Vendor,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Proveedor 01,2026-03-01,Aceite 5W30 1L,30,8.20\n+Proveedor 02,2026-03-02,Aceite 10W40 1L,30,7.80\n+Proveedor 03,2026-03-03,Filtro de aceite A1,60,3.80\n+Proveedor 04,2026-03-04,Filtro de aire A2,50,4.60\n+Proveedor 05,2026-03-05,Bujia NGK BKR6E,80,6.10\n+Proveedor 06,2026-03-06,Pastillas de freno delanteras,25,22.00\n+Proveedor 07,2026-03-07,Pastillas de freno traseras,25,20.50\n+Proveedor 08,2026-03-08,Disco de freno 280mm,20,30.00\n+Proveedor 09,2026-03-09,Bateria 12V 60Ah,12,90.00\n+Proveedor 10,2026-03-10,Neumatico 195/65R15,18,60.00\n+Proveedor 11,2026-03-11,Neumatico 205/55R16,16,68.00\n+Proveedor 12,2026-03-12,Amortiguador delantero,22,52.00\n+Proveedor 13,2026-03-13,Amortiguador trasero,22,49.00\n+Proveedor 14,2026-03-14,Correa de distribucion,30,37.00\n+Proveedor 15,2026-03-15,Correa auxiliar,45,16.00\n+Proveedor 16,2026-03-16,Liquido de frenos DOT4,70,4.20\n+Proveedor 17,2026-03-17,Liquido refrigerante 1L,65,3.90\n+Proveedor 18,2026-03-18,Filtro de combustible C1,40,6.70\n+Proveedor 19,2026-03-19,Limpiaparabrisas 22in,55,7.50\n+Proveedor 20,2026-03-20,Lampara H4 60/55W,90,3.10\n+Proveedor 21,2026-03-21,Kit de embrague,10,130.00\n+Proveedor 22,2026-03-22,Alternador 90A,8,160.00\n+Proveedor 23,2026-03-23,Motor de arranque,7,140.00\n+Proveedor 24,2026-03-24,Sensor de oxigeno,18,45.00\n+Proveedor 25,2026-03-25,Bobina de encendido,20,31.00\n+Proveedor 26,2026-03-26,Radiador compacto,9,95.00\n+Proveedor 27,2026-03-27,Termostato 88C,28,11.00\n+Proveedor 28,2026-03-28,Kit de afinamiento,15,40.00\n+Proveedor 29,2026-03-29,Aditivo limpiainyectores,50,5.20\n+Proveedor 30,2026-03-30,Grasa multiproposito 500g,55,4.10\n*** Add File: data_import/employees.csv\n+Name,Work Email,Work Phone,Mobile Phone,Job Title,Department,Manager\n+Luis Herrera,luis.herrera@terrabyteec.com,022910001,0999100001,Jefe de Taller,Taller,\n+Sofia Mena,sofia.mena@terrabyteec.com,022910002,0999100002,Asistente de Taller,Taller,Luis Herrera\n+Carlos Paredes,carlos.paredes@terrabyteec.com,022910003,0999100003,Mecanico Senior,Taller,Luis Herrera\n+Andrea Ruiz,andrea.ruiz@terrabyteec.com,022910004,0999100004,Mecanico,Taller,Luis Herrera\n+Jorge Vega,jorge.vega@terrabyteec.com,022910005,0999100005,Mecanico,Taller,Luis Herrera\n+Paola Castro,paola.castro@terrabyteec.com,022910006,0999100006,Mecanico,Taller,Luis Herrera\n+Diego Luna,diego.luna@terrabyteec.com,022910007,0999100007,Mecanico,Taller,Luis Herrera\n+Gabriela Ortiz,gabriela.ortiz@terrabyteec.com,022910008,0999100008,Auxiliar de Taller,Taller,Luis Herrera\n+Juan Mora,juan.mora@terrabyteec.com,022910009,0999100009,Jefe de Almacen,Almacen,\n+Valeria Nunez,valeria.nunez@terrabyteec.com,022910010,0999100010,Almacenista,Almacen,Juan Mora\n+Ricardo Salas,ricardo.salas@terrabyteec.com,022910011,0999100011,Almacenista,Almacen,Juan Mora\n+Mariana Paz,mariana.paz@terrabyteec.com,022910012,0999100012,Jefe de Compras,Compras,\n+Mateo Silva,mateo.silva@terrabyteec.com,022910013,0999100013,Analista de Compras,Compras,Mariana Paz\n+Natalia Velez,natalia.velez@terrabyteec.com,022910014,0999100014,Comprador,Compras,Mariana Paz\n+Esteban Rios,esteban.rios@terrabyteec.com,022910015,0999100015,Jefe de Ventas,Ventas,\n+Fernanda Cobo,fernanda.cobo@terrabyteec.com,022910016,0999100016,Asesora de Ventas,Ventas,Esteban Rios\n+Kevin Torres,kevin.torres@terrabyteec.com,022910017,0999100017,Asesor de Ventas,Ventas,Esteban Rios\n+Camila Rojas,camila.rojas@terrabyteec.com,022910018,0999100018,Asesora de Ventas,Ventas,Esteban Rios\n+Oscar Molina,oscar.molina@terrabyteec.com,022910019,0999100019,Asesor de Ventas,Ventas,Esteban Rios\n+Daniela Soria,daniela.soria@terrabyteec.com,022910020,0999100020,Gerente Administrativa,Administracion,\n+Pablo Leon,pablo.leon@terrabyteec.com,022910021,0999100021,Asistente Administrativa,Administracion,Daniela Soria\n+Irene Lara,irene.lara@terrabyteec.com,022910022,0999100022,Contadora,Administracion,Daniela Soria\n+Miguel Tapia,miguel.tapia@terrabyteec.com,022910023,0999100023,Auxiliar Contable,Administracion,Daniela Soria\n+Lorena Rivas,lorena.rivas@terrabyteec.com,022910024,0999100024,Recepcionista,Administracion,Daniela Soria\n+Hugo Viteri,hugo.viteri@terrabyteec.com,022910025,0999100025,Coordinador de Calidad,Administracion,Daniela Soria\n+Carla Pino,carla.pino@terrabyteec.com,022910026,0999100026,Asistente de Calidad,Administracion,Hugo Viteri\n+Sergio Ponce,sergio.ponce@terrabyteec.com,022910027,0999100027,Especialista en Diagnostico,Taller,Luis Herrera\n+Noelia Cruz,noelia.cruz@terrabyteec.com,022910028,0999100028,Especialista en Suspension,Taller,Luis Herrera\n+Adrian Loja,adrian.loja@terrabyteec.com,022910029,0999100029,Especialista en Frenos,Taller,Luis Herrera\n+Maria Vera,maria.vera@terrabyteec.com,022910030,0999100030,Especialista en Electricidad,Taller,Luis Herrera\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/contacts_customers.csv
A data_import/contacts_vendors.csv
A data_import/products.csv
A data_import/inventory_adjustments.csv
A data_import/sales_orders.csv
A data_import/purchase_orders.csv
A data_import/employees.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 9.4s)

_Thinking:_

**Outlining manual page creation**

I'm specifying instructions for manually creating website pages with textual content files, including where to place the logo image and how to import and link these elements, plus next steps to integrate them.

Listo. Te dejé los CSV con ~30 registros por módulo para importar directo en Odoo. Están en `data_import/`.

Archivos creados:
- `data_import/contacts_customers.csv` (30 clientes)
- `data_import/contacts_vendors.csv` (30 proveedores)
- `data_import/products.csv` (30 productos)
- `data_import/inventory_adjustments.csv` (ajustes de inventario para 30 productos)
- `data_import/purchase_orders.csv` (30 órdenes de compra)
- `data_import/sales_orders.csv` (30 órdenes de venta)
- `data_import/employees.csv` (30 empleados)

Guía paso a paso (Odoo 18, UI)
1) Configuración base de empresa
- Entra a `http://localhost:8070/` con `admin@gmail.com / admin123`.
- Activa apps: Sitio Web, Inventario, Compras, Ventas, Empleados.
- Ajustes → Compañía → Terrabyte EC.
  - Nombre: Terrabyte EC
  - Moneda: USD (por defecto)
  - Logo: sube `logo.jpeg` desde `/home/alexander/Desktop/das/Mechanic_Workshop/logo.jpeg`

2) Importar contactos (clientes y proveedores)
- Contactos → Importar.
- Importa `data_import/contacts_customers.csv`.
- Repite con `data_import/contacts_vendors.csv`.
- Verifica que “Customer Rank” y “Supplier Rank” queden correctos.

3) Importar productos
- Inventario → Productos → Importar.
- Importa `data_import/products.csv`.
- Asegúrate de mapear:
  - Name, Internal Reference, Sales Price, Cost, Product Type, Product Category, Can be Sold, Can be Purchased.

4) Ajuste de stock inicial
- Inventario → Operaciones → Ajustes de inventario → Importar.
- Importa `data_import/inventory_adjustments.csv`.
- Ubicación: `WH/Stock`.
- Valida el ajuste.

5) Importar empleados
- Empleados → Importar.
- Importa `data_import/employees.csv`.
- Mapea Department y Manager; si no existen departamentos, Odoo te los crea.

6) Importar compras
- Compras → Órdenes de compra → Importar.
- Importa `data_import/purchase_orders.csv`.
- Confirma varias órdenes para generar entradas de stock si quieres.

7) Importar ventas
- Ventas → Órdenes de venta → Importar.
- Importa `data_import/sales_orders.csv`.
- Confirma algunas para generar entregas/facturas.

8) Sitio web (3 páginas mínimas)
- Sitio Web → Ir al sitio.
- Crea 3 páginas:
  1. “Servicios” (mantenimiento, frenos, suspensión, electricidad, diagnóstico).
  2. “Repuestos” (catálogo destacado de aceites, filtros, frenos, baterías).
  3. “Contacto” (dirección, teléfono, horarios, formulario).
- En el editor, agrega el logo y textos con el nombre “Terrabyte EC”.

9) Flujo demostrable end-to-end (ejemplo)
- Sitio Web → Tienda (asegúrate de publicar algunos productos).
- Desde el sitio: cliente agrega un producto al carrito → compra.
- En Ventas: confirma el pedido.
- En Facturación: genera y valida la factura.
- En Inventario: valida la entrega.

Si quieres, también puedo prepararte textos exactos para las 3 páginas y una lista de productos “destacados” para el sitio.

Siguientes pasos sugeridos:
1) Importa los CSV en el orden anterior para evitar errores de referencia.
2) Publica 10–15 productos en la tienda y prueba la compra.
3) Genera una factura desde una venta para cerrar el flujo.

---

## User

Mira vamos a ahacer lo siguiente, no tengo la mitad de lo que tu describes, necesito primero datos, vamos comenzar con ventas, lo que pueda pasarte una plantilla de importacion te la dejare en data_import, son archivos xls, suerte, vamos a iniciar con cotizaciones, ordenes, clientes (si hay plantilla), productos (si hay), hazlo

---

## Assistant (Build · GPT-5.2-Codex · 2.0s)

_Thinking:_



**Tool: glob**

**Input:**
```json
{
  "path": ".",
  "pattern": "data_import/*.xls*"
}
```

**Output:**
```
/home/alexander/Desktop/das/Mechanic_Workshop/data_import/clientes_template.xlsx
/home/alexander/Desktop/das/Mechanic_Workshop/data_import/productos_template.xls
```

---

## Assistant (Build · GPT-5.2-Codex · 6.1s)

_Thinking:_

**Planning Excel file reading**

Decided to use Python with pandas or openpyxl for reading and writing Excel files, with one bash call to inspect column names before filling templates.

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\nimport pandas as pd\nfor path in ['data_import/clientes_template.xlsx','data_import/productos_template.xls']:\n    try:\n        df = pd.read_excel(path)\n        print(path, list(df.columns))\n    except Exception as e:\n        print(path, 'ERROR', e)\nPY",
  "description": "Shows column headers for Excel templates"
}
```

**Output:**
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'pandas'

```

---

## Assistant (Build · GPT-5.2-Codex · 1.8s)

**Tool: glob**

**Input:**
```json
{
  "path": ".",
  "pattern": "data_import/*template*.csv"
}
```

**Output:**
```
No files found
```

---

## Assistant (Build · GPT-5.2-Codex · 6.4s)

_Thinking:_

**Testing Python openpyxl availability**

I'm checking if Python's openpyxl module is installed to read Excel templates, since pandas and other tools aren't available; if not, I may need to ask the user for CSV exports or template details.

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\ntry:\n    import openpyxl\n    print('openpyxl', openpyxl.__version__)\nexcept Exception as e:\n    print('openpyxl not available', e)\ntry:\n    import xlrd\n    print('xlrd', xlrd.__version__)\nexcept Exception as e:\n    print('xlrd not available', e)\nPY",
  "description": "Checks for Excel reader libraries"
}
```

**Output:**
```
openpyxl not available No module named 'openpyxl'
xlrd not available No module named 'xlrd'

```

---

## Assistant (Build · GPT-5.2-Codex · 8.6s)

_Thinking:_

**Planning XLSX header extraction**

I'm deciding to parse .xlsx files by unzipping and extracting the header row using Python's zipfile and xml.etree, since no libraries are allowed and reading .xls is harder. Next, I'll focus on extracting column headers from sheet1.xml and sharedStrings.

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\nimport zipfile\nimport xml.etree.ElementTree as ET\nfrom collections import defaultdict\n\npath = 'data_import/clientes_template.xlsx'\nns = {'a': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}\n\nwith zipfile.ZipFile(path) as z:\n    shared = []\n    if 'xl/sharedStrings.xml' in z.namelist():\n        shared_xml = ET.fromstring(z.read('xl/sharedStrings.xml'))\n        for si in shared_xml.findall('a:si', ns):\n            t = ''.join(node.text or '' for node in si.findall('.//a:t', ns))\n            shared.append(t)\n    sheet_name = 'xl/worksheets/sheet1.xml'\n    sheet_xml = ET.fromstring(z.read(sheet_name))\n    rows = sheet_xml.findall('.//a:sheetData/a:row', ns)\n    if not rows:\n        print('no rows')\n        raise SystemExit\n    first = rows[0]\n    cells = first.findall('a:c', ns)\n    headers = []\n    for c in cells:\n        v = c.find('a:v', ns)\n        if v is None:\n            headers.append('')\n            continue\n        if c.get('t') == 's':\n            idx = int(v.text)\n            headers.append(shared[idx] if idx < len(shared) else '')\n        else:\n            headers.append(v.text or '')\n    print(headers)\nPY",
  "description": "Parses header row from clientes template"
}
```

**Output:**
```
['name', 'is_company', 'company_name', 'country_id', 'state_id', 'zip', 'city', 'street', 'street2', 'phone', 'mobile', 'email', 'vat', 'bank_ids/bank', 'bank_ids/acc_number', '', '', '', '', '', '', '', '', '', '', '', '']

```

---

## Assistant (Build · GPT-5.2-Codex · 6.0s)

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\nimport pandas as pd\n# try with openpyxl not available; use xlrd? not available\nPY",
  "description": "Attempts to read xls (will fail without libs)"
}
```

**Output:**
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'pandas'

```

---

## Assistant (Build · GPT-5.2-Codex · 2.9s)

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\ntry:\n    import openpyxl, xlrd\nexcept Exception:\n    pass\nPY",
  "description": "No-op import check"
}
```

**Output:**
```
(no output)
```

---

## Assistant (Build · GPT-5.2-Codex · 2.9s)

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\nimport xlrd\nPY",
  "description": "Attempts to import xlrd"
}
```

**Output:**
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'xlrd'

```

---

## Assistant (Build · GPT-5.2-Codex · 2.8s)

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\nfrom pathlib import Path\nfrom olefile import OleFileIO\n\npath = Path('data_import/productos_template.xls')\nprint('exists', path.exists())\nPY",
  "description": "Checks xls with olefile"
}
```

**Output:**
```
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ModuleNotFoundError: No module named 'olefile'

```

---

## Assistant (Build · GPT-5.2-Codex · 2.5s)

**Tool: bash**

**Input:**
```json
{
  "command": "python - <<'PY'\nimport struct\nimport binascii\n\npath = 'data_import/productos_template.xls'\nwith open(path, 'rb') as f:\n    header = f.read(8)\nprint('header', binascii.hexlify(header))\nPY",
  "description": "Reads binary header of xls file"
}
```

**Output:**
```
header b'd0cf11e0a1b11ae1'

```

---

## Assistant (Build · GPT-5.2-Codex · 4.4s)

_Thinking:_

**Proposing template format and dependencies**

I'm planning to ask the user whether they prefer to convert Excel templates to CSV for filling or to allow installing Python packages like openpyxl and xlrd for XLSX support, since direct XLSX parsing without these libs isn't feasible.

Puedo llenarlos, pero ahora mismo no tengo librerías para escribir Excel (`.xlsx/.xls`) en este entorno. Dos opciones:

1) (Recomendado) Convierte las plantillas a CSV y las dejo listas con ~30 registros cada una.  
2) Dame permiso para instalar dependencias Python (`openpyxl` para `.xlsx` y `xlrd`/`olefile` para `.xls`) y lleno directamente los XLS/XLSX.

¿Cuál prefieres?

---

## User

como convierto a csv?

---

## Assistant (Build · GPT-5.2-Codex · 2.9s)

La forma más simple es desde Odoo o desde Excel/LibreOffice.

Opción A (LibreOffice/Excel)
1) Abre `data_import/clientes_template.xlsx`
2) Archivo → Guardar como → Tipo: `CSV UTF-8 (.csv)`
3) Repite con `data_import/productos_template.xls`

Opción B (Odoo, si ya tienes la plantilla ahí)
- En Odoo, al importar, puedes descargar plantilla y luego exportarla como CSV desde Excel/LibreOffice.

Si quieres, también puedo convertirlos yo por terminal y luego llenarlos. Para eso necesito que me permitas instalar una librería (`sudo apt-get install python3-openpyxl python3-xlrd` o `pip install openpyxl xlrd`).

---

## User

ya esta

---

## Assistant (Build · GPT-5.2-Codex · 1.7s)

_Thinking:_



**Tool: glob**

**Input:**
```json
{
  "path": ".",
  "pattern": "data_import/*.csv"
}
```

**Output:**
```
/home/alexander/Desktop/das/Mechanic_Workshop/data_import/productos_template.csv
/home/alexander/Desktop/das/Mechanic_Workshop/data_import/clientes_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 1.4s)

**Tool: read**

**Input:**
```json
{
  "filePath": "/home/alexander/Desktop/das/Mechanic_Workshop/data_import/clientes_template.csv"
}
```

**Output:**
```
<path>/home/alexander/Desktop/das/Mechanic_Workshop/data_import/clientes_template.csv</path>
<type>file</type>
<content>
1: ﻿name;is_company;company_name;country_id;state_id;zip;city;street;street2;phone;mobile;email;vat;bank_ids/bank;bank_ids/acc_number;;;;;;;;;;;;
2: Deco Addict;1;;US;California;94523;Pleasant Hill;77 Santa Barbara Rd;;+3210588558;;azure@example.com;BE0477472701;GEBABEBB;12554641;;;;;;;;;;;;
3: Azure Interior;1;;US;California;94538;Fremont;4557 De Silva St;;;+582126810538;vauxoo@yourcompany.example.com;;;;;;;;;;;;;;;
4: Brandon Freeman;0;Azure Interior;US;California;94538;Fremont;4557 De Silva St;;;355-687-3262;brandon.freeman55@example.com;;BEBABEBB;321654987;;;;;;;;;;;;
5: ;;;;;;;;;;;;;;;;;;;;;;;;;;
6: ;;;;;;;;;;;;;;;;;;;;;;;;;;
7: ;;;;;;;;;;;;;;;;;;;;;;;;;;
8: ;;;;;;;;;;;;;;;;;;;;;;;;;;
9: ;;;;;;;;;;;;;;;;;;;;;;;;;;
10: ;;;;;;;;;;;;;;;;;;;;;;;;;;
11: ;;;;;;;;;;;;;;;;;;;;;;;;;;
12: ;;;;;;;;;;;;;;;;;;;;;;;;;;
13: ;;;;;;;;;;;;;;;;;;;;;;;;;;
14: ;;;;;;;;;;;;;;;;;;;;;;;;;;
15: ;;;;;;;;;;;;;;;;;;;;;;;;;;
16: ;;;;;;;;;;;;;;;;;;;;;;;;;;
17: ;;;;;;;;;;;;;;;;;;;;;;;;;;
18: ;;;;;;;;;;;;;;;;;;;;;;;;;;
19: ;;;;;;;;;;;;;;;;;;;;;;;;;;
20: ;;;;;;;;;;;;;;;;;;;;;;;;;;
21: ;;;;;;;;;;;;;;;;;;;;;;;;;;
22: ;;;;;;;;;;;;;;;;;;;;;;;;;;
23: ;;;;;;;;;;;;;;;;;;;;;;;;;;
24: ;;;;;;;;;;;;;;;;;;;;;;;;;;
25: ;;;;;;;;;;;;;;;;;;;;;;;;;;
26: ;;;;;;;;;;;;;;;;;;;;;;;;;;
27: ;;;;;;;;;;;;;;;;;;;;;;;;;;
28: ;;;;;;;;;;;;;;;;;;;;;;;;;;
29: ;;;;;;;;;;;;;;;;;;;;;;;;;;
30: ;;;;;;;;;;;;;;;;;;;;;;;;;;
31: ;;;;;;;;;;;;;;;;;;;;;;;;;;
32: ;;;;;;;;;;;;;;;;;;;;;;;;;;
33: ;;;;;;;;;;;;;;;;;;;;;;;;;;
34: ;;;;;;;;;;;;;;;;;;;;;;;;;;
35: ;;;;;;;;;;;;;;;;;;;;;;;;;;
36: ;;;;;;;;;;;;;;;;;;;;;;;;;;
37: ;;;;;;;;;;;;;;;;;;;;;;;;;;
38: ;;;;;;;;;;;;;;;;;;;;;;;;;;
39: ;;;;;;;;;;;;;;;;;;;;;;;;;;
40: ;;;;;;;;;;;;;;;;;;;;;;;;;;
41: ;;;;;;;;;;;;;;;;;;;;;;;;;;
42: ;;;;;;;;;;;;;;;;;;;;;;;;;;
43: ;;;;;;;;;;;;;;;;;;;;;;;;;;
44: ;;;;;;;;;;;;;;;;;;;;;;;;;;
45: ;;;;;;;;;;;;;;;;;;;;;;;;;;
46: ;;;;;;;;;;;;;;;;;;;;;;;;;;
47: ;;;;;;;;;;;;;;;;;;;;;;;;;;
48: ;;;;;;;;;;;;;;;;;;;;;;;;;;
49: ;;;;;;;;;;;;;;;;;;;;;;;;;;
50: ;;;;;;;;;;;;;;;;;;;;;;;;;;
51: ;;;;;;;;;;;;;;;;;;;;;;;;;;
52: ;;;;;;;;;;;;;;;;;;;;;;;;;;
53: ;;;;;;;;;;;;;;;;;;;;;;;;;;
54: ;;;;;;;;;;;;;;;;;;;;;;;;;;
55: ;;;;;;;;;;;;;;;;;;;;;;;;;;
56: ;;;;;;;;;;;;;;;;;;;;;;;;;;
57: ;;;;;;;;;;;;;;;;;;;;;;;;;;
58: ;;;;;;;;;;;;;;;;;;;;;;;;;;
59: ;;;;;;;;;;;;;;;;;;;;;;;;;;
60: ;;;;;;;;;;;;;;;;;;;;;;;;;;
61: ;;;;;;;;;;;;;;;;;;;;;;;;;;
62: ;;;;;;;;;;;;;;;;;;;;;;;;;;
63: ;;;;;;;;;;;;;;;;;;;;;;;;;;
64: ;;;;;;;;;;;;;;;;;;;;;;;;;;
65: ;;;;;;;;;;;;;;;;;;;;;;;;;;
66: ;;;;;;;;;;;;;;;;;;;;;;;;;;
67: ;;;;;;;;;;;;;;;;;;;;;;;;;;
68: ;;;;;;;;;;;;;;;;;;;;;;;;;;
69: ;;;;;;;;;;;;;;;;;;;;;;;;;;
70: ;;;;;;;;;;;;;;;;;;;;;;;;;;
71: ;;;;;;;;;;;;;;;;;;;;;;;;;;
72: ;;;;;;;;;;;;;;;;;;;;;;;;;;
73: ;;;;;;;;;;;;;;;;;;;;;;;;;;
74: ;;;;;;;;;;;;;;;;;;;;;;;;;;
75: ;;;;;;;;;;;;;;;;;;;;;;;;;;
76: ;;;;;;;;;;;;;;;;;;;;;;;;;;
77: ;;;;;;;;;;;;;;;;;;;;;;;;;;
78: ;;;;;;;;;;;;;;;;;;;;;;;;;;
79: ;;;;;;;;;;;;;;;;;;;;;;;;;;
80: ;;;;;;;;;;;;;;;;;;;;;;;;;;
81: ;;;;;;;;;;;;;;;;;;;;;;;;;;
82: ;;;;;;;;;;;;;;;;;;;;;;;;;;
83: ;;;;;;;;;;;;;;;;;;;;;;;;;;
84: ;;;;;;;;;;;;;;;;;;;;;;;;;;
85: ;;;;;;;;;;;;;;;;;;;;;;;;;;
86: ;;;;;;;;;;;;;;;;;;;;;;;;;;
87: ;;;;;;;;;;;;;;;;;;;;;;;;;;
88: ;;;;;;;;;;;;;;;;;;;;;;;;;;
89: ;;;;;;;;;;;;;;;;;;;;;;;;;;
90: ;;;;;;;;;;;;;;;;;;;;;;;;;;
91: ;;;;;;;;;;;;;;;;;;;;;;;;;;
92: ;;;;;;;;;;;;;;;;;;;;;;;;;;
93: ;;;;;;;;;;;;;;;;;;;;;;;;;;
94: ;;;;;;;;;;;;;;;;;;;;;;;;;;
95: ;;;;;;;;;;;;;;;;;;;;;;;;;;
96: ;;;;;;;;;;;;;;;;;;;;;;;;;;
97: ;;;;;;;;;;;;;;;;;;;;;;;;;;
98: ;;;;;;;;;;;;;;;;;;;;;;;;;;
99: ;;;;;;;;;;;;;;;;;;;;;;;;;;
100: ;;;;;;;;;;;;;;;;;;;;;;;;;;
101: ;;;;;;;;;;;;;;;;;;;;;;;;;;
102: ;;;;;;;;;;;;;;;;;;;;;;;;;;
103: ;;;;;;;;;;;;;;;;;;;;;;;;;;
104: ;;;;;;;;;;;;;;;;;;;;;;;;;;
105: ;;;;;;;;;;;;;;;;;;;;;;;;;;
106: ;;;;;;;;;;;;;;;;;;;;;;;;;;
107: ;;;;;;;;;;;;;;;;;;;;;;;;;;
108: ;;;;;;;;;;;;;;;;;;;;;;;;;;
109: ;;;;;;;;;;;;;;;;;;;;;;;;;;
110: ;;;;;;;;;;;;;;;;;;;;;;;;;;
111: ;;;;;;;;;;;;;;;;;;;;;;;;;;
112: ;;;;;;;;;;;;;;;;;;;;;;;;;;
113: ;;;;;;;;;;;;;;;;;;;;;;;;;;
114: ;;;;;;;;;;;;;;;;;;;;;;;;;;
115: ;;;;;;;;;;;;;;;;;;;;;;;;;;
116: ;;;;;;;;;;;;;;;;;;;;;;;;;;
117: ;;;;;;;;;;;;;;;;;;;;;;;;;;
118: ;;;;;;;;;;;;;;;;;;;;;;;;;;
119: ;;;;;;;;;;;;;;;;;;;;;;;;;;
120: ;;;;;;;;;;;;;;;;;;;;;;;;;;
121: ;;;;;;;;;;;;;;;;;;;;;;;;;;
122: ;;;;;;;;;;;;;;;;;;;;;;;;;;
123: ;;;;;;;;;;;;;;;;;;;;;;;;;;
124: ;;;;;;;;;;;;;;;;;;;;;;;;;;
125: ;;;;;;;;;;;;;;;;;;;;;;;;;;
126: ;;;;;;;;;;;;;;;;;;;;;;;;;;
127: ;;;;;;;;;;;;;;;;;;;;;;;;;;
128: ;;;;;;;;;;;;;;;;;;;;;;;;;;
129: ;;;;;;;;;;;;;;;;;;;;;;;;;;
130: ;;;;;;;;;;;;;;;;;;;;;;;;;;
131: ;;;;;;;;;;;;;;;;;;;;;;;;;;
132: ;;;;;;;;;;;;;;;;;;;;;;;;;;
133: ;;;;;;;;;;;;;;;;;;;;;;;;;;
134: ;;;;;;;;;;;;;;;;;;;;;;;;;;
135: ;;;;;;;;;;;;;;;;;;;;;;;;;;
136: ;;;;;;;;;;;;;;;;;;;;;;;;;;
137: ;;;;;;;;;;;;;;;;;;;;;;;;;;
138: ;;;;;;;;;;;;;;;;;;;;;;;;;;
139: ;;;;;;;;;;;;;;;;;;;;;;;;;;
140: ;;;;;;;;;;;;;;;;;;;;;;;;;;
141: ;;;;;;;;;;;;;;;;;;;;;;;;;;
142: ;;;;;;;;;;;;;;;;;;;;;;;;;;
143: ;;;;;;;;;;;;;;;;;;;;;;;;;;
144: ;;;;;;;;;;;;;;;;;;;;;;;;;;
145: ;;;;;;;;;;;;;;;;;;;;;;;;;;
146: ;;;;;;;;;;;;;;;;;;;;;;;;;;
147: ;;;;;;;;;;;;;;;;;;;;;;;;;;
148: ;;;;;;;;;;;;;;;;;;;;;;;;;;
149: ;;;;;;;;;;;;;;;;;;;;;;;;;;
150: ;;;;;;;;;;;;;;;;;;;;;;;;;;
151: ;;;;;;;;;;;;;;;;;;;;;;;;;;
152: ;;;;;;;;;;;;;;;;;;;;;;;;;;
153: ;;;;;;;;;;;;;;;;;;;;;;;;;;
154: ;;;;;;;;;;;;;;;;;;;;;;;;;;
155: ;;;;;;;;;;;;;;;;;;;;;;;;;;
156: ;;;;;;;;;;;;;;;;;;;;;;;;;;
157: ;;;;;;;;;;;;;;;;;;;;;;;;;;
158: ;;;;;;;;;;;;;;;;;;;;;;;;;;
159: ;;;;;;;;;;;;;;;;;;;;;;;;;;
160: ;;;;;;;;;;;;;;;;;;;;;;;;;;
161: ;;;;;;;;;;;;;;;;;;;;;;;;;;
162: ;;;;;;;;;;;;;;;;;;;;;;;;;;
163: ;;;;;;;;;;;;;;;;;;;;;;;;;;
164: ;;;;;;;;;;;;;;;;;;;;;;;;;;
165: ;;;;;;;;;;;;;;;;;;;;;;;;;;
166: ;;;;;;;;;;;;;;;;;;;;;;;;;;
167: ;;;;;;;;;;;;;;;;;;;;;;;;;;
168: ;;;;;;;;;;;;;;;;;;;;;;;;;;
169: ;;;;;;;;;;;;;;;;;;;;;;;;;;
170: ;;;;;;;;;;;;;;;;;;;;;;;;;;
171: ;;;;;;;;;;;;;;;;;;;;;;;;;;
172: ;;;;;;;;;;;;;;;;;;;;;;;;;;
173: ;;;;;;;;;;;;;;;;;;;;;;;;;;
174: ;;;;;;;;;;;;;;;;;;;;;;;;;;
175: ;;;;;;;;;;;;;;;;;;;;;;;;;;
176: ;;;;;;;;;;;;;;;;;;;;;;;;;;
177: ;;;;;;;;;;;;;;;;;;;;;;;;;;
178: ;;;;;;;;;;;;;;;;;;;;;;;;;;
179: ;;;;;;;;;;;;;;;;;;;;;;;;;;
180: ;;;;;;;;;;;;;;;;;;;;;;;;;;
181: ;;;;;;;;;;;;;;;;;;;;;;;;;;
182: ;;;;;;;;;;;;;;;;;;;;;;;;;;
183: ;;;;;;;;;;;;;;;;;;;;;;;;;;
184: ;;;;;;;;;;;;;;;;;;;;;;;;;;
185: ;;;;;;;;;;;;;;;;;;;;;;;;;;
186: ;;;;;;;;;;;;;;;;;;;;;;;;;;
187: ;;;;;;;;;;;;;;;;;;;;;;;;;;
188: ;;;;;;;;;;;;;;;;;;;;;;;;;;
189: ;;;;;;;;;;;;;;;;;;;;;;;;;;
190: ;;;;;;;;;;;;;;;;;;;;;;;;;;
191: ;;;;;;;;;;;;;;;;;;;;;;;;;;
192: ;;;;;;;;;;;;;;;;;;;;;;;;;;
193: ;;;;;;;;;;;;;;;;;;;;;;;;;;
194: ;;;;;;;;;;;;;;;;;;;;;;;;;;
195: ;;;;;;;;;;;;;;;;;;;;;;;;;;
196: ;;;;;;;;;;;;;;;;;;;;;;;;;;
197: ;;;;;;;;;;;;;;;;;;;;;;;;;;
198: ;;;;;;;;;;;;;;;;;;;;;;;;;;
199: ;;;;;;;;;;;;;;;;;;;;;;;;;;
200: ;;;;;;;;;;;;;;;;;;;;;;;;;;
201: ;;;;;;;;;;;;;;;;;;;;;;;;;;
202: ;;;;;;;;;;;;;;;;;;;;;;;;;;
203: ;;;;;;;;;;;;;;;;;;;;;;;;;;
204: ;;;;;;;;;;;;;;;;;;;;;;;;;;
205: ;;;;;;;;;;;;;;;;;;;;;;;;;;
206: ;;;;;;;;;;;;;;;;;;;;;;;;;;
207: ;;;;;;;;;;;;;;;;;;;;;;;;;;
208: ;;;;;;;;;;;;;;;;;;;;;;;;;;
209: ;;;;;;;;;;;;;;;;;;;;;;;;;;
210: ;;;;;;;;;;;;;;;;;;;;;;;;;;
211: ;;;;;;;;;;;;;;;;;;;;;;;;;;
212: ;;;;;;;;;;;;;;;;;;;;;;;;;;
213: ;;;;;;;;;;;;;;;;;;;;;;;;;;
214: ;;;;;;;;;;;;;;;;;;;;;;;;;;
215: ;;;;;;;;;;;;;;;;;;;;;;;;;;
216: ;;;;;;;;;;;;;;;;;;;;;;;;;;
217: ;;;;;;;;;;;;;;;;;;;;;;;;;;
218: ;;;;;;;;;;;;;;;;;;;;;;;;;;
219: ;;;;;;;;;;;;;;;;;;;;;;;;;;
220: ;;;;;;;;;;;;;;;;;;;;;;;;;;
221: ;;;;;;;;;;;;;;;;;;;;;;;;;;
222: ;;;;;;;;;;;;;;;;;;;;;;;;;;
223: ;;;;;;;;;;;;;;;;;;;;;;;;;;
224: ;;;;;;;;;;;;;;;;;;;;;;;;;;
225: ;;;;;;;;;;;;;;;;;;;;;;;;;;
226: ;;;;;;;;;;;;;;;;;;;;;;;;;;
227: ;;;;;;;;;;;;;;;;;;;;;;;;;;
228: ;;;;;;;;;;;;;;;;;;;;;;;;;;
229: ;;;;;;;;;;;;;;;;;;;;;;;;;;
230: ;;;;;;;;;;;;;;;;;;;;;;;;;;
231: ;;;;;;;;;;;;;;;;;;;;;;;;;;
232: ;;;;;;;;;;;;;;;;;;;;;;;;;;
233: ;;;;;;;;;;;;;;;;;;;;;;;;;;
234: ;;;;;;;;;;;;;;;;;;;;;;;;;;
235: ;;;;;;;;;;;;;;;;;;;;;;;;;;
236: ;;;;;;;;;;;;;;;;;;;;;;;;;;
237: ;;;;;;;;;;;;;;;;;;;;;;;;;;
238: ;;;;;;;;;;;;;;;;;;;;;;;;;;
239: ;;;;;;;;;;;;;;;;;;;;;;;;;;
240: ;;;;;;;;;;;;;;;;;;;;;;;;;;
241: ;;;;;;;;;;;;;;;;;;;;;;;;;;
242: ;;;;;;;;;;;;;;;;;;;;;;;;;;
243: ;;;;;;;;;;;;;;;;;;;;;;;;;;
244: ;;;;;;;;;;;;;;;;;;;;;;;;;;
245: ;;;;;;;;;;;;;;;;;;;;;;;;;;
246: ;;;;;;;;;;;;;;;;;;;;;;;;;;
247: ;;;;;;;;;;;;;;;;;;;;;;;;;;
248: ;;;;;;;;;;;;;;;;;;;;;;;;;;
249: ;;;;;;;;;;;;;;;;;;;;;;;;;;
250: ;;;;;;;;;;;;;;;;;;;;;;;;;;
251: ;;;;;;;;;;;;;;;;;;;;;;;;;;
252: ;;;;;;;;;;;;;;;;;;;;;;;;;;
253: ;;;;;;;;;;;;;;;;;;;;;;;;;;
254: ;;;;;;;;;;;;;;;;;;;;;;;;;;
255: ;;;;;;;;;;;;;;;;;;;;;;;;;;
256: ;;;;;;;;;;;;;;;;;;;;;;;;;;
257: ;;;;;;;;;;;;;;;;;;;;;;;;;;
258: ;;;;;;;;;;;;;;;;;;;;;;;;;;
259: ;;;;;;;;;;;;;;;;;;;;;;;;;;
260: ;;;;;;;;;;;;;;;;;;;;;;;;;;
261: ;;;;;;;;;;;;;;;;;;;;;;;;;;
262: ;;;;;;;;;;;;;;;;;;;;;;;;;;
263: ;;;;;;;;;;;;;;;;;;;;;;;;;;
264: ;;;;;;;;;;;;;;;;;;;;;;;;;;
265: ;;;;;;;;;;;;;;;;;;;;;;;;;;
266: ;;;;;;;;;;;;;;;;;;;;;;;;;;
267: ;;;;;;;;;;;;;;;;;;;;;;;;;;
268: ;;;;;;;;;;;;;;;;;;;;;;;;;;
269: ;;;;;;;;;;;;;;;;;;;;;;;;;;
270: ;;;;;;;;;;;;;;;;;;;;;;;;;;
271: ;;;;;;;;;;;;;;;;;;;;;;;;;;
272: ;;;;;;;;;;;;;;;;;;;;;;;;;;
273: ;;;;;;;;;;;;;;;;;;;;;;;;;;
274: ;;;;;;;;;;;;;;;;;;;;;;;;;;
275: ;;;;;;;;;;;;;;;;;;;;;;;;;;
276: ;;;;;;;;;;;;;;;;;;;;;;;;;;
277: ;;;;;;;;;;;;;;;;;;;;;;;;;;
278: ;;;;;;;;;;;;;;;;;;;;;;;;;;
279: ;;;;;;;;;;;;;;;;;;;;;;;;;;
280: ;;;;;;;;;;;;;;;;;;;;;;;;;;
281: ;;;;;;;;;;;;;;;;;;;;;;;;;;
282: ;;;;;;;;;;;;;;;;;;;;;;;;;;
283: ;;;;;;;;;;;;;;;;;;;;;;;;;;
284: ;;;;;;;;;;;;;;;;;;;;;;;;;;
285: ;;;;;;;;;;;;;;;;;;;;;;;;;;
286: ;;;;;;;;;;;;;;;;;;;;;;;;;;
287: ;;;;;;;;;;;;;;;;;;;;;;;;;;
288: ;;;;;;;;;;;;;;;;;;;;;;;;;;
289: ;;;;;;;;;;;;;;;;;;;;;;;;;;
290: ;;;;;;;;;;;;;;;;;;;;;;;;;;
291: ;;;;;;;;;;;;;;;;;;;;;;;;;;
292: ;;;;;;;;;;;;;;;;;;;;;;;;;;
293: ;;;;;;;;;;;;;;;;;;;;;;;;;;
294: ;;;;;;;;;;;;;;;;;;;;;;;;;;
295: ;;;;;;;;;;;;;;;;;;;;;;;;;;
296: ;;;;;;;;;;;;;;;;;;;;;;;;;;
297: ;;;;;;;;;;;;;;;;;;;;;;;;;;
298: ;;;;;;;;;;;;;;;;;;;;;;;;;;
299: ;;;;;;;;;;;;;;;;;;;;;;;;;;
300: ;;;;;;;;;;;;;;;;;;;;;;;;;;
301: ;;;;;;;;;;;;;;;;;;;;;;;;;;
302: ;;;;;;;;;;;;;;;;;;;;;;;;;;
303: ;;;;;;;;;;;;;;;;;;;;;;;;;;
304: ;;;;;;;;;;;;;;;;;;;;;;;;;;
305: ;;;;;;;;;;;;;;;;;;;;;;;;;;
306: ;;;;;;;;;;;;;;;;;;;;;;;;;;
307: ;;;;;;;;;;;;;;;;;;;;;;;;;;
308: ;;;;;;;;;;;;;;;;;;;;;;;;;;
309: ;;;;;;;;;;;;;;;;;;;;;;;;;;
310: ;;;;;;;;;;;;;;;;;;;;;;;;;;
311: ;;;;;;;;;;;;;;;;;;;;;;;;;;
312: ;;;;;;;;;;;;;;;;;;;;;;;;;;
313: ;;;;;;;;;;;;;;;;;;;;;;;;;;
314: ;;;;;;;;;;;;;;;;;;;;;;;;;;
315: ;;;;;;;;;;;;;;;;;;;;;;;;;;
316: ;;;;;;;;;;;;;;;;;;;;;;;;;;
317: ;;;;;;;;;;;;;;;;;;;;;;;;;;
318: ;;;;;;;;;;;;;;;;;;;;;;;;;;
319: ;;;;;;;;;;;;;;;;;;;;;;;;;;
320: ;;;;;;;;;;;;;;;;;;;;;;;;;;
321: ;;;;;;;;;;;;;;;;;;;;;;;;;;
322: ;;;;;;;;;;;;;;;;;;;;;;;;;;
323: ;;;;;;;;;;;;;;;;;;;;;;;;;;
324: ;;;;;;;;;;;;;;;;;;;;;;;;;;
325: ;;;;;;;;;;;;;;;;;;;;;;;;;;
326: ;;;;;;;;;;;;;;;;;;;;;;;;;;
327: ;;;;;;;;;;;;;;;;;;;;;;;;;;
328: ;;;;;;;;;;;;;;;;;;;;;;;;;;
329: ;;;;;;;;;;;;;;;;;;;;;;;;;;
330: ;;;;;;;;;;;;;;;;;;;;;;;;;;
331: ;;;;;;;;;;;;;;;;;;;;;;;;;;
332: ;;;;;;;;;;;;;;;;;;;;;;;;;;
333: ;;;;;;;;;;;;;;;;;;;;;;;;;;
334: ;;;;;;;;;;;;;;;;;;;;;;;;;;
335: ;;;;;;;;;;;;;;;;;;;;;;;;;;
336: ;;;;;;;;;;;;;;;;;;;;;;;;;;
337: ;;;;;;;;;;;;;;;;;;;;;;;;;;
338: ;;;;;;;;;;;;;;;;;;;;;;;;;;
339: ;;;;;;;;;;;;;;;;;;;;;;;;;;
340: ;;;;;;;;;;;;;;;;;;;;;;;;;;
341: ;;;;;;;;;;;;;;;;;;;;;;;;;;
342: ;;;;;;;;;;;;;;;;;;;;;;;;;;
343: ;;;;;;;;;;;;;;;;;;;;;;;;;;
344: ;;;;;;;;;;;;;;;;;;;;;;;;;;
345: ;;;;;;;;;;;;;;;;;;;;;;;;;;
346: ;;;;;;;;;;;;;;;;;;;;;;;;;;
347: ;;;;;;;;;;;;;;;;;;;;;;;;;;
348: ;;;;;;;;;;;;;;;;;;;;;;;;;;
349: ;;;;;;;;;;;;;;;;;;;;;;;;;;
350: ;;;;;;;;;;;;;;;;;;;;;;;;;;
351: ;;;;;;;;;;;;;;;;;;;;;;;;;;
352: ;;;;;;;;;;;;;;;;;;;;;;;;;;
353: ;;;;;;;;;;;;;;;;;;;;;;;;;;
354: ;;;;;;;;;;;;;;;;;;;;;;;;;;
355: ;;;;;;;;;;;;;;;;;;;;;;;;;;
356: ;;;;;;;;;;;;;;;;;;;;;;;;;;
357: ;;;;;;;;;;;;;;;;;;;;;;;;;;
358: ;;;;;;;;;;;;;;;;;;;;;;;;;;
359: ;;;;;;;;;;;;;;;;;;;;;;;;;;
360: ;;;;;;;;;;;;;;;;;;;;;;;;;;
361: ;;;;;;;;;;;;;;;;;;;;;;;;;;
362: ;;;;;;;;;;;;;;;;;;;;;;;;;;
363: ;;;;;;;;;;;;;;;;;;;;;;;;;;
364: ;;;;;;;;;;;;;;;;;;;;;;;;;;
365: ;;;;;;;;;;;;;;;;;;;;;;;;;;
366: ;;;;;;;;;;;;;;;;;;;;;;;;;;
367: ;;;;;;;;;;;;;;;;;;;;;;;;;;
368: ;;;;;;;;;;;;;;;;;;;;;;;;;;
369: ;;;;;;;;;;;;;;;;;;;;;;;;;;
370: ;;;;;;;;;;;;;;;;;;;;;;;;;;
371: ;;;;;;;;;;;;;;;;;;;;;;;;;;
372: ;;;;;;;;;;;;;;;;;;;;;;;;;;
373: ;;;;;;;;;;;;;;;;;;;;;;;;;;
374: ;;;;;;;;;;;;;;;;;;;;;;;;;;
375: ;;;;;;;;;;;;;;;;;;;;;;;;;;
376: ;;;;;;;;;;;;;;;;;;;;;;;;;;
377: ;;;;;;;;;;;;;;;;;;;;;;;;;;
378: ;;;;;;;;;;;;;;;;;;;;;;;;;;
379: ;;;;;;;;;;;;;;;;;;;;;;;;;;
380: ;;;;;;;;;;;;;;;;;;;;;;;;;;
381: ;;;;;;;;;;;;;;;;;;;;;;;;;;
382: ;;;;;;;;;;;;;;;;;;;;;;;;;;
383: ;;;;;;;;;;;;;;;;;;;;;;;;;;
384: ;;;;;;;;;;;;;;;;;;;;;;;;;;
385: ;;;;;;;;;;;;;;;;;;;;;;;;;;
386: ;;;;;;;;;;;;;;;;;;;;;;;;;;
387: ;;;;;;;;;;;;;;;;;;;;;;;;;;
388: ;;;;;;;;;;;;;;;;;;;;;;;;;;
389: ;;;;;;;;;;;;;;;;;;;;;;;;;;
390: ;;;;;;;;;;;;;;;;;;;;;;;;;;
391: ;;;;;;;;;;;;;;;;;;;;;;;;;;
392: ;;;;;;;;;;;;;;;;;;;;;;;;;;
393: ;;;;;;;;;;;;;;;;;;;;;;;;;;
394: ;;;;;;;;;;;;;;;;;;;;;;;;;;
395: ;;;;;;;;;;;;;;;;;;;;;;;;;;
396: ;;;;;;;;;;;;;;;;;;;;;;;;;;
397: ;;;;;;;;;;;;;;;;;;;;;;;;;;
398: ;;;;;;;;;;;;;;;;;;;;;;;;;;
399: ;;;;;;;;;;;;;;;;;;;;;;;;;;
400: ;;;;;;;;;;;;;;;;;;;;;;;;;;
401: ;;;;;;;;;;;;;;;;;;;;;;;;;;
402: ;;;;;;;;;;;;;;;;;;;;;;;;;;
403: ;;;;;;;;;;;;;;;;;;;;;;;;;;
404: ;;;;;;;;;;;;;;;;;;;;;;;;;;
405: ;;;;;;;;;;;;;;;;;;;;;;;;;;
406: ;;;;;;;;;;;;;;;;;;;;;;;;;;
407: ;;;;;;;;;;;;;;;;;;;;;;;;;;
408: ;;;;;;;;;;;;;;;;;;;;;;;;;;
409: ;;;;;;;;;;;;;;;;;;;;;;;;;;
410: ;;;;;;;;;;;;;;;;;;;;;;;;;;
411: ;;;;;;;;;;;;;;;;;;;;;;;;;;
412: ;;;;;;;;;;;;;;;;;;;;;;;;;;
413: ;;;;;;;;;;;;;;;;;;;;;;;;;;
414: ;;;;;;;;;;;;;;;;;;;;;;;;;;
415: ;;;;;;;;;;;;;;;;;;;;;;;;;;
416: ;;;;;;;;;;;;;;;;;;;;;;;;;;
417: ;;;;;;;;;;;;;;;;;;;;;;;;;;
418: ;;;;;;;;;;;;;;;;;;;;;;;;;;
419: ;;;;;;;;;;;;;;;;;;;;;;;;;;
420: ;;;;;;;;;;;;;;;;;;;;;;;;;;
421: ;;;;;;;;;;;;;;;;;;;;;;;;;;
422: ;;;;;;;;;;;;;;;;;;;;;;;;;;
423: ;;;;;;;;;;;;;;;;;;;;;;;;;;
424: ;;;;;;;;;;;;;;;;;;;;;;;;;;
425: ;;;;;;;;;;;;;;;;;;;;;;;;;;
426: ;;;;;;;;;;;;;;;;;;;;;;;;;;
427: ;;;;;;;;;;;;;;;;;;;;;;;;;;
428: ;;;;;;;;;;;;;;;;;;;;;;;;;;
429: ;;;;;;;;;;;;;;;;;;;;;;;;;;
430: ;;;;;;;;;;;;;;;;;;;;;;;;;;
431: ;;;;;;;;;;;;;;;;;;;;;;;;;;
432: ;;;;;;;;;;;;;;;;;;;;;;;;;;
433: ;;;;;;;;;;;;;;;;;;;;;;;;;;
434: ;;;;;;;;;;;;;;;;;;;;;;;;;;
435: ;;;;;;;;;;;;;;;;;;;;;;;;;;
436: ;;;;;;;;;;;;;;;;;;;;;;;;;;
437: ;;;;;;;;;;;;;;;;;;;;;;;;;;
438: ;;;;;;;;;;;;;;;;;;;;;;;;;;
439: ;;;;;;;;;;;;;;;;;;;;;;;;;;
440: ;;;;;;;;;;;;;;;;;;;;;;;;;;
441: ;;;;;;;;;;;;;;;;;;;;;;;;;;
442: ;;;;;;;;;;;;;;;;;;;;;;;;;;
443: ;;;;;;;;;;;;;;;;;;;;;;;;;;
444: ;;;;;;;;;;;;;;;;;;;;;;;;;;
445: ;;;;;;;;;;;;;;;;;;;;;;;;;;
446: ;;;;;;;;;;;;;;;;;;;;;;;;;;
447: ;;;;;;;;;;;;;;;;;;;;;;;;;;
448: ;;;;;;;;;;;;;;;;;;;;;;;;;;
449: ;;;;;;;;;;;;;;;;;;;;;;;;;;
450: ;;;;;;;;;;;;;;;;;;;;;;;;;;
451: ;;;;;;;;;;;;;;;;;;;;;;;;;;
452: ;;;;;;;;;;;;;;;;;;;;;;;;;;
453: ;;;;;;;;;;;;;;;;;;;;;;;;;;
454: ;;;;;;;;;;;;;;;;;;;;;;;;;;
455: ;;;;;;;;;;;;;;;;;;;;;;;;;;
456: ;;;;;;;;;;;;;;;;;;;;;;;;;;
457: ;;;;;;;;;;;;;;;;;;;;;;;;;;
458: ;;;;;;;;;;;;;;;;;;;;;;;;;;
459: ;;;;;;;;;;;;;;;;;;;;;;;;;;
460: ;;;;;;;;;;;;;;;;;;;;;;;;;;
461: ;;;;;;;;;;;;;;;;;;;;;;;;;;
462: ;;;;;;;;;;;;;;;;;;;;;;;;;;
463: ;;;;;;;;;;;;;;;;;;;;;;;;;;
464: ;;;;;;;;;;;;;;;;;;;;;;;;;;
465: ;;;;;;;;;;;;;;;;;;;;;;;;;;
466: ;;;;;;;;;;;;;;;;;;;;;;;;;;
467: ;;;;;;;;;;;;;;;;;;;;;;;;;;
468: ;;;;;;;;;;;;;;;;;;;;;;;;;;
469: ;;;;;;;;;;;;;;;;;;;;;;;;;;
470: ;;;;;;;;;;;;;;;;;;;;;;;;;;
471: ;;;;;;;;;;;;;;;;;;;;;;;;;;
472: ;;;;;;;;;;;;;;;;;;;;;;;;;;
473: ;;;;;;;;;;;;;;;;;;;;;;;;;;
474: ;;;;;;;;;;;;;;;;;;;;;;;;;;
475: ;;;;;;;;;;;;;;;;;;;;;;;;;;
476: ;;;;;;;;;;;;;;;;;;;;;;;;;;
477: ;;;;;;;;;;;;;;;;;;;;;;;;;;
478: ;;;;;;;;;;;;;;;;;;;;;;;;;;
479: ;;;;;;;;;;;;;;;;;;;;;;;;;;
480: ;;;;;;;;;;;;;;;;;;;;;;;;;;
481: ;;;;;;;;;;;;;;;;;;;;;;;;;;
482: ;;;;;;;;;;;;;;;;;;;;;;;;;;
483: ;;;;;;;;;;;;;;;;;;;;;;;;;;
484: ;;;;;;;;;;;;;;;;;;;;;;;;;;
485: ;;;;;;;;;;;;;;;;;;;;;;;;;;
486: ;;;;;;;;;;;;;;;;;;;;;;;;;;
487: ;;;;;;;;;;;;;;;;;;;;;;;;;;
488: ;;;;;;;;;;;;;;;;;;;;;;;;;;
489: ;;;;;;;;;;;;;;;;;;;;;;;;;;
490: ;;;;;;;;;;;;;;;;;;;;;;;;;;
491: ;;;;;;;;;;;;;;;;;;;;;;;;;;
492: ;;;;;;;;;;;;;;;;;;;;;;;;;;
493: ;;;;;;;;;;;;;;;;;;;;;;;;;;
494: ;;;;;;;;;;;;;;;;;;;;;;;;;;
495: ;;;;;;;;;;;;;;;;;;;;;;;;;;
496: ;;;;;;;;;;;;;;;;;;;;;;;;;;
497: ;;;;;;;;;;;;;;;;;;;;;;;;;;
498: ;;;;;;;;;;;;;;;;;;;;;;;;;;
499: ;;;;;;;;;;;;;;;;;;;;;;;;;;
500: ;;;;;;;;;;;;;;;;;;;;;;;;;;
501: ;;;;;;;;;;;;;;;;;;;;;;;;;;
502: ;;;;;;;;;;;;;;;;;;;;;;;;;;
503: ;;;;;;;;;;;;;;;;;;;;;;;;;;
504: ;;;;;;;;;;;;;;;;;;;;;;;;;;
505: ;;;;;;;;;;;;;;;;;;;;;;;;;;
506: ;;;;;;;;;;;;;;;;;;;;;;;;;;
507: ;;;;;;;;;;;;;;;;;;;;;;;;;;
508: ;;;;;;;;;;;;;;;;;;;;;;;;;;
509: ;;;;;;;;;;;;;;;;;;;;;;;;;;
510: ;;;;;;;;;;;;;;;;;;;;;;;;;;
511: ;;;;;;;;;;;;;;;;;;;;;;;;;;
512: ;;;;;;;;;;;;;;;;;;;;;;;;;;
513: ;;;;;;;;;;;;;;;;;;;;;;;;;;
514: ;;;;;;;;;;;;;;;;;;;;;;;;;;
515: ;;;;;;;;;;;;;;;;;;;;;;;;;;
516: ;;;;;;;;;;;;;;;;;;;;;;;;;;
517: ;;;;;;;;;;;;;;;;;;;;;;;;;;
518: ;;;;;;;;;;;;;;;;;;;;;;;;;;
519: ;;;;;;;;;;;;;;;;;;;;;;;;;;
520: ;;;;;;;;;;;;;;;;;;;;;;;;;;
521: ;;;;;;;;;;;;;;;;;;;;;;;;;;
522: ;;;;;;;;;;;;;;;;;;;;;;;;;;
523: ;;;;;;;;;;;;;;;;;;;;;;;;;;
524: ;;;;;;;;;;;;;;;;;;;;;;;;;;
525: ;;;;;;;;;;;;;;;;;;;;;;;;;;
526: ;;;;;;;;;;;;;;;;;;;;;;;;;;
527: ;;;;;;;;;;;;;;;;;;;;;;;;;;
528: ;;;;;;;;;;;;;;;;;;;;;;;;;;
529: ;;;;;;;;;;;;;;;;;;;;;;;;;;
530: ;;;;;;;;;;;;;;;;;;;;;;;;;;
531: ;;;;;;;;;;;;;;;;;;;;;;;;;;
532: ;;;;;;;;;;;;;;;;;;;;;;;;;;
533: ;;;;;;;;;;;;;;;;;;;;;;;;;;
534: ;;;;;;;;;;;;;;;;;;;;;;;;;;
535: ;;;;;;;;;;;;;;;;;;;;;;;;;;
536: ;;;;;;;;;;;;;;;;;;;;;;;;;;
537: ;;;;;;;;;;;;;;;;;;;;;;;;;;
538: ;;;;;;;;;;;;;;;;;;;;;;;;;;
539: ;;;;;;;;;;;;;;;;;;;;;;;;;;
540: ;;;;;;;;;;;;;;;;;;;;;;;;;;
541: ;;;;;;;;;;;;;;;;;;;;;;;;;;
542: ;;;;;;;;;;;;;;;;;;;;;;;;;;
543: ;;;;;;;;;;;;;;;;;;;;;;;;;;
544: ;;;;;;;;;;;;;;;;;;;;;;;;;;
545: ;;;;;;;;;;;;;;;;;;;;;;;;;;
546: ;;;;;;;;;;;;;;;;;;;;;;;;;;
547: ;;;;;;;;;;;;;;;;;;;;;;;;;;
548: ;;;;;;;;;;;;;;;;;;;;;;;;;;
549: ;;;;;;;;;;;;;;;;;;;;;;;;;;
550: ;;;;;;;;;;;;;;;;;;;;;;;;;;
551: ;;;;;;;;;;;;;;;;;;;;;;;;;;
552: ;;;;;;;;;;;;;;;;;;;;;;;;;;
553: ;;;;;;;;;;;;;;;;;;;;;;;;;;
554: ;;;;;;;;;;;;;;;;;;;;;;;;;;
555: ;;;;;;;;;;;;;;;;;;;;;;;;;;
556: ;;;;;;;;;;;;;;;;;;;;;;;;;;
557: ;;;;;;;;;;;;;;;;;;;;;;;;;;
558: ;;;;;;;;;;;;;;;;;;;;;;;;;;
559: ;;;;;;;;;;;;;;;;;;;;;;;;;;
560: ;;;;;;;;;;;;;;;;;;;;;;;;;;
561: ;;;;;;;;;;;;;;;;;;;;;;;;;;
562: ;;;;;;;;;;;;;;;;;;;;;;;;;;
563: ;;;;;;;;;;;;;;;;;;;;;;;;;;
564: ;;;;;;;;;;;;;;;;;;;;;;;;;;
565: ;;;;;;;;;;;;;;;;;;;;;;;;;;
566: ;;;;;;;;;;;;;;;;;;;;;;;;;;
567: ;;;;;;;;;;;;;;;;;;;;;;;;;;
568: ;;;;;;;;;;;;;;;;;;;;;;;;;;
569: ;;;;;;;;;;;;;;;;;;;;;;;;;;
570: ;;;;;;;;;;;;;;;;;;;;;;;;;;
571: ;;;;;;;;;;;;;;;;;;;;;;;;;;
572: ;;;;;;;;;;;;;;;;;;;;;;;;;;
573: ;;;;;;;;;;;;;;;;;;;;;;;;;;
574: ;;;;;;;;;;;;;;;;;;;;;;;;;;
575: ;;;;;;;;;;;;;;;;;;;;;;;;;;
576: ;;;;;;;;;;;;;;;;;;;;;;;;;;
577: ;;;;;;;;;;;;;;;;;;;;;;;;;;
578: ;;;;;;;;;;;;;;;;;;;;;;;;;;
579: ;;;;;;;;;;;;;;;;;;;;;;;;;;
580: ;;;;;;;;;;;;;;;;;;;;;;;;;;
581: ;;;;;;;;;;;;;;;;;;;;;;;;;;
582: ;;;;;;;;;;;;;;;;;;;;;;;;;;
583: ;;;;;;;;;;;;;;;;;;;;;;;;;;
584: ;;;;;;;;;;;;;;;;;;;;;;;;;;
585: ;;;;;;;;;;;;;;;;;;;;;;;;;;
586: ;;;;;;;;;;;;;;;;;;;;;;;;;;
587: ;;;;;;;;;;;;;;;;;;;;;;;;;;
588: ;;;;;;;;;;;;;;;;;;;;;;;;;;
589: ;;;;;;;;;;;;;;;;;;;;;;;;;;
590: ;;;;;;;;;;;;;;;;;;;;;;;;;;
591: ;;;;;;;;;;;;;;;;;;;;;;;;;;
592: ;;;;;;;;;;;;;;;;;;;;;;;;;;
593: ;;;;;;;;;;;;;;;;;;;;;;;;;;
594: ;;;;;;;;;;;;;;;;;;;;;;;;;;
595: ;;;;;;;;;;;;;;;;;;;;;;;;;;
596: ;;;;;;;;;;;;;;;;;;;;;;;;;;
597: ;;;;;;;;;;;;;;;;;;;;;;;;;;
598: ;;;;;;;;;;;;;;;;;;;;;;;;;;
599: ;;;;;;;;;;;;;;;;;;;;;;;;;;
600: ;;;;;;;;;;;;;;;;;;;;;;;;;;
601: ;;;;;;;;;;;;;;;;;;;;;;;;;;
602: ;;;;;;;;;;;;;;;;;;;;;;;;;;
603: ;;;;;;;;;;;;;;;;;;;;;;;;;;
604: ;;;;;;;;;;;;;;;;;;;;;;;;;;
605: ;;;;;;;;;;;;;;;;;;;;;;;;;;
606: ;;;;;;;;;;;;;;;;;;;;;;;;;;
607: ;;;;;;;;;;;;;;;;;;;;;;;;;;
608: ;;;;;;;;;;;;;;;;;;;;;;;;;;
609: ;;;;;;;;;;;;;;;;;;;;;;;;;;
610: ;;;;;;;;;;;;;;;;;;;;;;;;;;
611: ;;;;;;;;;;;;;;;;;;;;;;;;;;
612: ;;;;;;;;;;;;;;;;;;;;;;;;;;
613: ;;;;;;;;;;;;;;;;;;;;;;;;;;
614: ;;;;;;;;;;;;;;;;;;;;;;;;;;
615: ;;;;;;;;;;;;;;;;;;;;;;;;;;
616: ;;;;;;;;;;;;;;;;;;;;;;;;;;
617: ;;;;;;;;;;;;;;;;;;;;;;;;;;
618: ;;;;;;;;;;;;;;;;;;;;;;;;;;
619: ;;;;;;;;;;;;;;;;;;;;;;;;;;
620: ;;;;;;;;;;;;;;;;;;;;;;;;;;
621: ;;;;;;;;;;;;;;;;;;;;;;;;;;
622: ;;;;;;;;;;;;;;;;;;;;;;;;;;
623: ;;;;;;;;;;;;;;;;;;;;;;;;;;
624: ;;;;;;;;;;;;;;;;;;;;;;;;;;
625: ;;;;;;;;;;;;;;;;;;;;;;;;;;
626: ;;;;;;;;;;;;;;;;;;;;;;;;;;
627: ;;;;;;;;;;;;;;;;;;;;;;;;;;
628: ;;;;;;;;;;;;;;;;;;;;;;;;;;
629: ;;;;;;;;;;;;;;;;;;;;;;;;;;
630: ;;;;;;;;;;;;;;;;;;;;;;;;;;
631: ;;;;;;;;;;;;;;;;;;;;;;;;;;
632: ;;;;;;;;;;;;;;;;;;;;;;;;;;
633: ;;;;;;;;;;;;;;;;;;;;;;;;;;
634: ;;;;;;;;;;;;;;;;;;;;;;;;;;
635: ;;;;;;;;;;;;;;;;;;;;;;;;;;
636: ;;;;;;;;;;;;;;;;;;;;;;;;;;
637: ;;;;;;;;;;;;;;;;;;;;;;;;;;
638: ;;;;;;;;;;;;;;;;;;;;;;;;;;
639: ;;;;;;;;;;;;;;;;;;;;;;;;;;
640: ;;;;;;;;;;;;;;;;;;;;;;;;;;
641: ;;;;;;;;;;;;;;;;;;;;;;;;;;
642: ;;;;;;;;;;;;;;;;;;;;;;;;;;
643: ;;;;;;;;;;;;;;;;;;;;;;;;;;
644: ;;;;;;;;;;;;;;;;;;;;;;;;;;
645: ;;;;;;;;;;;;;;;;;;;;;;;;;;
646: ;;;;;;;;;;;;;;;;;;;;;;;;;;
647: ;;;;;;;;;;;;;;;;;;;;;;;;;;
648: ;;;;;;;;;;;;;;;;;;;;;;;;;;
649: ;;;;;;;;;;;;;;;;;;;;;;;;;;
650: ;;;;;;;;;;;;;;;;;;;;;;;;;;
651: ;;;;;;;;;;;;;;;;;;;;;;;;;;
652: ;;;;;;;;;;;;;;;;;;;;;;;;;;
653: ;;;;;;;;;;;;;;;;;;;;;;;;;;
654: ;;;;;;;;;;;;;;;;;;;;;;;;;;
655: ;;;;;;;;;;;;;;;;;;;;;;;;;;
656: ;;;;;;;;;;;;;;;;;;;;;;;;;;
657: ;;;;;;;;;;;;;;;;;;;;;;;;;;
658: ;;;;;;;;;;;;;;;;;;;;;;;;;;
659: ;;;;;;;;;;;;;;;;;;;;;;;;;;
660: ;;;;;;;;;;;;;;;;;;;;;;;;;;
661: ;;;;;;;;;;;;;;;;;;;;;;;;;;
662: ;;;;;;;;;;;;;;;;;;;;;;;;;;
663: ;;;;;;;;;;;;;;;;;;;;;;;;;;
664: ;;;;;;;;;;;;;;;;;;;;;;;;;;
665: ;;;;;;;;;;;;;;;;;;;;;;;;;;
666: ;;;;;;;;;;;;;;;;;;;;;;;;;;
667: ;;;;;;;;;;;;;;;;;;;;;;;;;;
668: ;;;;;;;;;;;;;;;;;;;;;;;;;;
669: ;;;;;;;;;;;;;;;;;;;;;;;;;;
670: ;;;;;;;;;;;;;;;;;;;;;;;;;;
671: ;;;;;;;;;;;;;;;;;;;;;;;;;;
672: ;;;;;;;;;;;;;;;;;;;;;;;;;;
673: ;;;;;;;;;;;;;;;;;;;;;;;;;;
674: ;;;;;;;;;;;;;;;;;;;;;;;;;;
675: ;;;;;;;;;;;;;;;;;;;;;;;;;;
676: ;;;;;;;;;;;;;;;;;;;;;;;;;;
677: ;;;;;;;;;;;;;;;;;;;;;;;;;;
678: ;;;;;;;;;;;;;;;;;;;;;;;;;;
679: ;;;;;;;;;;;;;;;;;;;;;;;;;;
680: ;;;;;;;;;;;;;;;;;;;;;;;;;;
681: ;;;;;;;;;;;;;;;;;;;;;;;;;;
682: ;;;;;;;;;;;;;;;;;;;;;;;;;;
683: ;;;;;;;;;;;;;;;;;;;;;;;;;;
684: ;;;;;;;;;;;;;;;;;;;;;;;;;;
685: ;;;;;;;;;;;;;;;;;;;;;;;;;;
686: ;;;;;;;;;;;;;;;;;;;;;;;;;;
687: ;;;;;;;;;;;;;;;;;;;;;;;;;;
688: ;;;;;;;;;;;;;;;;;;;;;;;;;;
689: ;;;;;;;;;;;;;;;;;;;;;;;;;;
690: ;;;;;;;;;;;;;;;;;;;;;;;;;;
691: ;;;;;;;;;;;;;;;;;;;;;;;;;;
692: ;;;;;;;;;;;;;;;;;;;;;;;;;;
693: ;;;;;;;;;;;;;;;;;;;;;;;;;;
694: ;;;;;;;;;;;;;;;;;;;;;;;;;;
695: ;;;;;;;;;;;;;;;;;;;;;;;;;;
696: ;;;;;;;;;;;;;;;;;;;;;;;;;;
697: ;;;;;;;;;;;;;;;;;;;;;;;;;;
698: ;;;;;;;;;;;;;;;;;;;;;;;;;;
699: ;;;;;;;;;;;;;;;;;;;;;;;;;;
700: ;;;;;;;;;;;;;;;;;;;;;;;;;;
701: ;;;;;;;;;;;;;;;;;;;;;;;;;;
702: ;;;;;;;;;;;;;;;;;;;;;;;;;;
703: ;;;;;;;;;;;;;;;;;;;;;;;;;;
704: ;;;;;;;;;;;;;;;;;;;;;;;;;;
705: ;;;;;;;;;;;;;;;;;;;;;;;;;;
706: ;;;;;;;;;;;;;;;;;;;;;;;;;;
707: ;;;;;;;;;;;;;;;;;;;;;;;;;;
708: ;;;;;;;;;;;;;;;;;;;;;;;;;;
709: ;;;;;;;;;;;;;;;;;;;;;;;;;;
710: ;;;;;;;;;;;;;;;;;;;;;;;;;;
711: ;;;;;;;;;;;;;;;;;;;;;;;;;;
712: ;;;;;;;;;;;;;;;;;;;;;;;;;;
713: ;;;;;;;;;;;;;;;;;;;;;;;;;;
714: ;;;;;;;;;;;;;;;;;;;;;;;;;;
715: ;;;;;;;;;;;;;;;;;;;;;;;;;;
716: ;;;;;;;;;;;;;;;;;;;;;;;;;;
717: ;;;;;;;;;;;;;;;;;;;;;;;;;;
718: ;;;;;;;;;;;;;;;;;;;;;;;;;;
719: ;;;;;;;;;;;;;;;;;;;;;;;;;;
720: ;;;;;;;;;;;;;;;;;;;;;;;;;;
721: ;;;;;;;;;;;;;;;;;;;;;;;;;;
722: ;;;;;;;;;;;;;;;;;;;;;;;;;;
723: ;;;;;;;;;;;;;;;;;;;;;;;;;;
724: ;;;;;;;;;;;;;;;;;;;;;;;;;;
725: ;;;;;;;;;;;;;;;;;;;;;;;;;;
726: ;;;;;;;;;;;;;;;;;;;;;;;;;;
727: ;;;;;;;;;;;;;;;;;;;;;;;;;;
728: ;;;;;;;;;;;;;;;;;;;;;;;;;;
729: ;;;;;;;;;;;;;;;;;;;;;;;;;;
730: ;;;;;;;;;;;;;;;;;;;;;;;;;;
731: ;;;;;;;;;;;;;;;;;;;;;;;;;;
732: ;;;;;;;;;;;;;;;;;;;;;;;;;;
733: ;;;;;;;;;;;;;;;;;;;;;;;;;;
734: ;;;;;;;;;;;;;;;;;;;;;;;;;;
735: ;;;;;;;;;;;;;;;;;;;;;;;;;;
736: ;;;;;;;;;;;;;;;;;;;;;;;;;;
737: ;;;;;;;;;;;;;;;;;;;;;;;;;;
738: ;;;;;;;;;;;;;;;;;;;;;;;;;;
739: ;;;;;;;;;;;;;;;;;;;;;;;;;;
740: ;;;;;;;;;;;;;;;;;;;;;;;;;;
741: ;;;;;;;;;;;;;;;;;;;;;;;;;;
742: ;;;;;;;;;;;;;;;;;;;;;;;;;;
743: ;;;;;;;;;;;;;;;;;;;;;;;;;;
744: ;;;;;;;;;;;;;;;;;;;;;;;;;;
745: ;;;;;;;;;;;;;;;;;;;;;;;;;;
746: ;;;;;;;;;;;;;;;;;;;;;;;;;;
747: ;;;;;;;;;;;;;;;;;;;;;;;;;;
748: ;;;;;;;;;;;;;;;;;;;;;;;;;;
749: ;;;;;;;;;;;;;;;;;;;;;;;;;;
750: ;;;;;;;;;;;;;;;;;;;;;;;;;;
751: ;;;;;;;;;;;;;;;;;;;;;;;;;;
752: ;;;;;;;;;;;;;;;;;;;;;;;;;;
753: ;;;;;;;;;;;;;;;;;;;;;;;;;;
754: ;;;;;;;;;;;;;;;;;;;;;;;;;;
755: ;;;;;;;;;;;;;;;;;;;;;;;;;;
756: ;;;;;;;;;;;;;;;;;;;;;;;;;;
757: ;;;;;;;;;;;;;;;;;;;;;;;;;;
758: ;;;;;;;;;;;;;;;;;;;;;;;;;;
759: ;;;;;;;;;;;;;;;;;;;;;;;;;;
760: ;;;;;;;;;;;;;;;;;;;;;;;;;;
761: ;;;;;;;;;;;;;;;;;;;;;;;;;;
762: ;;;;;;;;;;;;;;;;;;;;;;;;;;
763: ;;;;;;;;;;;;;;;;;;;;;;;;;;
764: ;;;;;;;;;;;;;;;;;;;;;;;;;;
765: ;;;;;;;;;;;;;;;;;;;;;;;;;;
766: ;;;;;;;;;;;;;;;;;;;;;;;;;;
767: ;;;;;;;;;;;;;;;;;;;;;;;;;;
768: ;;;;;;;;;;;;;;;;;;;;;;;;;;
769: ;;;;;;;;;;;;;;;;;;;;;;;;;;
770: ;;;;;;;;;;;;;;;;;;;;;;;;;;
771: ;;;;;;;;;;;;;;;;;;;;;;;;;;
772: ;;;;;;;;;;;;;;;;;;;;;;;;;;
773: ;;;;;;;;;;;;;;;;;;;;;;;;;;
774: ;;;;;;;;;;;;;;;;;;;;;;;;;;
775: ;;;;;;;;;;;;;;;;;;;;;;;;;;
776: ;;;;;;;;;;;;;;;;;;;;;;;;;;
777: ;;;;;;;;;;;;;;;;;;;;;;;;;;
778: ;;;;;;;;;;;;;;;;;;;;;;;;;;
779: ;;;;;;;;;;;;;;;;;;;;;;;;;;
780: ;;;;;;;;;;;;;;;;;;;;;;;;;;
781: ;;;;;;;;;;;;;;;;;;;;;;;;;;
782: ;;;;;;;;;;;;;;;;;;;;;;;;;;
783: ;;;;;;;;;;;;;;;;;;;;;;;;;;
784: ;;;;;;;;;;;;;;;;;;;;;;;;;;
785: ;;;;;;;;;;;;;;;;;;;;;;;;;;
786: ;;;;;;;;;;;;;;;;;;;;;;;;;;
787: ;;;;;;;;;;;;;;;;;;;;;;;;;;
788: ;;;;;;;;;;;;;;;;;;;;;;;;;;
789: ;;;;;;;;;;;;;;;;;;;;;;;;;;
790: ;;;;;;;;;;;;;;;;;;;;;;;;;;
791: ;;;;;;;;;;;;;;;;;;;;;;;;;;
792: ;;;;;;;;;;;;;;;;;;;;;;;;;;
793: ;;;;;;;;;;;;;;;;;;;;;;;;;;
794: ;;;;;;;;;;;;;;;;;;;;;;;;;;
795: ;;;;;;;;;;;;;;;;;;;;;;;;;;
796: ;;;;;;;;;;;;;;;;;;;;;;;;;;
797: ;;;;;;;;;;;;;;;;;;;;;;;;;;
798: ;;;;;;;;;;;;;;;;;;;;;;;;;;
799: ;;;;;;;;;;;;;;;;;;;;;;;;;;
800: ;;;;;;;;;;;;;;;;;;;;;;;;;;
801: ;;;;;;;;;;;;;;;;;;;;;;;;;;
802: ;;;;;;;;;;;;;;;;;;;;;;;;;;
803: ;;;;;;;;;;;;;;;;;;;;;;;;;;
804: ;;;;;;;;;;;;;;;;;;;;;;;;;;
805: ;;;;;;;;;;;;;;;;;;;;;;;;;;
806: ;;;;;;;;;;;;;;;;;;;;;;;;;;
807: ;;;;;;;;;;;;;;;;;;;;;;;;;;
808: ;;;;;;;;;;;;;;;;;;;;;;;;;;
809: ;;;;;;;;;;;;;;;;;;;;;;;;;;
810: ;;;;;;;;;;;;;;;;;;;;;;;;;;
811: ;;;;;;;;;;;;;;;;;;;;;;;;;;
812: ;;;;;;;;;;;;;;;;;;;;;;;;;;
813: ;;;;;;;;;;;;;;;;;;;;;;;;;;
814: ;;;;;;;;;;;;;;;;;;;;;;;;;;
815: ;;;;;;;;;;;;;;;;;;;;;;;;;;
816: ;;;;;;;;;;;;;;;;;;;;;;;;;;
817: ;;;;;;;;;;;;;;;;;;;;;;;;;;
818: ;;;;;;;;;;;;;;;;;;;;;;;;;;
819: ;;;;;;;;;;;;;;;;;;;;;;;;;;
820: ;;;;;;;;;;;;;;;;;;;;;;;;;;
821: ;;;;;;;;;;;;;;;;;;;;;;;;;;
822: ;;;;;;;;;;;;;;;;;;;;;;;;;;
823: ;;;;;;;;;;;;;;;;;;;;;;;;;;
824: ;;;;;;;;;;;;;;;;;;;;;;;;;;
825: ;;;;;;;;;;;;;;;;;;;;;;;;;;
826: ;;;;;;;;;;;;;;;;;;;;;;;;;;
827: ;;;;;;;;;;;;;;;;;;;;;;;;;;
828: ;;;;;;;;;;;;;;;;;;;;;;;;;;
829: ;;;;;;;;;;;;;;;;;;;;;;;;;;
830: ;;;;;;;;;;;;;;;;;;;;;;;;;;
831: ;;;;;;;;;;;;;;;;;;;;;;;;;;
832: ;;;;;;;;;;;;;;;;;;;;;;;;;;
833: ;;;;;;;;;;;;;;;;;;;;;;;;;;
834: ;;;;;;;;;;;;;;;;;;;;;;;;;;
835: ;;;;;;;;;;;;;;;;;;;;;;;;;;
836: ;;;;;;;;;;;;;;;;;;;;;;;;;;
837: ;;;;;;;;;;;;;;;;;;;;;;;;;;
838: ;;;;;;;;;;;;;;;;;;;;;;;;;;
839: ;;;;;;;;;;;;;;;;;;;;;;;;;;
840: ;;;;;;;;;;;;;;;;;;;;;;;;;;
841: ;;;;;;;;;;;;;;;;;;;;;;;;;;
842: ;;;;;;;;;;;;;;;;;;;;;;;;;;
843: ;;;;;;;;;;;;;;;;;;;;;;;;;;
844: ;;;;;;;;;;;;;;;;;;;;;;;;;;
845: ;;;;;;;;;;;;;;;;;;;;;;;;;;
846: ;;;;;;;;;;;;;;;;;;;;;;;;;;
847: ;;;;;;;;;;;;;;;;;;;;;;;;;;
848: ;;;;;;;;;;;;;;;;;;;;;;;;;;
849: ;;;;;;;;;;;;;;;;;;;;;;;;;;
850: ;;;;;;;;;;;;;;;;;;;;;;;;;;
851: ;;;;;;;;;;;;;;;;;;;;;;;;;;
852: ;;;;;;;;;;;;;;;;;;;;;;;;;;
853: ;;;;;;;;;;;;;;;;;;;;;;;;;;
854: ;;;;;;;;;;;;;;;;;;;;;;;;;;
855: ;;;;;;;;;;;;;;;;;;;;;;;;;;
856: ;;;;;;;;;;;;;;;;;;;;;;;;;;
857: ;;;;;;;;;;;;;;;;;;;;;;;;;;
858: ;;;;;;;;;;;;;;;;;;;;;;;;;;
859: ;;;;;;;;;;;;;;;;;;;;;;;;;;
860: ;;;;;;;;;;;;;;;;;;;;;;;;;;
861: ;;;;;;;;;;;;;;;;;;;;;;;;;;
862: ;;;;;;;;;;;;;;;;;;;;;;;;;;
863: ;;;;;;;;;;;;;;;;;;;;;;;;;;
864: ;;;;;;;;;;;;;;;;;;;;;;;;;;
865: ;;;;;;;;;;;;;;;;;;;;;;;;;;
866: ;;;;;;;;;;;;;;;;;;;;;;;;;;
867: ;;;;;;;;;;;;;;;;;;;;;;;;;;
868: ;;;;;;;;;;;;;;;;;;;;;;;;;;
869: ;;;;;;;;;;;;;;;;;;;;;;;;;;
870: ;;;;;;;;;;;;;;;;;;;;;;;;;;
871: ;;;;;;;;;;;;;;;;;;;;;;;;;;
872: ;;;;;;;;;;;;;;;;;;;;;;;;;;
873: ;;;;;;;;;;;;;;;;;;;;;;;;;;
874: ;;;;;;;;;;;;;;;;;;;;;;;;;;
875: ;;;;;;;;;;;;;;;;;;;;;;;;;;
876: ;;;;;;;;;;;;;;;;;;;;;;;;;;
877: ;;;;;;;;;;;;;;;;;;;;;;;;;;
878: ;;;;;;;;;;;;;;;;;;;;;;;;;;
879: ;;;;;;;;;;;;;;;;;;;;;;;;;;
880: ;;;;;;;;;;;;;;;;;;;;;;;;;;
881: ;;;;;;;;;;;;;;;;;;;;;;;;;;
882: ;;;;;;;;;;;;;;;;;;;;;;;;;;
883: ;;;;;;;;;;;;;;;;;;;;;;;;;;
884: ;;;;;;;;;;;;;;;;;;;;;;;;;;
885: ;;;;;;;;;;;;;;;;;;;;;;;;;;
886: ;;;;;;;;;;;;;;;;;;;;;;;;;;
887: ;;;;;;;;;;;;;;;;;;;;;;;;;;
888: ;;;;;;;;;;;;;;;;;;;;;;;;;;
889: ;;;;;;;;;;;;;;;;;;;;;;;;;;
890: ;;;;;;;;;;;;;;;;;;;;;;;;;;
891: ;;;;;;;;;;;;;;;;;;;;;;;;;;
892: ;;;;;;;;;;;;;;;;;;;;;;;;;;
893: ;;;;;;;;;;;;;;;;;;;;;;;;;;
894: ;;;;;;;;;;;;;;;;;;;;;;;;;;
895: ;;;;;;;;;;;;;;;;;;;;;;;;;;
896: ;;;;;;;;;;;;;;;;;;;;;;;;;;
897: ;;;;;;;;;;;;;;;;;;;;;;;;;;
898: ;;;;;;;;;;;;;;;;;;;;;;;;;;
899: ;;;;;;;;;;;;;;;;;;;;;;;;;;
900: ;;;;;;;;;;;;;;;;;;;;;;;;;;
901: ;;;;;;;;;;;;;;;;;;;;;;;;;;
902: ;;;;;;;;;;;;;;;;;;;;;;;;;;
903: ;;;;;;;;;;;;;;;;;;;;;;;;;;
904: ;;;;;;;;;;;;;;;;;;;;;;;;;;
905: ;;;;;;;;;;;;;;;;;;;;;;;;;;
906: ;;;;;;;;;;;;;;;;;;;;;;;;;;
907: ;;;;;;;;;;;;;;;;;;;;;;;;;;
908: ;;;;;;;;;;;;;;;;;;;;;;;;;;
909: ;;;;;;;;;;;;;;;;;;;;;;;;;;
910: ;;;;;;;;;;;;;;;;;;;;;;;;;;
911: ;;;;;;;;;;;;;;;;;;;;;;;;;;
912: ;;;;;;;;;;;;;;;;;;;;;;;;;;
913: ;;;;;;;;;;;;;;;;;;;;;;;;;;
914: ;;;;;;;;;;;;;;;;;;;;;;;;;;
915: ;;;;;;;;;;;;;;;;;;;;;;;;;;
916: ;;;;;;;;;;;;;;;;;;;;;;;;;;
917: ;;;;;;;;;;;;;;;;;;;;;;;;;;
918: ;;;;;;;;;;;;;;;;;;;;;;;;;;
919: ;;;;;;;;;;;;;;;;;;;;;;;;;;
920: ;;;;;;;;;;;;;;;;;;;;;;;;;;
921: ;;;;;;;;;;;;;;;;;;;;;;;;;;
922: ;;;;;;;;;;;;;;;;;;;;;;;;;;
923: ;;;;;;;;;;;;;;;;;;;;;;;;;;
924: ;;;;;;;;;;;;;;;;;;;;;;;;;;
925: ;;;;;;;;;;;;;;;;;;;;;;;;;;
926: ;;;;;;;;;;;;;;;;;;;;;;;;;;
927: ;;;;;;;;;;;;;;;;;;;;;;;;;;
928: ;;;;;;;;;;;;;;;;;;;;;;;;;;
929: ;;;;;;;;;;;;;;;;;;;;;;;;;;
930: ;;;;;;;;;;;;;;;;;;;;;;;;;;
931: ;;;;;;;;;;;;;;;;;;;;;;;;;;
932: ;;;;;;;;;;;;;;;;;;;;;;;;;;
933: ;;;;;;;;;;;;;;;;;;;;;;;;;;
934: ;;;;;;;;;;;;;;;;;;;;;;;;;;
935: ;;;;;;;;;;;;;;;;;;;;;;;;;;
936: ;;;;;;;;;;;;;;;;;;;;;;;;;;
937: ;;;;;;;;;;;;;;;;;;;;;;;;;;
938: ;;;;;;;;;;;;;;;;;;;;;;;;;;
939: ;;;;;;;;;;;;;;;;;;;;;;;;;;
940: ;;;;;;;;;;;;;;;;;;;;;;;;;;
941: ;;;;;;;;;;;;;;;;;;;;;;;;;;
942: ;;;;;;;;;;;;;;;;;;;;;;;;;;
943: ;;;;;;;;;;;;;;;;;;;;;;;;;;
944: ;;;;;;;;;;;;;;;;;;;;;;;;;;
945: ;;;;;;;;;;;;;;;;;;;;;;;;;;
946: ;;;;;;;;;;;;;;;;;;;;;;;;;;
947: ;;;;;;;;;;;;;;;;;;;;;;;;;;
948: ;;;;;;;;;;;;;;;;;;;;;;;;;;
949: ;;;;;;;;;;;;;;;;;;;;;;;;;;
950: ;;;;;;;;;;;;;;;;;;;;;;;;;;
951: ;;;;;;;;;;;;;;;;;;;;;;;;;;
952: ;;;;;;;;;;;;;;;;;;;;;;;;;;
953: ;;;;;;;;;;;;;;;;;;;;;;;;;;
954: ;;;;;;;;;;;;;;;;;;;;;;;;;;
955: ;;;;;;;;;;;;;;;;;;;;;;;;;;
956: ;;;;;;;;;;;;;;;;;;;;;;;;;;
957: ;;;;;;;;;;;;;;;;;;;;;;;;;;
958: ;;;;;;;;;;;;;;;;;;;;;;;;;;
959: ;;;;;;;;;;;;;;;;;;;;;;;;;;
960: ;;;;;;;;;;;;;;;;;;;;;;;;;;
961: ;;;;;;;;;;;;;;;;;;;;;;;;;;
962: ;;;;;;;;;;;;;;;;;;;;;;;;;;
963: ;;;;;;;;;;;;;;;;;;;;;;;;;;
964: ;;;;;;;;;;;;;;;;;;;;;;;;;;
965: ;;;;;;;;;;;;;;;;;;;;;;;;;;
966: ;;;;;;;;;;;;;;;;;;;;;;;;;;
967: ;;;;;;;;;;;;;;;;;;;;;;;;;;
968: ;;;;;;;;;;;;;;;;;;;;;;;;;;
969: ;;;;;;;;;;;;;;;;;;;;;;;;;;
970: ;;;;;;;;;;;;;;;;;;;;;;;;;;
971: ;;;;;;;;;;;;;;;;;;;;;;;;;;
972: ;;;;;;;;;;;;;;;;;;;;;;;;;;
973: ;;;;;;;;;;;;;;;;;;;;;;;;;;
974: ;;;;;;;;;;;;;;;;;;;;;;;;;;
975: ;;;;;;;;;;;;;;;;;;;;;;;;;;
976: ;;;;;;;;;;;;;;;;;;;;;;;;;;
977: ;;;;;;;;;;;;;;;;;;;;;;;;;;
978: ;;;;;;;;;;;;;;;;;;;;;;;;;;
979: ;;;;;;;;;;;;;;;;;;;;;;;;;;
980: ;;;;;;;;;;;;;;;;;;;;;;;;;;
981: ;;;;;;;;;;;;;;;;;;;;;;;;;;
982: ;;;;;;;;;;;;;;;;;;;;;;;;;;
983: ;;;;;;;;;;;;;;;;;;;;;;;;;;
984: ;;;;;;;;;;;;;;;;;;;;;;;;;;
985: ;;;;;;;;;;;;;;;;;;;;;;;;;;
986: ;;;;;;;;;;;;;;;;;;;;;;;;;;
987: ;;;;;;;;;;;;;;;;;;;;;;;;;;
988: ;;;;;;;;;;;;;;;;;;;;;;;;;;
989: ;;;;;;;;;;;;;;;;;;;;;;;;;;
990: ;;;;;;;;;;;;;;;;;;;;;;;;;;
991: ;;;;;;;;;;;;;;;;;;;;;;;;;;
992: ;;;;;;;;;;;;;;;;;;;;;;;;;;
993: ;;;;;;;;;;;;;;;;;;;;;;;;;;
994: ;;;;;;;;;;;;;;;;;;;;;;;;;;
995: ;;;;;;;;;;;;;;;;;;;;;;;;;;
996: ;;;;;;;;;;;;;;;;;;;;;;;;;;
997: ;;;;;;;;;;;;;;;;;;;;;;;;;;
998: ;;;;;;;;;;;;;;;;;;;;;;;;;;
999: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1000: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1001: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1002: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1003: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1004: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1005: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1006: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1007: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1008: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1009: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1010: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1011: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1012: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1013: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1014: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1015: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1016: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1017: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1018: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1019: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1020: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1021: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1022: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1023: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1024: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1025: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1026: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1027: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1028: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1029: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1030: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1031: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1032: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1033: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1034: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1035: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1036: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1037: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1038: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1039: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1040: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1041: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1042: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1043: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1044: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1045: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1046: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1047: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1048: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1049: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1050: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1051: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1052: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1053: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1054: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1055: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1056: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1057: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1058: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1059: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1060: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1061: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1062: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1063: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1064: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1065: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1066: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1067: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1068: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1069: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1070: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1071: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1072: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1073: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1074: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1075: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1076: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1077: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1078: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1079: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1080: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1081: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1082: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1083: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1084: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1085: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1086: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1087: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1088: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1089: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1090: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1091: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1092: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1093: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1094: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1095: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1096: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1097: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1098: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1099: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1100: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1101: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1102: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1103: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1104: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1105: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1106: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1107: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1108: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1109: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1110: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1111: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1112: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1113: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1114: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1115: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1116: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1117: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1118: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1119: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1120: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1121: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1122: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1123: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1124: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1125: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1126: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1127: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1128: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1129: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1130: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1131: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1132: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1133: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1134: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1135: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1136: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1137: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1138: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1139: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1140: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1141: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1142: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1143: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1144: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1145: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1146: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1147: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1148: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1149: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1150: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1151: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1152: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1153: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1154: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1155: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1156: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1157: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1158: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1159: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1160: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1161: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1162: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1163: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1164: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1165: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1166: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1167: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1168: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1169: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1170: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1171: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1172: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1173: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1174: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1175: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1176: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1177: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1178: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1179: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1180: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1181: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1182: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1183: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1184: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1185: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1186: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1187: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1188: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1189: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1190: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1191: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1192: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1193: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1194: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1195: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1196: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1197: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1198: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1199: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1200: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1201: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1202: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1203: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1204: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1205: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1206: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1207: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1208: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1209: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1210: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1211: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1212: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1213: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1214: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1215: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1216: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1217: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1218: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1219: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1220: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1221: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1222: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1223: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1224: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1225: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1226: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1227: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1228: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1229: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1230: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1231: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1232: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1233: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1234: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1235: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1236: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1237: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1238: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1239: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1240: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1241: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1242: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1243: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1244: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1245: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1246: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1247: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1248: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1249: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1250: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1251: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1252: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1253: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1254: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1255: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1256: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1257: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1258: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1259: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1260: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1261: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1262: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1263: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1264: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1265: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1266: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1267: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1268: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1269: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1270: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1271: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1272: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1273: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1274: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1275: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1276: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1277: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1278: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1279: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1280: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1281: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1282: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1283: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1284: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1285: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1286: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1287: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1288: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1289: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1290: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1291: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1292: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1293: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1294: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1295: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1296: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1297: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1298: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1299: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1300: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1301: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1302: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1303: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1304: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1305: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1306: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1307: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1308: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1309: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1310: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1311: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1312: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1313: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1314: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1315: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1316: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1317: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1318: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1319: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1320: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1321: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1322: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1323: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1324: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1325: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1326: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1327: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1328: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1329: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1330: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1331: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1332: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1333: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1334: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1335: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1336: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1337: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1338: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1339: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1340: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1341: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1342: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1343: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1344: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1345: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1346: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1347: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1348: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1349: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1350: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1351: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1352: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1353: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1354: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1355: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1356: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1357: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1358: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1359: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1360: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1361: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1362: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1363: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1364: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1365: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1366: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1367: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1368: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1369: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1370: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1371: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1372: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1373: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1374: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1375: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1376: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1377: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1378: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1379: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1380: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1381: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1382: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1383: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1384: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1385: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1386: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1387: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1388: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1389: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1390: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1391: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1392: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1393: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1394: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1395: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1396: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1397: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1398: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1399: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1400: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1401: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1402: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1403: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1404: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1405: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1406: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1407: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1408: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1409: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1410: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1411: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1412: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1413: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1414: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1415: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1416: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1417: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1418: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1419: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1420: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1421: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1422: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1423: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1424: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1425: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1426: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1427: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1428: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1429: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1430: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1431: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1432: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1433: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1434: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1435: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1436: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1437: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1438: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1439: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1440: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1441: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1442: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1443: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1444: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1445: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1446: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1447: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1448: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1449: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1450: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1451: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1452: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1453: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1454: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1455: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1456: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1457: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1458: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1459: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1460: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1461: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1462: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1463: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1464: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1465: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1466: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1467: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1468: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1469: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1470: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1471: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1472: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1473: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1474: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1475: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1476: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1477: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1478: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1479: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1480: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1481: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1482: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1483: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1484: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1485: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1486: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1487: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1488: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1489: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1490: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1491: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1492: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1493: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1494: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1495: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1496: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1497: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1498: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1499: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1500: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1501: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1502: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1503: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1504: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1505: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1506: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1507: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1508: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1509: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1510: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1511: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1512: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1513: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1514: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1515: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1516: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1517: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1518: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1519: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1520: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1521: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1522: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1523: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1524: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1525: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1526: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1527: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1528: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1529: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1530: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1531: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1532: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1533: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1534: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1535: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1536: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1537: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1538: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1539: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1540: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1541: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1542: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1543: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1544: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1545: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1546: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1547: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1548: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1549: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1550: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1551: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1552: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1553: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1554: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1555: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1556: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1557: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1558: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1559: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1560: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1561: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1562: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1563: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1564: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1565: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1566: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1567: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1568: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1569: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1570: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1571: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1572: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1573: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1574: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1575: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1576: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1577: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1578: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1579: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1580: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1581: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1582: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1583: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1584: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1585: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1586: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1587: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1588: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1589: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1590: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1591: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1592: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1593: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1594: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1595: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1596: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1597: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1598: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1599: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1600: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1601: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1602: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1603: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1604: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1605: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1606: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1607: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1608: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1609: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1610: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1611: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1612: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1613: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1614: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1615: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1616: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1617: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1618: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1619: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1620: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1621: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1622: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1623: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1624: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1625: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1626: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1627: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1628: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1629: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1630: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1631: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1632: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1633: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1634: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1635: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1636: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1637: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1638: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1639: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1640: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1641: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1642: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1643: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1644: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1645: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1646: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1647: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1648: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1649: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1650: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1651: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1652: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1653: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1654: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1655: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1656: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1657: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1658: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1659: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1660: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1661: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1662: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1663: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1664: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1665: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1666: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1667: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1668: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1669: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1670: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1671: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1672: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1673: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1674: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1675: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1676: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1677: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1678: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1679: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1680: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1681: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1682: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1683: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1684: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1685: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1686: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1687: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1688: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1689: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1690: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1691: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1692: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1693: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1694: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1695: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1696: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1697: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1698: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1699: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1700: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1701: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1702: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1703: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1704: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1705: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1706: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1707: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1708: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1709: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1710: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1711: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1712: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1713: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1714: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1715: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1716: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1717: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1718: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1719: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1720: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1721: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1722: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1723: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1724: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1725: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1726: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1727: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1728: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1729: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1730: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1731: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1732: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1733: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1734: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1735: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1736: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1737: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1738: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1739: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1740: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1741: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1742: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1743: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1744: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1745: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1746: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1747: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1748: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1749: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1750: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1751: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1752: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1753: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1754: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1755: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1756: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1757: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1758: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1759: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1760: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1761: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1762: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1763: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1764: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1765: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1766: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1767: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1768: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1769: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1770: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1771: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1772: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1773: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1774: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1775: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1776: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1777: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1778: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1779: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1780: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1781: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1782: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1783: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1784: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1785: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1786: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1787: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1788: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1789: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1790: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1791: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1792: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1793: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1794: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1795: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1796: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1797: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1798: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1799: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1800: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1801: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1802: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1803: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1804: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1805: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1806: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1807: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1808: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1809: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1810: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1811: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1812: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1813: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1814: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1815: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1816: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1817: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1818: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1819: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1820: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1821: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1822: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1823: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1824: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1825: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1826: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1827: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1828: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1829: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1830: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1831: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1832: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1833: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1834: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1835: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1836: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1837: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1838: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1839: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1840: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1841: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1842: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1843: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1844: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1845: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1846: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1847: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1848: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1849: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1850: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1851: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1852: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1853: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1854: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1855: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1856: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1857: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1858: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1859: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1860: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1861: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1862: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1863: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1864: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1865: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1866: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1867: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1868: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1869: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1870: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1871: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1872: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1873: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1874: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1875: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1876: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1877: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1878: ;;;;;;;;;;;;;;;;;;;;;;;;;;
1879: ;;;;;;;;;;;;;;;;;;;;;;;;;;

(Output capped at 50 KB. Showing lines 1-1879. Use offset=1880 to continue.)
</content>
```

---

## Assistant (Build · GPT-5.2-Codex · 1.8s)

**Tool: read**

**Input:**
```json
{
  "filePath": "/home/alexander/Desktop/das/Mechanic_Workshop/data_import/productos_template.csv"
}
```

**Output:**
```
<path>/home/alexander/Desktop/das/Mechanic_Workshop/data_import/productos_template.csv</path>
<type>file</type>
<content>
1: ﻿External ID;Name;Product Type;Internal Reference;Barcode;Sales Price;Cost;Weight;Sales Description
2: product_template_1;Apple In-Ear Headphones;Goods;E-COM08;;79;7044;;"Frequency: 5Hz to 21kHz
3: Impedance: 23 ohms
4: Sensitivity: 109 dB SPL/mW
5: Drivers: two-way balanced armature
6: Cable length: 1065 mm
7: Weight: 10.2 grams"
8: product_template_2;Apple Wireless Keyboard;Goods;E-COM10;;47;10;;The sleek aluminium Apple Wireless Keyboard.
9: product_template_3;Bose Mini Bluetooth Speaker;Goods;E-COM05;;247;140;;Bose's smallest portable Bluetooth speaker
10: product_template_4;iMac;Goods;E-COM09;;1799;1299;9,54;"2.7GHz quad-core Intel Core i5
11:  Turbo Boost up to 3.2GHz
12:  8GB (two 4GB) memory
13:  1TB hard drive
14:  Intel Iris Pro graphics"
15: product_template_5;iPod;Goods;E-COM12;;89;79;;"Height: 76.5 mm
16: Width: 39.6 mm
17: Depth: 5.4 mm
18: Weight: 31 grams"
19: product_template_6;iPad Mini;Goods;E-COM07;54398267125;320;260;0,33;"Color: White
20: Capacity: 16GB
21: Connectivity: Wifi
22: Beautiful 7.9-inch display
23: Over 375,000 apps
24: Ultrafast wireless
25: iOS7"
26: product_template_7;iPad Retina Display;Goods;E-COM01;;750;450;;"7.9‑inch (diagonal) LED-backlit, 128Gb
27: Dual-core A5 with quad-core graphics
28: FaceTime HD Camera, 1.2 MP Photos"
29: product_template_8;Computer SC234;Goods;PCSC234;;450;300;;
30: product_template_9;Laptop Customized;Goods;LAP-CUS;;3645;3300;;
31: product_template_10;Self Build Kit;Goods;E-COM92;;147;98;;
32: product_template_11;Mouse, Wireless;Goods;M-Wir;;12,5;18;;
33: product_template_12;RAM SR5;Goods;RAM-SR5;;85;78;;
34: product_template_13;Computer Case;Goods;C-Case;;25;20;;
35: product_template_14;HDD SH-1;Goods;HDD-SH1;;975;860;;
36: product_template_15;Motherboard I9P57;Goods;MBi9;;1950;1700;;
37: product_template_16;Processor Core i5 2.70 Ghz;Goods;CPUi5;;2100;2010;;
38: product_template_17;Graphics Card;Goods;CARD;;885;876;;
39: product_template_18;Laptop Charger;Goods;E-COM93;;2250;2000;;
40: product_template_19;Laptop Keypad;Goods;E-COM94;;850;800;;
41: product_template_20;Mouse, Wireless;Goods;M-Wir;;12,5;18;;
42: product_template_21;Alice's Adventures in Wonderland - Lewis Caroll;Service;;;4,5;2;;Alice's Adventures in Wonderland (commonly shortened to Alice in Wonderland) is an 1865 novel written by English author Charles Lutwidge Dodgson under the pseudonym Lewis Carroll. It tells of a girl named Alice falling through a rabbit hole into a fantasy world populated by peculiar, anthropomorphic creatures. The tale plays with logic, giving the story lasting popularity with adults as well as with children. It is considered to be one of the best examples of the literary nonsense genre. Its narrative course and structure, characters and imagery have been enormously influential in both popular culture and literature, especially in the fantasy genre.
43: product_template_22;Warranty;Service;;;20;;;Warranty, issued to the purchaser of an article by its manufacturer, promising to repair or replace it if necessary within a specified period of time.
44: product_template_23;Basic Membership;Service;;;40;;;
45: product_template_24;Silver Membership;Service;;;80;;;
46: product_template_25;Gold Membership;Service;;;180;;;

(End of file - total 46 lines)
</content>
```

---

## Assistant (Build · GPT-5.2-Codex · 7.1s)

_Thinking:_

**Deciding CSV filling approach**

I'll rewrite clientes and productos templates with 30 records each, using semicolon delimiters, ASCII encoding, and dot decimals. I'll keep country_id as "Ecuador" by name, leave optional fields blank, and stick to existing templates since no quotation/order templates were provided.

_Thinking:_

**Confirming template constraints**

I'll only update existing templates and suggest the user provide templates for quotations and orders if they want those filled.

**Tool: bash**

**Input:**
```json
{
  "command": "ls data_import",
  "description": "Lists files in data_import directory"
}
```

**Output:**
```
clientes_template.csv
clientes_template.xlsx
productos_template.csv
productos_template.xls

```

---

## Assistant (Build · GPT-5.2-Codex · 3.6s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Delete File: data_import/clientes_template.csv\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
D data_import/clientes_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 15.0s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/clientes_template.csv\n+name;is_company;company_name;country_id;state_id;zip;city;street;street2;phone;mobile;email;vat;bank_ids/bank;bank_ids/acc_number\n+Cliente 01;1;;EC;Pichincha;170101;Quito;Av. Principal 101;;022900001;0999000001;cliente01@terrabyteec.com;0990000001;PICHINCHA;00100100101\n+Cliente 02;1;;EC;Guayas;090101;Guayaquil;Calle 10 #202;;042800002;0999000002;cliente02@terrabyteec.com;0990000002;GUAYAQUIL;00100100102\n+Cliente 03;1;;EC;Azuay;010101;Cuenca;Av. Central 303;;072700003;0999000003;cliente03@terrabyteec.com;0990000003;AUSTRO;00100100103\n+Cliente 04;1;;EC;Manabi;130101;Manta;Calle Norte 404;;052600004;0999000004;cliente04@terrabyteec.com;0990000004;MANABI;00100100104\n+Cliente 05;1;;EC;Tungurahua;180101;Ambato;Av. Sur 505;;032500005;0999000005;cliente05@terrabyteec.com;0990000005;AMBATO;00100100105\n+Cliente 06;1;;EC;Pichincha;170102;Quito;Av. Sierra 606;;022900006;0999000006;cliente06@terrabyteec.com;0990000006;PICHINCHA;00100100106\n+Cliente 07;1;;EC;Guayas;090102;Guayaquil;Calle Costa 707;;042800007;0999000007;cliente07@terrabyteec.com;0990000007;GUAYAQUIL;00100100107\n+Cliente 08;1;;EC;Azuay;010102;Cuenca;Av. Andes 808;;072700008;0999000008;cliente08@terrabyteec.com;0990000008;AUSTRO;00100100108\n+Cliente 09;1;;EC;Manabi;130102;Portoviejo;Calle 9 #909;;052600009;0999000009;cliente09@terrabyteec.com;0990000009;MANABI;00100100109\n+Cliente 10;1;;EC;Pichincha;170103;Quito;Av. Taller 1010;;022900010;0999000010;cliente10@terrabyteec.com;0990000010;PICHINCHA;00100100110\n+Cliente 11;1;;EC;Guayas;090103;Guayaquil;Calle 11 #1111;;042800011;0999000011;cliente11@terrabyteec.com;0990000011;GUAYAQUIL;00100100111\n+Cliente 12;1;;EC;Azuay;010103;Cuenca;Av. 12 1212;;072700012;0999000012;cliente12@terrabyteec.com;0990000012;AUSTRO;00100100112\n+Cliente 13;1;;EC;Manabi;130103;Manta;Calle 13 #1313;;052600013;0999000013;cliente13@terrabyteec.com;0990000013;MANABI;00100100113\n+Cliente 14;1;;EC;Tungurahua;180102;Ambato;Av. 14 1414;;032500014;0999000014;cliente14@terrabyteec.com;0990000014;AMBATO;00100100114\n+Cliente 15;1;;EC;Pichincha;170104;Quito;Calle 15 #1515;;022900015;0999000015;cliente15@terrabyteec.com;0990000015;PICHINCHA;00100100115\n+Cliente 16;1;;EC;Guayas;090104;Guayaquil;Av. 16 1616;;042800016;0999000016;cliente16@terrabyteec.com;0990000016;GUAYAQUIL;00100100116\n+Cliente 17;1;;EC;Azuay;010104;Cuenca;Calle 17 #1717;;072700017;0999000017;cliente17@terrabyteec.com;0990000017;AUSTRO;00100100117\n+Cliente 18;1;;EC;Manabi;130104;Manta;Av. 18 1818;;052600018;0999000018;cliente18@terrabyteec.com;0990000018;MANABI;00100100118\n+Cliente 19;1;;EC;Tungurahua;180103;Ambato;Calle 19 #1919;;032500019;0999000019;cliente19@terrabyteec.com;0990000019;AMBATO;00100100119\n+Cliente 20;1;;EC;Pichincha;170105;Quito;Av. 20 2020;;022900020;0999000020;cliente20@terrabyteec.com;0990000020;PICHINCHA;00100100120\n+Cliente 21;1;;EC;Guayas;090105;Guayaquil;Calle 21 #2121;;042800021;0999000021;cliente21@terrabyteec.com;0990000021;GUAYAQUIL;00100100121\n+Cliente 22;1;;EC;Azuay;010105;Cuenca;Av. 22 2222;;072700022;0999000022;cliente22@terrabyteec.com;0990000022;AUSTRO;00100100122\n+Cliente 23;1;;EC;Manabi;130105;Manta;Calle 23 #2323;;052600023;0999000023;cliente23@terrabyteec.com;0990000023;MANABI;00100100123\n+Cliente 24;1;;EC;Tungurahua;180104;Ambato;Av. 24 2424;;032500024;0999000024;cliente24@terrabyteec.com;0990000024;AMBATO;00100100124\n+Cliente 25;1;;EC;Pichincha;170106;Quito;Calle 25 #2525;;022900025;0999000025;cliente25@terrabyteec.com;0990000025;PICHINCHA;00100100125\n+Cliente 26;1;;EC;Guayas;090106;Guayaquil;Av. 26 2626;;042800026;0999000026;cliente26@terrabyteec.com;0990000026;GUAYAQUIL;00100100126\n+Cliente 27;1;;EC;Azuay;010106;Cuenca;Calle 27 #2727;;072700027;0999000027;cliente27@terrabyteec.com;0990000027;AUSTRO;00100100127\n+Cliente 28;1;;EC;Manabi;130106;Manta;Av. 28 2828;;052600028;0999000028;cliente28@terrabyteec.com;0990000028;MANABI;00100100128\n+Cliente 29;1;;EC;Tungurahua;180105;Ambato;Calle 29 #2929;;032500029;0999000029;cliente29@terrabyteec.com;0990000029;AMBATO;00100100129\n+Cliente 30;1;;EC;Pichincha;170107;Quito;Av. 30 3030;;022900030;0999000030;cliente30@terrabyteec.com;0990000030;PICHINCHA;00100100130\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/clientes_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 3.1s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Delete File: data_import/productos_template.csv\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
D data_import/productos_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 11.0s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/productos_template.csv\n+External ID;Name;Product Type;Internal Reference;Barcode;Sales Price;Cost;Weight;Sales Description\n+product_template_01;Aceite 5W30 1L;Goods;MECH-001;;12.50;8.20;;Aceite sintetico para motores a gasolina.\n+product_template_02;Aceite 10W40 1L;Goods;MECH-002;;11.90;7.80;;Aceite semisintetico para uso diario.\n+product_template_03;Filtro de aceite A1;Goods;MECH-003;;6.50;3.80;;Filtro de aceite para motores 1.6 a 2.0.\n+product_template_04;Filtro de aire A2;Goods;MECH-004;;8.20;4.60;;Filtro de aire de alto flujo.\n+product_template_05;Bujia NGK BKR6E;Goods;MECH-005;;9.90;6.10;;Bujia estandar para motores de 4 cilindros.\n+product_template_06;Pastillas de freno delanteras;Goods;MECH-006;;35.00;22.00;;Pastillas ceramicas para eje delantero.\n+product_template_07;Pastillas de freno traseras;Goods;MECH-007;;32.00;20.50;;Pastillas semimetalicas para eje trasero.\n+product_template_08;Disco de freno 280mm;Goods;MECH-008;;45.00;30.00;;Disco ventilado 280 mm.\n+product_template_09;Bateria 12V 60Ah;Goods;MECH-009;;120.00;90.00;;Bateria libre de mantenimiento 60Ah.\n+product_template_10;Neumatico 195/65R15;Goods;MECH-010;;85.00;60.00;;Neumatico radial para sedanes.\n+product_template_11;Neumatico 205/55R16;Goods;MECH-011;;95.00;68.00;;Neumatico de alto agarre.\n+product_template_12;Amortiguador delantero;Goods;MECH-012;;78.00;52.00;;Amortiguador hidraulico delantero.\n+product_template_13;Amortiguador trasero;Goods;MECH-013;;74.00;49.00;;Amortiguador hidraulico trasero.\n+product_template_14;Correa de distribucion;Goods;MECH-014;;55.00;37.00;;Correa de distribucion reforzada.\n+product_template_15;Correa auxiliar;Goods;MECH-015;;25.00;16.00;;Correa auxiliar para accesorios.\n+product_template_16;Liquido de frenos DOT4;Goods;MECH-016;;7.50;4.20;;Liquido de frenos DOT4 500ml.\n+product_template_17;Liquido refrigerante 1L;Goods;MECH-017;;6.80;3.90;;Refrigerante 1L listo para usar.\n+product_template_18;Filtro de combustible C1;Goods;MECH-018;;10.50;6.70;;Filtro de combustible para inyeccion.\n+product_template_19;Limpiaparabrisas 22in;Goods;MECH-019;;12.00;7.50;;Plumilla 22 pulgadas.\n+product_template_20;Lampara H4 60/55W;Goods;MECH-020;;5.50;3.10;;Lampara halogena H4.\n+product_template_21;Kit de embrague;Goods;MECH-021;;180.00;130.00;;Kit de embrague completo.\n+product_template_22;Alternador 90A;Goods;MECH-022;;210.00;160.00;;Alternador 90 amperios.\n+product_template_23;Motor de arranque;Goods;MECH-023;;190.00;140.00;;Motor de arranque 12V.\n+product_template_24;Sensor de oxigeno;Goods;MECH-024;;65.00;45.00;;Sensor lambda 4 cables.\n+product_template_25;Bobina de encendido;Goods;MECH-025;;48.00;31.00;;Bobina de encendido individual.\n+product_template_26;Radiador compacto;Goods;MECH-026;;135.00;95.00;;Radiador aluminio compacto.\n+product_template_27;Termostato 88C;Goods;MECH-027;;18.00;11.00;;Termostato 88C.\n+product_template_28;Kit de afinamiento;Goods;MECH-028;;60.00;40.00;;Kit de afinamiento basico.\n+product_template_29;Aditivo limpiainyectores;Goods;MECH-029;;9.50;5.20;;Aditivo para limpieza de inyectores.\n+product_template_30;Grasa multiproposito 500g;Goods;MECH-030;;7.80;4.10;;Grasa multiproposito 500g.\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/productos_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 2.8s)

_Thinking:_

**Confirming missing templates and delimiter**

I need to ask the user specifically for orders and quotes template files since only customers and products templates are present. I'll also clarify that the delimiter is semicolon before proceeding.

Listo: ya rellené las plantillas CSV con ~30 registros para clientes y productos.

Archivos actualizados:
- `data_import/clientes_template.csv`
- `data_import/productos_template.csv`

Ahora necesito las plantillas para cotizaciones y órdenes. No las veo en `data_import/`.  
Déjame esos archivos (CSV/XLS/XLSX) en `data_import/` y los lleno igual.

---

## User

para esas no tengo plantillas, esas si dame data y luego te aviso si necesitan modificaciones

---

## Assistant (Build · GPT-5.2-Codex · 8.6s)

_Thinking:_

**Preparing CSV data files**

Planning to create two CSV files for quotations and sales orders with standard fields like customer, order date, product, quantity, and unit price, reusing existing products and clients and providing about 30 rows each.

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/cotizaciones_ventas.csv\n+Customer,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Cliente 01,2026-05-01,Aceite 5W30 1L,2,12.50\n+Cliente 02,2026-05-02,Filtro de aceite A1,3,6.50\n+Cliente 03,2026-05-03,Pastillas de freno delanteras,1,35.00\n+Cliente 04,2026-05-04,Disco de freno 280mm,2,45.00\n+Cliente 05,2026-05-05,Bateria 12V 60Ah,1,120.00\n+Cliente 06,2026-05-06,Neumatico 195/65R15,2,85.00\n+Cliente 07,2026-05-07,Amortiguador delantero,2,78.00\n+Cliente 08,2026-05-08,Correa de distribucion,1,55.00\n+Cliente 09,2026-05-09,Liquido de frenos DOT4,4,7.50\n+Cliente 10,2026-05-10,Liquido refrigerante 1L,3,6.80\n+Cliente 11,2026-05-11,Filtro de aire A2,2,8.20\n+Cliente 12,2026-05-12,Limpiaparabrisas 22in,2,12.00\n+Cliente 13,2026-05-13,Lampara H4 60/55W,4,5.50\n+Cliente 14,2026-05-14,Kit de embrague,1,180.00\n+Cliente 15,2026-05-15,Alternador 90A,1,210.00\n+Cliente 16,2026-05-16,Motor de arranque,1,190.00\n+Cliente 17,2026-05-17,Sensor de oxigeno,1,65.00\n+Cliente 18,2026-05-18,Bobina de encendido,2,48.00\n+Cliente 19,2026-05-19,Radiador compacto,1,135.00\n+Cliente 20,2026-05-20,Termostato 88C,2,18.00\n+Cliente 21,2026-05-21,Kit de afinamiento,1,60.00\n+Cliente 22,2026-05-22,Aditivo limpiainyectores,3,9.50\n+Cliente 23,2026-05-23,Grasa multiproposito 500g,4,7.80\n+Cliente 24,2026-05-24,Correa auxiliar,2,25.00\n+Cliente 25,2026-05-25,Neumatico 205/55R16,2,95.00\n+Cliente 26,2026-05-26,Filtro de combustible C1,2,10.50\n+Cliente 27,2026-05-27,Pastillas de freno traseras,1,32.00\n+Cliente 28,2026-05-28,Aceite 10W40 1L,2,11.90\n+Cliente 29,2026-05-29,Bujia NGK BKR6E,4,9.90\n+Cliente 30,2026-05-30,Amortiguador trasero,2,74.00\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/cotizaciones_ventas.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 6.9s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/ordenes_ventas.csv\n+Customer,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Cliente 01,2026-06-01,Aceite 5W30 1L,1,12.50\n+Cliente 02,2026-06-02,Filtro de aceite A1,2,6.50\n+Cliente 03,2026-06-03,Pastillas de freno delanteras,1,35.00\n+Cliente 04,2026-06-04,Disco de freno 280mm,1,45.00\n+Cliente 05,2026-06-05,Bateria 12V 60Ah,1,120.00\n+Cliente 06,2026-06-06,Neumatico 195/65R15,2,85.00\n+Cliente 07,2026-06-07,Amortiguador delantero,1,78.00\n+Cliente 08,2026-06-08,Correa de distribucion,1,55.00\n+Cliente 09,2026-06-09,Liquido de frenos DOT4,2,7.50\n+Cliente 10,2026-06-10,Liquido refrigerante 1L,2,6.80\n+Cliente 11,2026-06-11,Filtro de aire A2,1,8.20\n+Cliente 12,2026-06-12,Limpiaparabrisas 22in,2,12.00\n+Cliente 13,2026-06-13,Lampara H4 60/55W,2,5.50\n+Cliente 14,2026-06-14,Kit de embrague,1,180.00\n+Cliente 15,2026-06-15,Alternador 90A,1,210.00\n+Cliente 16,2026-06-16,Motor de arranque,1,190.00\n+Cliente 17,2026-06-17,Sensor de oxigeno,1,65.00\n+Cliente 18,2026-06-18,Bobina de encendido,1,48.00\n+Cliente 19,2026-06-19,Radiador compacto,1,135.00\n+Cliente 20,2026-06-20,Termostato 88C,1,18.00\n+Cliente 21,2026-06-21,Kit de afinamiento,1,60.00\n+Cliente 22,2026-06-22,Aditivo limpiainyectores,2,9.50\n+Cliente 23,2026-06-23,Grasa multiproposito 500g,2,7.80\n+Cliente 24,2026-06-24,Correa auxiliar,1,25.00\n+Cliente 25,2026-06-25,Neumatico 205/55R16,2,95.00\n+Cliente 26,2026-06-26,Filtro de combustible C1,1,10.50\n+Cliente 27,2026-06-27,Pastillas de freno traseras,1,32.00\n+Cliente 28,2026-06-28,Aceite 10W40 1L,1,11.90\n+Cliente 29,2026-06-29,Bujia NGK BKR6E,2,9.90\n+Cliente 30,2026-06-30,Amortiguador trasero,1,74.00\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/ordenes_ventas.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 2.5s)

Listo. Ya generé data para cotizaciones y órdenes de venta:

- `data_import/cotizaciones_ventas.csv`
- `data_import/ordenes_ventas.csv`

Importación sugerida en Odoo:
1) Contactos → Importar `data_import/clientes_template.csv`
2) Ventas → Productos → Importar `data_import/productos_template.csv`
3) Ventas → Cotizaciones → Importar `data_import/cotizaciones_ventas.csv`
4) Ventas → Órdenes → Importar `data_import/ordenes_ventas.csv`

Si necesitas ajustes en columnas o formato, dime el error exacto de importación y lo adapto.

---

## User

antes de continuar el odoo me pregunta lo siguiente Delimitador de texto, Formato de fecha, formato de fecha y hora, separador de miles, separador de decimales.

---

## Assistant (Build · GPT-5.2-Codex · 3.0s)

_Thinking:_

**Providing CSV settings summary**

The CSV uses semicolon as delimiter, double quotes for text, date format YYYY-MM-DD, datetime including time in the same format, no thousands separator, and dot as decimal separator; comma is not used in templates.

Usa estos valores:

- Delimitador de texto: `"`
- Formato de fecha: `YYYY-MM-DD` (ej. 2026-05-01)
- Formato de fecha y hora: `YYYY-MM-DD HH:MM:SS`
- Separador de miles: vacío (sin separador)
- Separador de decimales: `.`

Si Odoo no acepta punto decimal por idioma, cambia a:
- Separador de decimales: `,`
y te ajusto los CSV.

---

## User

que significa el campo is_company de productos?

---

## Assistant (Build · GPT-5.2-Codex · 4.0s)

_Thinking:_

**Clarifying data model confusion**

The "is_company" field belongs to contacts, not the product template. I'll ask if the user is mistakenly seeing it in products to clarify this point.

Ese campo `is_company` no es de productos, es de contactos/clientes.  
- `is_company = 1` significa que el contacto es una empresa.  
- `is_company = 0` significa que es una persona.

Si lo estás viendo en productos, probablemente estás importando la plantilla de contactos por error.

---

## User

Ahora pasamos con el modulo de compras, para este necesito para los siguientes apartados: solicitudes de cotizacion, ordenes de compra, proveedores (aqui si hay plantilla pero es la misma que usaste para clientes, pero no les pongas nombres como Cliente01, algo inventado), y ya no hay plantillas para los demas

---

## Assistant (Build · GPT-5.2-Codex · 23.9s)

_Thinking:_

**Creating vendor and purchase CSV templates**

I'm creating a vendor CSV using a semicolon delimiter to match the client template and making purchase RFQ and PO CSVs similar to purchase_orders.csv but with vendor details, using commas. I'll add these files via patch and specify their import order.

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/proveedores_template.csv\n+name;is_company;company_name;country_id;state_id;zip;city;street;street2;phone;mobile;email;vat;bank_ids/bank;bank_ids/acc_number\n+Repuestos Andinos;1;;EC;Pichincha;170102;Quito;Av. Industrial 101;;022810001;0988100001;contacto@repuestosandinos.ec;0991000001;PICHINCHA;00200100101\n+Lubricantes Sierra;1;;EC;Pichincha;170103;Quito;Calle Motores 202;;022810002;0988100002;ventas@lubricantessierra.ec;0991000002;PICHINCHA;00200100102\n+Autopartes Guayas;1;;EC;Guayas;090101;Guayaquil;Av. Logistica 303;;042810003;0988100003;info@autopartesguayas.ec;0991000003;GUAYAQUIL;00200100103\n+Frenos del Pacifico;1;;EC;Guayas;090102;Guayaquil;Calle Taller 404;;042810004;0988100004;comercial@frenospacifico.ec;0991000004;GUAYAQUIL;00200100104\n+Electricos Austro;1;;EC;Azuay;010101;Cuenca;Av. Repuestos 505;;072810005;0988100005;ventas@electricosaustro.ec;0991000005;AUSTRO;00200100105\n+Suspensiones Azuay;1;;EC;Azuay;010102;Cuenca;Calle Direccion 606;;072810006;0988100006;contacto@suspensionesazuay.ec;0991000006;AUSTRO;00200100106\n+Filtros Manabi;1;;EC;Manabi;130101;Manta;Av. Filtros 707;;052810007;0988100007;info@filtrosmanabi.ec;0991000007;MANABI;00200100107\n+Neumaticos Costa;1;;EC;Manabi;130102;Portoviejo;Calle Neumaticos 808;;052810008;0988100008;ventas@neumaticoscosta.ec;0991000008;MANABI;00200100108\n+Transmision Ambato;1;;EC;Tungurahua;180101;Ambato;Av. Transmision 909;;032810009;0988100009;info@transmisionambato.ec;0991000009;AMBATO;00200100109\n+Refrigeracion Central;1;;EC;Tungurahua;180102;Ambato;Calle Refrigeracion 1010;;032810010;0988100010;ventas@refrigeracioncentral.ec;0991000010;AMBATO;00200100110\n+Iluminacion Quito;1;;EC;Pichincha;170104;Quito;Av. Iluminacion 1111;;022810011;0988100011;contacto@iluminacionquito.ec;0991000011;PICHINCHA;00200100111\n+Correas y Bandas;1;;EC;Pichincha;170105;Quito;Calle Bandas 1212;;022810012;0988100012;ventas@correasbandas.ec;0991000012;PICHINCHA;00200100112\n+Rodamientos Guayaquil;1;;EC;Guayas;090103;Guayaquil;Av. Rodamientos 1313;;042810013;0988100013;info@rodamientosgye.ec;0991000013;GUAYAQUIL;00200100113\n+Quimicos del Valle;1;;EC;Guayas;090104;Guayaquil;Calle Quimicos 1414;;042810014;0988100014;ventas@quimicosdelvalle.ec;0991000014;GUAYAQUIL;00200100114\n+Accesorios Cuenca;1;;EC;Azuay;010103;Cuenca;Av. Accesorios 1515;;072810015;0988100015;contacto@accesorioscuenca.ec;0991000015;AUSTRO;00200100115\n+Herramientas Sierra;1;;EC;Azuay;010104;Cuenca;Calle Herramientas 1616;;072810016;0988100016;ventas@herramientassierra.ec;0991000016;AUSTRO;00200100116\n+Sensores Manta;1;;EC;Manabi;130103;Manta;Av. Sensores 1717;;052810017;0988100017;info@sensoresmanta.ec;0991000017;MANABI;00200100117\n+Electronica Auto;1;;EC;Manabi;130104;Manta;Calle Electronica 1818;;052810018;0988100018;ventas@electronicaauto.ec;0991000018;MANABI;00200100118\n+Baterias Ambato;1;;EC;Tungurahua;180103;Ambato;Av. Baterias 1919;;032810019;0988100019;contacto@bateriasambato.ec;0991000019;AMBATO;00200100119\n+Lubricantes Andinos;1;;EC;Tungurahua;180104;Ambato;Calle Lubricantes 2020;;032810020;0988100020;ventas@lubricantesandinos.ec;0991000020;AMBATO;00200100120\n+Repuestos Premium;1;;EC;Pichincha;170106;Quito;Av. Repuestos 2121;;022810021;0988100021;info@repuestospremium.ec;0991000021;PICHINCHA;00200100121\n+Frenos Seguros;1;;EC;Pichincha;170107;Quito;Calle Frenos 2222;;022810022;0988100022;ventas@frenosseguros.ec;0991000022;PICHINCHA;00200100122\n+Suspension Plus;1;;EC;Guayas;090105;Guayaquil;Av. Suspension 2323;;042810023;0988100023;contacto@suspensionplus.ec;0991000023;GUAYAQUIL;00200100123\n+Motor Parts EC;1;;EC;Guayas;090106;Guayaquil;Calle Motor 2424;;042810024;0988100024;ventas@motorpartsec.ec;0991000024;GUAYAQUIL;00200100124\n+Filtros del Austro;1;;EC;Azuay;010105;Cuenca;Av. Filtros 2525;;072810025;0988100025;info@filtrosaustro.ec;0991000025;AUSTRO;00200100125\n+Neumaticos Sierra;1;;EC;Azuay;010106;Cuenca;Calle Neumaticos 2626;;072810026;0988100026;ventas@neumaticossierrra.ec;0991000026;AUSTRO;00200100126\n+Direccion Hidraulica;1;;EC;Manabi;130105;Manta;Av. Direccion 2727;;052810027;0988100027;contacto@direccionhidraulica.ec;0991000027;MANABI;00200100127\n+Escape y Catalizadores;1;;EC;Manabi;130106;Manta;Calle Escape 2828;;052810028;0988100028;ventas@escapecatalizadores.ec;0991000028;MANABI;00200100128\n+Pinturas y Limpieza;1;;EC;Tungurahua;180105;Ambato;Av. Limpieza 2929;;032810029;0988100029;info@pinturasylimpieza.ec;0991000029;AMBATO;00200100129\n+Insumos Automotrices;1;;EC;Tungurahua;180106;Ambato;Calle Insumos 3030;;032810030;0988100030;ventas@insumosautomotrices.ec;0991000030;AMBATO;00200100130\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/proveedores_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 9.7s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/solicitudes_cotizacion_compras.csv\n+Vendor,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Repuestos Andinos,2026-05-01,Aceite 5W30 1L,30,8.20\n+Lubricantes Sierra,2026-05-02,Aceite 10W40 1L,30,7.80\n+Autopartes Guayas,2026-05-03,Filtro de aceite A1,60,3.80\n+Frenos del Pacifico,2026-05-04,Filtro de aire A2,50,4.60\n+Electricos Austro,2026-05-05,Bujia NGK BKR6E,80,6.10\n+Suspensiones Azuay,2026-05-06,Pastillas de freno delanteras,25,22.00\n+Filtros Manabi,2026-05-07,Pastillas de freno traseras,25,20.50\n+Neumaticos Costa,2026-05-08,Disco de freno 280mm,20,30.00\n+Transmision Ambato,2026-05-09,Bateria 12V 60Ah,12,90.00\n+Refrigeracion Central,2026-05-10,Neumatico 195/65R15,18,60.00\n+Iluminacion Quito,2026-05-11,Neumatico 205/55R16,16,68.00\n+Correas y Bandas,2026-05-12,Amortiguador delantero,22,52.00\n+Rodamientos Guayaquil,2026-05-13,Amortiguador trasero,22,49.00\n+Quimicos del Valle,2026-05-14,Correa de distribucion,30,37.00\n+Accesorios Cuenca,2026-05-15,Correa auxiliar,45,16.00\n+Herramientas Sierra,2026-05-16,Liquido de frenos DOT4,70,4.20\n+Sensores Manta,2026-05-17,Liquido refrigerante 1L,65,3.90\n+Electronica Auto,2026-05-18,Filtro de combustible C1,40,6.70\n+Baterias Ambato,2026-05-19,Limpiaparabrisas 22in,55,7.50\n+Lubricantes Andinos,2026-05-20,Lampara H4 60/55W,90,3.10\n+Repuestos Premium,2026-05-21,Kit de embrague,10,130.00\n+Frenos Seguros,2026-05-22,Alternador 90A,8,160.00\n+Suspension Plus,2026-05-23,Motor de arranque,7,140.00\n+Motor Parts EC,2026-05-24,Sensor de oxigeno,18,45.00\n+Filtros del Austro,2026-05-25,Bobina de encendido,20,31.00\n+Neumaticos Sierra,2026-05-26,Radiador compacto,9,95.00\n+Direccion Hidraulica,2026-05-27,Termostato 88C,28,11.00\n+Escape y Catalizadores,2026-05-28,Kit de afinamiento,15,40.00\n+Pinturas y Limpieza,2026-05-29,Aditivo limpiainyectores,50,5.20\n+Insumos Automotrices,2026-05-30,Grasa multiproposito 500g,55,4.10\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/solicitudes_cotizacion_compras.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 9.7s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/ordenes_compra.csv\n+Vendor,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Repuestos Andinos,2026-06-01,Aceite 5W30 1L,20,8.20\n+Lubricantes Sierra,2026-06-02,Aceite 10W40 1L,20,7.80\n+Autopartes Guayas,2026-06-03,Filtro de aceite A1,50,3.80\n+Frenos del Pacifico,2026-06-04,Filtro de aire A2,40,4.60\n+Electricos Austro,2026-06-05,Bujia NGK BKR6E,60,6.10\n+Suspensiones Azuay,2026-06-06,Pastillas de freno delanteras,20,22.00\n+Filtros Manabi,2026-06-07,Pastillas de freno traseras,20,20.50\n+Neumaticos Costa,2026-06-08,Disco de freno 280mm,15,30.00\n+Transmision Ambato,2026-06-09,Bateria 12V 60Ah,10,90.00\n+Refrigeracion Central,2026-06-10,Neumatico 195/65R15,15,60.00\n+Iluminacion Quito,2026-06-11,Neumatico 205/55R16,12,68.00\n+Correas y Bandas,2026-06-12,Amortiguador delantero,18,52.00\n+Rodamientos Guayaquil,2026-06-13,Amortiguador trasero,18,49.00\n+Quimicos del Valle,2026-06-14,Correa de distribucion,25,37.00\n+Accesorios Cuenca,2026-06-15,Correa auxiliar,35,16.00\n+Herramientas Sierra,2026-06-16,Liquido de frenos DOT4,60,4.20\n+Sensores Manta,2026-06-17,Liquido refrigerante 1L,55,3.90\n+Electronica Auto,2026-06-18,Filtro de combustible C1,30,6.70\n+Baterias Ambato,2026-06-19,Limpiaparabrisas 22in,40,7.50\n+Lubricantes Andinos,2026-06-20,Lampara H4 60/55W,70,3.10\n+Repuestos Premium,2026-06-21,Kit de embrague,8,130.00\n+Frenos Seguros,2026-06-22,Alternador 90A,6,160.00\n+Suspension Plus,2026-06-23,Motor de arranque,6,140.00\n+Motor Parts EC,2026-06-24,Sensor de oxigeno,15,45.00\n+Filtros del Austro,2026-06-25,Bobina de encendido,15,31.00\n+Neumaticos Sierra,2026-06-26,Radiador compacto,7,95.00\n+Direccion Hidraulica,2026-06-27,Termostato 88C,20,11.00\n+Escape y Catalizadores,2026-06-28,Kit de afinamiento,12,40.00\n+Pinturas y Limpieza,2026-06-29,Aditivo limpiainyectores,40,5.20\n+Insumos Automotrices,2026-06-30,Grasa multiproposito 500g,45,4.10\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/ordenes_compra.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 3.6s)

Listo: ya tienes data para Compras.

Archivos creados:
- `data_import/proveedores_template.csv` (30 proveedores, mismos campos de contactos)
- `data_import/solicitudes_cotizacion_compras.csv`
- `data_import/ordenes_compra.csv`

Importación sugerida:
1) Contactos → Importar `data_import/proveedores_template.csv`
2) Compras → Solicitudes de cotización → Importar `data_import/solicitudes_cotizacion_compras.csv`
3) Compras → Órdenes de compra → Importar `data_import/ordenes_compra.csv`

Si Odoo te pide formato/columnas distintas en compras, dime el error exacto y ajusto.

---

## User

en solicitudes de cotization no hay fecha de orden solo fecha limite de la orden

---

## Assistant (Build · GPT-5.2-Codex · 3.5s)

_Thinking:_

**Adjusting column header to Order Deadline**

I'm updating the solicitudes file header from "Order Date" to "Order Deadline" and ensuring the date values align, while keeping the ordenes compra file using the original "Order Date" header.

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: data_import/solicitudes_cotizacion_compras.csv\n@@\n-Vendor,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Vendor,Order Deadline,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M data_import/solicitudes_cotizacion_compras.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 2.2s)

Listo, cambié la columna a fecha límite.

Archivo actualizado:
- `data_import/solicitudes_cotizacion_compras.csv` (columna `Order Deadline`)

Prueba ese import. Si el nombre exacto de la columna difiere, pásame el texto exacto del campo y lo ajusto.

---

## User

lo mismo en ordenes de compra solo hay fecha limite de la orden

---

## Assistant (Build · GPT-5.2-Codex · 2.2s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: data_import/ordenes_compra.csv\n@@\n-Vendor,Order Date,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n+Vendor,Order Deadline,Order Lines / Product,Order Lines / Quantity,Order Lines / Unit Price\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M data_import/ordenes_compra.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 1.9s)

Listo, actualizado.

Archivo:
- `data_import/ordenes_compra.csv` (columna `Order Deadline`)

---

## User

Ahora necesito datos para los empleados, ahi tienes una plantilla

---

## Assistant (Build · GPT-5.2-Codex · 2.1s)

_Thinking:_



**Tool: glob**

**Input:**
```json
{
  "path": ".",
  "pattern": "data_import/*emplead*.*"
}
```

**Output:**
```
No files found
```

---

## Assistant (Build · GPT-5.2-Codex · 2.1s)

_Thinking:_



No veo la plantilla de empleados en `data_import/`.  
Déjame el archivo ahí (CSV/XLS/XLSX) y lo lleno. Si ya está, dime el nombre exacto.

---

## User

si esta como employees_template, ademas primero vamos con departamentos, aqui si no tengo plantilla

---

## Assistant (Build · GPT-5.2-Codex · 1.7s)

**Tool: glob**

**Input:**
```json
{
  "path": ".",
  "pattern": "data_import/*employees_template*"
}
```

**Output:**
```
No files found
```

---

## Assistant (Build · GPT-5.2-Codex · 3.3s)

_Thinking:_

**Planning department CSV creation and employee template search**

I'm considering creating a simple departments CSV with a default "Name" column but need to confirm if a specific structure is required. I'll also search for the existing employee template in the root or via glob as indicated.

**Tool: glob**

**Input:**
```json
{
  "path": ".",
  "pattern": "**/*employees_template*"
}
```

**Output:**
```
No files found
```

---

## Assistant (Build · GPT-5.2-Codex · 3.5s)

_Thinking:_

**Preparing department CSV and requesting employee template name**

I need to create a CSV for departments with columns Name, Company, and Manager, using "Terrabyte EC" as the company. I'll also ask for the exact employee import template filename for clarity.

No encuentro `employees_template` en el repo.  
Confírmame el nombre exacto y la ruta dentro de `data_import/`.

Mientras tanto, te preparo una plantilla de departamentos con 30 registros. ¿Te sirve con estas columnas?
- `Name`, `Company`, `Manager` (recomendado)

---

## User

se llama employee_template.csv, y necesito nombre, gerente, departamento principal, color, pero primero crea para empleados y luego para departamentos tal vez departamentos no sea necesario 30, como lo ves tu

---

## Assistant (Build · GPT-5.2-Codex · 1.9s)

_Thinking:_

**Planning template reading**

I'll read the template file first before filling it to ensure I have the content ready for processing.

**Tool: read**

**Input:**
```json
{
  "filePath": "/home/alexander/Desktop/das/Mechanic_Workshop/data_import/employee_template.csv"
}
```

**Output:**
```
<path>/home/alexander/Desktop/das/Mechanic_Workshop/data_import/employee_template.csv</path>
<type>file</type>
<content>
1: ﻿External ID;Name;Work Email;Work Phone;Work Mobile;Department;Gender;Notes;Marital Status;Date of Birth;Nationality (Country);Identification No;Passport No;Visa No;Work Permit No;Visa Expire Date;;;;;;;
2: hr_employee_1;Antoine Langlais;antoine@odoo.com;=+3281813700;;Sales;Male;;Single;14/10/1985;France;;;;;;;;;;;;
3: hr_employee_2;Ashley Presley;ashley@odoo.com;=+3281813700;;Administration;Female;;Married;;United States;;;;;;;;;;;;
4: hr_employee_3;David Samson;david@odoo.com;3281813700;;Sales;Male;;Single;19/05/1982;Belgium;;;;;;;;;;;;
5: hr_employee_4;Famke Jenssens;famke@odoo.com;3281813700;;Sales;Male;;Married;;Belgium;;;;;;;;;;;;
6: hr_employee_5;Hans Anders;;3282823500;;Sales;Female;;Single;;Germany;;;;;;;;;;;;
7: hr_employee_6;Jack Macklin;jack@odoo.com;3281813700;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;
8: hr_employee_7;Jan Van Eyck;jve@odoo.com;3282823500;;Administration;Male;;Married;;Netherlands;;;;;;;;;;;;
9: hr_employee_8;Jean-Pierre Carnaud;jep@odoo.com;3282823500;;Sales;Male;;Single;;Belgium;;;;;;;;;;;;
10: hr_employee_9;Jimmy Kosikin;jimmy@odoo.com;3281813700;;Administration;Male;;Single;;United Kingdom;;;;;;;;;;;;
11: hr_employee_10;John Doe;jod@odoo.com;3282823500;;Administration;Male;;Married;;Belgium;;;;;;;;;;;;
12: hr_employee_11;John Smith;john@odoo.com;3281813700;32486571630;Sales;Male;;Single;;Belgium;;;;;;;;;;;;
13: hr_employee_12;João Gomer;jog@odoo.com;3282823500;;Administration;Male;;Single;;Brazil;;;;;;;;;;;;
14: hr_employee_13;Juan Gomez;;3282823500;;Administration;Male;;Single;;Mexico;;;;;;;;;;;;
15: hr_employee_14;Laurie Poiret;;;;Sales;Female;;Married;28/07/1991;Switzerland;91-07-28-458-83;;;;;;;;;;;
16: hr_employee_15;Liam Nelson;liam@odoo.com;3281813700;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;
17: hr_employee_16;Luigi Rondi;lur@odoo.com;3282823500;;Sales;Male;;Single;;Italy;;;;;;;;;;;;
18: hr_employee_17;Martin Lawrence;martin@odoo.com;3281813700;;Sales;Male;;Divorced;;Belgium;;;;;;;;;;;;
19: hr_employee_18;Michael Hawkins;michael@odoo.com;3281813700;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;
20: hr_employee_19;Pieter Parker;pieter@odoo.com;3281813700;;Sales;Male;;Single;;Ireland;;;;;;;;;;;;
21: hr_employee_20;Roger Scott;;3282823500;;Sales;Male;;Married;;United States;;;;;;;;;;;;
22: hr_employee_21;Николай Петра;;3282823500;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;
23: hr_employee_22;佐藤さくら;;3282823500;;Sales;Male;;Single;;China;;;;;;;;;;;;
24: hr_employee_23;趙生;;3282823500;;Sales;Male;;Single;;Japan;;;;;;;;;;;;

(End of file - total 24 lines)
</content>
```

---

## Assistant (Build · GPT-5.2-Codex · 23.5s)

_Thinking:_

**Preparing patches for employees and departments CSVs**

I'm creating an ASCII-only employees CSV with 30 entries, matching template columns and date format dd/mm/yyyy, and a departments CSV with 8–10 entries using specified Spanish column names and linking managers to employee names; will apply as file replacements.

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Update File: data_import/employee_template.csv\n@@\n-﻿External ID;Name;Work Email;Work Phone;Work Mobile;Department;Gender;Notes;Marital Status;Date of Birth;Nationality (Country);Identification No;Passport No;Visa No;Work Permit No;Visa Expire Date;;;;;;;\n-hr_employee_1;Antoine Langlais;antoine@odoo.com;=+3281813700;;Sales;Male;;Single;14/10/1985;France;;;;;;;;;;;;\n-hr_employee_2;Ashley Presley;ashley@odoo.com;=+3281813700;;Administration;Female;;Married;;United States;;;;;;;;;;;;\n-hr_employee_3;David Samson;david@odoo.com;3281813700;;Sales;Male;;Single;19/05/1982;Belgium;;;;;;;;;;;;\n-hr_employee_4;Famke Jenssens;famke@odoo.com;3281813700;;Sales;Male;;Married;;Belgium;;;;;;;;;;;;\n-hr_employee_5;Hans Anders;;3282823500;;Sales;Female;;Single;;Germany;;;;;;;;;;;;\n-hr_employee_6;Jack Macklin;jack@odoo.com;3281813700;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;\n-hr_employee_7;Jan Van Eyck;jve@odoo.com;3282823500;;Administration;Male;;Married;;Netherlands;;;;;;;;;;;;\n-hr_employee_8;Jean-Pierre Carnaud;jep@odoo.com;3282823500;;Sales;Male;;Single;;Belgium;;;;;;;;;;;;\n-hr_employee_9;Jimmy Kosikin;jimmy@odoo.com;3281813700;;Administration;Male;;Single;;United Kingdom;;;;;;;;;;;;\n-hr_employee_10;John Doe;jod@odoo.com;3282823500;;Administration;Male;;Married;;Belgium;;;;;;;;;;;;\n-hr_employee_11;John Smith;john@odoo.com;3281813700;32486571630;Sales;Male;;Single;;Belgium;;;;;;;;;;;;\n-hr_employee_12;João Gomer;jog@odoo.com;3282823500;;Administration;Male;;Single;;Brazil;;;;;;;;;;;;\n-hr_employee_13;Juan Gomez;;3282823500;;Administration;Male;;Single;;Mexico;;;;;;;;;;;;\n-hr_employee_14;Laurie Poiret;;;;Sales;Female;;Married;28/07/1991;Switzerland;91-07-28-458-83;;;;;;;;;;;\n-hr_employee_15;Liam Nelson;liam@odoo.com;3281813700;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;\n-hr_employee_16;Luigi Rondi;lur@odoo.com;3282823500;;Sales;Male;;Single;;Italy;;;;;;;;;;;;\n-hr_employee_17;Martin Lawrence;martin@odoo.com;3281813700;;Sales;Male;;Divorced;;Belgium;;;;;;;;;;;;\n-hr_employee_18;Michael Hawkins;michael@odoo.com;3281813700;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;\n-hr_employee_19;Pieter Parker;pieter@odoo.com;3281813700;;Sales;Male;;Single;;Ireland;;;;;;;;;;;;\n-hr_employee_20;Roger Scott;;3282823500;;Sales;Male;;Married;;United States;;;;;;;;;;;;\n-hr_employee_21;Николай Петра;;3282823500;;Administration;Male;;Single;;Belgium;;;;;;;;;;;;\n-hr_employee_22;佐藤さくら;;3282823500;;Sales;Male;;Single;;China;;;;;;;;;;;;\n-hr_employee_23;趙生;;3282823500;;Sales;Male;;Single;;Japan;;;;;;;;;;;;\n+﻿External ID;Name;Work Email;Work Phone;Work Mobile;Department;Gender;Notes;Marital Status;Date of Birth;Nationality (Country);Identification No;Passport No;Visa No;Work Permit No;Visa Expire Date;;;;;;;\n+hr_employee_01;Luis Herrera;luis.herrera@terrabyteec.com;022910001;0999100001;Taller;Male;;Married;12/02/1983;Ecuador;0102030405;;;;;;;;;;\n+hr_employee_02;Sofia Mena;sofia.mena@terrabyteec.com;022910002;0999100002;Taller;Female;;Single;08/09/1990;Ecuador;0102030406;;;;;;;;;;\n+hr_employee_03;Carlos Paredes;carlos.paredes@terrabyteec.com;022910003;0999100003;Taller;Male;;Married;21/06/1985;Ecuador;0102030407;;;;;;;;;;\n+hr_employee_04;Andrea Ruiz;andrea.ruiz@terrabyteec.com;022910004;0999100004;Taller;Female;;Single;03/11/1992;Ecuador;0102030408;;;;;;;;;;\n+hr_employee_05;Jorge Vega;jorge.vega@terrabyteec.com;022910005;0999100005;Taller;Male;;Married;17/01/1987;Ecuador;0102030409;;;;;;;;;;\n+hr_employee_06;Paola Castro;paola.castro@terrabyteec.com;022910006;0999100006;Taller;Female;;Single;30/07/1991;Ecuador;0102030410;;;;;;;;;;\n+hr_employee_07;Diego Luna;diego.luna@terrabyteec.com;022910007;0999100007;Taller;Male;;Single;25/05/1989;Ecuador;0102030411;;;;;;;;;;\n+hr_employee_08;Gabriela Ortiz;gabriela.ortiz@terrabyteec.com;022910008;0999100008;Taller;Female;;Married;14/03/1988;Ecuador;0102030412;;;;;;;;;;\n+hr_employee_09;Juan Mora;juan.mora@terrabyteec.com;022910009;0999100009;Almacen;Male;;Married;09/10/1984;Ecuador;0102030413;;;;;;;;;;\n+hr_employee_10;Valeria Nunez;valeria.nunez@terrabyteec.com;022910010;0999100010;Almacen;Female;;Single;06/12/1993;Ecuador;0102030414;;;;;;;;;;\n+hr_employee_11;Ricardo Salas;ricardo.salas@terrabyteec.com;022910011;0999100011;Almacen;Male;;Married;19/04/1986;Ecuador;0102030415;;;;;;;;;;\n+hr_employee_12;Mariana Paz;mariana.paz@terrabyteec.com;022910012;0999100012;Compras;Female;;Married;02/08/1985;Ecuador;0102030416;;;;;;;;;;\n+hr_employee_13;Mateo Silva;mateo.silva@terrabyteec.com;022910013;0999100013;Compras;Male;;Single;11/09/1991;Ecuador;0102030417;;;;;;;;;;\n+hr_employee_14;Natalia Velez;natalia.velez@terrabyteec.com;022910014;0999100014;Compras;Female;;Single;27/01/1994;Ecuador;0102030418;;;;;;;;;;\n+hr_employee_15;Esteban Rios;esteban.rios@terrabyteec.com;022910015;0999100015;Ventas;Male;;Married;22/05/1982;Ecuador;0102030419;;;;;;;;;;\n+hr_employee_16;Fernanda Cobo;fernanda.cobo@terrabyteec.com;022910016;0999100016;Ventas;Female;;Single;10/10/1992;Ecuador;0102030420;;;;;;;;;;\n+hr_employee_17;Kevin Torres;kevin.torres@terrabyteec.com;022910017;0999100017;Ventas;Male;;Single;05/06/1993;Ecuador;0102030421;;;;;;;;;;\n+hr_employee_18;Camila Rojas;camila.rojas@terrabyteec.com;022910018;0999100018;Ventas;Female;;Single;15/09/1994;Ecuador;0102030422;;;;;;;;;;\n+hr_employee_19;Oscar Molina;oscar.molina@terrabyteec.com;022910019;0999100019;Ventas;Male;;Married;28/02/1988;Ecuador;0102030423;;;;;;;;;;\n+hr_employee_20;Daniela Soria;daniela.soria@terrabyteec.com;022910020;0999100020;Administracion;Female;;Married;07/07/1986;Ecuador;0102030424;;;;;;;;;;\n+hr_employee_21;Pablo Leon;pablo.leon@terrabyteec.com;022910021;0999100021;Administracion;Male;;Single;18/03/1992;Ecuador;0102030425;;;;;;;;;;\n+hr_employee_22;Irene Lara;irene.lara@terrabyteec.com;022910022;0999100022;Administracion;Female;;Married;23/01/1987;Ecuador;0102030426;;;;;;;;;;\n+hr_employee_23;Miguel Tapia;miguel.tapia@terrabyteec.com;022910023;0999100023;Administracion;Male;;Single;29/11/1995;Ecuador;0102030427;;;;;;;;;;\n+hr_employee_24;Lorena Rivas;lorena.rivas@terrabyteec.com;022910024;0999100024;Administracion;Female;;Single;04/04/1993;Ecuador;0102030428;;;;;;;;;;\n+hr_employee_25;Hugo Viteri;hugo.viteri@terrabyteec.com;022910025;0999100025;Calidad;Male;;Married;16/06/1984;Ecuador;0102030429;;;;;;;;;;\n+hr_employee_26;Carla Pino;carla.pino@terrabyteec.com;022910026;0999100026;Calidad;Female;;Single;12/12/1996;Ecuador;0102030430;;;;;;;;;;\n+hr_employee_27;Sergio Ponce;sergio.ponce@terrabyteec.com;022910027;0999100027;Taller;Male;;Single;09/09/1989;Ecuador;0102030431;;;;;;;;;;\n+hr_employee_28;Noelia Cruz;noelia.cruz@terrabyteec.com;022910028;0999100028;Taller;Female;;Single;01/01/1991;Ecuador;0102030432;;;;;;;;;;\n+hr_employee_29;Adrian Loja;adrian.loja@terrabyteec.com;022910029;0999100029;Taller;Male;;Married;20/08/1987;Ecuador;0102030433;;;;;;;;;;\n+hr_employee_30;Maria Vera;maria.vera@terrabyteec.com;022910030;0999100030;Taller;Female;;Single;13/05/1994;Ecuador;0102030434;;;;;;;;;;\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
M data_import/employee_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 2.3s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/departamentos.csv\n+Name,Manager,Parent Department,Color\n+Taller,Luis Herrera,,1\n+Almacen,Juan Mora,,2\n+Compras,Mariana Paz,,3\n+Ventas,Esteban Rios,,4\n+Administracion,Daniela Soria,,5\n+Calidad,Hugo Viteri,Administracion,6\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/departamentos.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 2.4s)

Listo. Actualicé empleados y creé departamentos.

Archivos:
- `data_import/employee_template.csv` (30 empleados de Terrabyte EC)
- `data_import/departamentos.csv` (6 departamentos con gerente, departamento principal y color)

Orden recomendado de importación:
1) Empleados → Departamentos → Importar `data_import/departamentos.csv`
2) Empleados → Importar `data_import/employee_template.csv`

Si Odoo te pide nombres exactos de columnas diferentes, pásame el error o una plantilla de departamentos y lo ajusto.

---

## User

algo hiciste mal en el employe template, me dice: Se encontró una sola columna en el archivo, por lo general esto indica que el separador de archivos no es correcto.

---

## Assistant (Build · GPT-5.2-Codex · 6.4s)

_Thinking:_

**Planning CSV delimiter fix**

I’m preparing to convert the CSV file from semicolon- to comma-delimited, remove the BOM, ensure ASCII encoding, and clean up trailing empty columns by rewriting the entire file via an apply_patch that replaces its content.

_Thinking:_

**Trimming CSV columns**

Decided to keep header columns only up to "Visa Expire Date," removing trailing empty columns to simplify the CSV while maintaining compatibility with Odoo.

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Delete File: data_import/employee_template.csv\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
D data_import/employee_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 14.3s)

**Tool: apply_patch**

**Input:**
```json
{
  "patchText": "*** Begin Patch\n*** Add File: data_import/employee_template.csv\n+External ID;Name;Work Email;Work Phone;Work Mobile;Department;Gender;Notes;Marital Status;Date of Birth;Nationality (Country);Identification No;Passport No;Visa No;Work Permit No;Visa Expire Date\n+hr_employee_01;Luis Herrera;luis.herrera@terrabyteec.com;022910001;0999100001;Taller;Male;;Married;12/02/1983;Ecuador;0102030405;;;;\n+hr_employee_02;Sofia Mena;sofia.mena@terrabyteec.com;022910002;0999100002;Taller;Female;;Single;08/09/1990;Ecuador;0102030406;;;;\n+hr_employee_03;Carlos Paredes;carlos.paredes@terrabyteec.com;022910003;0999100003;Taller;Male;;Married;21/06/1985;Ecuador;0102030407;;;;\n+hr_employee_04;Andrea Ruiz;andrea.ruiz@terrabyteec.com;022910004;0999100004;Taller;Female;;Single;03/11/1992;Ecuador;0102030408;;;;\n+hr_employee_05;Jorge Vega;jorge.vega@terrabyteec.com;022910005;0999100005;Taller;Male;;Married;17/01/1987;Ecuador;0102030409;;;;\n+hr_employee_06;Paola Castro;paola.castro@terrabyteec.com;022910006;0999100006;Taller;Female;;Single;30/07/1991;Ecuador;0102030410;;;;\n+hr_employee_07;Diego Luna;diego.luna@terrabyteec.com;022910007;0999100007;Taller;Male;;Single;25/05/1989;Ecuador;0102030411;;;;\n+hr_employee_08;Gabriela Ortiz;gabriela.ortiz@terrabyteec.com;022910008;0999100008;Taller;Female;;Married;14/03/1988;Ecuador;0102030412;;;;\n+hr_employee_09;Juan Mora;juan.mora@terrabyteec.com;022910009;0999100009;Almacen;Male;;Married;09/10/1984;Ecuador;0102030413;;;;\n+hr_employee_10;Valeria Nunez;valeria.nunez@terrabyteec.com;022910010;0999100010;Almacen;Female;;Single;06/12/1993;Ecuador;0102030414;;;;\n+hr_employee_11;Ricardo Salas;ricardo.salas@terrabyteec.com;022910011;0999100011;Almacen;Male;;Married;19/04/1986;Ecuador;0102030415;;;;\n+hr_employee_12;Mariana Paz;mariana.paz@terrabyteec.com;022910012;0999100012;Compras;Female;;Married;02/08/1985;Ecuador;0102030416;;;;\n+hr_employee_13;Mateo Silva;mateo.silva@terrabyteec.com;022910013;0999100013;Compras;Male;;Single;11/09/1991;Ecuador;0102030417;;;;\n+hr_employee_14;Natalia Velez;natalia.velez@terrabyteec.com;022910014;0999100014;Compras;Female;;Single;27/01/1994;Ecuador;0102030418;;;;\n+hr_employee_15;Esteban Rios;esteban.rios@terrabyteec.com;022910015;0999100015;Ventas;Male;;Married;22/05/1982;Ecuador;0102030419;;;;\n+hr_employee_16;Fernanda Cobo;fernanda.cobo@terrabyteec.com;022910016;0999100016;Ventas;Female;;Single;10/10/1992;Ecuador;0102030420;;;;\n+hr_employee_17;Kevin Torres;kevin.torres@terrabyteec.com;022910017;0999100017;Ventas;Male;;Single;05/06/1993;Ecuador;0102030421;;;;\n+hr_employee_18;Camila Rojas;camila.rojas@terrabyteec.com;022910018;0999100018;Ventas;Female;;Single;15/09/1994;Ecuador;0102030422;;;;\n+hr_employee_19;Oscar Molina;oscar.molina@terrabyteec.com;022910019;0999100019;Ventas;Male;;Married;28/02/1988;Ecuador;0102030423;;;;\n+hr_employee_20;Daniela Soria;daniela.soria@terrabyteec.com;022910020;0999100020;Administracion;Female;;Married;07/07/1986;Ecuador;0102030424;;;;\n+hr_employee_21;Pablo Leon;pablo.leon@terrabyteec.com;022910021;0999100021;Administracion;Male;;Single;18/03/1992;Ecuador;0102030425;;;;\n+hr_employee_22;Irene Lara;irene.lara@terrabyteec.com;022910022;0999100022;Administracion;Female;;Married;23/01/1987;Ecuador;0102030426;;;;\n+hr_employee_23;Miguel Tapia;miguel.tapia@terrabyteec.com;022910023;0999100023;Administracion;Male;;Single;29/11/1995;Ecuador;0102030427;;;;\n+hr_employee_24;Lorena Rivas;lorena.rivas@terrabyteec.com;022910024;0999100024;Administracion;Female;;Single;04/04/1993;Ecuador;0102030428;;;;\n+hr_employee_25;Hugo Viteri;hugo.viteri@terrabyteec.com;022910025;0999100025;Calidad;Male;;Married;16/06/1984;Ecuador;0102030429;;;;\n+hr_employee_26;Carla Pino;carla.pino@terrabyteec.com;022910026;0999100026;Calidad;Female;;Single;12/12/1996;Ecuador;0102030430;;;;\n+hr_employee_27;Sergio Ponce;sergio.ponce@terrabyteec.com;022910027;0999100027;Taller;Male;;Single;09/09/1989;Ecuador;0102030431;;;;\n+hr_employee_28;Noelia Cruz;noelia.cruz@terrabyteec.com;022910028;0999100028;Taller;Female;;Single;01/01/1991;Ecuador;0102030432;;;;\n+hr_employee_29;Adrian Loja;adrian.loja@terrabyteec.com;022910029;0999100029;Taller;Male;;Married;20/08/1987;Ecuador;0102030433;;;;\n+hr_employee_30;Maria Vera;maria.vera@terrabyteec.com;022910030;0999100030;Taller;Female;;Single;13/05/1994;Ecuador;0102030434;;;;\n*** End Patch"
}
```

**Output:**
```
Success. Updated the following files:
A data_import/employee_template.csv
```

---

## Assistant (Build · GPT-5.2-Codex · 2.6s)

Arreglado. El problema era el separador detectado; dejé el archivo limpio sin BOM ni columnas vacías, con `;` como separador.

Archivo actualizado:
- `data_import/employee_template.csv`

Al importar:
- Separador de campo: `;`
- Delimitador de texto: `"`
- Formato fecha: `DD/MM/YYYY`

Prueba y si aún falla, dime exactamente qué separador estás seleccionando en Odoo y lo ajusto.

---

## User

me salio esto: Encontramos más de 10 errores y más de un error por cada 10 registros. El sistema interrumpió el proceso para evitar que aparezcan demasiados errores.

Error en la fila 0: "El ID de la credencial debe ser alfanumérico, no debe tener acentos y tampoco debe exceder los 18 caracteres."

Error en la fila 0: "El registro no existe o fue eliminado. (Registro: resource.resource(104,), Usuario: 2)"

Error en la fila 1: "El registro no existe o fue eliminado. (Registro: resource.resource(105,), Usuario: 2)"

Error en la fila 2: "El registro no existe o fue eliminado. (Registro: resource.resource(106,), Usuario: 2)"

Error en la fila 3: "El registro no existe o fue eliminado. (Registro: resource.resource(107,), Usuario: 2)"

Error en la fila 4: "El registro no existe o fue eliminado. (Registro: resource.resource(108,), Usuario: 2)"

Error en la fila 5: "El registro no existe o fue eliminado. (Registro: resource.resource(109,), Usuario: 2)"

Error en la fila 6: "El registro no existe o fue eliminado. (Registro: resource.resource(110,), Usuario: 2)"

Error en la fila 7: "El registro no existe o fue eliminado. (Registro: resource.resource(111,), Usuario: 2)"

Error en la fila 8: "El registro no existe o fue eliminado. (Registro: resource.resource(112,), Usuario: 2)"

Error en la fila 9: "El registro no existe o fue eliminado. (Registro: resource.resource(113,), Usuario: 2)" 

---

## Assistant (Build · GPT-5.2-Codex · 4.6s)

_Thinking:_

**Requesting exact import template**

I'll ask the user to share the exact employee import template or a screenshot of the Odoo import mapping to clarify External ID issues and verify field names.

Ese error viene del campo **External ID** (debe ser alfanumérico, sin acentos y máx. 18 caracteres). Además, los errores de `resource.resource(...)` suelen aparecer cuando Odoo está intentando mapear columnas incorrectas para empleados.

Para corregirlo con precisión necesito la plantilla real de Odoo.

Por favor:
- Descarga la **plantilla de importación de Empleados** desde Odoo (Importar → Descargar plantilla) y guárdala en `data_import/`.
- Dime el nombre exacto del archivo.

Con esa plantilla te la dejo lista sin errores.

---

