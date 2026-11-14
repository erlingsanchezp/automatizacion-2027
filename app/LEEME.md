# Laboratorios de Automatización 2027

Empieza por el capítulo 9 del libro. Este paquete acompaña las treinta prácticas de Zapier, Make y n8n y conserva el manuscrito editable en libro/.

## Inicio rápido

1. Extrae el ZIP completo. Abre una terminal en la carpeta que contiene este archivo.
2. Comprueba Python 3.11 o posterior: `python3 --version`. En Windows puedes usar `py` en lugar de `python3` en todos estos comandos.
3. Ejecuta `python3 lab/server.py` y deja abierta esa terminal.
4. En otra terminal ejecuta `python3 lab/client.py GET http://127.0.0.1:8787/health`.
5. Ejecuta `python3 lab/client.py GET http://127.0.0.1:8787/catalog --auth`.
6. La clave aleatoria está en lab/token.txt, creado durante el primer inicio. Consérvala privada y utiliza el gestor de credenciales de tu plataforma.
7. Para llamadas desde la nube instala cloudflared y ejecuta `cloudflared tunnel --url http://127.0.0.1:8787`. La URL HTTPS real que te devuelva será BASE.
8. Detén el túnel y el servidor con Ctrl+C al terminar.

## Enviar eventos

Para validar directamente contra el servidor:

```bash
python3 lab/client.py POST http://127.0.0.1:8787/validate --file datos/evento_01.json --auth
```

Para enviar a un webhook de práctica reemplaza la URL y no uses --auth, que corresponde solamente al token de este servidor:

```bash
python3 lab/client.py POST "URL_REAL_DEL_WEBHOOK" --file datos/evento_01.json
```

## Resultados de referencia

- Cinco registros; tres estructuralmente válidos; dos elegibles.
- Dos tareas finales después de aprobar las dos solicitudes elegibles.
- Misma clave y cuerpo: mismo task_id. Cuerpo diferente con misma clave: 409.
- Reporte CSV: 46 contactos, 11 citas, conversión 23.91 por ciento.
- /classify es una simulación determinista: no usa un modelo real ni constituye un filtro completo de seguridad.

## Pruebas

```bash
python3 -m unittest discover -s pruebas -v
node pruebas/test_codigo.js
```

La primera suite utiliza Python estándar. La segunda necesita Node.js y comprueba lógica JavaScript. No son pruebas de integración de tus cuentas Zapier, Make o n8n. Las importaciones n8n deben revisarse en tu versión.

## Bases independientes

Detén primero el servidor actual y ejecuta uno de estos comandos para medir un proyecto nuevo:

```bash
python3 lab/server.py --db lab/proyecto_z.sqlite3
python3 lab/server.py --db lab/proyecto_m.sqlite3
python3 lab/server.py --db lab/proyecto_n.sqlite3
```

Ejecuta solo uno a la vez en el puerto predeterminado. Un nombre de archivo ya usado conserva sus tareas. El servidor no tiene un endpoint público de borrado o reinicio. No compartas las bases ni token.txt con terceros.

## Alcance

Base documental: 18 de octubre de 2026. Edición de aprendizaje para 2027, con revisión de compatibilidad antes del uso. El servidor es educativo y no está diseñado para alojar datos reales ni operar como servicio público permanente.
