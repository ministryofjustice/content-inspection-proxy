import logging
from logstash_formatter import LogstashFormatter


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = LogstashFormatter()


handler.setFormatter(formatter)
logger.addHandler(handler)

logger.setLevel('DEBUG')


def main():
    account = 'foo."bar".baz'
    logger.info({"account": 123, "ip": "172.20.19.18"})
    logger.info("classic message for account: %s", account, extra={"account": account})

    account = "foo.'bar'.baz"
    logger.info("classic message for account: %s", account, extra={"account": account})

    try:
        h = {}
        h['key']
    except:
        logger.info("something unexpected happened", exc_info=True)

if __name__ == '__main__':
    main()
