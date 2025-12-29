import logging
import json
import os
import time
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Configuração de logs para não poluir o terminal, mostrando apenas INFO
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

class PriceSpy:
    def __init__(self, url, target_price):
        self.url = url
        self.target_price = target_price
        self.driver = None

    def _start_driver(self):
        print(f"🕵️  Iniciando modo espião...") # Print visual é melhor para CLI
        options = uc.ChromeOptions()
        # options.add_argument('--headless') 
        self.driver = uc.Chrome(options=options)

    def _extract_price(self):
        print(f"🌍 Acessando: {self.url}")
        self.driver.get(self.url)
        time.sleep(5) # Sites reais precisam de tempo para carregar
        
        try:
            # --- ESTRATÉGIA DE SELETORES (O Segredo do Web Scraping) ---
            # Aqui tentamos achar o preço. Na Amazon, geralmente é a classe 'a-price-whole'
            # Se for outro site, você precisará inspecionar e adicionar o seletor aqui.
            
            preco_texto = ""
            
            # Tenta seletor da Amazon
            try:
                elemento = self.driver.find_element(By.CLASS_NAME, "a-price-whole")
                preco_texto = elemento.text
            except:
                pass # Se falhar, tenta outra estratégia (pode adicionar ML, Magalu aqui depois)

            if not preco_texto:
                # Estratégia genérica de "Desespero": Tenta achar pelo símbolo R$
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
                # (Lógica simplificada para teste - em produção usariamos Regex)
                logging.warning("Seletor específico não encontrado. Retornando 0.0 para teste.")
                return 0.0

            # Limpeza do dado: transforma "1.200,00" em 1200.00
            preco_limpo = float(preco_texto.replace('.', '').replace(',', '.'))
            return preco_limpo

        except Exception as e:
            logging.error(f"❌ Erro ao extrair preço: {e}")
            return None

    def _save_data(self, preco_encontrado):
        arquivo = 'historico_precos.json'
        novo_registro = {
            'Data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Produto_URL': self.url,
            'Preco_Encontrado': preco_encontrado,
            'Target': self.target_price
        }

        dados = []
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
            except json.JSONDecodeError:
                dados = []

        dados.append(novo_registro)

        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        print("💾 Dados salvos no histórico.")

    def run(self):
        self._start_driver()
        try:
            preco = self._extract_price()
            if preco is not None:
                print(f"💲 Preço Encontrado: R$ {preco}")
                self._save_data(preco)
                
                if preco > 0 and preco <= self.target_price:
                    print("\n" + "="*40)
                    print(f"🚨 ALERTA DE OFERTA! O PREÇO BAIXOU PARA R$ {preco}!")
                    print("="*40 + "\n")
                else:
                    print(f"📉 Ainda não. Meta: R$ {self.target_price} | Atual: R$ {preco}")
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except OSError:
                    pass # Ignora o erro do Windows "WinError 6"
                print("🔒 Navegador fechado.")

# --- INTERFACE DE USUÁRIO (CLI) ---
if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa o terminal
    print("="*40)
    print("      🕵️‍♂️  PRICE SPY BOT v2.0  🕵️‍♂️")
    print("="*40)
    
    # Aqui está a mágica: Input do usuário
    user_url = input("🔗 Cole a URL do produto (Amazon): ").strip()
    
    while True:
        try:
            user_target = float(input("💰 Qual seu preço alvo (ex: 100.00)? "))
            break
        except ValueError:
            print("❌ Por favor, digite um número válido (use ponto para centavos).")

    if not user_url:
        print("URL vazia. Usando Google para teste.")
        user_url = 'https://www.google.com'

    bot = PriceSpy(user_url, user_target)
    bot.run()