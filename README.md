# Pre-entrega Automation Testing — SauceDemo

Proyecto de automatización de pruebas web para la aplicación de demostración
[SauceDemo](https://www.saucedemo.com/) usando **Python + Pytest + Selenium
WebDriver**. Cubre tres flujos: login exitoso, validación del catálogo de
productos y agregado de un producto al carrito. Incluye además pruebas de API
REST con **Requests** contra [JSONPlaceholder](https://jsonplaceholder.typicode.com/).

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python | Lenguaje del proyecto |
| Pytest | Framework de tests y fixtures |
| Selenium WebDriver | Automatización del navegador (Chrome) |
| pytest-html | Reporte HTML de ejecución |
| Requests | Pruebas de API REST |
| Git / GitHub | Versionado y entrega |

## Instalación

Prerrequisitos: Python 3.x y Google Chrome instalados.

```bash
git clone <URL-del-repo>
cd pre-entrega-automation-testing-fernando-verdus
python -m venv .venv
```

Activar el entorno virtual:

```powershell
.venv\Scripts\Activate.ps1    # Windows PowerShell
source .venv/bin/activate     # macOS / Linux
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución de pruebas

```bash
pytest -v              # UI + API
pytest -v tests/ui/    # solo UI (Selenium)
pytest -v tests/api/   # solo API (no abre navegador)
```

Cada ejecución genera además el reporte HTML `reports/reporte.html`: las
opciones están en `pytest.ini` (`--html=reports/reporte.html --self-contained-html`).
El comando explícito equivalente es:

```bash
pytest -v --html=reports/reporte.html --self-contained-html
```

Selenium Manager (incluido en Selenium) descarga automáticamente el driver de
Chrome adecuado; no hace falta instalarlo a mano.

## Estructura del proyecto

```text
├── tests/
│   ├── ui/                    # Pruebas de interfaz (Selenium)
│   │   ├── test_login.py      # Login positivo, fallos con banner y sesión
│   │   ├── test_inventory.py  # Catálogo, ordenamiento y detalle de producto
│   │   ├── test_cart.py       # Agregado al carrito
│   │   └── test_checkout.py   # Checkout: resumen, validaciones y cancelación
│   └── api/                   # Pruebas de API (Requests)
│       └── test_posts.py      # GET, POST, DELETE y error 404 sobre /posts
├── pages/                     # Page Objects: locators e interacciones por página
│   ├── header.py              # Header compartido (título, carrito, menú, logout)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── utils/
│   ├── driver.py              # Creación/configuración del WebDriver
│   ├── helpers.py             # Configuración, esperas explícitas y clicks compartidos
│   ├── data_loader.py         # Carga de datos de prueba desde data/
│   └── api_client.py          # Cliente HTTP de la API (Requests) con logging
├── data/                      # Datos de prueba externos (JSON)
│   ├── login_data.json        # Casos de login válidos e inválidos con su error esperado
│   ├── checkout_data.json     # Datos del comprador y caso sin código postal
│   └── api_data.json          # Payload del POST de la API
├── reports/
│   ├── reporte.html           # Reporte HTML (última ejecución; se regenera)
│   ├── screenshots/           # Capturas automáticas de fallos (generado)
│   └── logs/                  # test_execution.log (última ejecución)
├── conftest.py                # Fixtures del navegador y cliente API, logging y captura de fallos
├── pytest.ini                 # Configuración de pytest (descubrimiento y reporte HTML)
├── requirements.txt           # Dependencias
└── README.md
```

## Cobertura de pruebas

| Test | Qué valida |
|---|---|
| `test_successful_login` | El usuario `standard_user` inicia sesión y llega a `/inventory.html`, con encabezado `Products` y título `Swag Labs` |
| `test_login_failure_shows_error_banner` ×4 | Usuario bloqueado, credenciales incorrectas, username vacío y password vacío muestran el banner de error y no avanzan al inventario |
| `test_back_button_after_logout_does_not_restore_session` | Tras logout, el botón "back" del navegador no muestra el inventario: vuelve al login |
| `test_inventory_catalog` | El catálogo carga con al menos un producto, navegación/carrito/orden visibles, y extrae nombre y precio del primer producto |
| `test_product_sorting` | Las cuatro opciones de ordenamiento (nombre y precio, ascendente/descendente) dejan el producto esperado primero |
| `test_product_detail_page_matches_catalog` | La página de detalle muestra nombre y precio idénticos al catálogo; agregar desde allí setea el badge y persiste al volver |
| `test_add_first_product_to_cart` | El primer producto se agrega al carrito, el contador muestra `1` y el producto aparece en `/cart.html` |
| `test_checkout_completes_order` | Flujo completo carrito → datos → resumen (subtotal $29.99, impuesto $2.40, total $32.39) → finish → "Thank you for your order!" |
| `test_checkout_requires_postal_code` | Sin código postal, el banner "Postal Code is required" bloquea el paso 2 |
| `test_checkout_cancel_returns_to_cart` | Cancelar en el paso 1 vuelve al carrito con el producto intacto |

### API (JSONPlaceholder `/posts`)

JSONPlaceholder simula las escrituras: POST y DELETE responden como si
persistieran, pero no cambian los datos. Los tests validan el contrato
observado y no asumen persistencia.

| Test | Qué valida |
|---|---|
| `test_get_post_by_id` | GET `/posts/1`: 200, JSON, campos `userId`/`id`/`title`/`body` con sus tipos e `id == 1` |
| `test_get_posts_filtered_by_user` | GET `/posts?userId=1`: 200, lista de 10 posts, todos del usuario 1 |
| `test_create_post` | POST `/posts`: 201, devuelve los campos enviados y un `id` nuevo |
| `test_delete_post` | DELETE `/posts/1`: 200 y objeto vacío (borrado simulado) |
| `test_get_missing_post_returns_404` | GET `/posts/99999`: 404 con objeto JSON vacío (escenario de error) |

Cada test UI es independiente: abre su propio navegador, inicia sesión por su
cuenta y cierra el navegador al terminar (fixture de alcance de test).

## Decisiones de automatización

- **Esperas explícitas** (`WebDriverWait` + `expected_conditions`) en toda
  interacción; un único timeout centralizado en `utils/helpers.py`.
- **Locators estables**: IDs donde existen (`#user-name`, `#password`,
  `#login-button`) y atributos `data-test` del DOM de SauceDemo para el
  resto, verificados contra la aplicación en vivo.
- **Clicks por evento DOM**: la aplicación React descarta ocasionalmente el
  click nativo si aún no montó sus listeners; se dispara el evento de click
  del DOM directamente y el alta al carrito se confirma leyendo el badge,
  con reintento controlado (nunca doble alta).

## Reportes y evidencia

- **Reporte HTML:** `reports/reporte.html`, autocontenido (se puede mover o
  compartir sin perder imágenes). Muestra estado, categoría **UI** o **API**,
  duración y detalle de fallo de cada test. Se incluye la última ejecución
  como evidencia; cada corrida lo regenera.
- **Capturas de fallo:** `reports/screenshots/<test>_<AAAAMMDD_HHMMSS>.png`.
  Se toman automáticamente solo cuando falla un test de UI, se embeben en la
  entrada del reporte junto con la URL de la página y no se pisan entre
  corridas. Los caracteres no válidos en nombres de archivo (p. ej. los `[ ]`
  de los tests parametrizados) se reemplazan por `-`. Si la captura falla, se
  registra en el log y el test conserva su falla original.
- **Logs de ejecución:** `reports/logs/test_execution.log`, se sobrescribe en
  cada corrida. Registra inicio de cada test, acciones principales de UI,
  cada request de API (método, URL y status) y el resultado. Las contraseñas
  nunca se escriben en el log.
- **Clasificación de fallas:** ninguna falla se omite ni se convierte en
  aprobada. El mensaje distingue servicio no disponible (`SauceDemo
  unavailable` / `External API unavailable`, incluye errores de conexión,
  timeouts y HTTP 5xx), status HTTP inesperado (esperado vs. recibido con la
  URL) y error de validación (esperado vs. encontrado).

## Credenciales

`standard_user` / `secret_sauce` — provistas públicamente por el entorno de
demostración de SauceDemo.
