import pickle
import random
from itertools import combinations

import pandas as pd
import tkinter as tk
import tkinter.filedialog
import time
import numpy as np
from mlxtend.classifier import LogisticRegression
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

data_frame = None
data_list = None
data_frame_columns = None
purchases = {}


# Loading from file and processing data
def load_file():
    global data_frame

    data_frame = None
    data_list = None
    purchases = {}

    start_time = time.time()

    file_name = tk.filedialog.askopenfilename(initialdir="D:/others/university/data mining/laboratory 5/code/",
                                              title="Select file",
                                              filetypes=(  # ("pkl files", "*.pkl"),
                                                  ("xlsx files", "*.xlsx"),
                                                  ("all files", "."))
                                              )
    if len(purchases) == 0:
        data_frame = load_xlsx(file_name)

        label['text'] = 'Processing data...'

        # data_frame = data_frame[~data_frame['InvoiceNo'].str.contains('C')]
        data_frame.dropna(axis=0, subset=['InvoiceNo'], inplace=True)
        data_frame['InvoiceNo'] = data_frame['InvoiceNo'].astype('str')
        data_frame['Description'] = data_frame['Description'].str.strip()

        # Delete rows that starts from 'C' symbol in InvoiceNo column
        data_frame = data_frame.drop(data_frame[data_frame.InvoiceNo.str.contains('C', na=False)].index)
        # Delete rows that null is there
        data_frame = data_frame.dropna()

    label['text'] = "Load take " + str(round(time.time() - start_time, 3)) + " seconds"

    return 0


# Load xlsx file and return pandas DataFrame object
def load_xlsx(file_name=None):
    label['text'] = 'Loading..'

    if file_name is None:
        file_name = tk.filedialog.askopenfilename(initialdir="D:/others/university/data mining/laboratory 5/code/",
                                                  title="Select file",
                                                  filetypes=(("xlsx files", "*.xlsx"),
                                                             ("all files", "."))
                                                  )
    data = 0
    if file_name:
        data = pd.read_excel(file_name)
    label['text'] = 'Loaded'

    return data


def analyze():
    global data_frame

    if len(data_frame) == 0:
        return 0

    start_time = time.time()

    basket = (data_frame.groupby(['InvoiceNo', 'Description'])['Quantity']
              .sum().unstack().reset_index().fillna(0)
              .set_index('InvoiceNo'))

    basket2 = basket

    step = 3
    count_of_elements_in_basket = 0
    min_support = 0.02

    basket = basket.dropna(how='all', axis=1)

    for j in range(1, step + 1):
        count_of_elements_in_basket = 0
        for element in basket:
            for value in basket[element]:
                count_of_elements_in_basket += value

        all_combinations_of_basket = list(combinations(basket.columns, j))

        support = 0
        most_frequent = {}
        for ccombination in all_combinations_of_basket:
            for combination in ccombination:
                # Select column contents by column name using [] operator
                columnSeriesObj = basket[combination]
                # print('Colunm Name : ', combination)
                # print('Column Contents : ', columnSeriesObj.values)
                support = 0
                for value in columnSeriesObj.values:
                    support += value
                if (support / count_of_elements_in_basket) < min_support:
                    print(len(basket.columns))
                    basket = basket.drop(columns=combination)
                else:
                    most_frequent[combination] = support / count_of_elements_in_basket

    print(most_frequent)

    label['text'] = "Done in " + str(round(time.time() - start_time, 3)) + " seconds"

    def hot_encode(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    basket_encoded = basket2.applymap(hot_encode)
    basket2 = basket_encoded

    frq_items = apriori(basket2, min_support=0.05, use_colnames=True)

    # print(frq_items.head())

    return 0

# Window GUI
window = tk.Tk()
label = tk.Label(window, text="", fg='black', font=("Consolas", 11))
label.place(x=0, y=0)
# text_field = tk.Text(window, bd=3)
# text_field.place(x=0, y=30, height=60, width=300)
open_file_for_analyze_button = tk.Button(window, text="Select file", fg='black', command=load_file)
open_file_for_analyze_button.place(x=160, y=100)
analyze_button = tk.Button(window, text="Analyze", fg='black', command=analyze)
analyze_button.place(x=90, y=100)
window.title('Laboratory 5')
width = window.winfo_width() + (2 * window.winfo_rootx() - window.winfo_x())
height = window.winfo_height() + (window.winfo_rooty() - window.winfo_y() + window.winfo_rootx() - window.winfo_x())
window.geometry('300x130')
window.eval('tk::PlaceWindow . center')
window.resizable(width=False, height=False)
window.mainloop()
# END Window GUI
