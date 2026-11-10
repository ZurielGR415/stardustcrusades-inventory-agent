"""
=============================================================================
             STARDUST INVENTORY AGENT - INTEGRACIÓN WATSONX & PYTHON
                 Equipo: Stardust Crusaders | IBM Experiential Lab
=============================================================================
Este script une:
  1. Base de datos local (inventario_pyme.json).
  2. Motor de diagnóstico y reglas de negocio (inventario_logic.py).
  3. API de watsonx.ai (IBM Granite) para formulación en lenguaje natural.
=============================================================================
"""

import json
import os
import sys
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import urllib.request
import urllib.parse
from datetime import date

# Importar lógica del archivo local
import inventario_logic

cargar_inventario = inventario_logic.cargar_inventario
diagnosticar_producto = inventario_logic.diagnosticar_producto
registrar_movimiento = inventario_logic.registrar_movimiento
buscar_producto = inventario_logic.buscar_producto

# Soporte para reporte_proactivo o reporte_general_alertas
if hasattr(inventario_logic, "reporte_proactivo"):
    obtener_alertas = inventario_logic.reporte_proactivo
elif hasattr(inventario_logic, "reporte_general_alertas"):
    obtener_alertas = inventario_logic.reporte_general_alertas
else:
    obtener_alertas = lambda: []

# Configuración de tu proyecto en watsonx.ai (Dallas)
PROJECT_ID = "4c10607b-acf4-4587-9cb8-d6cde48b63d6"
URL_WATSONX = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
MODEL_ID = "ibm/granite-13b-chat-v2"

# Variable de entorno opcional
IBM_API_KEY = os.environ.get("IBM_CLOUD_API_KEY", "")

def obtener_token_iam(api_key):
    """Genera token de acceso temporal mediante IBM Cloud IAM."""
    url = "https://iam.cloud.ibm.com/identity/token"
    data = urllib.parse.urlencode({
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    })
    
    with urllib.request.urlopen(req) as resp:
        res_json = json.loads(resp.read().decode("utf-8"))
        return res_json["access_token"]

def consultar_watsonx(prompt_completo, api_key):
    """Llama a la API de inferencia de watsonx.ai."""
    token = obtener_token_iam(api_key)
    
    payload = {
        "input": prompt_completo,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 300,
            "min_new_tokens": 1,
            "repetition_penalty": 1.1
        },
        "model_id": MODEL_ID,
        "project_id": PROJECT_ID
    }
    
    req = urllib.request.Request(URL_WATSONX, data=json.dumps(payload).encode("utf-8"), headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["results"][0]["generated_text"].strip()

SYSTEM_PROMPT = """Eres "Stardust Inventory Agent", empleado digital de control de inventario para una PYME comercial.
Tu misión es asistir al bodeguero y al gerente basándote en la política POL-INV-2026-v1.

Reglas:
- MERMA_RIESGO: Recomienda aplicar etiqueta amarilla (25% descuento) y exhibir al frente (regla PEPS).
- CADUCADO: Retiro inmediato de anaquel, prohibida su venta y registrar merma.
- REORDEN_URGENTE: Sugiere orden de compra preventiva calculando las unidades requeridas.
- DESABASTO_TOTAL: Alerta prioritaria a Gerencia.
- GOBERNANZA: Montos superiores a $3,000 MXN requieren VoBo del Dueño/Gerente.
Responde de forma concisa, cordial y fundamentada en los datos."""

def responder_consulta_agente(pregunta_usuario, api_key=""):
    inventario = cargar_inventario()
    
    # Identificar producto mencionado de forma flexible (SKU o palabras clave del nombre)
    producto_detectado = None
    pregunta_low = pregunta_usuario.lower()
    
    # 1. Búsqueda exacta por SKU
    for p in inventario:
        if p["sku"].lower() in pregunta_low:
            producto_detectado = p
            break
            
    # 2. Búsqueda por palabras clave del nombre (ej. 'yogur', 'leche', 'frijol', 'aceite')
    if not producto_detectado:
        for p in inventario:
            palabras = [w for w in p["nombre"].lower().split() if len(w) > 3]
            for palabra in palabras:
                if palabra in pregunta_low:
                    producto_detectado = p
                    break
            if producto_detectado:
                break
            
    # Manejar consultas de reporte o productos individuales
    if any(k in pregunta_usuario.lower() for k in ["alertas", "reporte", "resumen", "que falta", "caducan"]):
        alertas = obtener_alertas()
        datos_contexto = f"Reporte general de alertas: {json.dumps(alertas, ensure_ascii=False)}"
    elif producto_detectado:
        diag = diagnosticar_producto(producto_detectado["sku"])
        datos_contexto = f"Datos del producto consultado: {json.dumps(diag, ensure_ascii=False)}"
    else:
        datos_contexto = "No se especificó un producto específico o no existe en el catálogo."

    prompt_final = f"""<sistema>
{SYSTEM_PROMPT}
</sistema>

<evidencia_datos_inventario>
{datos_contexto}
</evidencia_datos_inventario>

<consulta_usuario>
{pregunta_usuario}
</consulta_usuario>

Respuesta del Agente:"""

    if not api_key:
        print("\n[MODO DEMO LOCAL - Sin API Key de watsonx]")
        if any(k in pregunta_usuario.lower() for k in ["alertas", "reporte", "resumen", "que falta", "caducan"]):
            alertas = obtener_alertas()
            lineas = [f"Resumen de Alertas en Almacén ({len(alertas)} productos requieren atención):"]
            for a in alertas:
                lineas.append(f" • [{a['codigo']}] {a['nombre']}: {a['accion']} (Stock: {a['stock_actual']})")
            return "\n".join(lineas)
        elif producto_detectado:
            diag = diagnosticar_producto(producto_detectado["sku"])
            return diag.get("tarjeta_visual", f"[{diag['codigo']}] {diag['nombre']}: {diag['accion']}")
        else:
            return "Producto no identificado en el almacén. Por favor menciona el nombre o SKU (ej. Leche, Yogur, Frijol)."
    
    try:
        return consultar_watsonx(prompt_final, api_key)
    except Exception as e:
        return f"Error al comunicar con watsonx.ai: {e}"

def consola_interactiva():
    print("=" * 65)
    print("      STARDUST INVENTORY AGENT - CONSOLA DE OPERACIÓN PYME")
    print("           IBM Experiential Learning Lab | IBM Bob")
    print("=" * 65)
    
    key = IBM_API_KEY
    if not key:
        print("\n[!] No se detectó IBM_CLOUD_API_KEY configurada.")
        ingreso = input("Ingresa tu IBM Cloud API Key (o presiona ENTER para modo demo local): ").strip()
        if ingreso:
            key = ingreso

    print("\n[✓] Agente conectado. Escribe tus preguntas en lenguaje natural.")
    print("    Ejemplos:")
    print("    - '¿Cómo andamos de yogur de fresa?'")
    print("    - 'Revisa el frijol negro'")
    print("    - 'Dame el reporte de alertas de hoy'")
    print("    - 'salir' para terminar\n")

    while True:
        try:
            pregunta = input("\nBodeguero/Gerente > ").strip()
            if not pregunta:
                continue
            if pregunta.lower() in ["salir", "exit", "quit"]:
                print("Cerrando sesión del Agente. ¡Hasta luego!")
                break
            
            print("\n[Stardust Agent consultando con watsonx...]")
            respuesta = responder_consulta_agente(pregunta, key)
            print(f"\nStardust Agent:\n{respuesta}\n")
            print("-" * 65)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    consola_interactiva()
