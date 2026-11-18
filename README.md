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

## Capacidades Operativas del Agente

### 1. Onboarding Asistido (Configuración Dinámica)
Al ejecutarse por primera vez (o con el comando `"calibrar negocio"`), el agente realiza un breve cuestionario interactivo para adaptar sus reglas operativas a cualquier comercio sin modificar código:
* Nombre comercial de la empresa.
* Manejo de productos perecederos (activa o desactiva reglas de caducidad).
* Días promedio de entrega de proveedores.
* Límite de compra para compras automáticas antes de requerir aprobación del gerente ($3,000 MXN por defecto).
* Persistencia automática en `config_pyme.json`.

### 2. Acciones en Tiempo Real por Lenguaje Natural (Entradas, Salidas y Mermas)
El agente no se limita a responder preguntas: ejecuta mutaciones transaccionales en la base de datos local (`inventario_pyme.json`) en tiempo real:
* **Entradas de mercancía:** Interpreta cantidades y actualiza la fecha de vencimiento con soporte multiformato (`YYYY-MM-DD`, `DD/MM/YYYY`, o texto coloquial como `"30 de diciembre"`).
* **Salidas por venta y bajas por merma:** Descuenta inventario, valida que haya existencias suficientes y reporta el nuevo semáforo del producto al instante.

### 3. Generador Formal de Órdenes de Compra con Gobernanza (PO)
Al detectar desabasto o por petición directa, el agente genera un documento formal de compra listo para enviar a proveedores:
* Asignación de folio oficial (ej. `OC-20261118-ABR-003`).
* Cálculo exacto de inversión requerida según costo unitario del proveedor.
* **Gobernanza Human-in-the-Loop:** Evalúa el total contra el límite configurado ($3,000 MXN). Si lo excede, clasifica la orden como `⚠️ REQUIERE VOBO DE GERENCIA`; si está dentro del umbral, la cataloga como `✅ APROBADO AUTOMÁTICAMENTE`.
* Generación física del archivo de texto `orden_compra_{sku}.txt` en el directorio de trabajo para su despacho por WhatsApp o correo electrónico.

---

## Arquitectura de la Solución (3 Capas)

```text
[ENTRADA (Percepción)]
Consultas, entradas, salidas y pedidos del bodeguero/gerente en lenguaje natural
             │
             ▼
[FLUJO (Lógica y Reglas de Negocio en Python - IBM Bob)]
1. Normalización de lenguaje, extracción de fechas y tolerancia a plurales.
2. Consulta y mutación transaccional de base de datos (inventario_pyme.json).
3. Gobernanza y límites de autorización según config_pyme.json.
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
├── inventario_pyme.json       # Base de datos local transaccional (JSON) con productos del catálogo.
├── config_pyme.json           # Configuración personalizada de la PYME (límites, perecederos, plazos).
├── inventario_logic.py        # Motor de lógica, transacciones, reglas de negocio y cálculo financiero.
├── agent_stardust.py          # Agente orquestador con soporte para watsonx.ai (IBM Granite) y modo local.
├── politicas_inventario.pdf   # Manual normativo oficial del almacén (Knowledge Base sin encabezados).
├── politicas_inventario.txt   # Versión de texto plano de las políticas oficiales.
└── README.md                  # Documentación integral del proyecto.
```

---

## Instrucciones de Ejecución Local

### Prerrequisitos
* Python 3.10 o superior instalado.
* Conexión a Internet (opcional para el modo en vivo con watsonx.ai).

### Pasos para ejecutar
1. Clona este repositorio o descarga los archivos en tu equipo.
2. Abre una terminal dentro de la carpeta del proyecto.
3. Ejecuta el agente interactivo:
   ```bash
   python agent_stardust.py
   ```
4. El sistema solicitará tu `IBM_CLOUD_API_KEY` para interactuar con **IBM Granite** en vivo en la nube de Dallas, o puedes presionar **Enter** para utilizar el modo demostración local.

### Comandos de ejemplo para probar:
* **Consultas de stock:**
  * *"¿Cómo andamos de yogur?"* $\rightarrow$ Diagnostica estado normativo y pérdida potencial.
  * *"Revisa el frijol negro"* $\rightarrow$ Detecta desabasto y sugiere reorden inmediato.
* **Entradas de mercancía (Punto 2):**
  * *"Llegaron 15 leches con caducidad 2026-12-25"* $\rightarrow$ Suma existencias y actualiza la fecha en tiempo real.
  * *"Entrada de 10 yogures con caducidad 30 de diciembre"* $\rightarrow$ Acepta lenguaje natural y calcula año automáticamente.
* **Salidas y Mermas (Punto 2):**
  * *"Se vendieron 5 leches"* $\rightarrow$ Descuenta del almacén y recalcula semáforo.
  * *"Se mermaron 2 yogures"* $\rightarrow$ Registra la baja y advierte el stock remanente.
* **Órdenes de Compra y Gobernanza (Punto 3):**
  * *"Generar orden de compra frijol"* $\rightarrow$ Emite borrador oficial aprobado automáticamente (dentro del límite de $3,000 MXN).
  * *"Generar orden de compra de 120 aceites"* $\rightarrow$ Emite orden y marca `⚠️ REQUIERE VOBO DE GERENCIA` por superar el presupuesto.
* **Alertas y Calibración:**
  * *"Dame el reporte de alertas de hoy"* $\rightarrow$ Resumen proactivo de todos los productos en riesgo.
  * *"calibrar negocio"* $\rightarrow$ Relanza el asistente de Onboarding para ajustar datos y umbrales.

---

## Licencia y Reconocimientos
Desarrollado para el **IBM Experiential Learning Lab** por el equipo **Stardust Crusaders**. Tecnologías impulsadas por **IBM Bob** y **IBM watsonx.ai**.
