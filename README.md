# 🕵️‍♂️ PriceSpy - Monitoramento de Preços com Anti-Detecção

O **PriceSpy** é um bot de automação inteligente que monitora preços em lojas online (como Amazon, Mercado Livre), utilizando técnicas de anti-detecção para evitar bloqueios e garantir dados precisos.

## 🚀 Funcionalidades
* **Anti-Detecção:** Usa `undetected_chromedriver` para navegar como um humano.
* **Histórico em JSON:** Salva todos os preços encontrados em `historico_precos.json`.
* **Sistema de Alerta:** Identifica quando o preço atinge seu alvo desejado.
* **Arquitetura Robusta:** Código modular orientado a objetos (POO) e Logs detalhados.

## 🛠️ Tecnologias Utilizadas
* Python 3.x
* Selenium WebDriver
* Undetected Chromedriver

## 📦 Como Instalar

1.  Clone este repositório:
    ```bash
    git clone [https://github.com/nytstalk/price-spy-bot.git](https://github.com/nytstalk/price-spy-bot.git)
    ```
2.  Instale as dependências:
    ```bash
    pip install selenium undetected-chromedriver
    ```

## 🤖 Como Usar

1.  Abra o terminal na pasta do projeto.
2.  Execute o bot:
    ```bash
    python price_spy.py
    ```
3.  O navegador abrirá, verificará o preço e salvará o resultado no arquivo de histórico.

---
Desenvolvido com 💜 e Python.