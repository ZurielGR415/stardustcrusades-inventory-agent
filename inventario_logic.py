"""
=============================================================================
             MÓDULO DE LÓGICA DE INVENTARIO - VERSIÓN MEJORADA (V2)
                 Equipo: Stardust Crusaders | IBM Experiential Lab
=============================================================================
Mejoras incorporadas:
 1. Tolerancia a plurales y lenguaje coloquial (leches, frijoles, yogures).
 2. Semáforo visual con emojis (🟢, 🟡, 🔴) en formato de tarjeta rápida.
 3. Métrica de impacto financiero (Capital en riesgo vs Dinero recuperado).
=============================================================================
"""

import json
import os
import sys
import unicodedata
from datetime import datetime, date

# Asegurar compatibilidad de consola con caracteres especiales y emojis en Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ARCHIVO_DB = os.path.join(os.path.dirname(__file__), "inventario_pyme.json")

def cargar_inventario():
    if not os.path.exists(ARCHIVO_DB):
        return []
    with open(ARCHIVO_DB, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_inventario(datos):
    with open(ARCHIVO_DB, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def normalizar(texto):
    """Elimina acentos, pasa a minúsculas y limpia espacios."""
    if not texto:
        return ""
    sin_acento = unicodedata.normalize('NFKD', texto)
    return ''.join(c for c in sin_acento if not unicodedata.combining(c)).lower().strip()

def obtener_raiz_singular(palabra):
    """Quita terminaciones plurales comunes en español (es, s)."""
    p = palabra
    if p.endswith("es") and len(p) > 4:
        return p[:-2]  # frijoles -> frijol, yogures -> yogur
    elif p.endswith("s") and len(p) > 3:
        return p[:-1]  # leches -> leche, aceites -> aceite
    return p

def buscar_producto(termino, inventario):
    """
    Búsqueda flexible: tolera mayúsculas, acentos, plurales y sinónimos.
    """
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

    # 3. Búsqueda por raíz de palabras (tolerancia a plurales: frijoles -> frijol)
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
                "mensaje": f"No hay suficiente stock. Disponible: {stock_anterior}, solicitado: {cantidad}.",
                "accion": "Ajustar cantidad solicitada."
            }
        producto["stock_actual"] -= cantidad
    else:
        return {
            "exito": False,
            "codigo": "ERR_TIPO_INVALIDO",
            "mensaje": f"Tipo '{tipo_movimiento}' inválido. Use ENTRADA o SALIDA."
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
        "caducidad": producto["fecha_caducidad"]
    }

def diagnosticar_producto(sku_o_nombre, fecha_referencia=None):
    """
    Diagnostica producto con Semáforo Visual (🟢, 🟡, 🔴) y Cálculo Financiero.
    """
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
    dias_entrega = producto.get("dias_entrega_proveedor", 3)
    costo_unitario = producto.get("precio_costo", 0.0)
    precio_venta = producto.get("precio_venta", 0.0)
    
    dias_cobertura = (stock / ventas_dia) if ventas_dia > 0 else 999

    dias_para_caducar = 999
    if "fecha_caducidad" in producto and producto["fecha_caducidad"]:
        f_cad = datetime.strptime(producto["fecha_caducidad"], "%Y-%m-%d").date()
        dias_para_caducar = (f_cad - hoy).days

    # 1. Caso CADUCADO
    if dias_para_caducar <= 0:
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
                f"• Pérdida financiera registrada: ${perdida_financiera:.2f} MXN\n"
                f"• Acción: RETIRAR DE ANAQUEL DE INMEDIATO."
            )
        }

    # 2. Caso MERMA_RIESGO (1 a 3 días de caducidad)
    elif dias_para_caducar <= 3:
        capital_en_riesgo = round(stock * costo_unitario, 2)
        recuperacion_estimada = round(stock * (precio_venta * 0.75), 2)
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
            "accion": "Aplicar etiqueta amarilla (25% descuento) y colocar al frente (regla PEPS).",
            "escalar_humano": False,
            "tarjeta_visual": (
                f"🟡 ALERTA DE MERMA: {producto['nombre']} ({producto['sku']})\n"
                f"• Vencimiento: Faltan {dias_para_caducar} día(s) (Caduca: {producto['fecha_caducidad']})\n"
                f"• Stock en riesgo: {stock} unidades\n"
                f"• Impacto financiero: ${capital_en_riesgo:.2f} MXN en costo. Con -25% se recuperan ${recuperacion_estimada:.2f} MXN.\n"
                f"• Acción requerida: ETIQUETA AMARILLA (-25%) y mover al frente de anaquel."
            )
        }

    # 3. Caso DESABASTO_TOTAL
    elif stock <= 0:
        unidades_reorden = max(stock_min * 2, 10)
        costo_pedido = round(unidades_reorden * costo_unitario, 2)
        requiere_gerente = costo_pedido > 3000.00
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
                (" (Requiere VoBo de Gerencia por superar $3,000 MXN)\n" if requiere_gerente else "\n") +
                f"• Acción: Generar orden de compra urgente."
            )
        }

    # 4. Caso REORDEN_URGENTE
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
                f"• Acción: Preparar orden de reposición con {producto['proveedor']}."
            )
        }

    # 5. Caso STOCK_OK
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

if __name__ == "__main__":
    print("=== PRUEBA DE TOLERANCIA A PLURALES ===")
    print("Buscando 'frijoles':", buscar_producto("frijoles", cargar_inventario())["nombre"])
    print("Buscando 'yogures':", buscar_producto("yogures", cargar_inventario())["nombre"])
    print("Buscando 'leches':", buscar_producto("leches", cargar_inventario())["nombre"])
    
    print("\n=== PRUEBA DE TARJETA CON SEMÁFORO Y FINANZAS ===")
    diag = diagnosticar_producto("yogur", "2026-11-08")
    print(diag["tarjeta_visual"])
