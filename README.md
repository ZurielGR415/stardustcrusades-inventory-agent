# Stardust Inventory Agent

> **Agente de Inteligencia Artificial para la Gestión de Inventarios y Prevención de Mermas en PYMEs**  
> Proyecto desarrollado en el marco del **IBM Experiential Learning Lab** (IBM SkillsBuild & SkillUp Online).

---

## Equipo: Stardust Crusaders
* **Hernández Hidalgo Héctor**
* **Solís Hernández Juan Abraham**
* **Gómez Rubio Zuriel**

---

## Descripción del Proyecto
**Stardust Inventory Agent** es un empleado digital concebido bajo un modelo **SaaS B2B**, diseñado específicamente para pequeñas y medianas empresas comerciales (tiendas de abarrotes, minisúpers y comercios locales). 

Su propósito central es reducir pérdidas económicas causadas por:
1. **Mermas por caducidad no detectadas a tiempo** en productos perecederos.
2. **Desabastos imprevistos (quiebres de stock)** que detienen las ventas.
3. **Auditorías manuales lentas y propensas a errores** por parte del personal de almacén.

El agente interactúa mediante lenguaje natural con el **personal de almacén (bodegueros)** para registrar movimientos y consultar stock en segundos, y con el **dueño o gerente** para emitir reportes proactivos de alertas y sugerencias de compra fundamentadas.

---

## Arquitectura de la Solución (3 Capas)

```text
[ENTRADA (Percepción)]
Consultas y registros del bodeguero/gerente en lenguaje natural
             │
             ▼
[FLUJO (Lógica y Reglas de Negocio en Python - IBM Bob)]
1. Normalización de lenguaje y tolerancia a plurales.
2. Consulta / actualización de base de datos (inventario_pyme.json).
3. Cálculo de días de cobertura y días restantes de vida útil.
4. Diagnóstico de estado según la política oficial POL-INV-2026-v1.
             │
             ▼
[SALIDA (Inferencia y Razonamiento - watsonx.ai)]
Modelo fundacional (IBM Granite) formula la respuesta en lenguaje natural,
estructurada con semáforos visuales (🟢, 🟡, 🔴) e impacto financiero.
```

---

## Códigos de Estado y Semáforo Normativo (`POL-INV-2026-v1`)

| Semáforo | Código | Condición | Acción Requerida |
| :---: | :--- | :--- | :--- |
| 🟢 | **STOCK_OK** | Cobertura suficiente y sin riesgo de vencimiento. | Niveles saludables. Monitoreo pasivo. |
| 🟡 | **MERMA_RIESGO** | Caducidad entre 1 y 3 días restantes. | Aplicar etiqueta amarilla (-25% descuento) y mover al frente (PEPS). |
| 🟡 | **REORDEN_URGENTE** | Días de cobertura $\le$ tiempo de entrega del proveedor. | Preparar borrador de orden de compra preventiva. |
| 🔴 | **DESABASTO_TOTAL** | Existencias en 0 unidades. | Alerta prioritaria y solicitud de pedido express. |
| 🔴 | **CADUCADO** | Fecha de caducidad vencida ($\le 0$ días). | Retiro inmediato del anaquel, venta prohibida y registro contable de merma. |

---

## Estructura del Repositorio

```text
├── inventario_pyme.json       # Base de datos local simulada con productos perecederos y no perecederos.
├── inventario_logic.py        # Motor de lógica, reglas de negocio y cálculo financiero.
├── agent_stardust.py          # Script integrador que conecta la lógica con la API de watsonx.ai (IBM Granite).
├── politicas_inventario.pdf   # Manual normativo oficial del almacén (Knowledge Base).
├── politicas_inventario.txt   # Versión de texto plano de las políticas oficiales.
└── README.md                  # Documentación general del proyecto.
```

---

## Instrucciones de Ejecución Local

### Prerrequisitos
* Python 3.10 o superior instalado.
* Conexión a Internet (opcional para el modo en vivo con watsonx).

### Pasos para ejecutar
1. Clona este repositorio o descarga los archivos en tu equipo.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Ejecuta el agente interactivo:
   ```bash
   python agent_stardust.py
   ```
4. El sistema solicitará tu `IBM_CLOUD_API_KEY` para interactuar con **IBM Granite** en vivo en la nube de Dallas, o puedes presionar **Enter** para utilizar el modo demostración local.

### Consultas de ejemplo para probar:
* *"¿Cómo andamos de yogur de fresa?"* $\rightarrow$ Diagnostica `MERMA_RIESGO` y calcula el dinero en riesgo.
* *"Revisa el frijol negro"* $\rightarrow$ Diagnostica `DESABASTO_TOTAL` y genera sugerencia de compra.
* *"Dame el reporte de alertas de hoy"* $\rightarrow$ Escanea el almacén completo y lista productos que requieren atención inmediata.

---

## Licencia y Reconocimientos
Desarrollado para el **IBM Experiential Learning Lab** por el equipo **Stardust Crusaders**. Tecnologías impulsadas por **IBM Bob** y **IBM watsonx.ai**.
