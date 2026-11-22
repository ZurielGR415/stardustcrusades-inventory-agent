# Documentación Integral del Proyecto: Stardust Inventory Agent

**Programa:** IBM Experiential Learning Lab (IBM SkillsBuild & SkillUp Online)  
**Equipo:** Stardust Crusaders  
**Integrantes:**
* Gómez Rubio Zuriel
* Hernández Hidalgo Héctor
* Solís Hernández Juan Abraham  

**Repositorio del Proyecto:** [https://github.com/ZurielGR415/stardustcrusades-inventory-agent](https://github.com/ZurielGR415/stardustcrusades-inventory-agent)  
**Fecha de Entrega:** Noviembre 2026  

---

## 1. Introducción

En el panorama socioeconómico de América Latina, las Micro, Pequeñas y Medianas Empresas (MiPyMEs) representan más del 99% del tejido empresarial y generan aproximadamente el 60% del empleo formal e informal. Dentro de este sector, las tiendas de abarrotes, minisúpers y comercializadoras locales desempeñan un rol estratégico en la cadena de distribución minorista de productos de consumo básico y de alta rotación.

No obstante su relevancia económica, la inmensa mayoría de estos comercios opera bajo procesos manuales, reactivos y fragmentados. La ausencia de presupuestos para adquirir sistemas ERP (Enterprise Resource Planning) complejos, sumada a la falta de personal especializado en logística, ocasiona que el control de existencias dependa casi exclusivamente de la memoria y anotaciones en papel o cuadernos informales.

Esta vulnerabilidad operativa detona dos problemáticas financieras críticas:
1. **Mermas por caducidad inadvertida:** Productos perecederos (lácteos, embutidos, jugos) que vencen en el anaquel por falta de rotación oportuna, traduciéndose en pérdidas económicas directas que absorbe el comerciante.
2. **Quiebres de inventario (desabastos):** Incapacidad para anticipar el momento de reorden antes de que las existencias caigan a cero, provocando la pérdida inmediata de ventas y el deterioro de la lealtad de la clientela.

Ante este desafío, surge **Stardust Inventory Agent**, una solución de Inteligencia Artificial Agéntica concebida bajo el modelo **SaaS B2B (Software as a Service Business-to-Business)**. El proyecto transforma la gestión del almacén mediante un empleado digital autónomo capaz de comunicarse en lenguaje natural con el personal operativo (bodegueros) y gerencial (dueños de tienda), garantizando diagnósticos visuales normativos, auditorías continuas y ejecución de acciones transaccionales en tiempo real sin requerir capacitación técnica especializada.

---

## 2. Objetivo del Problema

### 2.1. Definición del Problema Central
El personal de bodega y los administradores de pequeñas empresas comerciales carecen de un mecanismo ágil, certero y automatizado para auditar en tiempo real la vida útil de sus existencias y calcular el punto óptimo de reorden a proveedores. La dependencia de revisiones físicas esporádicas y hojas de cálculo desactualizadas genera:
* Pérdidas de capital por mercancía vencida que no fue rematada con anticipación.
* Pérdida de ventas por agotamiento súbito de productos de alta demanda.
* Asignación ineficiente de horas-hombre en tareas mecánicas de conteo manual.
* Falta de gobernanza en los pedidos a distribuidores, propiciando sobrecostos o compras sin control financiero.

### 2.2. Objetivo General
Diseñar, implementar y validar un **Agente de Inteligencia Artificial Agéntica autónomo (Stardust Inventory Agent)** que, fundamentado en una política normativa rigurosa (`POL-INV-2026-v1`) y soportado por la tecnología de **IBM watsonx.ai** e **IBM Bob**, permita a las MiPyMEs comerciales prevenir mermas por caducidad, evitar desabastos y automatizar órdenes de compra mediante interacción en lenguaje natural.

### 2.3. Objetivos Específicos
1. **Percepción e Interacción en Lenguaje Natural:** Proveer una interfaz conversacional tolerante a modismos, términos coloquiales y plurales, accesible tanto para el bodeguero en piso como para el gerente.
2. **Motor Determinista de Reglas de Negocio:** Desarrollar en Python un núcleo de cálculo exacto que evalúe días de cobertura de venta y días restantes de vida útil, eliminando riesgos de alucinación numérica en modelos fundacionales de lenguaje.
3. **Semáforo Normativo y Métrica Financiera:** Asignar códigos de estado estandarizados (🟢 `STOCK_OK`, 🟡 `MERMA_RIESGO`, 🟡 `REORDEN_URGENTE`, 🔴 `DESABASTO_TOTAL`, 🔴 `CADUCADO`) con indicación inmediata del dinero en riesgo y potencial de recuperación.
4. **Mutación Transaccional en Tiempo Real:** Permitir que el agente ejecute acciones operativas directas (entradas de mercancía con fechas de caducidad flexibles y salidas/mermas) actualizando la base de datos persistente.
5. **Gobernanza Human-in-the-Loop:** Automatizar la generación de borradores de Órdenes de Compra (PO) con folios únicos y aplicar un filtro de autorización cuando el importe estimado supere el umbral configurado ($3,000 MXN).
6. **Onboarding Asistido:** Incorporar una entrevista inicial interactiva que parametrice las reglas de negocio de cualquier comercio (días de surtido, límites de compra, perecederos) sin tocar una sola línea de código fuente.

---

## 3. Cursos Vistos (Capacitación en IBM SkillsBuild & Experiential Lab)

El desarrollo del proyecto se consolidó gracias a la integración transversal de los módulos teóricos y prácticos impartidos a lo largo de la trayectoria del **IBM Experiential Learning Lab**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│            TRAYECTORIA FORMATIVA - IBM EXPERIENTIAL LAB                │
├────────────────────────────────┬───────────────────────────────────────┤
│ Módulo / Curso                 │ Competencias Clave Desarrolladas      │
├────────────────────────────────┼───────────────────────────────────────┤
│ Enterprise Design Thinking     │ • The Loop: Observar, Reflexionar,    │
│ (EDT) de IBM                   │   Hacer (Continuous Iteration).       │
│                                │ • The Keys: Hills, Sponsor Users,     │
│                                │   Playbacks.                          │
│                                │ • Mapas de Empatía y Escenarios       │
│                                │   As-Is / To-Be.                      │
├────────────────────────────────┼───────────────────────────────────────┤
│ Fundamentos de Inteligencia    │ • Arquitectura de Transformers y LLMs.│
│ Artificial & GenAI             │ • Tokenización, Decoding y Parámetros │
│                                │   (Greedy, Temperature, Penalties).   │
│                                │ • Ingeniería de Prompts (Zero/Few-Shot│
│                                │   y Chain of Thought).                │
├────────────────────────────────┼───────────────────────────────────────┤
│ Arquitectura de IA Agéntica    │ • Diferenciación entre LLM reactivo   │
│ (Agentic AI)                   │   y Agente Autónomo con toma de       │
│                                │   decisiones y ejecución de acciones. │
│                                │ • Principios de Gobernanza y límites: │
│                                │   Human-in-the-Loop.                  │
├────────────────────────────────┼───────────────────────────────────────┤
│ Plataforma IBM watsonx.ai      │ • Experimentación en Prompt Lab.      │
│ & watsonx Orchestrate          │ • Inferencia con modelos IBM Granite  │
│                                │   (ibm/granite-13b-chat-v2).          │
│                                │ • Gestión de Data Assets para         │
│                                │   Grounding Normativo (RAG).          │
├────────────────────────────────┼───────────────────────────────────────┤
│ Desarrollo Asistido por IA con │ • Flujo de desarrollo en entorno IDE. │
│ IBM Bob                        │ • Desglose y planeación de código.    │
│                                │ • Pruebas automatizadas y depuración. │
├────────────────────────────────┼───────────────────────────────────────┤
│ Modelo de Negocios B2B SaaS    │ • Diferenciación crítica: Comprador   │
│ & Propuesta de Valor           │   (Buyer/Dueño) vs Usuario Operativo  │
│                                │   (User/Bodeguero).                   │
│                                │ • Métricas de Retorno de Inversión.   │
└────────────────────────────────┴───────────────────────────────────────┘
```

---

## 4. Herramientas Usadas

Para materializar la solución se integró un ecosistema tecnológico coordinado, equilibrando servicios en la nube de IBM, herramientas de desarrollo asistido y bibliotecas de código estándar:

### 4.1. IBM watsonx.ai (Cloud Platform - Región Dallas `us-south`)
* **Propósito:** Núcleo de inferencia, comprensión de lenguaje natural y formulación de respuestas empáticas.
* **Componentes utilizados:**
  * **Prompt Lab:** Entorno para la calibración del System Prompt, contextualización dinámica y definición de hiperparámetros de inferencia (`decoding_method: greedy`, `max_new_tokens: 350`, `repetition_penalty: 1.1`).
  * **Modelo Fundacional:** `ibm/granite-13b-chat-v2`, seleccionado por su alto desempeño en tareas empresariales, consistencia sintáctica en español y cumplimiento de lineamientos de seguridad ética de IBM.
  * **Data Assets:** Almacenamiento en nube de la base de conocimiento (`politicas_inventario.pdf`) y del catálogo inicial (`inventario_pyme.json`).

### 4.2. IBM Bob
* **Propósito:** Entorno interactivo de desarrollo asistido por Inteligencia Artificial.
* **Uso:** Estructuración de la arquitectura de scripts, planeación colaborativa de funciones modulares, depuración guiada de excepciones sintácticas y ejecución de pruebas en consola local.

### 4.3. Python 3.10+
* **Propósito:** Lenguaje principal de backend que implementa la lógica determinista, cálculo matemático, normalización lingüística y mutaciones de datos.
* **Módulos estándar aprovechados (sin dependencias pesadas de terceros):**
  * `datetime` y `date`: Aritmética de fechas, cálculo de vida útil remanente y días de entrega.
  * `re`: Expresiones regulares para extracción de cantidades y fechas multiformato (`YYYY-MM-DD`, `DD/MM/YYYY`, meses en texto).
  * `unicodedata`: Normalización NFKD para tolerancia a acentos, mayúsculas y diacríticos.
  * `json`: Persistencia y lectura de bases de datos locales transaccionales.
  * `urllib.request` y `urllib.parse`: Cliente HTTP nativo para autenticación IAM y consumo de la API REST de watsonx.ai.

### 4.4. Git & GitHub
* **Propósito:** Control de versiones distribuido y colaboración del equipo Stardust Crusaders.
* **Repositorio:** [stardustcrusades-inventory-agent](https://github.com/ZurielGR415/stardustcrusades-inventory-agent), implementando un flujo estricto de commits semánticos y sincronización de código limpio.

### 4.5. Headless Chromium / Edge Engine
* **Propósito:** Generación del artefacto normativo formal (`politicas_inventario.pdf`) en maquetación editorial limpia, desprovisto de encabezados y pies de página no deseados mediante flags de compilación `--no-pdf-header-footer`.

---

## 5. Cómo lo Estamos Llevando a Cabo con Esas Herramientas

### 5.1. Arquitectura de Tres Capas (Three-Layer Architecture)
Para evitar los errores comunes de los sistemas basados puramente en LLMs (alucinación de cálculos matemáticos, falta de memoria transaccional y respuestas ambiguas), el sistema se diseñó bajo una arquitectura desacoplada de 3 capas:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      1. CAPA DE ENTRADA (PERCEPCIÓN)                   │
│  El bodeguero o gerente escribe en lenguaje natural mediante consola   │
│  (ej. "¿Cómo andamos de yogur?", "Llegaron 15 leches caducidad 25/12") │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             2. CAPA DE FLUJO Y LÓGICA DE NEGOCIO (PYTHON / BOB)         │
│  • Normalización lingüística (NFKD) y reducción de plurales.          │
│  • Enrutador de intenciones:                                           │
│    a) Onboarding / Calibración (config_pyme.json).                     │
│    b) Movimiento transaccional de entrada/salida (inventario_pyme.json)│
│    c) Generador de Órdenes de Compra (PO) con Gobernanza.              │
│    d) Consulta de stock o Reporte proactivo general.                   │
│  • Motor de Auditoría Normativa POL-INV-2026-v1:                       │
│    - Días Cobertura = Stock Actual / Ventas Diarias Promedio           │
│    - Días Caducidad = Fecha Caducidad - Fecha Hoy                      │
│    - Asignación de Semáforos (🟢, 🟡, 🔴) y Cálculo Financiero Exacto  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│            3. CAPA DE SALIDA (INFERENCIA & RAZONAMIENTO - WATSONX)     │
│  • En modo conectado: watsonx.ai (IBM Granite) recibe el contexto      │
│    estructurado y redacta una respuesta concisa y profesional.         │
│  • En modo local/demostración: El motor genera tarjetas visuales       │
│    inmediatas con métricas financieras y pasos a seguir.               │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 5.2. Componentes y Flujos de Ejecución

#### A) Base de Conocimiento Normativo (`politicas_inventario.pdf`)
El agente no opera sobre opiniones arbitrarias, sino sobre la política oficial **`POL-INV-2026-v1`**, que establece cinco cuadrantes de decisión inmutables:

| Semáforo | Código | Condición Matemática | Acción Operativa Obligatoria |
| :---: | :--- | :--- | :--- |
| 🟢 | **STOCK_OK** | Días Cobertura > Tiempo Entrega $\land$ Días Caducidad > 3 | Niveles saludables. Monitoreo pasivo continuo. |
| 🟡 | **MERMA_RIESGO** | $1 \le \text{Días Caducidad} \le 3$ días | Colocar **Etiqueta Amarilla (-25% descuento)** y desplazar producto al frente del anaquel (regla PEPS). |
| 🟡 | **REORDEN_URGENTE** | Días Cobertura $\le$ Tiempo Entrega Proveedor | Elaborar borrador preventivo de orden de compra para evitar quiebre de stock. |
| 🔴 | **DESABASTO_TOTAL** | $\text{Stock Actual} = 0$ unidades | Alerta máxima y emisión de orden de compra express prioritaria. |
| 🔴 | **CADUCADO** | $\text{Días Caducidad} \le 0$ días | **Retiro inmediato del anaquel**, prohibición absoluta de venta y registro contable de merma definitiva. |

#### B) Onboarding Asistido (`config_pyme.json`)
Al arrancar por primera vez o al invocar el comando `"calibrar negocio"`, la función `ejecutar_cuestionario_onboarding()` guía al usuario en 4 preguntas:
1. Nombre comercial de la empresa.
2. Manejo de perecederos con caducidad (activa o desactiva las auditorías de fechas).
3. Plazo promedio de entrega de distribuidores (días).
4. Monto máximo de compra sin requerir autorización ($ MXN).

Los parámetros se almacenan en `config_pyme.json`, permitiendo que el mismo código sirva para una tienda de abarrotes, una ferretería o una farmacia.

#### C) Acciones Transaccionales por Chat (Punto 2)
El analizador sintáctico en `procesar_accion_movimiento()` interpreta órdenes directas:
* **Entradas:** `"Llegaron 15 leches con caducidad 2026-12-25"`. El agente extrae la cantidad (`+15`), busca el producto por raíz singular (`leche`), actualiza la fecha en la base de datos y confirma el incremento:
  ```text
  🟢 ENTRADA REGISTRADA EN TIEMPO REAL
  • Producto: Leche Entera 1L (LAC-001)
  • Cantidad ingresada: +15 piezas
  • Stock: 8 ➔ 23 piezas disponibles
  • Caducidad en sistema: 2026-12-25
  • Estado del producto: 🟢 ÓPTIMO
  ```
* **Salidas y Mermas:** `"Se vendieron 5 leches"` o `"Se mermaron 2 yogures"`. Descuenta unidades, valida que el almacén no quede con saldo negativo ficticio y recalcula el estado normativo al instante.

#### D) Generación de Órdenes de Compra con Gobernanza (Punto 3)
La función `generar_orden_compra()` calcula el volumen óptimo:
$$\text{Unidades Reorden} = \max((\text{Stock Mínimo} \times 2) - \text{Stock Actual},\; 10)$$

* Si el costo total es $\le \$3,000\text{ MXN}$: Asigna `ESTADO DE GOBERNANZA: ✅ APROBADO AUTOMÁTICAMENTE`.
* Si el costo total excede el límite (ej. pedido de 120 aceites por $\$4,200\text{ MXN}$): Aplica el principio de *Human-in-the-Loop* y estampa: `ESTADO DE GOBERNANZA: ⚠️ REQUIERE VOBO DE GERENCIA`.
* Genera simultáneamente un archivo físico de despacho (`orden_compra_<SKU>.txt`) listo para su envío por canales digitales.

---

## 6. Conclusiones

1. **Democratización Tecnológica para MiPyMEs:** Se demostró la viabilidad de implementar un agente de Inteligencia Artificial Agéntica de grado empresarial en entornos de bajos recursos computacionales, eliminando la barrera de entrada que representan los ERPs tradicionales costosos.
2. **Efectividad de la Arquitectura Desacoplada (Hybrid Deterministic-LLM):** La combinación de un motor lógico determinista en Python con el razonamiento contextual de IBM Granite en watsonx.ai garantiza una fiabilidad del 100% en cálculos financieros y transaccionales, erradicando alucinaciones numéricas mientras se preserva una interacción conversacional empática y fluida.
3. **Validación del Enfoque Enterprise Design Thinking:** El diseño no comenzó en el código, sino en la comprensión profunda de los dolores de los actores clave. La distinción entre el **Comprador (Dueño/Gerente)** y el **Usuario (Bodeguero)** permitió construir herramientas específicas para cada uno: semáforos rápidos para el piso de venta y gobernanza presupuestal para la administración.
4. **Trascendencia de la IA Agéntica:** El proyecto cumple con la premisa medular transmitida por los mentores de IBM: *"Un modelo generativo solo redacta respuestas; un agente de IA evalúa reglas, ejecuta mutaciones transaccionales y respeta límites de gobernanza humana"*.
5. **Líneas de Trabajo Futuro:** Se proyecta la integración de lectores ópticos de código de barras (Barcode/QR) mediante cámara web, la conexión a mensajería instantánea (API de WhatsApp Business) y la migración de la base de datos a un clúster relacional en IBM Cloud PostgreSQL.

---

## 7. Referencias Bibliográficas

1. **IBM SkillsBuild & IBM Training.** (2025). *Enterprise Design Thinking Practitioner & Co-Creator Courseware*. IBM Corporation.
2. **IBM Corporation.** (2024). *IBM watsonx.ai: Enterprise studio for AI builders*. IBM Cloud Documentation. Recuperado de: [https://cloud.ibm.com/docs/watsonx-ai](https://cloud.ibm.com/docs/watsonx-ai)
3. **IBM Research.** (2024). *Granite Models: Technical Overview and Enterprise Capabilities*. IBM AI Foundations.
4. **Silver, E. A., Pyke, D. F., & Thomas, D. J.** (2016). *Inventory and Production Management in Supply Chains* (4th ed.). CRC Press.
5. **Ballou, R. H.** (2004). *Logística: Administración de la cadena de suministro* (5.ª ed.). Pearson Educación.
6. **Van Rossum, G., & Drake, F. L.** (2024). *Python 3 Language Reference Manual*. Python Software Foundation.
7. **Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO).** (2021). *Prevención y reducción de pérdidas y desperdicios de alimentos en el comercio minorista*. Colección Manuales Prácticos de Gestión Alimentaria.
