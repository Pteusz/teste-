BOT_NAME = "generic_scraper"

SPIDER_MODULES = ["generic_scraper.spiders"]
NEWSPIDER_MODULE = "generic_scraper.spiders"

# Respeita robots.txt por padrão. Só desative para sites onde você tem
# permissão explícita para raspar — não é um interruptor de conveniência.
ROBOTSTXT_OBEY = True

USER_AGENT = "generic_scraper (contato: defina-um-email-real-aqui)"

# Rate limiting educado por padrão.
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

CONCURRENT_REQUESTS = 8
CONCURRENT_REQUESTS_PER_DOMAIN = 4

FEED_EXPORT_ENCODING = "utf-8"
