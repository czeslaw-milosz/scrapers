# Scrapy settings for otodom project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import latest_user_agents

BOT_NAME = "otodom"

SPIDER_MODULES = ["otodom.spiders"]
NEWSPIDER_MODULE = "otodom.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "otodom (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS =  {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            # "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Referer": "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/",
            # "Sec-Ch-Ua": "Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"
            # "Sec-Ch-Ua-Mobile": "?0",
            # "Sec-Ch-Ua-Platform": "Linux",
            # "Sec-Fetch-Dest": "empty",
            # "Sec-Fetch-Mode": "no-cors",
            # "Sec-Fetch-Site": "same-origin",
            # "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "otodom.middlewares.OtodomSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "otodom.middlewares.OtodomDownloaderMiddleware": 543,
#}
# DOWNLOADER_MIDDLEWARES = {
#         'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#         'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#         'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
#         'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
#     }
# FAKER_RANDOM_UA_TYPE = "edge"
# FAKEUSERAGENT_PROVIDERS = [
#     # 'scrapy_fake_useragent.providers.FakeUserAgentProvider',  # this is the first provider we'll try
#     'scrapy_fake_useragent.providers.FakerProvider',  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
#     'scrapy_fake_useragent.providers.FixedUserAgentProvider',  # fall back to USER_AGENT value
# ]
# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
USER_AGENT = latest_user_agents.get_random_user_agent()


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "otodom.pipelines.BatchDeltaExportPipeline": 300,
   "otodom.pipelines.RootImagesPipeline": 1,
   # "scrapy.pipelines.images.ImagesPipeline": 1,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 5.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# Configure export feed
# FEEDS = {
#     "s3://scrapytest/%(name)s_%(time)s.csv": {
#         "format": "csv",
#         "overwrite": True,
#     }
# }
IMAGES_STORE = f"s3://housingdatalake/images/{BOT_NAME}/"
AWS_ENDPOINT_URL = "http://minio:9000"
AWS_ACCESS_KEY_ID = "admin"
AWS_SECRET_ACCESS_KEY = "adminadmin"

# PULSAR_BATCH_SIZE = 512
# PULSAR_URL = "pulsar://localhost:6650"
# PULSAR_TOPIC = "crawl"

EXPORT_BATCH_SIZE = 512
DELTA_TABLE = f"housingdatalake/{BOT_NAME}/"

# Logging settings
# LOG_FILE = "logs/otodom.log"
LOG_ENCODING = "utf-8"

