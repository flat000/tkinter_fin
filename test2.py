#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import random

root = tk.Tk()
root.title("お言葉先生")
root.geometry("400x200")

words = ('ハングリーであれ。愚か者であれ。', 
'夢は大きく、失敗は大胆に。', 
'困難の中に、機会がある。',
'知識とは、天に飛翔するための翼である。',
'人生は公平ではない。そのことに慣れよう。',
'重要なことに集中する唯一の方法は「ノー」と言うことだ。',
'活動的な馬鹿より恐ろしいものはない。',
'最も大きな危険は勝利の瞬間にある。',
'輝けるもの必ずしも金ならず。'
)

def outputWords(event): 

    value = txtBox.get()
    txtBox.configure(state='normal')

    # 既に文字があれば削除する
    if value: 
        txtBox.delete(0, tk.END)

    txtBox.insert(tk.END, random.choice(words))
    txtBox.configure(state='readonly')

# ラベルを追加
label = tk.Label(root, text="今のそなたに必要な言葉を授けよう")
label.pack()

# テキストボックスを追加
txtBox = tk.Entry()
txtBox.configure(state='readonly', width=50)
txtBox.place(x=55, y=80)

# ボタンの追加
button = tk.Button(text='さあ、ボタンを押すがよい', width=30)
button.place(x=90, y=120)
button.bind('<Button-1>', outputWords)

root.mainloop()