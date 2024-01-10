# Define your item pipelines here
#
# Don"t forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pandas as pd
import pulsar
from scrapy.exporters import PythonItemExporter

class BatchPulsarExportPipeline:
    def __init__(self, batch_size=128, pulsar_url="pulsar://localhost:6650", topic="default_topic"):
        self.batch_size = batch_size
        self.pulsar_url = pulsar_url
        self.topic = topic
        self.batch_items = []
        self.exporter = PythonItemExporter()

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        batch_size = settings.getint("BATCH_SIZE", 128)
        pulsar_url = settings.get("PULSAR_URL", "pulsar://localhost:6650")
        topic = settings.get("PULSAR_TOPIC", "default_topic")
        return cls(batch_size=batch_size, pulsar_url=pulsar_url, topic=topic)

    def open_spider(self, spider):
        """ on spider open, create pulsar client and producer and initialize scrapy exporter. """
        self.client = pulsar.Client(self.pulsar_url)
        self.producer = self.client.create_producer(self.topic, block_if_queue_full=True)

    def close_spider(self, spider):
        """ on spider close, export remaining items and close pulsar producer. """
        if self.batch_items:
            self.export_batch()
        self.client.close()

    def process_item(self, item, spider):
        """ Process items in batches (export only when batch is full). """
        self.batch_items.append(item)
        if len(self.batch_items) >= self.batch_size:
            self.export_batch()
        return item

    def export_batch(self):
        if self.batch_items:
            logging.info(f"Exporting batch of type {type(self.batch_items[0])} of {len(self.batch_items)} items")
            df = pd.DataFrame(self.batch_items)
            logging.info(df.head())
            self.producer.send(df.to_csv().encode("utf-8"))
            self.batch_items = []
