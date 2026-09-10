# khoral scrap API

API de consulta (somente leitura) dos catálogos raspados. Base URL:

```
https://scrap.khoral.com.br
```

## Endpoints

### `GET /health`
Verifica se a API está no ar.
```bash
curl https://scrap.khoral.com.br/health
```
```json
{"status": "ok", "output_dir": "/data/saidas"}
```

### `GET /sites`
Lista os catálogos disponíveis.
```bash
curl https://scrap.khoral.com.br/sites
```
```json
["apple", "disney", "htbo", "netflix", "prime"]
```

### `GET /sites/{site}`
Retorna os itens raspados de um catálogo.

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `q` | string | — | filtra itens que contenham esse texto (qualquer campo) |
| `limit` | int | 100 | máximo de itens retornados (até 1000) |
| `offset` | int | 0 | quantos itens pular (paginação) |

```bash
curl "https://scrap.khoral.com.br/sites/netflix?limit=5"
curl "https://scrap.khoral.com.br/sites/netflix?q=fundadores"
curl "https://scrap.khoral.com.br/sites/netflix?limit=20&offset=20"
```
```json
{
  "total": 12,
  "count": 5,
  "offset": 0,
  "items": [
    {"titulo": "Netflix", "link": "/wiki/Streaming", "imagem": "...", "info_extra": "...", "_source_site": "netflix", "_source_url": "...", "_page": 1}
  ]
}
```

Site inexistente retorna `404`:
```json
{"detail": "Nenhuma raspagem encontrada para 'xyz'"}
```

## Usando via JavaScript (navegador)

```js
fetch("https://scrap.khoral.com.br/sites/netflix?limit=20")
  .then(r => r.json())
  .then(data => console.log(data.items));
```

## Atualizando os dados

Os catálogos são gerados pelo scraper (`../generic_scraper/`) e ficam salvos como `.jsonl` em `../saidas/saidas/`. Pra atualizar um catálogo:

```bash
cd /opt/scraper
scrapy crawl generic -a site=netflix -o saidas/saidas/netflix.jsonl
```

A API lê o arquivo direto a cada requisição — não precisa reiniciar o container depois de atualizar um `.jsonl`.
