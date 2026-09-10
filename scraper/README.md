# generic_scraper

Scraper Scrapy genérico: uma única spider (`generic`), dirigida por
arquivos de configuração YAML — um por site. Para raspar um novo site
você não escreve código, só adiciona um arquivo `sites/<nome>.yaml`
descrevendo o "fluxo": seletor do card, campos, seletor de paginação.

## Instalação

```bash
cd scraper
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Adicionando um site

1. Copie `generic_scraper/sites/_template.yaml` para `generic_scraper/sites/<nome>.yaml`.
2. Preencha `allowed_domains`, `start_urls`, `item_selector` (seletor CSS
   de cada card na listagem), `fields` (o que extrair de dentro de cada
   card) e `pagination_selector` (link "próxima página").
3. Antes de rodar: confira o `robots.txt` e os Termos de Uso do site.
   Só adicione sites que você tem direito de raspar.

Formato de `fields`: cada campo é uma string (seletor CSS relativo ao
item) ou um dict `{selector, multiple, strip, join_with}`. Veja
`sites/_template.yaml` e `sites/example_books.yaml` para exemplos.

## Rodando

```bash
scrapy crawl generic -a site=example_books -o saida.jsonl
```

A spider segue a paginação (`pagination_selector`) automaticamente até
ela sumir da página, ou até `max_pages` (definido na config ou via
`-a max_pages=N`).

Cada item extraído sai com três campos extras: `_source_site`,
`_source_url` e `_page`.

## Configuração de rede

`generic_scraper/settings.py` já vem com `ROBOTSTXT_OBEY = True`,
`AUTOTHROTTLE` ligado e um `DOWNLOAD_DELAY` de 1s por padrão — desative
essas proteções só se souber exatamente o que está fazendo e tiver
permissão para isso no site em questão.
