from browser import Browser
from analyzer import analyze
import time

MAX_STEPS = 5

def main():
    objective = input("🎯 Escribe el objetivo del agente: ").strip()
    if not objective:
        objective = "Navegar la página"
    print(f"[🎯 OBJETIVO]: {objective}")

    browser = Browser()
    browser.go_to("https://example.com")

    memory = []  # Aquí guardamos las acciones realizadas
    previous_snapshot = None

    for step in range(MAX_STEPS):
        print(f"\n[🔁 PASO {step + 1}]")

        snapshot = browser.get_dom_snapshot()

        if previous_snapshot and snapshot != previous_snapshot:
            print("[⚠️ DETECTADO CAMBIO EN DOM]")
            time.sleep(2)  # Esperar que termine carga dinámica

        previous_snapshot = snapshot

        context = {
            "text": browser.get_visible_text(),
            "buttons": browser.get_buttons_and_links(),
            "inputs": browser.get_input_fields(),
            "checkboxes": browser.get_checkboxes(),
            "radio_buttons": browser.get_radio_buttons(),
            "selects": browser.get_selects(),
            "textareas": browser.get_textareas(),
            "meta": browser.get_url_and_title()
        }

        decision = analyze(context, objective, memory)
        print("[🤖 DECISIÓN IA]:", decision)

        if decision["action"] == "click":
            success = browser.click_element_by_text(decision["target"])
            action_result = "✅ OK" if success else "❌ FALLÓ"
            print(f"[🖱️ Click]: {action_result}")
            memory.append({"action": "click", "target": decision["target"], "result": action_result})

        elif decision["action"] == "fill":
            success = browser.fill_input_by_placeholder(decision["placeholder"], decision["value"])
            action_result = "✅ OK" if success else "❌ FALLÓ"
            print(f"[📝 Formulario]: {action_result}")
            memory.append({"action": "fill", "placeholder": decision["placeholder"], "value": decision["value"], "result": action_result})

        elif decision["action"] == "check":
            success = browser.click_element_by_text(decision["target"])  # Usamos click para checkbox/radio
            action_result = "✅ OK" if success else "❌ FALLÓ"
            print(f"[☑️ Check]: {action_result}")
            memory.append({"action": "check", "target": decision["target"], "result": action_result})

        elif decision["action"] == "select":
            success = browser.select_option_by_name(decision["placeholder"], decision["value"])
            action_result = "✅ OK" if success else "❌ FALLÓ"
            print(f"[📋 Select]: {action_result}")
            memory.append({"action": "select", "placeholder": decision["placeholder"], "value": decision["value"], "result": action_result})

        elif decision["action"] == "none":
            print("[✅ Acción]: Ninguna acción tomada. Finalizando...")
            break

        else:
            print("[⚠️ Acción]: Desconocida. Finalizando...")
            break

    browser.quit()

if __name__ == "__main__":
    main()
