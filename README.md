# Sistema de Nodos Incrementales con Docker Compose

Este proyecto implementa una aplicación distribuida de nodos que se pasan un valor incrementalmente usando Flask y Docker.

---

## Contenido del repositorio

- `node.py` — Código Python que ejecuta el servidor Flask para cada nodo.
- `Dockerfile` — Imagen Docker para construir el contenedor con Python y dependencias.
- `docker-compose.yaml` — Orquestación de varios nodos con diferentes variables de entorno.

---

## Requisitos previos

- Tener instalado Docker y Docker Compose.
- Acceso a terminal / consola.

---

## Pasos para ejecutar la aplicación

### 1. Comando para crear imagen, contenedores y ejecutarlo (Se ejecuta en la carpeta raiz)

```bash
docker compose up
```
### 2. Acceder al programa

Para acceder al programa se tendrá que acceder al localhost:5000 trás el docker compose up y ahí ya se podrá ejecutar.
#### IMPORTANTE: PARA VER LOS VALORES ACTUALIZADOS EN LA PESTAÑA, HAY QUE RECARGARLA MANUALMENTE

### 3. Desinstalar/Borrar el programa

Lo primero es realizar control + c

Después se realiza el comando: 

```bash
docker compose down
```
Por último se accede a docker y se borra manualmente la imagen residual que queda ahí guardada.

### 4. Diagrama de Flujo

```mermaid
graph TD
    A[Inicio] --> B[Nodo 1: Recibe solicitud /iniciar]
    B --> C[Incrementa valor + INCREMENT]
    C --> D[Guarda valor en historial]
    D --> E{NEXT_NODE existe?}
    E -->|Sí| F[Envía valor a siguiente nodo vía POST /process]
    E -->|No| G[Envía valor a nodo1 vía POST /reset]
    F --> H[Nodo siguiente: Recibe solicitud /process]
    H --> C
    G --> I[Nodo 1: Recibe solicitud /reset]
    I --> J[Actualiza current_value y guarda en historial]
    J --> K[Fin]
```
