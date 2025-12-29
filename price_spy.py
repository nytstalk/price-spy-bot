import logging
import json
import os
import time
from datetime import datetime
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# Configuração básica de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PriceSpy:
    def __init__(self, url, target_price):
        self.url = url
        self.target_price = target_price
        self.driver = None

    def _start_driver(self):
        logging.info("Iniciando o navegador...")
        options = uc.ChromeOptions()
        # options.add_argument('--headless') # Descomente para rodar sem ver a janela
        self.driver = uc.Chrome(options=options)

    def _extract_price(self):
        # LÓGICA PLACEHOLDER - Aqui você vai ajustar o seletor dependendo do site (Amazon, ML, etc)
        logging.info(f"Acessando {self.url}")
        self.driver.get(self.url)
        time.sleep(3) # Espera carregar
        
        try:
            # Exemplo genérico: tenta achar qualquer preço (você terá que ajustar isso depois)
            # Para Amazon seria algo como: self.driver.find_element(By.CLASS_NAME, "a-price-whole")
            return 0.0 # Retornando 0.0 só para o teste não quebrar
        except Exception as e:
            logging.error(f"Erro ao extrair preço: {e}")
            return None

    def _save_data(self, preco_encontrado):
        arquivo = 'historico_precos.json'
        novo_registro = {
            'Data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Produto_URL': self.url,
            'Preco_Encontrado': preco_encontrado,
            'Target': self.target_price
        }

        # Lógica robusta para criar o arquivo se não existir
        dados = []
        if os.path.exists(arquivo):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
            except json.JSONDecodeError:
                dados = [] # Se o arquivo estiver corrompido, começa do zero

        dados.append(novo_registro)

        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        logging.info("Dados salvos no histórico com sucesso.")

    def run(self):
        self._start_driver()
        try:
            preco = self._extract_price()
            if preco is not None:
                self._save_data(preco)
                if preco <= self.target_price:
                    logging.info("ALERTA: Preço alvo atingido!")
                else:
                    logging.info(f"Preço atual ({preco}) ainda está acima do alvo ({self.target_price})")
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Navegador fechado.")

if __name__ == '__main__':
    # Teste com uma URL qualquer
    bot = PriceSpy('https://www.google.com', 100.00)
    bot.run()