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
    
    data_pd = pd.read_csv(path, dtype=object, encoding=encode_set)

    code = str(ent_keyword1.get())

    result = data_pd[data_pd['エラーコード'].str.contains(code)] #エラーコードの一致抽出
    index = result.index

    for i in tree.get_children():
        tree.delete(i)

    for num in index:
        error1 = result.loc[num]['エラーコード']
        error2 = result.loc[num]['エラー名称']
        tree.insert("","end",values=(error1, error2))

def search_name():
    # パスを取得
    path = path_get()
    
    data_pd = pd.read_csv(path, dtype=object, encoding=encode_set)

    name = str(ent_keyword2.get())

    result = data_pd[data_pd['エラー名称'].str.contains(name)] #エラーコードの一致抽出
    index = result.index #抽出したインデックス

    for i in tree.get_children():
        tree.delete(i)

    for num in index:
        error1 = result.loc[num]['エラーコード']
        error2 = result.loc[num]['エラー名称']
        tree.insert("","end",values=(error1, error2))

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

def set_utf8():
    global encode_set
    encode_set = "utf-8"

def set_sjis():
    global encode_set
    encode_set = "shift-jis"

def new_window():
    ###########################################################################
    # ツリービューで選択されている部分のデータを取得
    for item in tree.selection():
        data = tree.item(item) # 選択されば部分のデータを取得
        value = data["values"] # valuesのみを取得
        code = value[0] # エラーコードを取得

    ##########################################################################
    # パスを取得
    path = path_get()
    
    data_pd = pd.read_csv(path, dtype=object, encoding=encode_set)

    result = data_pd[data_pd['エラーコード'].str.contains(code)] #エラーコードの一致抽出
    index = result.index

    # 抽出したデータを取り出し、データタイプの関係でバッファに一度取り出してから保存
    error1 = data_ext(result.loc[index]['エラー名称'])
    error2 = data_ext(result.loc[index]['エラー内容'])
    error3 = data_ext(result.loc[index]['対処方法'])
    error4 = data_ext(result.loc[index]['参考資料'])

    print(error1, error2, error3, error4)

    ##########################################################################
    ######### テキスト表示の設定 ##########
    font_size = tkFont.Font(size=16) 
 
    newwindow = tk.Toplevel(root)

    error1_label = tk.Label(newwindow, text='エラー名称')
    error1_label.grid(row=1, column=1)
    txtBox1 = tk.Text(newwindow)
    txtBox1.configure(state='normal', font=font_size, width=60, height=1)
    txtBox1.grid(row=1, column=2)

    error2_label = tk.Label(newwindow, text='エラー内容')
    error2_label.grid(row=2, column=1)
    txtBox2 = tk.Text(newwindow)
    txtBox2.configure(state='normal', font=font_size, width=60, height=3)
    txtBox2.grid(row=2, column=2)
    
    error3_label = tk.Label(newwindow, text='対処方法')
    error3_label.grid(row=3, column=1)
    txtBox3 = tk.Text(newwindow)
    txtBox3.configure(state='normal', font=font_size, width=60, height=5)
    txtBox3.grid(row=3, column=2)

    error4_label = tk.Label(newwindow, text='参考資料')
    error4_label.grid(row=4, column=1)
    txtBox4 = tk.Text(newwindow)
    txtBox4.configure(state='normal', font=font_size, width=60, height=10)
    txtBox4.grid(row=4, column=2)

    # テキストボックスにエラー内容を設定
    txtBox1.insert(tk.END, error1)
    txtBox2.insert(tk.END, error2)
    txtBox3.insert(tk.END, error3)
    txtBox4.insert(tk.END, error4)

subfolders = read_subfolder()
dict_data = {}

encode_set="shift-jis"

for subfolder in subfolders:
    datas = read_file(subfolder)
    for data in datas:
        dict_data.setdefault(subfolder, []).append(data)

# Tkクラス生成
root = tk.Tk()
# 画面サイズ
root.geometry('900x500')
# 画面タイトル
root.title('エラー検索')

##########################################################################
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

##########################################################################
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

###########################################################################
# メニューバーを作成(マスターはウィンドウ)
menubar = tk.Menu(root)
# メニューを作成(マスターはメニューバー)、tearoff=Falseにして切り取らせないようにする
menu1 = tk.Menu(menubar, tearoff=False)
# メニューにアイテムを追加
menu1.add_command(label="UTF-8", command=set_utf8)
# セパレーター
menu1.add_separator()
menu1.add_command(label="shift-JIS", command=set_sjis)
#4. メニューバーにメニューをカスケード
menubar.add_cascade(label="文字コード設定", menu=menu1)
#5. ウィンドウにメニューバーを追加
root["menu"] = menubar

###########################################################################
# ツリービューの作成
tree = ttk.Treeview(root)
# 列インデックスの作成
tree["columns"] = (1,2)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1,width=150)
tree.column(2,width=500)

# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1,text="エラーコード")
tree.heading(2,text="エラー名称")

# ツリービューの配置
tree.grid(row=5, column=2, sticky='w')

nw_button = tk.Button(text='エラー詳細表示', command=new_window)
nw_button.grid(row=6, column=2, sticky=tk.W)

root.mainloop() # 実行
