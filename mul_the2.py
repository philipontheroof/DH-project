import pandas as pd
from konlpy.tag import Komoran
from tqdm import tqdm
import pickle
from collections import Counter

kom = Komoran()


def counter_dump_between(start, end, paper):
    for year in tqdm(range(start, end+1), position=0):
        df = pd.read_parquet(f'./data/{paper}_{year}.parquet')
        data = df.loc[:, 'body_trans']

        r = Counter()
        err_log = ''
        for text in tqdm(data, position=1):
            try:
                morphs = kom.morphs(text)
                r += Counter(morphs)
            except Exception as error:
                err_log += f'{year}\n{error}\n{text}\n------------------\n'

        with open(f'./data/komoran_counter_{year}_{paper}.pickle', 'wb') as f:
            pickle.dump(r, f)

        with open(f'./data/error_log_komoran_counter_{year}_{paper}.txt', "w") as f:
            f.write(err_log)


if __name__ == '__main__':
    counter_dump_between(1988, 1992, 'donga')
