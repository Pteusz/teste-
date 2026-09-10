from pathlib import Path

import scrapy
import yaml

SITES_DIR = Path(__file__).resolve().parent.parent / "sites"


def load_site_config(site_name):
    path = SITES_DIR / f"{site_name}.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"Nenhuma configuração encontrada em {path}. "
            f"Crie um arquivo sites/{site_name}.yaml (veja sites/_template.yaml)."
        )
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_field(selector_scope, field_config):
    """Extrai um campo a partir de um seletor CSS relativo ao item.

    field_config pode ser só uma string (seletor CSS) ou um dict com:
      selector: str (obrigatório)
      multiple: bool  -> retorna lista em vez de valor único (default False)
      strip: bool     -> remove espaços nas pontas (default True)
      join_with: str  -> junta múltiplos textos quando multiple=False (default " ")
    """
    if isinstance(field_config, str):
        field_config = {"selector": field_config}

    css = field_config["selector"]
    multiple = field_config.get("multiple", False)
    strip = field_config.get("strip", True)
    join_with = field_config.get("join_with", " ")

    values = selector_scope.css(css).getall()
    if strip:
        values = [v.strip() for v in values if v and v.strip()]

    if multiple:
        return values
    if not values:
        return None
    return join_with.join(values) if len(values) > 1 else values[0]


class GenericSpider(scrapy.Spider):
    """Spider dirigida por configuração: uma spider, N sites.

    Uso:
        scrapy crawl generic -a site=example_books -o saida.jsonl

    Cada site é um arquivo YAML em generic_scraper/sites/<site>.yaml
    descrevendo o seletor do card do item, os campos a extrair e o
    seletor de paginação. Ver sites/_template.yaml para o formato.
    """

    name = "generic"

    def __init__(self, site=None, max_pages=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not site:
            raise ValueError(
                "Passe -a site=<nome> apontando para generic_scraper/sites/<nome>.yaml"
            )

        config = load_site_config(site)
        self.site_name = config.get("name", site)
        self.allowed_domains = config.get("allowed_domains", [])
        self.start_urls = config["start_urls"]
        self.item_selector = config["item_selector"]
        self.fields = config["fields"]
        self.pagination_selector = config.get("pagination_selector")

        # -a max_pages=N na linha de comando sobrepõe o valor da config.
        configured_limit = config.get("max_pages", 0)
        self.max_pages = int(max_pages) if max_pages is not None else configured_limit

    def parse(self, response, page=1):
        for item_sel in response.css(self.item_selector):
            data = {
                field_name: extract_field(item_sel, field_cfg)
                for field_name, field_cfg in self.fields.items()
            }
            data["_source_site"] = self.site_name
            data["_source_url"] = response.url
            data["_page"] = page
            yield data

        if self.max_pages and page >= self.max_pages:
            return

        if not self.pagination_selector:
            return

        next_page = response.css(self.pagination_selector).get()
        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                cb_kwargs={"page": page + 1},
            )
