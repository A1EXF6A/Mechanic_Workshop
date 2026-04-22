# Odoo with Podman Compose

Este proyecto levanta Odoo + Postgres usando `podman-compose`.

## 1) Configurar variables

1. Copia el ejemplo de entorno:

```bash
cp .env.example .env
```

2. Edita `.env` y cambia al menos `DB_PASSWORD`.

### Compatibilidad Linux / Windows

- Linux con SELinux (Fedora/RHEL/CentOS): usa `BIND_MOUNT_SUFFIX=:Z` (o `:z`) en `.env`.
- Linux sin SELinux y Windows: deja `BIND_MOUNT_SUFFIX=` vacio.

## 2) Levantar servicios

```bash
podman-compose up -d
```

## 3) Ver estado y logs

```bash
podman-compose ps
podman-compose logs -f
```

## 4) Acceso

- Odoo: `http://localhost:${ODOO_HTTP_PORT}` (por defecto `8070`)

## Notas

- `depends_on` usa `condition: service_healthy`, por lo que Odoo espera a que Postgres este sano.
- Se incluyen `healthcheck` para `db` y `odoo`.
