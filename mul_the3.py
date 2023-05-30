import pandas as pd
from konlpy.tag import Komoran
from tqdm import tqdm
import pickle
from collections import Counter

kom = Komoran()


def counter_dump_between(start, end, paper):
    for year in tqdm(range(start, end+1), position=0):
        df = pd.read_parquet(f'./data/{paper}_1980.parquet')
        data = df.loc[:, 'body_archaic_hangul']

        r = Counter()
        err_log = ''
        for text in tqdm(data, position=1):
            try:
                morphs = kom.morphs(text)
                r += Counter(morphs)
            except Exception as error:
                err_log += f'{year}\n{error}\n{text}\n------------------\n'

        with open(f'./data/komoran_counter_{year}.pickle', 'wb') as f:
            pickle.dump(r, f)

        with open(f'./data/error_log_komoran_counter_{year}.txt', "w") as f:
            f.write(err_log)


if __name__ == '__main__':
    counter_dump_between(1980, 1989, 'donga')
