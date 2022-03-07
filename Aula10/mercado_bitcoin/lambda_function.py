import logging
import datetime


from mercado_bitcoin.ingestors import AwsDaySummaryIngestor
from mercado_bitcoin.writers import S3Writer

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def lambda_handler(event, context):
    logger.info(f"{event}")
    logger.info(f"{context}")
    logging.info(f"event received: {event}")

    AwsDaySummaryIngestor(
        writer=S3Writer,
        coins=["BTC", "ETH", "LTC", "BCH"],
        default_start_date=datetime.date(2021, 3, 1),
    ).ingest()
