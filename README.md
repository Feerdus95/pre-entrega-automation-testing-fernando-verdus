# Pre-entrega Automation Testing — SauceDemo

Proyecto de automatización de pruebas web para la aplicación de demostración
[SauceDemo](https://www.saucedemo.com/) usando **Python + Pytest + Selenium
WebDriver**. Cubre tres flujos: login exitoso, validación del catálogo de
productos y agregado de un producto al carrito.

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python | Lenguaje del proyecto |
| Pytest | Framework de tests y fixtures |
| Selenium WebDriver | Automatización del navegador (Chrome) |
| pytest-html | Reporte HTML de ejecución |
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
pytest -v
```

Con reporte HTML:

```bash
pytest -v --html=reports/reporte.html
```

Selenium Manager (incluido en Selenium) descarga automáticamente el driver de
Chrome adecuado; no hace falta instalarlo a mano.

## Estructura del proyecto

```text
├── tests/
│   └── test_saucedemo.py      # Casos de prueba y aserciones
├── utils/
│   ├── driver.py              # Creación/configuración del WebDriver
│   └── helpers.py             # Login, esperas, catálogo y carrito
├── reports/
│   ├── reporte.html           # Reporte HTML (generado al ejecutar)
│   ├── screenshots/           # Capturas automáticas de fallos (generado)
│   └── logs/                  # test_execution.log (generado)
├── conftest.py                # Fixtures del navegador, logging y captura de fallos
├── requirements.txt           # Dependencias
└── README.md
```

## Cobertura de pruebas

| Test | Qué valida |
|---|---|
| `test_successful_login` | El usuario `standard_user` inicia sesión y llega a `/inventory.html`, con encabezado `Products` y título `Swag Labs` |
| `test_inventory_catalog` | El catálogo carga con al menos un producto, navegación/carrito/orden visibles, y extrae nombre y precio del primer producto |
| `test_add_first_product_to_cart` | El primer producto se agrega al carrito, el contador muestra `1` y el producto aparece en `/cart.html` |

Cada test es independiente: abre su propio navegador, inicia sesión por su
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

- **Reporte HTML:** `reports/reporte.html` (estados por test, tiempos, detalles
  de fallo). Se incluye en el repositorio la última ejecución como evidencia;
  cada corrida lo regenera.
- **Capturas de fallo:** `reports/screenshots/test_<nombre>.png` — se generan
  automáticamente solo cuando un test falla (no hay capturas en la última
  ejecución porque los tres tests pasaron).
- **Logs de ejecución:** `reports/logs/test_execution.log` — inicio de cada
  test, acciones principales y resultado. Se incluye la última corrida como
  evidencia. Las contraseñas nunca se escriben en el log.

## Credenciales

`standard_user` / `secret_sauce` — provistas públicamente por el entorno de
demostración de SauceDemo.
