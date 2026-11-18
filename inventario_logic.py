"""
=============================================================================
           STARDUST INVENTORY AGENT - MOTOR DE LÓGICA Y REGLAS (V4)
               Equipo: Stardust Crusaders | IBM Experiential Lab
=============================================================================
Capacidades implementadas:
 1. Onboarding Asistido (config_pyme.json persistente y dinámico).
 2. Acciones en tiempo real por lenguaje natural (Entradas, Salidas, Mermas).
 3. Generador formal de Órdenes de Compra con Gobernanza ($3,000 MXN límite).
 4. Diagnóstico normativo POL-INV-2026-v1 con semáforos e impacto financiero.
 5. Tolerancia a plurales y lenguaje coloquial.
=============================================================================
"""

import json
import os
import re
import sys
import unicodedata
from datetime import date, datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_DB = os.path.join(DIRECTORIO_ACTUAL, "inventario_pyme.json")
ARCHIVO_CONFIG = os.path.join(DIRECTORIO_ACTUAL, "config_pyme.json")

CONFIG_DEFAULT = {
    "nombre_tienda": "Mi Tienda PYME",
    "maneja_perecederos": True,
    "dias_entrega_promedio": 3,
    "monto_maximo_autorizacion": 3000.0,
    "descuento_merma_pct": 25,
    "dias_anticipacion_merma": 3,
    "onboarding_completado": False
}

# =============================================================================
# SECCIÓN 1: ONBOARDING ASISTIDO Y CONFIGURACIÓN DINÁMICA (PUNTO 1)
# =============================================================================

def cargar_configuracion():
    if not os.path.exists(ARCHIVO_CONFIG):
        return None
    try:
        with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def guardar_configuracion(config):
    with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def ejecutar_cuestionario_onboarding(interactivo=True):
    config_actual = cargar_configuracion() or CONFIG_DEFAULT.copy()

    if not interactivo:
        config_actual["onboarding_completado"] = True
        guardar_configuracion(config_actual)
        return config_actual

    print("\n" + "=" * 65)
    print("      CONFIGURACIÓN ASISTIDA DEL NEGOCIO (ONBOARDING INICIAL)")
    print("        Adaptando Stardust Inventory Agent a tu empresa")
    print("=" * 65)
    print("Por favor responde a estas 4 preguntas clave para calibrar las reglas:\n")

    resp_nombre = input("1. ¿Cuál es el nombre comercial de tu negocio/tienda? [Mi Tienda PYME]: ").strip()
    config_actual["nombre_tienda"] = resp_nombre if resp_nombre else "Mi Tienda PYME"

    resp_perecederos = input("2. ¿Comercializas productos perecederos con caducidad (leche, yogur, etc.)? (s/n) [s]: ").strip().lower()
    config_actual["maneja_perecederos"] = False if resp_perecederos in ["n", "no"] else True

    resp_dias = input("3. ¿Cuántos días promedio tardan tus proveedores en surtir pedidos? [3]: ").strip()
    try:
        config_actual["dias_entrega_promedio"] = int(resp_dias) if resp_dias else 3
    except ValueError:
        config_actual["dias_entrega_promedio"] = 3

    resp_monto = input("4. ¿A partir de qué monto ($ MXN) requieres aprobación del dueño para comprar? [3000]: ").strip()
    try:
        config_actual["monto_maximo_autorizacion"] = float(resp_monto) if resp_monto else 3000.0
    except ValueError:
        config_actual["monto_maximo_autorizacion"] = 3000.0

    config_actual["onboarding_completado"] = True
    guardar_configuracion(config_actual)

    print("\n[✓] ¡Configuración guardada con éxito en config_pyme.json!")
    print(f"    • Negocio: {config_actual['nombre_tienda']}")
    print(f"    • Control de perecederos: {'Activado' if config_actual['maneja_perecederos'] else 'Desactivado'}")
    print(f"    • Límite de compras sin autorización: ${config_actual['monto_maximo_autorizacion']:,.2f} MXN")
    print("=" * 65 + "\n")

    return config_actual

