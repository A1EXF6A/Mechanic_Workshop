from locust import HttpUser, task, between

class TallerLoadTestUser(HttpUser):
    # Tiempo de espera entre peticiones de cada usuario virtual (entre 1 y 3 segundos)
    wait_time = between(1, 3)
    
    # URL base del entorno local de Odoo
    host = "http://localhost:8070"

    @task(2)
    def index_page(self):
        """Simula al usuario visitando la página de inicio"""
        self.client.get("/")

    @task(1)
    def tienda_productos(self):
        """Simula al usuario navegando al catálogo de repuestos"""
        self.client.get("/taller/productos")

    @task(1)
    def nosotros_page(self):
        """Simula al usuario revisando la información del taller"""
        self.client.get("/taller/nosotros")
