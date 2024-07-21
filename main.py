import ttkbootstrap as tb
import json
import uuid

global data

def load_data():
    with open('save.json', 'r') as file:
        global data
        data = json.load(file)

root = tb.Window(themename='superhero')

tree = tb.Treeview(root, show='headings', style='primary')
tree.config(columns=('mods'))
tree.heading("mods", text="Mods")



tree.insert(parent='', index='end', iid=uuid.uuid4(), values=('blob'))
tree.insert(parent='', index='end', values=('blorp'))

tree.pack()

load_data()

root.mainloop()