# =============================================================================
# SECCIÓN 2: BASE DE DATOS Y BÚSQUEDA FLEXIBLE
# =============================================================================

def cargar_inventario():
    if not os.path.exists(ARCHIVO_DB):
        return []
    with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_inventario(datos):
    with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def normalizar(texto):
    if not texto:
        return ""
    sin_acento = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in sin_acento if not unicodedata.combining(c)).lower().strip()

def obtener_raiz_singular(palabra):
    p = palabra
    if p.endswith("es") and len(p) > 4:
        return p[:-2]
    elif p.endswith("s") and len(p) > 3:
        return p[:-1]
    return p

def buscar_producto(termino, inventario):
    term_clean = normalizar(termino)
    if not term_clean:
        return None

    # 1. Búsqueda exacta por SKU
    for item in inventario:
        if normalizar(item["sku"]) == term_clean:
            return item

    # 2. Búsqueda por coincidencia de nombre completa o parcial
    for item in inventario:
        nom_clean = normalizar(item["nombre"])
        if term_clean in nom_clean or nom_clean in term_clean:
            return item

    # 3. Búsqueda por raíz singular (plurales: frijoles -> frijol)
    palabras_busqueda = [obtener_raiz_singular(w) for w in term_clean.split() if len(w) > 2]
    for item in inventario:
        palabras_item = [obtener_raiz_singular(w) for w in normalizar(item["nombre"]).split()]
        for pb in palabras_busqueda:
            for pi in palabras_item:
                if pb == pi or pb in pi or pi in pb:
                    return item

    return None

def registrar_movimiento(sku_o_nombre, tipo_movimiento, cantidad, fecha_caducidad_nueva=None):
    inventario = cargar_inventario()
    producto = buscar_producto(sku_o_nombre, inventario)

    if not producto:
        return {
            "exito": False,
            "codigo": "ERR_NO_ENCONTRADO",
            "mensaje": f"El producto '{sku_o_nombre}' no existe en el catálogo.",
            "accion": "Verificar SKU o dar de alta el producto nuevo."
        }

    tipo = tipo_movimiento.upper()
    stock_anterior = producto["stock_actual"]

    if tipo == "ENTRADA":
        producto["stock_actual"] += cantidad
        if fecha_caducidad_nueva:
            producto["fecha_caducidad"] = fecha_caducidad_nueva
    elif tipo == "SALIDA":
        if producto["stock_actual"] < cantidad:
            return {
                "exito": False,
                "codigo": "ERR_STOCK_INSUFICIENTE",
                "mensaje": f"Stock insuficiente en bodega. Hay {stock_anterior} disponibles y se solicitaron {cantidad}.",
                "accion": "Ajustar la cantidad a retirar."
            }
        producto["stock_actual"] -= cantidad
    else:
        return {
            "exito": False,
            "codigo": "ERR_TIPO_INVALIDO",
            "mensaje": f"Tipo de movimiento '{tipo_movimiento}' inválido. Use ENTRADA o SALIDA."
        }

    guardar_inventario(inventario)
    return {
        "exito": True,
        "codigo": "MOVIMIENTO_EXITOSO",
        "sku": producto["sku"],
        "nombre": producto["nombre"],
        "tipo": tipo,
        "cantidad": cantidad,
        "stock_anterior": stock_anterior,
        "nuevo_stock": producto["stock_actual"],
        "caducidad": producto.get("fecha_caducidad", "N/A")
    }

# =============================================================================
# SECCIÓN 3: PROCESAMIENTO DE ACCIONES POR LENGUAJE NATURAL (PUNTO 2)
# =============================================================================

MESES_MAPA = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12
}

