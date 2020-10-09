import argparse
import logging
logging.basicConfig(level=logging.INFO)
from urllib.parse import urlparse

import pandas as pd

logger = logging.getLogger(__name__)

def main(filename):
    logger.info('Empezando el proseso de limpiado')

    df = _read_data(filename)
    newspaper_uid = _extract_newspaper_uid(filename)
    df = _add_newspaper_uid_column(df, newspaper_uid) 
    df = _extract_host(df)

    return df

def _read_data(filename):
    logger.info('Leyendo el archivo {}'.format(filename))
    return pd.read_csv(filename)

def _extract_newspaper_uid(filename):
    logger.info('Extrayendo el newspaper uid')
    newspaper_uid = filename.split('_')[0]

    logger.info('Newspaper uid detectado: {}'.format(newspaper_uid))
    return newspaper_uid 

def _add_newspaper_uid_column(df, newspaper_uid):
    logger.info('LLenando la columna newspaper_uid con {}'.format(newspaper_uid))
    df['newspaper_uid'] = newspaper_uid

    return df

def _extract_host(df):
    logger.info('Extrayendo el host de las urls')
    df['host'] = df['url'].apply(lambda url: urlparse(url).netloc)
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',help='La raiz de los datos sucios', type=str)

    args = parser.parse_args()
    df = main(args.filename) 

    print(df)