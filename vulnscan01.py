#!/usr/bin/env python

import scanner

#especificar url do alvo
url_alvo = ""

vulnscan = scanner.scanner(url_alvo)

forms = vulnscan.extrair_forms(url_alvo)
response = vulnscan.xss_em_form(forms[0], "testtest", url_alvo)
print(response.content)