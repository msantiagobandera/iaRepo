import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY", "")

def analyze(context, objective, memory=None):
    memory_text = ""
    if memory:
        memory_text = "\nHistorial de acciones previas:\n" + json.dumps(memory, indent=2)
    else:
        memory_text = "\nNo hay historial previo."

    prompt = f"""
Eres un agente inteligente de navegación web. Tu objetivo es: **{objective}**.

Aquí tienes la información actual de la página:

🌐 URL: {context['meta']['url']}
📄 Título: {context['meta']['title']}

📘 Texto visible:
{context['text'][:1000]}

🔘 Botones y enlaces visibles:
{json.dumps(context['buttons'], indent=2)}

📝 Campos de formulario detectados:
{json.dumps(context['inputs'], indent=2)}

☑️ Checkboxes:
{json.dumps(context['checkboxes'], indent=2)}

🔘 Radio buttons:
{json.dumps(context['radio_buttons'], indent=2)}

📋 Selects (desplegables):
{json.dumps(context['selects'], indent=2)}

📝 Textareas:
{json.dumps(context['textareas'], indent=2)}

{memory_text}

Decide qué acción tomar para avanzar hacia el objetivo. Responde en JSON así:

{{
  "action": "click" | "fill" | "check" | "select" | "none",
  "target": "texto del botón o enlace",
  "placeholder": "texto del campo a rellenar",
  "value": "texto a escribir o seleccionar"
}}

Si no puedes hacer nada más útil, responde con: {{"action": "none"}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un agente de navegación web que actúa en función de un objetivo y memoria."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    try:
        return json.loads(response.choices[0].message["content"])
    except Exception as e:
        print("⚠️ Error procesando la respuesta de la IA:", e)
        return {"action": "none"}
