# Define your item pipelines here
#
# Don"t forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from dataclasses import asdict

import polars as pl
from scrapy.exporters import PythonItemExporter

# class BatchPulsarExportPipeline:
#     def __init__(self, batch_size=128, pulsar_url="pulsar://localhost:6650", topic="default_topic"):
#         self.batch_size = batch_size
#         self.pulsar_url = pulsar_url
#         self.topic = topic
#         self.batch_items = []
#         self.exporter = PythonItemExporter()

#     @classmethod
#     def from_crawler(cls, crawler):
#         settings = crawler.settings
#         batch_size = settings.getint("BATCH_SIZE", 128)
#         pulsar_url = settings.get("PULSAR_URL", "pulsar://localhost:6650")
#         topic = settings.get("PULSAR_TOPIC", "default_topic")
#         return cls(batch_size=batch_size, pulsar_url=pulsar_url, topic=topic)

#     def open_spider(self, spider):
#         """ on spider open, create pulsar client and producer and initialize scrapy exporter. """
#         self.client = pulsar.Client(self.pulsar_url)
#         self.producer = self.client.create_producer(self.topic, block_if_queue_full=True)

#     def close_spider(self, spider):
#         """ on spider close, export remaining items and close pulsar producer. """
#         if self.batch_items:
#             self.export_batch()
#         self.client.close()

#     def process_item(self, item, spider):
#         """ Process items in batches (export only when batch is full). """
#         self.batch_items.append(item)
#         if len(self.batch_items) >= self.batch_size:
#             self.export_batch()
#         return item

#     def export_batch(self):
#         if self.batch_items:
#             logging.info(f"Exporting batch of type {type(self.batch_items[0])} of {len(self.batch_items)} items")
#             df = pd.DataFrame(self.batch_items)
#             logging.info(df.head())
#             self.producer.send(df.to_csv().encode("utf-8"))
#             self.batch_items = []


class BatchDeltaExportPipeline:
    def __init__(self, batch_size, delta_endpoint, delta_table, delta_id, delta_key):
        self.batch_size = batch_size
        self.delta_endpoint = delta_endpoint
        self.delta_table = delta_table
        self.delta_id = delta_id
        self.delta_key = delta_key
        self.batch_items = []
        self.exporter = PythonItemExporter()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        batch_size = settings.getint("EXPORT_BATCH_SIZE")
        delta_endpoint = settings.get("AWS_ENDPOINT_URL")
        delta_table = settings.get("DELTA_TABLE")
        delta_id = settings.get("AWS_ACCESS_KEY_ID")
        delta_key = settings.get("AWS_SECRET_ACCESS_KEY")
        return cls(batch_size=batch_size, delta_endpoint=delta_endpoint,
                    delta_table=delta_table, delta_id=delta_id, delta_key=delta_key)

    def open_spider(self, spider):
        """ on spider open, create pulsar client and producer and initialize scrapy exporter. """
        pass

    def close_spider(self, spider):
        """ on spider close, export remaining items and close pulsar producer. """
        if self.batch_items:
            self.export_batch()

    def process_item(self, item, spider):
        """ Process items in batches (export only when batch is full). """
        self.batch_items.append(asdict(item))
        if len(self.batch_items) >= self.batch_size:
            self.export_batch()
        return item

    def export_batch(self):
        if self.batch_items:
            df = pl.DataFrame(self.batch_items)
            df.write_delta(
                target=f"s3://{self.delta_table}",
                mode="append",
                overwrite_schema=True,
                storage_options={
                    "AWS_ENDPOINT_URL": self.delta_endpoint,
                    "AWS_ACCESS_KEY_ID": self.delta_id,
                    "AWS_SECRET_ACCESS_KEY": self.delta_key,
                    "AWS_REGION": "us-east-1",
                    "AWS_ALLOW_HTTP": "true",
                    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
                    },
            )
            self.batch_items = []
