import sys
import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.protocol.states import EventType
from kazoo.exceptions import NoNodeError

class ZookeeperApp:
    def __init__(self, app_path):
        self.app_path = app_path
        self.app_process = None

        self.root = tk.Tk()
        self.root.title("Zookeeper GUI")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.children_count = tk.StringVar()
        self.children_count.set("Number of Children: 0")
        self.children_label = tk.Label(self.frame, textvariable=self.children_count)
        self.children_label.pack()

        self.log_text = scrolledtext.ScrolledText(self.frame, width=60, height=20, wrap=tk.WORD)
        self.log_text.pack()

        self.zk = KazooClient(hosts='127.0.0.1:2181')
        self.zk.start()

        @self.zk.DataWatch('/a')
        def watch_a(data, stat, event):
            if event:
                self.watch_node(event)

        self.update_tree()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.on_quit_command)
        self.quit_button.pack(side=tk.BOTTOM)

    def start_application(self):
        if self.app_process is None:
            self.app_process = subprocess.Popen([self.app_path])
            print("Application started.")

    def stop_application(self):
        if self.app_process is not None:
            self.app_process.terminate()
            self.app_process = None
            print("Application stopped.")

    def display_message(self, message):
        self.log_text.delete(1.0, tk.END)  
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.yview(tk.END)

    def display_children_count(self):
        try:
            children = self.zk.get_children('/a')
            self.children_count.set(f"Number of Children: {len(children)}")
        except NoNodeError:
            pass  
        except Exception as e:
            print(f"Error while getting children count: {e}")

    def watch_node(self, event):
        if event.type == EventType.CREATED:
            print("Node '/a' created.")
            self.start_application()
        elif event.type == EventType.DELETED:
            print("Node '/a' deleted.")
            self.stop_application()

    def display_tree(self, path, level=0):
        try:
            children = self.zk.get_children(path)
            tree_structure = '  ' * level + os.path.basename(path) + '\n'
            for child in children:
                tree_structure += self.display_tree(os.path.join(path, child), level + 1)
            return tree_structure
        except NoNodeError:
            return f"Node '{path}' does not exist.\n"

    def update_tree(self):
        tree = self.display_tree('/a')
        self.display_message(tree)
        self.display_children_count()  
        self.root.after(5000, self.update_tree)  

    def on_quit_command(self):
        self.root.quit()
        self.zk.stop()
        self.zk.close()
        self.stop_application()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <path_to_graphical_application>")
        sys.exit(1)

    app_path = sys.argv[1]
    app = ZookeeperApp(app_path)
    app.root.mainloop()
