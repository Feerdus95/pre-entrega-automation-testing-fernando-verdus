# Pre-entrega Automation Testing — SauceDemo (Fernando Verdus)

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
│   └── helpers.py             # Login, waits explícitos, interacciones de catálogo y carrito
├── reports/
│   ├── reporte.html           # Reporte HTML (generado)
│   ├── screenshots/           # Capturas automáticas de fallos (generado)
│   └── logs/                  # test_execution.log (generado)
├── conftest.py                # Fixtures (ciclo de vida del navegador) y hooks de evidencia
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

La sincronización usa esperas explícitas (`WebDriverWait` +
`expected_conditions`), nunca `time.sleep()`. Las credenciales (`standard_user` /
`secret_sauce`) son públicas del entorno demo de SauceDemo.

## Reportes y evidencia

- **Reporte HTML:** `reports/reporte.html` (estados por test, tiempos, detalles de fallo).
- **Capturas de fallo:** `reports/screenshots/test_<nombre>.png` — se generan
  automáticamente solo cuando un test falla.
- **Logs de ejecución:** `reports/logs/test_execution.log` — inicio de cada
  test, acciones principales y resultado. Las contraseñas nunca se escriben
  en el log.