def extraer_fecha_caducidad(texto):
    """Extrae fechas en formato YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY o '30 de diciembre'."""
    m1 = re.search(r'\b(20\d{2})[-/](0?[1-9]|1[0-2])[-/](0?[1-9]|[12]\d|3[01])\b', texto)
    if m1:
        return f"{int(m1.group(1)):04d}-{int(m1.group(2)):02d}-{int(m1.group(3)):02d}"

    m2 = re.search(r'\b(0?[1-9]|[12]\d|3[01])[-/](0?[1-9]|1[0-2])[-/](20\d{2})\b', texto)
    if m2:
        return f"{int(m2.group(3)):04d}-{int(m2.group(2)):02d}-{int(m2.group(1)):02d}"

    m3 = re.search(r'\b(0?[1-9]|[12]\d|3[01])\s+de\s+([a-zA-Z]+)(?:\s+de\s+(20\d{2}))?\b', texto, re.IGNORECASE)
    if m3:
        dia = int(m3.group(1))
        mes_str = m3.group(2).lower()
        anio = int(m3.group(3)) if m3.group(3) else date.today().year
        if mes_str in MESES_MAPA:
            mes = MESES_MAPA[mes_str]
            return f"{anio:04d}-{mes:02d}-{dia:02d}"

    return None

def procesar_accion_movimiento(texto_comando):
    """
    Interpreta comandos en lenguaje natural para registrar ENTRADAS o SALIDAS.
    Ejemplos:
      - 'Llegaron 15 leches con caducidad 2026-12-20'
      - 'Entrada de 20 cajas de yogur caducidad 25/12/2026'
      - 'Se vendieron 5 frijoles'
      - 'Se mermaron 3 yogures'
      - 'Salida de 2 unidades de aceite'
    """
    texto_low = texto_comando.lower()

    palabras_entrada = ["llegaron", "llego", "entrada", "recibimos", "recibir", "ingreso", "alta", "compramos", "surtieron"]
    palabras_salida = ["vendieron", "vendio", "venta", "salida", "retiro", "retirar", "baja", "despacho", "merma", "mermaron", "mermo", "desechar", "caducado", "tirar"]

    es_entrada = any(w in texto_low for w in palabras_entrada)
    es_salida = any(w in texto_low for w in palabras_salida)

    if not es_entrada and not es_salida:
        return None

    tipo = "ENTRADA" if es_entrada else "SALIDA"

    # Extraer fecha de caducidad si aplica
    fecha_caducidad = extraer_fecha_caducidad(texto_comando)

    # Remover fechas del texto para aislar la cantidad sin colisiones
    texto_sin_fechas = texto_comando
    texto_sin_fechas = re.sub(r'\b20\d{2}[-/]\d{1,2}[-/]\d{1,2}\b', '', texto_sin_fechas)
    texto_sin_fechas = re.sub(r'\b\d{1,2}[-/]\d{1,2}[-/]20\d{2}\b', '', texto_sin_fechas)
    texto_sin_fechas = re.sub(r'\b\d{1,2}\s+de\s+[a-zA-Z]+(?:\s+de\s+\d{4})?\b', '', texto_sin_fechas, flags=re.IGNORECASE)

    cantidades = [int(n) for n in re.findall(r'\b(\d+)\b', texto_sin_fechas)]
    cantidad = cantidades[0] if cantidades else 1

    # Identificar producto
    inventario = cargar_inventario()
    producto = buscar_producto(texto_sin_fechas, inventario)

    if not producto:
        return {
            "exito": False,
            "respuesta": f"⚪ No pude identificar qué producto deseas registrar en: '{texto_comando}'. Por favor menciona el nombre (ej. leche, yogur, frijol, aceite)."
        }

    resultado = registrar_movimiento(producto["sku"], tipo, cantidad, fecha_caducidad)
    if not resultado["exito"]:
        return {
            "exito": False,
            "respuesta": f"❌ Error al registrar movimiento: {resultado['mensaje']}"
        }

    diag = diagnosticar_producto(producto["sku"])
    simbolo = "🟢" if tipo == "ENTRADA" else "📦"
    lineas = [
        f"{simbolo} {tipo} REGISTRADA EN TIEMPO REAL",
        f"• Producto: {producto['nombre']} ({producto['sku']})",
        f"• Cantidad {'ingresada' if tipo == 'ENTRADA' else 'retirada'}: {('+' if tipo == 'ENTRADA' else '-')}{cantidad} piezas",
        f"• Stock: {resultado['stock_anterior']} ➔ {resultado['nuevo_stock']} piezas disponibles",
        f"• Caducidad en sistema: {resultado['caducidad']}",
        f"• Estado del producto: {diag['semaforo']}"
    ]
    return {
        "exito": True,
        "respuesta": "\n".join(lineas)
    }

