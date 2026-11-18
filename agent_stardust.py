"""
=============================================================================
             STARDUST INVENTORY AGENT - INTEGRACIÓN WATSONX & PYTHON (V3)
                 Equipo: Stardust Crusaders | IBM Experiential Lab
=============================================================================
Mejoras integradas:
 1. Onboarding Asistido (Cuestionario inicial persistente).
 2. Semáforos visuales con emojis y cálculo de impacto financiero.
 3. Normalización y tolerancia a plurales y lenguaje coloquial.
=============================================================================
"""

import json
import os
import sys
import urllib.request
import urllib.parse
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    try:
        getattr(sys.stdout, "reconfigure")(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Importar lógica del archivo local
import inventario_logic

cargar_inventario = inventario_logic.cargar_inventario
diagnosticar_producto = inventario_logic.diagnosticar_producto
registrar_movimiento = inventario_logic.registrar_movimiento
buscar_producto = inventario_logic.buscar_producto
reporte_proactivo = inventario_logic.reporte_proactivo
cargar_configuracion = inventario_logic.cargar_configuracion
ejecutar_cuestionario_onboarding = inventario_logic.ejecutar_cuestionario_onboarding

# Configuración de tu proyecto en watsonx.ai (Dallas)
PROJECT_ID = "4c10607b-acf4-4587-9cb8-d6cde48b63d6"
URL_WATSONX = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
MODEL_ID = "ibm/granite-13b-chat-v2"

IBM_API_KEY = os.environ.get("IBM_CLOUD_API_KEY", "")

def obtener_token_iam(api_key):
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

def responder_consulta_agente(pregunta_usuario, api_key=""):
    config = cargar_configuracion() or inventario_logic.CONFIG_DEFAULT
    nombre_tienda = config.get("nombre_tienda", "Mi Tienda PYME")
    limite_compra = config.get("monto_maximo_autorizacion", 3000.0)

    # 1. Comandos de re-calibración / Onboarding
    preg_low = pregunta_usuario.lower().strip()
    if any(k in preg_low for k in ["calibrar negocio", "configurar tienda", "aplicar cuestionario", "onboarding"]):
        ejecutar_cuestionario_onboarding(interactivo=True)
        return "Configuración del negocio actualizada con éxito. Las nuevas reglas ya están vigentes."

    inventario = cargar_inventario()
    producto_detectado = buscar_producto(pregunta_usuario, inventario)

    # 2. Manejo de reportes generales
    if any(k in preg_low for k in ["alertas", "reporte", "resumen", "que falta", "caducan"]):
        alertas = reporte_proactivo()
        if not api_key:
            lineas = [f"Resumen de Alertas en {nombre_tienda} ({len(alertas)} productos requieren atención):"]
            for a in alertas:
                lineas.append(f" • [{a['codigo']}] {a['nombre']}: {a['accion']} (Stock: {a['stock_actual']})")
            return "\n".join(lineas)
        datos_contexto = f"Reporte de alertas: {json.dumps(alertas, ensure_ascii=False)}"
    elif producto_detectado:
        diag = diagnosticar_producto(producto_detectado["sku"])
        if not api_key:
            return diag.get("tarjeta_visual", f"[{diag['codigo']}] {diag['nombre']}: {diag['accion']}")
        datos_contexto = f"Datos del producto consultado: {json.dumps(diag, ensure_ascii=False)}"
    else:
        if not api_key:
            return "Producto no identificado en el almacén. Por favor menciona el nombre o SKU (ej. Leche, Yogur, Frijol)."
        datos_contexto = "No se especificó un producto específico o no existe en el catálogo."

    system_prompt = f"""Eres "Stardust Inventory Agent", empleado digital de control de inventario para la empresa "{nombre_tienda}".
Tu misión es asistir al bodeguero y al gerente basándote en la política POL-INV-2026-v1 y en la configuración del negocio:
- Límite de compra sin VoBo del dueño: ${limite_compra:,.2f} MXN.
- Presenta las respuestas como tarjetas cortas con semáforos (🟢 Óptimo, 🟡 Alerta/Reorden, 🔴 Desabasto/Caducado).
- Responde de forma concisa, cordial y fundamentada."""

    prompt_final = f"""<sistema>
{system_prompt}
</sistema>

<evidencia_datos_inventario>
{datos_contexto}
</evidencia_datos_inventario>

<consulta_usuario>
{pregunta_usuario}
</consulta_usuario>

Respuesta del Agente:"""

    try:
        return consultar_watsonx(prompt_final, api_key)
    except Exception as e:
        return f"Error al comunicar con watsonx.ai: {e}"

def consola_interactiva():
    print("=" * 65)
    print("      STARDUST INVENTORY AGENT - CONSOLA DE OPERACIÓN PYME")
    print("           IBM Experiential Learning Lab | IBM Bob")
    print("=" * 65)

    # Comprobación de Onboarding en la primera ejecución
    config = cargar_configuracion()
    if config is None or not config.get("onboarding_completado", False):
        print("\n[!] Primera ejecución detectada en este equipo.")
        print("    Iniciando el cuestionario de Onboarding para calibrar el negocio...")
        config = ejecutar_cuestionario_onboarding(interactivo=True)
    else:
        print(f"\n[✓] Negocio cargado: '{config.get('nombre_tienda', 'Mi Tienda')}'")
        print(f"    • Control de caducidades: {'Activo' if config.get('maneja_perecederos') else 'Inactivo'}")
        print(f"    • Límite de compras del gerente: ${config.get('monto_maximo_autorizacion', 3000):,.2f} MXN")

    key = IBM_API_KEY
    if not key:
        print("\n[!] No se detectó IBM_CLOUD_API_KEY configurada.")
        ingreso = input("Ingresa tu IBM Cloud API Key (o presiona ENTER para modo demo local): ").strip()
        if ingreso:
            key = ingreso

    print("\n[✓] Agente listo. Escribe tus preguntas en lenguaje natural.")
    print("    Comandos rápidos:")
    print("    - '¿Cómo andamos de yogur?'")
    print("    - 'Revisa los frijoles'")
    print("    - 'Dame el reporte de alertas de hoy'")
    print("    - 'calibrar negocio' (para volver a contestar el cuestionario)")
    print("    - 'salir' para terminar\n")

    while True:
        try:
            pregunta = input("\nBodeguero/Gerente > ").strip()
            if not pregunta:
                continue
            if pregunta.lower() in ["salir", "exit", "quit"]:
                print("Cerrando sesión del Agente. ¡Hasta pronto!")
                break
            
            print("\n[Stardust Agent procesando...]")
            respuesta = responder_consulta_agente(pregunta, key)
            print(f"\nStardust Agent:\n{respuesta}\n")
            print("-" * 65)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    consola_interactiva()
