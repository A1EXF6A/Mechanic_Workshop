import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  // Configuración de la prueba: 50 usuarios virtuales durante 30 segundos
  stages: [
    { duration: '10s', target: 50 }, // Ramp-up: subir a 50 usuarios en 10s
    { duration: '15s', target: 50 }, // Mantener 50 usuarios por 15s
    { duration: '5s', target: 0 },   // Ramp-down: bajar a 0 usuarios en 5s
  ],
  thresholds: {
    // Definimos criterios de aceptación de rendimiento
    http_req_failed: ['rate<0.01'],   // Menos del 1% de las peticiones pueden fallar
    http_req_duration: ['p(95)<1500'], // El 95% de las peticiones deben tardar menos de 1.5s
  },
};

export default function () {
  // Simulamos un usuario navegando a la página principal y luego a la tienda
  const baseUrl = 'http://localhost:8070'; // Usamos IP del host interno desde Docker o localhost si corremos local
  
  // 1. Visitar inicio
  let res = http.get(`${baseUrl}/`);
  check(res, {
    'Inicio - status es 200': (r) => r.status === 200,
  });
  sleep(1);

  // 2. Visitar Catálogo de Tienda
  let resTienda = http.get(`${baseUrl}/taller/productos`);
  check(resTienda, {
    'Tienda - status es 200': (r) => r.status === 200,
    'Tienda - contiene Catálogo': (r) => r.body && r.body.includes('Repuestos'),
  });
  sleep(1);
}