# =============================================================================
# SECCIÓN 4: GENERACIÓN DE ORDEN DE COMPRA (PUNTO 3)
# =============================================================================

def generar_orden_compra(sku_o_nombre, cantidad_solicitada=None, cantidad=None):
    """
    Genera un borrador formal de Orden de Compra para el proveedor.
    Calcula costos y verifica el límite de autorización del Gerente (Gobernanza).
    """
    if cantidad is not None and cantidad_solicitada is None:
        cantidad_solicitada = cantidad

    config = cargar_configuracion() or CONFIG_DEFAULT
    inventario = cargar_inventario()
    producto = buscar_producto(sku_o_nombre, inventario)

    if not producto:
        return f"⚪ Producto '{sku_o_nombre}' no encontrado para generar orden de compra."

    stock_min = producto["stock_minimo"]
    stock_act = producto["stock_actual"]
    costo_unit = producto.get("precio_costo", 0.0)
    proveedor = producto.get("proveedor", "Proveedor General")
    limite = config.get("monto_maximo_autorizacion", 3000.0)
    tienda = config.get("nombre_tienda", "Mi Tienda PYME")

    if cantidad_solicitada and cantidad_solicitada > 0:
        unidades = cantidad_solicitada
    else:
        unidades = max((stock_min * 2) - stock_act, 10)

    total_estimado = round(unidades * costo_unit, 2)
    requiere_gerente = total_estimado > limite

    hoy_str = date.today().strftime("%Y-%m-%d")
    folio = f"OC-{date.today().strftime('%Y%m%d')}-{producto['sku']}"

    estado_aprobacion = (
        f"⚠️ REQUIERE VOBO DE GERENCIA (Supera límite de ${limite:,.2f} MXN)"
        if requiere_gerente else
        f"✅ APROBADO AUTOMÁTICAMENTE (Dentro del límite de ${limite:,.2f} MXN)"
    )

    orden_texto = f"""=================================================================
                    ORDEN DE COMPRA SUGERIDA
=================================================================
Folio: {folio}                    Fecha: {hoy_str}
Empresa: {tienda}
Proveedor: {proveedor}
-----------------------------------------------------------------
Detalle de Mercancía:
• Producto: {producto['nombre']}
• Código SKU: {producto['sku']}
• Cantidad solicitada: {unidades} unidades
• Costo unitario estimado: ${costo_unit:.2f} MXN
-----------------------------------------------------------------
TOTAL ESTIMADO DE COMPRA: ${total_estimado:,.2f} MXN
ESTADO DE GOBERNANZA: {estado_aprobacion}
-----------------------------------------------------------------
Instrucciones operativas:
- Borrador oficial listo para enviar al proveedor vía WhatsApp/Correo.
- El proveedor tiene un tiempo estimado de entrega de {producto.get('dias_entrega_proveedor', 3)} días hábiles.
================================================================="""

    # Guardar copia del borrador en un archivo de texto en la carpeta
    archivo_oc = os.path.join(DIRECTORIO_ACTUAL, f"orden_compra_{producto['sku']}.txt")
    try:
        with open(archivo_oc, "w", encoding="utf-8") as f:
            f.write(orden_texto)
    except Exception:
        pass

    return orden_texto

# =============================================================================
# SECCIÓN 5: DIAGNÓSTICO CALIBRADO POR REGLAS DE NEGOCIO
# =============================================================================

