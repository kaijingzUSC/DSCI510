import sys
import os
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm


# utility functions used for general purpose of this program

def load_json(path):
    """ Load a json file. 
    Params: path: str, json file path.
    Returns: python objects (usually dictionaries)
    """
    if not os.path.exists(path):  # when no file found
        print(f"Invalid path: {path} ")
        sys.exit()
    with open(path, 'r') as f:
        return json.load(f)


def save_json(data, path):
    """ Save json file. 
    Params:
        data: python objects. 
        path: str, json file path.
    """
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'w') as f:  # enable Chinese and indention
        json.dump(data, f, ensure_ascii=False, indent=4)


def convert_pos(pos):
    """ Convert Chinese positions to English. """
    if pos == '上单':
        return 'TOP'
    elif pos == '打野':
        return 'JUG'
    elif pos == '中单':
        return 'MID'
    elif pos == '辅助':
        return 'SUP'
    elif pos == 'ADC':
        return 'BOT'
    print("Wrong position name. ")
    sys.exit()


def get_float(data):
    """ Return float value of input data. """
    if type(data) is float:
        return data
    elif type(data) is str:
        if '%' in data:
            return float(data[:-1]) / 100
        elif ':' in data:
            mins, secs = tuple(data.split(':'))
            return float(mins) * 60 + float(secs)
        else:
            return float(data) 
    print(f"Wrong data type: {type(data)} ")
    sys.exit()


def get_champion(c_key=None, c_id=None, c_name=None):
    """ Get champion information from local. 
    Params:
        c_key: str, champion number.
        c_id: str, simplified champion name.
        c_name: str, champion name.
    Returns: champion information dict.
    """
    if not (c_key or c_id or c_name):
        print("Champion key or id or name must be provided. ")
        sys.exit()
    data_path = '../data/dragontail-9.24.2/9.24.2/data/en_US/champion.json'
    all_champions = load_json(data_path)['data']
    for c_data in all_champions.values():
        if (c_key and c_key == c_data['key'] or 
            c_id and c_id == c_data['id'] or
            c_name and c_name == c_data['name']
        ):
            return c_data
    print(f"No compatible data: {c_key, c_id, c_name} ")
    sys.exit()


def get_std_df(df):
    """ Standardize DataFrame. 
    Params: df: Pandas DataFrame.
    Returns: std_df: standardized DataFrame.
    """
    std_df = pd.DataFrame(StandardScaler().fit_transform(df))
    std_df.columns = df.columns
    return std_df


def get_key_factors(df, measure):
    """ Get key factors that lead to win. 
    Params: 
        df: standardized DataFrame.
        measure: str, measurement.
    Returns: Pandas Series, factor and their importance value.
    """
    cov = df.cov().iloc[1:]
    return cov[cov[measure]>0.7][measure]


def pie_factors(data, title):
    """ Show pie graph of Pandas Series data. 
    Params:
        data: Pandas Series.
        title: str, title.
    """
    plt.style.use('ggplot')
    labels = data.index
    values = data.values
    explode = [0.1 if i == max(values) else 0 for i in values]
    colors = cm.rainbow(np.arange(len(values))/len(values))
    fig, ax = plt.subplots(figsize=(10, 6), subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(
        values, explode=explode, autopct='%1.1f%%',
        textprops=dict(color="w"), colors=colors)
    ax.legend(
        wedges, labels, title=title,
        loc='center left', bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=12, weight='bold')
    plt.show()

def show_img(img_path, imgs):
    """ Show image from certain path. """
    if type(imgs) == str:
        if os.path.exists(os.path.join(img_path, imgs+'.png')):
            img = mpimg.imread(os.path.join(img_path, imgs+'.png'))
            plt.figure(figsize=(1.2, 1.2))
            plt.imshow(img)
            plt.title(imgs)
            plt.axis('off')
            plt.show()
    elif type(imgs) == list:
        fig, ax = plt.subplots(ncols=len(imgs), figsize=(1.2*len(imgs), 1.2))
        for i in range(len(imgs)):
            if os.path.exists(os.path.join(img_path, imgs[i]+'.png')):
                img = mpimg.imread(os.path.join(img_path, imgs[i]+'.png'))
                ax[i].imshow(img)
                ax[i].set_title(imgs[i])
                ax[i].axis('off')
        plt.show()
    else:
        print(f"Wrong data type: {type(imgs)} ")


if __name__ == '__main__':
    show_img(
        '../data/dragontail-9.24.2/9.24.2/img/champion', ['Aatrox', 'Fiora'])
