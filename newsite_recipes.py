import argparse
import hashlib
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
    df = _fill_mising_titles(df) 
    df = _generate_uids_for_rows(df)
    df = _remove_new_lines_from_body(df)
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

def _fill_mising_titles(df):
    logger.info('Generando uids para cada columna')
    uids = (df
                .apply(lambda row: hashlib.md5(bytes(row['url'].encode())), axis=1)
                .apply(lambda hash_object: hash_object.hexdigest())
            )
    df['uid'] = uids
    return df.set_index('uid')

def _generate_uids_for_rows(df):
    logger.info('Removiendo nuevas lineas del cuerpo')

    stripped_body = (
        df
        .apply(lambda row: row['body'], axis=1)
        .apply(lambda body: list(body))
        .apply(lambda letters: list(map(lambda letter: letter.replace('\n',' '),letters)))
        .apply(lambda letters: ''.join(letters))
    )
    df['body'] = stripped_body
    return 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',help='La raiz de los datos sucios', type=str)

    args = parser.parse_args()
    df = main(args.filename) 

    print(df)