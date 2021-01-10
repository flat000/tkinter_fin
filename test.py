import csv
import os
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pandas as pd

def read_subfolder():

    sub_folder = []

    for foldername, subfolders, filenames in os.walk('./'):
        for subfolder in subfolders:
            sub_folder.append(subfolder)

    return sub_folder

def read_file(sub_folder):
    current_folder = './' + sub_folder
    file_name = []

    for  foldername, subfolders, filenames in os.walk(current_folder):
        for filename in filenames:
            file_name.append(filename)
    
    return file_name

def cb1_selected(event):
    var = combo1.get()
    combo2['value'] = dict_data[var]

def cb2_selected(event):
    pass

def search_code():
    # パスを取得
    path = path_get()
    
    data_pd = pd.read_csv(path, dtype=object, encoding="utf-8")

    code = str(ent_keyword1.get())

    # テキストボックスを書き込み可能にモード変更
    txt_mode_write()

    # テキストボックスをクリア
    txt_delete()

    result = data_pd[data_pd['エラーコード'].str.contains(code)] #エラーコードの一致抽出
    index = result.index #抽出したインデックス

    # 抽出したデータを取り出し、データタイプの関係でバッファに一度取り出してから保存
    error1 = data_ext(result.loc[index]['エラー名称'])
    error2 = data_ext(result.loc[index]['エラー内容'])
    error3 = data_ext(result.loc[index]['対処方法'])
    error4 = data_ext(result.loc[index]['参考資料'])

    # テキストボックスにエラー内容を挿入
    txt_insert(error1, error2, error3, error4)
    txt_mode_read()

def search_name():
    # パスを取得
    path = path_get()
    
    data_pd = pd.read_csv(path, dtype=object, encoding="utf-8")

    name = str(ent_keyword2.get())

    # テキストボックスを書き込み可能にモード変更
    txt_mode_write()

    # テキストボックスをクリア
    txt_delete()

    result = data_pd[data_pd['エラー名称'].str.contains(name)] #エラーコードの一致抽出
    index = result.index #抽出したインデックス

    # 抽出したデータを取り出し、データタイプの関係でバッファに一度取り出してから保存
    error1 = data_ext(result.loc[index]['エラー名称'])
    error2 = data_ext(result.loc[index]['エラー内容'])
    error3 = data_ext(result.loc[index]['対処方法'])
    error4 = data_ext(result.loc[index]['参考資料'])

    # テキストボックスにエラー内容を挿入
    txt_insert(error1, error2, error3, error4)
    txt_mode_read()

def path_get():
    # パスを取得
    var1 = combo1.get()
    var2 = combo2.get()
    path = './' + var1 + '/' + var2
    return path

def data_ext(data):
    # pandaのSeries型からデータのみを抽出
    _test = data
    _test = _test.iloc[0]
    return _test

def txt_mode_write():
    # テキストボックスを書き込み可能にモード変更
    txtBox1.configure(state='normal')
    txtBox2.configure(state='normal')
    txtBox3.configure(state='normal')
    txtBox4.configure(state='normal')

def txt_delete():
    # テキストボックスをクリア
    txtBox1.delete("1.0","end")
    txtBox2.delete("1.0","end")
    txtBox3.delete("1.0","end")
    txtBox4.delete("1.0","end")

def txt_mode_read():
    # テキストボックスをread onlyモード変更
    txtBox1.configure(state='disabled')
    txtBox2.configure(state='disabled')
    txtBox3.configure(state='disabled')
    txtBox4.configure(state='disabled')

def txt_insert(data1, data2, data3, data4):
    # データをテキストボックスに挿入
    txtBox1.insert(tk.END, data1)
    txtBox2.insert(tk.END, data2)
    txtBox3.insert(tk.END, data3)
    txtBox4.insert(tk.END, data4)

subfolders = read_subfolder()
dict_data = {}

for subfolder in subfolders:
    datas = read_file(subfolder)
    for data in datas:
        dict_data.setdefault(subfolder, []).append(data)

# Tkクラス生成
root = tk.Tk()
# 画面サイズ
root.geometry('900x500')
# 画面タイトル
root.title('エラーコード検索')

######### 機種名の設定 #########

combo1_label = tk.Label(text='機種名称')
combo1_label.grid(row=1, column=1)
# コンボボックスの作成(rootに配置,リストの値を編集不可(readonly)に設定)
combo1 = ttk.Combobox(root, state='readonly', values=list(dict_data.keys()))
# デフォルトの値をindex=0に設定
combo1.current()
# コンボボックスの配置
combo1.grid(row=1, column=2, sticky='w')

######### パーツ名の設定 #########

combo2_label = tk.Label(text='パーツ名称')
combo2_label.grid(row=2, column=1)

# コンボボックスの作成(rootに配置,リストの値を編集不可(readonly)に設定)
combo2 = ttk.Combobox(root, state='readonly')
# コンボボックスの配置
combo2.grid(row=2, column=2, sticky='w')

combo1.bind('<<ComboboxSelected>>', cb1_selected)
combo2.bind('<<ComboboxSelected>>', cb2_selected)


######### エラーコード検索ボックスの設定 ##########
la1 = tk.Button(text='エラーコード検索', command=search_code)
la1.grid(row=3, column=1, sticky=tk.W)
keyword1 = tk.StringVar()
ent_keyword1 = ttk.Entry(justify="left", textvariable=keyword1)
ent_keyword1.grid(row=3, column=2, sticky='w')

######### エラー名称検索ボックスの設定 ##########
la2 = tk.Button(text='エラー名称検索', command=search_name)
la2.grid(row=4, column=1, sticky=tk.W)
keyword2 = tk.StringVar()
ent_keyword2 = ttk.Entry(justify="left", textvariable=keyword2)
ent_keyword2.grid(row=4, column=2, sticky='w')

######### テキスト表示の設定 ##########
font_size = tkFont.Font(size=16)

error1_label = tk.Label(text='エラー名称')
error1_label.grid(row=5, column=1)
txtBox1 = tk.Text()
txtBox1.configure(state='disabled', font=font_size, width=60, height=1)
txtBox1.grid(row=5, column=2)

error2_label = tk.Label(text='エラー内容')
error2_label.grid(row=6, column=1)
txtBox2 = tk.Text()
txtBox2.configure(state='disabled', font=font_size, width=60, height=3)
txtBox2.grid(row=6, column=2)
    
error3_label = tk.Label(text='対処方法')
error3_label.grid(row=7, column=1)
txtBox3 = tk.Text()
txtBox3.configure(state='disabled', font=font_size, width=60, height=5)
txtBox3.grid(row=7, column=2)

error4_label = tk.Label(text='参考資料')
error4_label.grid(row=8, column=1)
txtBox4 = tk.Text()
txtBox4.configure(state='disabled', font=font_size, width=60, height=10)
txtBox4.grid(row=8, column=2)

root.mainloop() # 実行
