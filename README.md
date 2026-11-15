# QA Automation — SauceDemo UI + JSONPlaceholder API

Framework de automatización de pruebas en **Python + Pytest** con dos suites:

- **UI** (Selenium WebDriver) sobre la tienda de demostración
  [SauceDemo](https://www.saucedemo.com/): login (positivo y negativos),
  catálogo, ordenamiento, detalle de producto, carrito y checkout completo.
- **API** (Requests) sobre la API pública de demostración
  [JSONPlaceholder](https://jsonplaceholder.typicode.com/): GET, POST, DELETE
  y un escenario de error.

Cada ejecución produce un reporte HTML, un log de ejecución y, si falla un
test de UI, una captura de pantalla embebida en el reporte.

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

Prerrequisitos: Python 3.10 o superior (lo exigen las versiones actuales de
pytest, Selenium y Requests), Google Chrome y acceso a internet (ambas
aplicaciones bajo prueba son servicios públicos en línea).

```bash
git clone https://github.com/Feerdus95/proyecto-final-automation-testing-fernando-verdus.git
cd proyecto-final-automation-testing-fernando-verdus
python -m venv .venv
```

Activar el entorno virtual:

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux (bash/zsh):

```bash
source .venv/bin/activate
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
pytest -v tests/ui/test_login.py::test_successful_login   # un test puntual
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

| Suite | Funciones de test | Ejecuciones |
|---|---|---|
| UI | 10 | 13 (el login negativo se parametriza en 4 casos) |
| API | 5 | 5 |
| **Total** | **15** | **18** |

### UI (SauceDemo)

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

Cada test UI es independiente: abre su propio navegador, prepara por su
cuenta el estado que necesita (los escenarios autenticados hacen su propio
login; los de login fallido parten de la pantalla de login) y cierra el
navegador al terminar (fixture de alcance de test).

## Datos de prueba externos

Los datos de los escenarios viven en `data/` como JSON y se cargan con
`utils/data_loader.py` (`load_json`), sin dependencia de Selenium.

| Archivo | Estructura | Lo usa |
|---|---|---|
| `login_data.json` | `valid`: lista de `{id, username, password}`; `invalid`: lista de `{id, username, password, expected_error}` | `test_successful_login` y `test_login_failure_shows_error_banner` (parametrizados; `id` nombra cada caso en el reporte) |
| `checkout_data.json` | `buyer`: `{first_name, last_name, postal_code}`; `missing_postal_code`: lo mismo con `postal_code` vacío y `expected_error` | Tests de checkout |
| `api_data.json` | `new_post`: `{title, body, userId}` | `test_create_post` |

Agregar un caso de login negativo es agregar un objeto a `invalid`: el test
lo toma sin cambios de código.

## Arquitectura

- **Page Object Model** (`pages/`): cada página de SauceDemo es una clase con
  sus locators y acciones (`LoginPage`, `InventoryPage`, `ProductDetailPage`,
  `CartPage`, `CheckoutPage`). Los tests solo llaman acciones y hacen
  aserciones; no contienen locators ni esperas de Selenium.
- **Header como componente**: el encabezado común (título, carrito, menú,
  logout) es la clase `Header`, que las páginas incluyen por composición
  (`inventory.header.cart_badge_value()`), sin clases base.
- **Separación de responsabilidades**:
  - `tests/ui/` y `tests/api/`: escenarios y aserciones, cada suite ejecutable
    por separado.
  - `utils/`: infraestructura compartida (driver, esperas, cliente API,
    carga de datos).
  - `data/`: datos de prueba.
  - `conftest.py`: fixtures (`driver` con un navegador nuevo por test,
    `api_client`), logging y captura de fallos.

### Decisiones de automatización

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
  Se toman automáticamente solo cuando un test de UI falla durante su ejecución
  (fase `call`), no ante errores de preparación o cierre (`setup`/`teardown`); se embeben en la
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

### Cómo interpretar los resultados

**1. Resumen en la consola.** La última línea de `pytest -v` resume la
corrida, por ejemplo `18 passed in 46.75s`. Si algo falla, aparece
`N failed` y, arriba, un bloque `FAILED <test>` con el motivo.

**2. Reporte HTML.** Abrir `reports/reporte.html` en el navegador.

- Arriba, **Summary** muestra cuántos tests pasaron, fallaron o dieron
  error. Cada contador es también un filtro: destildar *Passed* deja a la
  vista solo los fallos.
- La tabla tiene una fila por ejecución, con **Result** (Passed/Failed),
  **Category** (UI o API), nombre del test (los casos parametrizados llevan
  su id entre corchetes, p. ej. `[locked-out]`) y **Duration**.
- Las filas fallidas se muestran desplegadas (cualquier fila se abre o
  cierra con un clic). El detalle incluye la línea del test que falló, el
  mensaje de error y, si es de UI, la **captura de pantalla** del momento de
  la falla y el link *Page at failure* con la URL donde estaba el navegador.

**3. Qué significa el mensaje de falla.**

| El mensaje dice | Significa | Qué hacer |
|---|---|---|
| `SauceDemo unavailable ...` o `External API unavailable ...` | El servicio externo no respondió (sin conexión, timeout o HTTP 5xx) | Revisar la conexión o reintentar más tarde; no es un defecto del sitio ni de los tests |
| `Unexpected HTTP status for GET <URL>: expected 200, got 404` | La API respondió, pero con otro status que el del contrato | Revisar si cambió el contrato de la API |
| `Expected ..., found ...` / `Element (...) not visible after 10s` | La aplicación respondió, pero distinto de lo esperado | Mirar la captura y el detalle: es un posible defecto o un cambio en la página |

**4. Log de ejecución.** `reports/logs/test_execution.log` cuenta la
corrida paso a paso, en orden. Cada test empieza con `START` y termina con
una única línea `RESULT`, escrita después del cierre del test, con el
resultado final: `PASSED`, `FAILED` o `ERROR` (falla en la preparación o en
el cierre, por ejemplo al cerrar el navegador). En el medio están sus
acciones:

```text
2026-11-15 13:29:17,560 INFO START tests/api/test_posts.py::test_get_post_by_id
2026-11-15 13:29:18,111 INFO API GET https://jsonplaceholder.typicode.com/posts/1 -> 200
2026-11-15 13:29:18,112 INFO RESULT tests/api/test_posts.py::test_get_post_by_id: PASSED
...
2026-11-15 13:29:20,639 INFO Opening login page: https://www.saucedemo.com/
2026-11-15 13:29:22,286 INFO Login succeeded for user 'standard_user' (password not logged)
2026-11-15 13:29:22,354 INFO Added first product to cart: Sauce Labs Backpack
```

Ante un fallo, el log agrega una línea `ERROR FAILURE DETAILS` con la fase
(`setup`, `call` o `teardown`) y el error completo y `Screenshot saved: <ruta> (page: <URL>)` con la ubicación de la
captura.

## Flujo de trabajo Git

- `main` contiene solo trabajo integrado. Cada fase se desarrolló en su rama
  (`feature/project-structure`, `feature/page-object-model`,
  `feature/external-test-data`, `feature/api-testing`, `feature/reporting`,
  `docs/final-delivery`) y entró por Pull Request con **merge commit**
  (sin squash ni rebase), así el historial conserva cada commit y cada merge.
- Commits en inglés con **Conventional Commits** (`feat`, `fix`, `test`,
  `docs`, `refactor`, `build`, `chore`), título y cuerpo con viñetas.

## Disponibilidad de servicios externos

SauceDemo y JSONPlaceholder son servicios públicos de demostración que este
proyecto no controla. Se asume que están en línea y que JSONPlaceholder
mantiene sus datos de ejemplo (por ejemplo, 10 posts del usuario 1).

Si alguno no responde, los tests **fallan** (nunca se omiten ni pasan) con un
mensaje que nombra el servicio: `SauceDemo unavailable at ...` o
`External API unavailable: <método> <URL> ...`. Así una caída externa se
distingue de un defecto real (ver *Clasificación de fallas* arriba).

## Credenciales

`standard_user` / `secret_sauce` — provistas públicamente por el entorno de
demostración de SauceDemo.
