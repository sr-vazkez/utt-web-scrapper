import argparse
import lodding

lodding.basicConfig(level = logging.INFO)

from common import config

logger = logging.getLogger(__name__)

def _news_scraper(news_site_uid):
    host = config()['new_sites'][news_site_uid]['url']

    lodding.info(f'Iniciando el scrape for {host}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
else:
    pass