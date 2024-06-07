import sys
import os
import subprocess
from kazoo.client import KazooClient
from kazoo.recipe.watchers import ChildrenWatch
from kazoo.protocol.states import EventType

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

def display_children_count(children):
    print(f"\nCurrent number of children: {len(children)}")

def watch_node(event):
    if event.type == EventType.CREATED:
        print("Node 'a' created.")
        start_application()
    elif event.type == EventType.DELETED:
        print("Node 'a' deleted.")
        stop_application()

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

@zk.DataWatch('/a')
def watch_a(data, stat, event):
    if event:
        watch_node(event)

children_watch = ChildrenWatch(zk, '/a', func=display_children_count)

def display_tree(path, level=0):
    children = zk.get_children(path)
    print('  ' * level + os.path.basename(path))
    for child in children:
        display_tree(os.path.join(path, child), level + 1)

try:
    while True:
        command = input("Enter 'tree' to display the tree structure or 'quit' to exit: ").strip().lower()
        if command == 'tree':
            display_tree('/a')
        elif command == 'quit':
            break
except KeyboardInterrupt:
    pass
finally:
    zk.stop()
    zk.close()
    stop_application()