def diagnosticar_producto(sku_o_nombre, fecha_referencia=None):
    config = cargar_configuracion() or CONFIG_DEFAULT

    if fecha_referencia is None:
        hoy = date.today()
    else:
        hoy = datetime.strptime(fecha_referencia, "%Y-%m-%d").date()

    inventario = cargar_inventario()
    producto = buscar_producto(sku_o_nombre, inventario)

    if not producto:
        return {
            "semaforo": "⚪ NO REGISTRADO",
            "codigo": "ERR_NO_ENCONTRADO",
            "mensaje": f"Producto '{sku_o_nombre}' no encontrado en catálogo.",
            "accion": "Solicitar revisión manual al encargado de compras.",
            "tarjeta_visual": f"⚪ NO ENCONTRADO: '{sku_o_nombre}' no está registrado en el sistema."
        }

    stock = producto["stock_actual"]
    stock_min = producto["stock_minimo"]
    ventas_dia = producto.get("ventas_diarias_promedio", 1)
    dias_entrega = producto.get("dias_entrega_proveedor", config.get("dias_entrega_promedio", 3))
    costo_unitario = producto.get("precio_costo", 0.0)
    precio_venta = producto.get("precio_venta", 0.0)
    limite_compra = config.get("monto_maximo_autorizacion", 3000.0)
    controla_perecederos = config.get("maneja_perecederos", True)
    descuento_pct = config.get("descuento_merma_pct", 25)
    dias_alerta_merma = config.get("dias_anticipacion_merma", 3)
    
    dias_cobertura = (stock / ventas_dia) if ventas_dia > 0 else 999

    dias_para_caducar = 999
    if controla_perecederos and "fecha_caducidad" in producto and producto["fecha_caducidad"]:
        f_cad = datetime.strptime(producto["fecha_caducidad"], "%Y-%m-%d").date()
        dias_para_caducar = (f_cad - hoy).days

    if controla_perecederos and dias_para_caducar <= 0:
        perdida_financiera = round(stock * costo_unitario, 2)
        return {
            "semaforo": "🔴 CADUCADO",
            "codigo": "CADUCADO",
            "estado": "Producto vencido",
            "sku": producto["sku"],
            "nombre": producto["nombre"],
            "stock_actual": stock,
            "dias_para_caducar": dias_para_caducar,
            "capital_en_riesgo": f"${perdida_financiera:.2f} MXN",
            "accion": "Retirar de inmediato de anaquel, prohibida su venta y registrar merma.",
            "escalar_humano": True,
            "tarjeta_visual": (
                f"🔴 CADUCADO: {producto['nombre']} ({producto['sku']})\n"
                f"• Estado: Venció hace {abs(dias_para_caducar)} día(s) ({producto['fecha_caducidad']})\n"
                f"• Existencias a desechar: {stock} unidades\n"
                f"• Pérdida financiera: ${perdida_financiera:.2f} MXN\n"
                f"• Acción: RETIRAR DE ANAQUEL DE INMEDIATO."
            )
        }

    elif controla_perecederos and dias_para_caducar <= dias_alerta_merma:
        capital_en_riesgo = round(stock * costo_unitario, 2)
        factor_descuento = (100 - descuento_pct) / 100.0
        recuperacion_estimada = round(stock * (precio_venta * factor_descuento), 2)
        return {
            "semaforo": "🟡 MERMA_RIESGO",
            "codigo": "MERMA_RIESGO",
            "estado": "Riesgo de merma por caducidad próxima",
            "sku": producto["sku"],
            "nombre": producto["nombre"],
            "stock_actual": stock,
            "dias_para_caducar": dias_para_caducar,
            "capital_en_riesgo": f"${capital_en_riesgo:.2f} MXN",
            "recuperacion_estimada": f"${recuperacion_estimada:.2f} MXN",
            "accion": f"Aplicar etiqueta amarilla ({descuento_pct}% descuento) y colocar al frente (regla PEPS).",
            "escalar_humano": False,
            "tarjeta_visual": (
                f"🟡 ALERTA DE MERMA: {producto['nombre']} ({producto['sku']})\n"
                f"• Vencimiento: Faltan {dias_para_caducar} día(s) (Caduca: {producto['fecha_caducidad']})\n"
                f"• Stock en riesgo: {stock} unidades\n"
                f"• Impacto financiero: ${capital_en_riesgo:.2f} MXN en costo. Con -{descuento_pct}% se recuperan ${recuperacion_estimada:.2f} MXN.\n"
                f"• Acción requerida: ETIQUETA AMARILLA (-{descuento_pct}%) y mover al frente."
            )
        }

    elif stock <= 0:
        unidades_reorden = max(stock_min * 2, 10)
        costo_pedido = round(unidades_reorden * costo_unitario, 2)
        requiere_gerente = costo_pedido > limite_compra
        return {
            "semaforo": "🔴 DESABASTO",
            "codigo": "DESABASTO_TOTAL",
            "estado": "Sin existencias en almacén",
            "sku": producto["sku"],
            "nombre": producto["nombre"],
            "stock_actual": 0,
            "sugerencia_compra": unidades_reorden,
            "proveedor": producto["proveedor"],
            "costo_pedido_estimado": f"${costo_pedido:.2f} MXN",
            "accion": f"Emitir orden urgente por {unidades_reorden} unidades a {producto['proveedor']}.",
            "escalar_humano": requiere_gerente,
            "tarjeta_visual": (
                f"🔴 DESABASTO TOTAL: {producto['nombre']} ({producto['sku']})\n"
                f"• Existencias actuales: 0 piezas\n"
                f"• Pedido sugerido: {unidades_reorden} unidades con {producto['proveedor']}\n"
                f"• Inversión estimada: ${costo_pedido:.2f} MXN" +
                (f" (Requiere VoBo de Gerencia por superar límite de ${limite_compra:,.2f} MXN)\n" if requiere_gerente else "\n") +
                f"• Escribe: 'generar orden de compra frijol' para crear el borrador oficial."
            )
        }

    elif dias_cobertura <= dias_entrega or stock <= stock_min:
        unidades_reorden = (stock_min * 2) - stock
        costo_pedido = round(unidades_reorden * costo_unitario, 2)
        return {
            "semaforo": "🟡 REORDEN_URGENTE",
            "codigo": "REORDEN_URGENTE",
            "estado": "Stock bajo / punto de reorden",
            "sku": producto["sku"],
            "nombre": producto["nombre"],
            "stock_actual": stock,
            "dias_cobertura": round(dias_cobertura, 1),
            "dias_entrega": dias_entrega,
            "sugerencia_compra": unidades_reorden,
            "proveedor": producto["proveedor"],
            "costo_pedido_estimado": f"${costo_pedido:.2f} MXN",
            "accion": f"Elaborar borrador de orden por {unidades_reorden} unidades con {producto['proveedor']}.",
            "escalar_humano": False,
            "tarjeta_visual": (
                f"🟡 REORDEN PREVENTIVO: {producto['nombre']} ({producto['sku']})\n"
                f"• Stock actual: {stock} piezas (Cobertura para {dias_cobertura:.1f} días)\n"
                f"• El proveedor tarda {dias_entrega} días en entregar.\n"
                f"• Sugerencia de compra: {unidades_reorden} unidades (${costo_pedido:.2f} MXN)\n"
                f"• Escribe: 'generar orden de compra' para crear el borrador oficial."
            )
        }

    else:
        return {
            "semaforo": "🟢 ÓPTIMO",
            "codigo": "STOCK_OK",
            "estado": "Inventario en nivel óptimo",
            "sku": producto["sku"],
            "nombre": producto["nombre"],
            "stock_actual": stock,
            "dias_cobertura": round(dias_cobertura, 1),
            "accion": "Ninguna acción requerida.",
            "escalar_humano": False,
            "tarjeta_visual": (
                f"🟢 STOCK ÓPTIMO: {producto['nombre']} ({producto['sku']})\n"
                f"• Existencias: {stock} piezas\n"
                f"• Cobertura estimada: {dias_cobertura:.1f} días de venta\n"
                f"• Estado: Niveles saludables. No requiere compra."
            )
        }

def reporte_proactivo(fecha_referencia=None):
    inventario = cargar_inventario()
    alertas = []
    for item in inventario:
        diag = diagnosticar_producto(item["sku"], fecha_referencia)
        if diag["codigo"] in ["CADUCADO", "MERMA_RIESGO", "DESABASTO_TOTAL", "REORDEN_URGENTE"]:
            alertas.append(diag)
    return alertas
