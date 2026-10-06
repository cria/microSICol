#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza as traduções do microSICol (Windows-friendly, sem gettext/apt).

Faz todo o pipeline em Python puro usando Babel:
  1. Extrai as strings _( ... ) dos arquivos listados em po/POTFILES.in  -> po/sicol.pot
  2. Mescla as strings novas em cada .po (preserva o que já foi traduzido)
  3. Compila cada .po em seu .mo (po/<lang>/LC_MESSAGES/sicol.mo)

Depois disso, os arquivos js/js_i18n/translation_*.js se regeneram sozinhos
no proximo carregamento de pagina (o .mo fica mais novo que o .js).

Pre-requisito (uma vez):
    pip install babel

Uso (a partir de qualquer lugar):
    python po\\update_translations.py
"""

import os
import sys

try:
    from babel.messages.catalog import Catalog
    from babel.messages.extract import extract_from_file
    from babel.messages.pofile import read_po, write_po
    from babel.messages.mofile import write_mo
except ImportError:
    sys.exit("Babel nao encontrado. Rode:  pip install babel")

# Raiz do projeto = pasta pai deste script (po/..)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POT = os.path.join(ROOT, "po", "sicol.pot")

# Mapeia lang_code -> (arquivo .po de origem, arquivo .mo de destino)
LOCALES = {
    "pt_BR": (os.path.join(ROOT, "po", "pt_BR.po"),
              os.path.join(ROOT, "po", "pt_BR", "LC_MESSAGES", "sicol.mo")),
    "en":    (os.path.join(ROOT, "po", "en.po"),
              os.path.join(ROOT, "po", "en", "LC_MESSAGES", "sicol.mo")),
}


def build_template():
    """Extrai as strings dos arquivos do POTFILES.in para um catalogo template."""
    potfiles = os.path.join(ROOT, "po", "POTFILES.in")
    with open(potfiles, encoding="utf-8") as f:
        rel_paths = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]

    template = Catalog()
    scanned = 0
    for rel in rel_paths:
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.exists(path):
            print("  (aviso) nao encontrado, pulando: %s" % rel)
            continue
        method = "python" if rel.endswith(".py") else "javascript"
        for lineno, message, comments, context in extract_from_file(method, path):
            template.add(message, locations=[(rel, lineno)],
                         auto_comments=comments, context=context)
        scanned += 1

    with open(POT, "wb") as f:
        write_po(f, template, omit_header=False)
    print("1) Extraidas %d mensagens de %d arquivos -> po/sicol.pot"
          % (len(template), scanned))
    return template


def update_locale(lang, po_path, mo_path, template):
    if not os.path.exists(po_path):
        print("  (aviso) %s nao existe, pulando %s" % (po_path, lang))
        return
    with open(po_path, "rb") as f:
        catalog = read_po(f, locale=lang, domain="sicol")

    catalog.update(template)  # equivalente ao msgmerge

    with open(po_path, "wb") as f:
        write_po(f, catalog)

    os.makedirs(os.path.dirname(mo_path), exist_ok=True)
    with open(mo_path, "wb") as f:
        write_mo(f, catalog, use_fuzzy=False)

    faltando = [m.id for m in catalog if m.id and not m.string and not m.fuzzy]
    print("2/3) %s: %d entradas, %d SEM traducao" % (lang, len(catalog), len(faltando)))
    for mid in faltando[:40]:
        print("       - %s" % (mid if isinstance(mid, str) else mid[0]))
    if len(faltando) > 40:
        print("       ... (+%d)" % (len(faltando) - 40))


def main():
    print("Atualizando traducoes em: %s" % ROOT)
    template = build_template()
    for lang, (po_path, mo_path) in LOCALES.items():
        update_locale(lang, po_path, mo_path, template)
    print("\nPronto. Edite os .po para preencher o que estiver SEM traducao,")
    print("rode este script de novo para recompilar, e recarregue a pagina.")


if __name__ == "__main__":
    main()
