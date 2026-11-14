# Alcance de verificación de esta edición

Fecha de preparación: 18 de octubre de 2026.

## Ejecutado localmente

- 21 pruebas de Python del servidor, autenticación, paginación, validación, reportes, escritura idempotente, conflictos y errores simulados.
- Ocho llamadas simultáneas con igual clave y cuerpo: una creación y el mismo task_id en todas las respuestas satisfactorias.
- Pruebas de lógica JavaScript de normalización y adaptadores, revisión humana, validación de clasificación y reporte.
- Programa de paginación de Zapier ejecutado con JavaScript asíncrono contra la API local: cinco eventos únicos recuperados en tres páginas.
- Análisis estructural de los dos JSON de n8n: sintaxis válida, conexiones internas completas, sin credenciales y desactivados.
- Contraste entre los nombres de archivos usados en el libro y el contenido del paquete.
- PDF renderizado, índice y enlaces internos comprobados, inspección visual de las páginas y comprobación de límites del contenido.

## Requiere prueba en la cuenta del lector

No se ejecutaron los flujos en cuentas autenticadas de Zapier, Make o n8n durante la elaboración. Los ejemplos se basan en documentación oficial. Es necesario verificar conexiones, permisos, plan, interfaz, versión e importación antes del uso.

Las pruebas de JavaScript fuera de la plataforma no reproducen sus límites, permisos ni todas sus reglas de ejecución. La documentación y disponibilidad de funciones deben volver a comprobarse durante 2027. El simulador /classify no es un modelo de IA real.
