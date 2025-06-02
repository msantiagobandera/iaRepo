from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import hashlib


class Browser:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # quitar si quieres ver la navegación
        self.driver = webdriver.Chrome(options=options)

    def go_to(self, url):
        self.driver.get(url)

    def get_visible_text(self):
        body = self.driver.find_element(By.TAG_NAME, "body")
        return body.text

    def click_element_by_text(self, text):
        elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
        if elements:
            elements[0].click()
            return True
        return False

    def fill_input_by_placeholder(self, placeholder, value):
        try:
            input_elem = self.driver.find_element(By.XPATH, f"//input[@placeholder='{placeholder}']")
            input_elem.send_keys(value)
            return True
        except:
            return False
    
    def get_buttons_and_links(self):
        elements = self.driver.find_elements(By.XPATH, "//a | //button")
        items = []
        for el in elements:
            text = el.text.strip()
            if not text:
                # Intenta con aria-label o title
                text = el.get_attribute("aria-label") or el.get_attribute("title") or ""
                text = text.strip()
            if text:
                items.append(text)
        return items


    def get_input_fields(self):
        inputs = self.driver.find_elements(By.XPATH, "//input")
        fields = []
        for i in inputs:
            placeholder = i.get_attribute("placeholder")
            name = i.get_attribute("name")
            aria = i.get_attribute("aria-label")
            label = placeholder or aria or name
            if label:
                fields.append(label)
        return fields

    def get_url_and_title(self):
        return {
            "url": self.driver.current_url,
            "title": self.driver.title
        }

    def get_checkboxes(self):
        elements = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
        checkboxes = []
        for el in elements:
            label = self._get_label_for_element(el)
            checkboxes.append(label or "Checkbox sin label")
        return checkboxes

    def get_radio_buttons(self):
        elements = self.driver.find_elements(By.XPATH, "//input[@type='radio']")
        radios = []
        for el in elements:
            label = self._get_label_for_element(el)
            radios.append(label or "Radio button sin label")
        return radios

    def get_selects(self):
        elements = self.driver.find_elements(By.TAG_NAME, "select")
        selects = []
        for el in elements:
            name = el.get_attribute("name") or el.get_attribute("id") or "select sin nombre"
            selects.append(name)
        return selects

    def get_textareas(self):
        elements = self.driver.find_elements(By.TAG_NAME, "textarea")
        textareas = []
        for el in elements:
            placeholder = el.get_attribute("placeholder")
            name = el.get_attribute("name")
            label = placeholder or name or "textarea sin label"
            textareas.append(label)
        return textareas

    def _get_label_for_element(self, element):
        try:
            id_attr = element.get_attribute("id")
            if id_attr:
                label = self.driver.find_element(By.XPATH, f"//label[@for='{id_attr}']")
                if label and label.text.strip():
                    return label.text.strip()
            parent = element.find_element(By.XPATH, "./ancestor::label")
            if parent and parent.text.strip():
                return parent.text.strip()
        except:
            return None
        
    def select_option_by_name(self, select_name, option_text):
        from selenium.webdriver.support.ui import Select
        try:
            select_elem = None
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            for s in selects:
                name = s.get_attribute("name") or s.get_attribute("id")
                if name == select_name:
                    select_elem = Select(s)
                    break
            if not select_elem:
                return False
            select_elem.select_by_visible_text(option_text)
            return True
        except Exception as e:
            print(f"Error seleccionando opción: {e}")
            return False

        
    def quit(self):
        self.driver.quit()


    def get_dom_snapshot(self):
        # Tomamos el innerHTML del body visible para resumen
        html = self.driver.execute_script("return document.body.innerHTML;")
        # Resumir con hash para comparar rápido
        hash_digest = hashlib.md5(html.encode('utf-8')).hexdigest()
        return hash_digest

