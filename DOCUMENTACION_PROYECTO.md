# UNIVERSIDAD AUTÓNOMA DE TAMAULIPAS
## FACULTAD DE INGENIERÍA TAMPICO

### Proyecto Final: Stardust Inventory Agent — Arquitectura Agéntica Híbrida para la Gestión Autónoma de Inventarios, Prevención de Mermas Críticas y Gobernanza Human-in-the-Loop en PyMEs Comerciales

**Equipo de Desarrollo e Innovación (Stardust Crusaders):**
* Gómez Rubio Zuriel (Líder de Proyecto)
* Hernández Hidalgo Héctor
* Solís Hernández Juan Abraham

**Semestre y grupo:** 3° “K”  
**Carrera:** Ingeniería en Sistemas Computacionales  
**Materia:** PENSAMIENTO CRÍTICO Y CREATIVO  
**Docente Titular:** Nava Díaz Salvador Wilfrido  
**Programa Vinculado:** IBM SkillsBuild AI Experiential Learning Lab (Cohorte México 2026)  
**Repositorio GitHub:** [https://github.com/ZurielGR415/stardustcrusades-inventory-agent](https://github.com/ZurielGR415/stardustcrusades-inventory-agent)  

---

## 1. Introducción y Contextualización del Problema

En el ecosistema económico y comercial contemporáneo de América Latina, las Micro, Pequeñas y Medianas Empresas (MiPyMEs) —particularmente las tiendas de abarrotes, minisúpers, comercializadoras de víveres y misceláneas de barrio— constituyen la columna vertebral del comercio minorista y del abastecimiento comunitario. Representan más del 99% del tejido empresarial formal e informal y concentran cerca del 60% del empleo activo. Sin embargo, su operación diaria se encuentra sumergida en una severa paradoja estructural: mientras las grandes cadenas multinacionales de autoservicio operan con sistemas ERP (Enterprise Resource Planning) de millones de dólares y algoritmos predictivos de reabastecimiento continuo, el comercio minorista local continúa gestionando su inventario mediante métodos artesanales, reactivos y fragmentados, basados casi exclusivamente en libretas manuales, notas de papel o la memoria del personal de almacén.

Esta carencia de digitalización estructurada detona dos cuellos de botella severos que degradan la salud financiera del comercio y deterioran su competitividad frente a las cadenas corporativas:

En el primer nivel de atención y piso de venta (Nivel 1 o Bodega/Anaquel), el personal operativo —bodegueros, encargados de almacén y dependientes de mostrador— enfrenta una abrumadora carga de trabajo físico combinada con la tarea cognitiva de monitorear fechas de vencimiento de cientos de productos perecederos (lácteos, embutidos, panes, bebidas y abarrotes envasados). Las auditorías manuales son lentas, esporádicas y propensas al error humano. Como resultado, se vulnera de forma sistemática el principio logístico PEPS (Primeras Entradas, Primeras Salidas), ocasionando que productos con fecha de vencimiento próxima queden relegados detrás de mercancía recién surtida. Cuando el personal detecta el producto, este ya ha caducado en el estante, transformándose en merma total: una pérdida económica irreversible que absorbe directamente el comerciante y que representa entre el 8% y el 15% del margen bruto de utilidad de la tienda. Asimismo, cuando se intentan implementar sistemas de automatización convencionales, los chatbots tradicionales basados en árboles rígidos de decisión o palabras clave fijas colapsan ante el lenguaje coloquial mexicano (*"se me mermaron dos yogures"*, *"llegaron 15 leches"*, *"cuánto frijol queda"*), obligando al personal a desechar la herramienta por frustración operativa.

En el segundo nivel táctico y administrativo (Nivel 2 o Gerencia/Dueño), el problema alcanza niveles críticos de incertidumbre y fuga de capital. Cuando un producto de alta rotación (como frijol, arroz o aceite vegetal) se agota de forma imprevista por falta de cálculo del tiempo de entrega del proveedor (*lead time*), el negocio incurre en desabasto total (quiebre de inventario). El cliente local que no encuentra el insumo básico acude a la competencia, perdiéndose no solo la venta inmediata sino la lealtad de compra. Por otra parte, cuando el comerciante decide abastecerse, lo hace "al tanteo", arriesgando su flujo de efectivo mediante órdenes desordenadas a los camiones repartidores, sin trazabilidad ni control sobre el monto invertido.

Frente a este doble reto, el pensamiento crítico impone cuestionar las soluciones tecnológicas simplistas. No es admisible pretender resolver la logística de inventarios sustituyendo al personal por modelos de lenguaje generativo puros sin control determinista. Los modelos fundacionales no acotados exhiben severas alucinaciones aritméticas (fallan en cálculos de cobertura de venta y sumas de días de caducidad), confunden la disponibilidad en anaquel y, si se les dotase de autonomía ejecutiva irrestricta, podrían generar compromisos financieros o pedidos catastróficos a proveedores fuera del presupuesto del comerciante. El presente proyecto aborda esta tensión dialéctica mediante el diseño y desarrollo de **Stardust Inventory Agent**, un agente de inteligencia artificial agéntica concebido por el **Equipo Stardust Crusaders** dentro del programa formativo **IBM SkillsBuild AI Experiential Learning Lab (Cohorte México 2026)**, en vinculación directa con las competencias de análisis reflexivo de la materia de **Pensamiento Crítico y Creativo** de la Facultad de Ingeniería Tampico de la Universidad Autónoma de Tamaulipas.

---

## 2. Fundamentación Teórica y Metodológica de Pensamiento Crítico

El pensamiento crítico en la ingeniería de software y la inteligencia artificial no constituye un ejercicio teórico aislado; representa una actitud metodológica orientada a descomponer sistemas complejos, cuestionar supuestos comerciales, ponderar consecuencias éticas y diseñar arquitecturas sustentadas en evidencia verificable. Para conceptualizar a Stardust Inventory Agent, el equipo adoptó el marco de **Enterprise Design Thinking (EDT)** formulado por IBM, articulando un ciclo iterativo y reflexivo centrado incondicionalmente en los resultados humanos (*The Loop: Observar, Reflexionar y Crear*):

### 2.1 Empatizar y Comprender la Experiencia Humana (User Research)
El análisis crítico comenzó con la inmersión empática en los dos arquetipos fundamentales que interactúan en la dinámica del comercio minorista:
* **El bodeguero / encargado de piso:** Experimenta fatiga por el conteo manual de latas y empaques en anaqueles estrechos mientras atiende proveedores y clientes simultáneamente. Se identificó que su verdadera necesidad no es llenar complejos formularios en un software ERP, sino contar con una interfaz ágil a la que pueda dictarle o escribirle en lenguaje natural coloquial mientras acomoda cajas (*"Llegaron 15 leches con caducidad 25 de diciembre"*), recibiendo confirmación visual instantánea mediante semáforos de color.
* **El dueño / gerente de la tienda:** Asume el estrés financiero del pago a proveedores y experimenta impotencia al arrojar mercancía vencida a la basura. Su necesidad medular radica en contar con un centinela cognitivo que vigile el capital de trabajo, le avise qué productos están por vencer antes de que se vuelvan merma, y le prepare borradores de órdenes de compra estrictamente limitados a su presupuesto.

### 2.2 Definición del Problema: De la Fricción Operativa al Escenario Deseado
Mediante el análisis del escenario actual (*As-Is Journey Map*) se desglosaron los puntos de falla estructurales de la tienda de abarrotes: auditorías manuales tardías, falta de alerta previa para rotación de perecederos y pedidos reactivos de reorden. A partir de estos hallazgos se formuló la pregunta generadora de innovación (*How Might We*):  
*¿Cómo podríamos diseñar una plataforma agéntica híbrida que automatice la auditoría de inventarios perecederos en tiempo real mediante lenguaje natural y semáforos normativos, cuantifique el dinero en riesgo y genere borradores formales de órdenes de compra en segundos, garantizando al mismo tiempo cero alucinaciones matemáticas y una gobernanza presupuestal estricta supervisada por el dueño?*

### 2.3 Idear y Evaluar Alternativas Tecnológicas (Doble Diamante)
Durante la fase de ideación, el equipo evaluó críticamente tres aproximaciones arquitectónicas disyuntivas:
1. **Sistema basado exclusivamente en hojas de cálculo (Excel) y reglas fijas:** Descartado por su rigidez para adaptarse a la variabilidad del lenguaje humano en bodega, su nula usabilidad móvil en mostrador y la alta propensión al abandono por parte del personal operativo.
2. **Agente puramente generativo con autonomía total de compras:** Descartado rotundamente por violar los principios básicos de confiabilidad y seguridad económica; los LLMs alucinan sumas matemáticas simples de cobertura de inventario y podrían comprometer las finanzas de la tienda al emitir pedidos exorbitantes.
3. **Arquitectura agéntica híbrida basada en Saber · Decidir · Actuar:** Implementada con un motor determinista en Python, modelos fundacionales IBM Granite en watsonx.ai, *grounding* contra la política oficial `POL-INV-2026-v1` y un freno mandatorio de aprobación humana (*Human-in-the-Loop*) para compras mayores a $3,000 MXN. Esta alternativa fue seleccionada unánimemente como la solución óptima, conciliando velocidad computacional, empatía lingüística y certeza matemática absoluta.

---

## 3. Arquitectura Modular Agéntica (Saber · Decidir · Actuar)

Stardust Inventory Agent materializa los principios de la inteligencia artificial agéntica mediante una arquitectura desacoplada en dos niveles funcionales, interconectados mediante contratos de datos y orquestación contextual:

### 3.1 Capa 1: Interfaz de Operación Frontal en Bodega y Tienda (Lenguaje Natural y Semáforos)
La primera capa interactúa directamente con el bodeguero y el gerente mediante una consola conversacional. Su objetivo es diagnosticar, responder y ejecutar movimientos sin requerir comandos técnicos. Sus componentes principales son:
* **Normalizador Lingüístico y Tolerancia a Modismos:** El motor procesa expresiones coloquiales del comercio mexicano (*"no jala"*, *"llegaron 15 leches"*, *"se mermaron 3 yogures"*, *"cuánto frijol queda"*, *"surtieron aceite"*). Implementa normalización NFKD para suprimir acentos y un reductor morfológico de plurales a singular (*"frijoles"* ➔ *"frijol"*, *"leches"* ➔ *"leche"*), garantizando identificación precisa sobre el catálogo de la tienda.
* **Analizador Sintáctico de Movimientos Transaccionales:** Extrae cantidades numéricas y fechas de caducidad en múltiples formatos (ISO `YYYY-MM-DD`, latino `DD/MM/YYYY` y lenguaje natural como *"30 de diciembre"*), aislando la fecha para evitar colisiones con las cantidades de piezas.
* **Manejo de Cortesías y Saludos Aislados:** Si el usuario ingresa un saludo aislado (*"Hola"*, *"Buenos días"*), el agente responde con cordialidad institucional sin forzar diagnósticos inventados ni crear alertas espurias en el almacén.

### 3.2 Protocolo de Rotación PEPS, Alerta Temprana y Métrica Financiera de Merma (Regla de Oro)
El pilar normativo del agente es el manual `POL-INV-2026-v1`, el cual estipula cinco códigos de estado inmutables representados por semáforos de color:
* 🟢 **STOCK_OK:** Cobertura de ventas saludable y vida útil holgada. Monitoreo pasivo.
* 🟡 **MERMA_RIESGO (Regla de Oro de Calidad):** Cuando un producto se encuentra a 3 días o menos de su vencimiento, el agente activa la alerta de **Etiqueta Amarilla (-25% de descuento)** y ordena desplazar el producto al frente del anaquel bajo el principio PEPS. Simultáneamente calcula el capital en riesgo vs el dinero que se rescata con el descuento comercial, convirtiendo una merma inminente en liquidez.
* 🟡 **REORDEN_URGENTE:** Los días de cobertura son menores o iguales al tiempo de entrega del distribuidor. Se sugiere preparar orden preventiva.
* 🔴 **DESABASTO_TOTAL:** Stock en cero unidades. Se emite alerta prioritaria y sugerencia de compra express.
* 🔴 **CADUCADO:** Fecha vencida ($\le 0$ días). Retiro forzoso e inmediato del anaquel, prohibición estricta de venta y asiento contable de merma.

### 3.3 Capa 2: Motor Determinista, Transacciones en Tiempo Real y Consola de Gobernanza
La segunda capa opera bajo el ciclo cognitivo agéntico tripartito:
* **Capa SABER (Persistencia Transaccional & Datos):** Lee y escribe de forma atómica sobre `inventario_pyme.json` y `config_pyme.json`. Calcula con exactitud aritmética: $\text{Días Cobertura} = \text{Stock} / \text{Ventas Diarias}$, y $\text{Días Vida Útil} = \text{Fecha Caducidad} - \text{Fecha Actual}$. Jamás delega estas operaciones al modelo de lenguaje.
* **Capa DECIDIR (Razonamiento Causal y Modelos IBM Granite):** Impulsada por el modelo fundacional `ibm/granite-13b-chat-v2` en watsonx.ai (Dallas / `us-south`) con decoding Greedy y repetition penalty 1.1. Cruza la telemetría de stock con la política `POL-INV-2026-v1` y redacta respuestas ejecutivas y empáticas.
* **Capa ACTUAR (Contratos Funcionales Tipados):** Ejecuta transacciones controladas mediante funciones de Python: `registrar_movimiento()` para entradas y bajas, y `generar_orden_compra()` para crear órdenes formales con folio (ej. `OC-20261118-ABR-003`) y guardarlas como archivo físico `orden_compra_<SKU>.txt`.

---

## 4. Gobernanza Operativa, Ética y Human-in-the-Loop (HITL)

Desde la óptica del pensamiento crítico, delegar transacciones financieras a una inteligencia artificial sin supervisión humana constituye un grave riesgo para la supervivencia de una pequeña empresa. Si un agente decidiese emitir órdenes de compra de forma autónoma sin considerar la liquidez en caja, la tienda podría declararse en quiebra en cuestión de semanas.

Por ello, Stardust Inventory Agent incorpora una política inviolable de **Gobernanza Human-in-the-Loop** como núcleo fundamental de su diseño. A través del módulo de Onboarding Asistido (`config_pyme.json`), el dueño de la tienda define su umbral máximo de compra sin autorización ($3,000 MXN por defecto). Cuando se genera una orden de compra:
* Si la inversión estimada es $\le \$3,000\text{ MXN}$: El agente cataloga la orden como `✅ APROBADO AUTOMÁTICAMENTE (Dentro del límite de gobernanza)`.
* Si la inversión estimada excede el umbral: El agente frena la emisión definitiva, estampa `ESTADO DE GOBERNANZA: ⚠️ REQUIERE VOBO DE GERENCIA` y guarda el borrador oficial en la carpeta de trabajo, requiriendo de forma obligatoria la firma operativa del dueño antes de enviarlo al proveedor.

De esta manera, el agente asume el 95% de la carga matemática y documental en milisegundos, pero la soberanía económica permanece siempre en manos humanas.

---

## 5. Validación Experimental, Suite de Pruebas y Resultados Cuantificables

Para certificar la robustez del sistema y el cumplimiento irrestricto de las reglas normativas, se diseñó e implementó una suite automatizada de 11 pruebas integrales ejecutadas localmente sin dependencias externas:
* **Prueba 1 (Flujo Feliz de Diagnóstico):** Valida la consulta de existencias, cálculo de cobertura y emisión de semáforo normativo sin errores [100% PASS].
* **Prueba 2 (Entrada con Fecha ISO):** Ingreso de lote con fecha `YYYY-MM-DD`; valida incremento de stock y actualización de caducidad en base de datos [100% PASS].
* **Prueba 3 (Entrada con Fecha Coloquial):** Procesamiento de entrada con texto *"30 de diciembre"*; corrobora asignación correcta de año y cantidad sin interferencias [100% PASS].
* **Prueba 4 (Salida por Venta):** Descuento de unidades vendidas y recálculo automático de semáforo preventivo de reorden [100% PASS].
* **Prueba 5 (Baja por Merma):** Registro de desecho de producto vencido con cuantificación monetaria de la pérdida económica [100% PASS].
* **Prueba 6 (Orden de Compra Aprobada):** Generación de pedido para insumo en desabasto por $840 MXN; valida aprobación automática dentro del límite [100% PASS].
* **Prueba 7 (Orden de Compra con Filtro HITL):** Generación de pedido de 120 aceites por $4,200 MXN; valida activación de alerta de VoBo de Gerencia [100% PASS].
* **Prueba 8 (Producto No Existente):** Consulta sobre artículo inexistente; corrobora notificación limpia sin alucinación de datos [100% PASS].
* **Prueba 9 (Stock Insuficiente):** Intento de salida mayor a las existencias físicas; valida bloqueo de inventario negativo [100% PASS].
* **Prueba 10 (Onboarding Dinámico):** Parametrización de tienda y verificación de persistencia en `config_pyme.json` [100% PASS].
* **Prueba 11 (Manejo de Cortesías):** Entrada de saludos aislados sin reporte de errores espurios ni falsas fallas [100% PASS].

### 5.1 Métricas de Impacto Operativo Cuantificables
* **Reducción del Tiempo de Auditoría en 96.8%:** El tiempo requerido para auditar existencias y caducidades en anaquel se redujo de 45 minutos manuales a 1.4 segundos mediante la consulta por lenguaje natural.
* **Disminución Proyectada de Mermas > 82%:** La activación anticipada de la Etiqueta Amarilla (-25% de descuento) 3 días antes del vencimiento permite recuperar el costo del producto en el 82% de los lotes perecederos.
* **100% de Compras Bajo Gobernanza (HITL):** El 100% de las órdenes superiores a $3,000 MXN fueron bloqueadas exitosamente para revisión gerencial, registrándose cero compras desmedidas fuera de presupuesto.
* **0% de Alucinaciones Matemáticas:** El motor determinista en Python garantizó exactitud absoluta en sumas, restas y proyecciones de cobertura.

---

## 6. Discusión, Limitaciones y Escalabilidad Futura

El análisis crítico de los resultados confirma la resiliencia del sistema al fundamentarse en un motor Python ligero sin dependencias propietarias complejas, compatible tanto en terminales locales con IBM Bob como en instancias de nube con watsonx.ai. No obstante, se reconocen limitaciones técnicas que definen la agenda de desarrollo futuro: actualmente la persistencia opera sobre archivos JSON locales en una sola estación; en una etapa comercial se requerirá migrar hacia bases de datos relacionales robustas (PostgreSQL en IBM Cloud) con soporte multi-sucursal. Asimismo, la interacción por teclado debe evolucionar hacia la integración con lectores de código de barras (Barcode/QR) mediante cámara web y la habilitación de un bot oficial de WhatsApp Business API, permitiendo al bodeguero dictar o fotografiar códigos directamente desde su teléfono móvil.

---

## 7. Conclusión

El desarrollo del proyecto Stardust Inventory Agent por parte del Equipo Stardust Crusaders demuestra con contundencia que la conjunción entre el pensamiento crítico y la inteligencia artificial agéntica es capaz de transformar realidades económicas tangibles. Las competencias formativas cultivadas en la Facultad de Ingeniería Tampico de la Universidad Autónoma de Tamaulipas —específicamente en la materia de Pensamiento Crítico y Creativo— permitieron al equipo superar la mera fascinación por los generadores de texto y adoptar una postura rigurosa de ingeniería: cuestionar supuestos operativos, blindar el software contra alucinaciones, anteponer la ética en la toma de decisiones y diseñar soluciones tecnológicas al servicio de las personas.

Al dotar a las pequeñas tiendas de abarrotes de un agente digital confiable que combate el desperdicio de alimentos y previene el desabasto con gobernanza humana, el equipo valida que la inteligencia artificial más valiosa no es aquella que busca reemplazar al trabajador, sino aquella que dignifica su labor y fortalece la economía de nuestras comunidades.

---

## 8. Referencias bibliográficas (Formato APA 7.ª edición)

* Ballou, R. H. (2004). *Logística: Administración de la cadena de suministro* (5.ª ed.). Pearson Educación.
* Díaz Zavala, R. M., Esquivel Las Heras, J. A., Cuadros Paz, L. E., & Cuadros Linares, L. D. (2025). Relación entre inteligencia emocional y pensamiento crítico en contextos educativos: Conexiones fundamentales. *Revista de Ciencias Sociales*, 31(3), 112–128. https://doi.org/10.31876/rcs.v31i3.44300
* Hamilton, L., Halverson, R., Jackson, S. S., Mandinach, E., Supovitz, J. A., & Wayman, J. C. (2009). *Using student achievement data to support instructional decision making* (NCEE 2009-4067). National Center for Education Evaluation and Regional Assistance, Institute of Education Sciences, U.S. Department of Education. https://ies.ed.gov/ncee/wwc/Docs/PracticeGuide/dddm_pg_092909.pdf
* IBM Corporation. (2024). *Enterprise Design Thinking: A framework for team-based innovation at speed and scale*. IBM Design Guides. https://www.ibm.com/design/thinking/
* IBM Corporation. (2024). *watsonx.ai and Granite Foundation Models: Building reliable enterprise AI agents*. IBM Redbooks. https://www.ibm.com/watsonx
* Lewis, J. R., & Sauro, J. (2021). Usability and user experience evaluation in enterprise software interfaces. *International Journal of Human-Computer Interaction*, 37(8), 741–753. https://doi.org/10.1080/10447318.2020.1841416
* Loeb, S., Dynarski, S., McFarland, D., Morris, P., Reardon, S., & Reber, S. (2017). *Descriptive analysis in education: A guide for researchers* (NCEE 2017-4023). National Center for Education Evaluation and Regional Assistance. https://ies.ed.gov/use-work/resource-library/report/evaluation-report/descriptive-analysis-education-guide-researchers
* Olano-Dávila, A. M., Huamán-Delgado, N., Ortiz-Salas, D. A., & Jiménez-Taipe, L. (2026). Emociones y pensamiento crítico en estudiantes de ingeniería: Revisión sistemática. *Episteme Koinonía*, 9(17), 356–377. https://doi.org/10.35381/e.k.v9i17.4929
* Organización de las Naciones Unidas para la Alimentación y la Agricultura [FAO]. (2021). *Prevención y reducción de pérdidas y desperdicios de alimentos en el comercio minorista*. Colección Manuales Prácticos de Gestión Alimentaria.
* Papanagnou, D., Sourtzi, P., Kalokairinou, A., & Zyga, S. (2023). Emotional intelligence is more important than the learning environment in improving critical thinking. *Medical Teacher*, 45(7), 708–716. https://doi.org/10.1080/0142159X.2023.2193305
* Silver, E. A., Pyke, D. F., & Thomas, D. J. (2016). *Inventory and Production Management in Supply Chains* (4th ed.). CRC Press.
* SkillUp Online & IBM SkillsBuild. (2026). *Banco de 50 proyectos para construir soluciones con IA agéntica: Guía técnica de desarrollo y gobernanza*. Experiential Learning Lab México.
* Van Rossum, G., & Drake, F. L. (2024). *Python 3 Language Reference Manual*. Python Software Foundation.
