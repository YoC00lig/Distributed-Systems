import sys
import os
import subprocess
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.protocol.states import EventType
from kazoo.exceptions import NoNodeError
import tkinter as tk
from tkinter import scrolledtext

if len(sys.argv) != 2:
    print("Usage: python main.py <path_to_graphical_application>")
    sys.exit(1)

app_path = sys.argv[1]
app_process = None

def start_application():
    global app_process
    if app_process is None:
        app_process = subprocess.Popen([app_path])
        print("Application started.")

def stop_application():
    global app_process
    if app_process is not None:
        app_process.terminate()
        app_process = None
        print("Application stopped.")

def display_message(message):
    log_text.delete(1.0, tk.END)  
    log_text.insert(tk.END, message + '\n')
    log_text.yview(tk.END)

def display_children_count():
    try:
        children = zk.get_children('/a')
        children_count.set(f"Number of Children: {len(children)}")
    except NoNodeError:
        pass  
    except Exception as e:
        print(f"Error while getting children count: {e}")

def watch_node(event):
    if event.type == EventType.CREATED:
        print("Node '/a' created.")
        start_application()
    elif event.type == EventType.DELETED:
        print("Node '/a' deleted.")
        stop_application()

def display_tree(path, level=0):
    try:
        children = zk.get_children(path)
        tree_structure = '  ' * level + os.path.basename(path) + '\n'
        for child in children:
            tree_structure += display_tree(os.path.join(path, child), level + 1)
        return tree_structure
    except NoNodeError:
        return f"Node '{path}' does not exist.\n"

def update_tree():
    tree = display_tree('/a')
    display_message(tree)
    display_children_count()  
    root.after(5000, update_tree)  

def on_quit_command():
    root.quit()

root = tk.Tk()
root.title("Zookeeper GUI")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

children_count = tk.StringVar()
children_count.set("Number of Children: 0")
children_label = tk.Label(frame, textvariable=children_count)
children_label.pack()

log_text = scrolledtext.ScrolledText(frame, width=60, height=20, wrap=tk.WORD)
log_text.pack()

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

@zk.DataWatch('/a')
def watch_a(data, stat, event):
    if event:
        watch_node(event)

update_tree() 
try:
    root.mainloop()
except KeyboardInterrupt:
    pass
finally:
    zk.stop()
    zk.close()
    stop_application()
