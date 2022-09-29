 #!/usr/bin/env python

#bibliotecas
import requests
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup

class scanner:
    def __init__(self, url):
        self.url_alvo = url
        self.links_alvo = []

    def extrair_links_de(self, url):
        response = requests.get(url)
        return re.findall('(?:href=")(.*?)"', response.content.decode(errors="ignore"))

#código crawler
    def crawl(self, url=None):
        if url == None:
            url = self.url_alvo
        href_links = self.extrair_links_de(url)
        for link in href_links:
            link = urljoin(url, link)

            if "#" in link:
                link = link.splif("#")[0]

            if self.url_alvo in link and link not in self.url_alvo:
                self.links_alvo.append(link)
                print(link)
                self.crawl(link)

#extrair form da url
    def extrair_forms(self, url):
        response = requests.get(url)
        parsed_html = BeautifulSoup(response.content)
        return parsed_html.findAll("form")

#envia form para url
    def enviar_form(self, form, valor, url):
        acao = form.get("action")
        post_url = urljoin(url, acao)
        metodo = form.get("method")

        inputs_list = form.findAll("input")
        post_data = {}
        for input in inputs_list:
            nome_input = input.get("name")
            tipo_input = input.get("type")
            valor_input = input.get("value")
            if tipo_input == "text":
                valor_input = valor

            post_data[nome_input] = valor_input
        if metodo == "post":
            return requests.post(post_url, data=post_data)
        return requests.get(post_url, params=post_data)

    def rodar_scan(self):
        for link in self.links_alvo:
            forms = self.extrair_forms(link)
            for form in forms:
                print("[+] Testando form em " + link)
                vulneravel = self.xss_em_form(form, link)
                if vulneravel:
                    print("[***] XSS descoberto em " + link + "na form")
                    print(form)

            if "=" in link:
                print("[+] Testando " + link)
                vulneravel = self.xss_em_parametro(link)
                if vulneravel:
                    print("[***] XSS descoberto em "+ link)

    def xss_em_parametro(self, url):
        xss_test_script = "<script>alert('teste')</script>"
        url = url.replace("=", "=" + xss_test_script)
        response = self.session.get(url)
        return xss_test_script in response.content

    def xss_em_form(self, form, url):
        xss_test_scrip = "<script>alert('teste')</script>"
        response = self.enviar_form(form, xss_test_scrip, url)
        return xss_test_scrip in response.content
