import os
import json
import shutil
import ttkbootstrap as tb
import ttkbootstrap.dialogs as dialogs

class App(tb.Frame):
    def __init__(self, master):
        tb.Frame.__init__(self, master)

        self.tree = tb.Treeview(self, style="primary")
        ysb = tb.Scrollbar(self, orient='vertical', command=self.tree.yview)
        xsb = tb.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.tag_configure("Active", foreground='#007700')
        self.tree.tag_configure("Deactive", foreground="#770000")
        self.tree.heading('#0', text="Mods")
        self.tree.bind("<ButtonRelease>", self.activate_buttons)

        
        self.conrols = Controls(self)


        self.reload()


        self.tree.grid(row=0, column=0, sticky='nw', ipadx=100)
        ysb.grid(row=0, column=1, sticky='ns')
        xsb.grid(row=1, column=0, sticky='ew')
        self.conrols.grid(row=2, column=0, columnspan=2, pady=10)
        self.pack(expand=True)

    def setup_path(self):
        with open('save.json', 'r') as file:
            self.data = json.load(file)
        
        self.modPath = self.data['modsFilePath']
        self.active = self.data['active']

        if self.modPath == "":
            self.modPath = dialogs.Querybox.get_string("Where is your mods directory?", "Mods")
            self.data['modsFilePath'] = self.modPath

            self.save_data()

        abspath = os.path.abspath('mods/')
        root_node = self.tree.insert('', 'end', text=os.path.basename(abspath), open=True)
        self.process_directory(root_node, abspath)

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            if ".DS_Store" not in p:
                oid = self.tree.insert(parent, 'end', text=p, iid=abspath, tags='Deactive')
                
                if oid in self.data['active']:
                    self.tree.item(oid, tags="Active")

                if isdir:
                    self.process_directory(oid, abspath)
                    self.tree.item(oid, tags="")
    
    def reload(self):
        self.conrols.inputs('disabled')
        for child in self.tree.get_children():
            self.tree.delete(child)
        
        self.setup_path()
    
    def save_data(self):
        with open('save.json', 'w') as file:
            json.dump(self.data, file, indent=4)
    
    def activate_buttons(self, event):
        selected: str = self.tree.selection()[0]
        if ".jar" in selected:
            self.conrols.inputs('normal')
        
        else:
            self.conrols.inputs('disabled')
    
    def activate(self):
        selected = self.tree.selection()[0]

        if selected not in self.data['active']:
            shutil.copy(selected, f"{self.modPath}/{os.path.basename(selected)}")
            self.data['active'].append(selected)

            self.save_data()
            
            self.tree.item(selected, tags='Active')
        self.tree.selection_remove(selected)
        self.conrols.inputs('disabled')

    def deactivate(self):
        
        selected = self.tree.selection()[0]

        if selected in self.data['active']:
            os.remove(f'{self.modPath}/{os.path.basename(selected)}')
            self.data['active'].remove(selected)

            self.save_data()

            self.tree.item(selected, tags='Deactive')
        self.tree.selection_remove(selected)
        self.conrols.inputs('disabled')

class Controls(tb.Frame):
    def __init__(self, master):
        tb.Frame.__init__(self, master)

        self.activate_button = tb.Button(self, text="activate", style='success', command=master.activate)
        self.deactivate_button = tb.Button(self, text="deactivate", style='danger', command=master.deactivate)

        self.activate_button.grid(row=0, column=0, padx=5)
        self.deactivate_button.grid(row=0, column=1, padx=5)
    
    def inputs(self, state):
        self.activate_button['state'] = state
        self.deactivate_button['state'] = state

root = tb.Window(themename='journal')
app = App(root)
app.mainloop()