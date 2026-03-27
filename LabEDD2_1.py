from datetime import  datetime
from platform import node 
from numpy._core.umath import rint
import pandas as pd
from graphviz import Digraph, dot
data = pd.read_csv(r"C:\Users\mayma\Downloads\dataset_courses_with_reviews.csv")
                   
class nodo:
    def __init__(self, data):
        self.data = data
        self.key = nodo.satisfaction(data)
        self.left = None
        self.right = None
        self.height = 1

    @staticmethod
    def satisfaction(row):
        rating = row["rating"]
        pos = row["positive_reviews"]
        neg = row["negative_reviews"]
        neu = row["neutral_reviews"]
        num = row["num_reviews"]
        if num == 0:
            return 0.0
        sat = rating * 0.7 + ((5 * pos + 3 * neu + neg) / num) * 0.3
        return round(sat, 5)


class AVL:
    def __init__(self):
        self.root = None
        self.row_metric_list = data.columns.tolist()

    def get_height(self, nodo):
        if nodo: 
            return nodo.height
        else: 
            return 0

    def get_balance(self, nodo):
        if nodo is None:
            return 0
        return self.get_height(nodo.left) - self.get_height(nodo.right)

    def update_height(self, nodo):
        nodo.height = 1 + max(self.get_height(nodo.left), self.get_height(nodo.right))

    def left_rotation(self, p):
        q = p.right  
        temp = q.left
        q.left = p  
        p.right = temp
        self.update_height(p)
        self.update_height(q)
        return q 
    
    def right_rotation(self, p):
        q = p.left  
        temp = q.right
        q.right = p
        p.left = temp
        self.update_height(p)
        self.update_height(q)
        return q  
    
    def left_right_rotation(self, p):
        p.left = self.left_rotation(p.left)
        return self.right_rotation(p)
    
    def right_left_rotation(self, p):
        p.right = self.right_rotation(p.right)
        return self.left_rotation(p)

    def search_generic(self, key):
        p = self.root
        pad = None
        while p is not None:
            if key == p.key:
                return p, pad
            pad = p
            if key < p.key:
                p = p.left
            else:
                p = p.right
        return p, pad

    def max_der(self, nodo):
        if nodo is None:
            return None
        if nodo.right is None:
            return nodo
        return self.max_der(nodo.right)

    def predecesor(self, nodo):
        if nodo is None:
            return None
        return self.max_der(nodo.left)

    def search_by_id(self, nodo, id):
        if nodo is None:
            return None
        if nodo.data["id"] == id:
            return nodo
        # como el árbol no está ordenado por id, toca buscar en ambos lados
        resultado = self.search_by_id(nodo.left, id)
        if resultado is not None:
            return resultado
        return self.search_by_id(nodo.right, id)

    def delete_by_id(self, id):
        nodo = self.search_by_id(self.root, id)
        if nodo is None:
            return False  # no existe
        self.root = self.delete(self.root, nodo.key)
        self.visualize()
        return True

    def delete_by_key(self, key):
        p, padre = self.search_generic(key)
        if p is None:
            return False  # no existe
        self.root = self.delete(self.root, key)
        self.visualize()
        return True

    def delete(self, nodo, key):
        if nodo is None:
            return None
        if key < nodo.key:
            nodo.left = self.delete(nodo.left, key)
        elif key > nodo.key:
            nodo.right = self.delete(nodo.right, key)
        else:
            # Caso 1: hoja
            if nodo.left is None and nodo.right is None:
                return None
            # Caso 2a: solo hijo derecho
            elif nodo.left is None:
                return nodo.right
            # Caso 2b: solo hijo izquierdo
            elif nodo.right is None:
                return nodo.left
            # Caso 3: dos hijos
            else:
                pred = self.predecesor(nodo)
                nodo.data = pred.data
                nodo.key = pred.key
                nodo.left = self.delete(nodo.left, pred.key)
        self.update_height(nodo)
        balance = self.get_balance(nodo)

        # Caso izquierda-izquierda
        if balance > 1 and self.get_balance(nodo.left) >= 0:
            return self.right_rotation(nodo)
        # Caso izquierda-derecha
        elif balance > 1 and self.get_balance(nodo.left) < 0:
            return self.left_right_rotation(nodo)
        # Caso derecha-derecha
        elif balance < -1 and self.get_balance(nodo.right) <= 0:
            return self.left_rotation(nodo)
        # Caso derecha-izquierda
        elif balance < -1 and self.get_balance(nodo.right) > 0:
            return self.right_left_rotation(nodo)

        return nodo

    def search_positive_reviews(self, nodo=None, result=None, yacomenzo=False):
        if result is None:
            result = []
        if not yacomenzo:
            nodo = self.root
            yacomenzo = True
        if nodo is not None:
            if nodo.data["positive_reviews"] > nodo.data["negative_reviews"] + nodo.data["neutral_reviews"]:
                result.append(nodo)
            self.search_positive_reviews(nodo.left, result, yacomenzo)
            self.search_positive_reviews(nodo.right, result, yacomenzo)
        return result
    
    def search_by_date(self, fecha, node=None, result=None, yacomenzo=False):
        if result is None:
            result = []
        if not yacomenzo:
            node = self.root
            yacomenzo = True
        if node is not None:
            fecha_dada = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_nodo = datetime.strptime(node.data["created"][:10], "%Y-%m-%d")
            if fecha_nodo > fecha_dada:
                result.append(node)
            self.search_by_date(fecha, node.left, result, yacomenzo)
            self.search_by_date(fecha, node.right, result, yacomenzo)
        return result
    
    def search_by_lectures(self, min_lectures, max_lectures, node=None, result=None, yacomenzo=False):
        if result is None:
            result = []
        if not yacomenzo:
            node = self.root
            yacomenzo = True
        if node is not None:
            if min_lectures <= node.data["num_published_lectures"] <= max_lectures:
                result.append(node)
            self.search_by_lectures(min_lectures, max_lectures, node.left, result, yacomenzo)
            self.search_by_lectures(min_lectures, max_lectures, node.right, result, yacomenzo)
        return result
    
    def search_by_reviews(self, promedio, node=None, result=None, yacomenzo=False):
        if result is None:
            result = []
        if not yacomenzo:
            node = self.root
            yacomenzo = True
        if node is not None:
            if (node.data["positive_reviews"] > promedio or node.data["negative_reviews"] > promedio or node.data["neutral_reviews"] > promedio):
                result.append(node)
            self.search_by_reviews(promedio, node.left, result, yacomenzo)
            self.search_by_reviews(promedio, node.right, result, yacomenzo)
        return result
    
    def get_average_reviews(self):
        total, count = self.get_average(self.root, 0, 0)
        if count == 0:
            return 0
        return total / count

    def get_average(self, node, total, count):
        if node is None:
            return total, count
        total += node.data["num_reviews"]
        count += 1
        total, count = self.get_average(node.left, total, count)
        total, count = self.get_average(node.right, total, count)
        return total, count
    

        ##################################################################
        ##lo mio de insertar por id y que se balancee automaticamente#####
        ##################################################################
    def insert_balance(self, node, data):
        key = nodo.satisfaction(data)
        if node is None:
            return nodo(data)
        if key < node.key:
            node.left = self.insert_balance(node.left, data)
        elif key > node.key:
            node.right = self.insert_balance(node.right, data)
        else:
            return node
        self.update_height(node)
        balance = self.get_balance(node)
        if balance > 1 and key < node.left.key:
            return self.right_rotation(node)
        if balance < -1 and key > node.right.key:
            return self.left_rotation(node)
        if balance > 1 and key > node.left.key:
            return self.left_right_rotation(node)
        if balance < -1 and key < node.right.key:
            return self.right_left_rotation(node)
        return node

    def insert_by_ID_user(self, dataset):
        try:
            course_id = int(input("Insert course ID: "))
        except ValueError:
            print("Invalid ID")
            return False
        if course_id not in dataset:
            print("ID not found")
            return False
        data = dataset[course_id]
        self.root = self.insert_balance(self.root, data)
        self.visualize()
        return True
    
    def delete_by_metric(self, metric, value):
        results = self.search_by_metric(self.root, metric, value)
        if not results:
            print(f"No nodes found with {metric}={value}")
            return False
        for node in results:
            self.root = self.delete(self.root, node.key)
        self.visualize()
        print(f"{len(results)} node(s) deleted.")
        return True


    def BFS(self):
        height = self.get_height(self.root)
        for level in range(0, height):
            print(f"Level {level}:")
            self.Layer_Traversal(self.root, level)



    def Layer_Traversal(self, node, level, i=0):
        if node is None:
            return
        if i == level:
            print(f"{i}.{node.data.get('id', '')}")
            return
        self.Layer_Traversal(node.left, level, i + 1)
        self.Layer_Traversal(node.right, level, i + 1)


    def search_by_metric(self, node, metric, value, results=None):
        if results is None:
            results = []
        if node is None:
            return results
        node_value = node.data.get(metric, "")
        try:
            if float(node_value) == float(value):        ###cambiado para poder buscar por numeros y no solo string
                results.append(node)
        except (ValueError, TypeError):
            if str(node_value).lower() == str(value).lower():
                results.append(node)
        self.search_by_metric(node.left, metric, value, results)
        self.search_by_metric(node.right, metric, value, results)
        return results

    def search_specific(self):
        for i in range(len(self.row_metric_list)):
            print(f"{i+1}. {self.row_metric_list[i]}")

        metric = input("Chosen metric ").strip()
        value = input(f"Enter value of metric ").strip()


        results = self.search_by_metric(self.root, metric, value)
        if results:
            print(f"{len(results)} result(s) found:")
            for node in results:
                print(f"satisfaction={node.key} | {node.data.get('title', '')}")
        else:
            print("No results found.")
        return results
   
    def get_info(self, node):
        for key, value in node.data.items():
            print(f"{key}: {value}")

    def get_balance_node(self, node):
        return self.get_balance(node)

    def get_level(self, node, current=None, level=0):
        if current is None:
            current = self.root
        if current is None:
            return None
        if current.key == node.key:
            return level
        if node.key < current.key:
            return self.get_level(node, current.left, level + 1)
        return self.get_level(node, current.right, level + 1)

    def get_parent(self, node, current=None, parent=None):
        if current is None:
            current = self.root
        if current is None:
            return None
        if current.key == node.key:
            return parent
        if node.key < current.key:
            return self.get_parent(node, current.left, current)
        return self.get_parent(node, current.right, current)

    def get_grandparent(self, node):
        parent = self.get_parent(node)
        if parent is None:
            return None
        return self.get_parent(parent)

    def get_uncle(self, node):
        parent = self.get_parent(node)
        if parent is None:
            return None
        grandparent = self.get_grandparent(node)
        if grandparent is None:
            return None
        if grandparent.left and grandparent.left.key == parent.key:
            return grandparent.right
        return grandparent.left

    ####################################################################
    ##aqui termina lo mio##
###### aqui empieza lo de graphviz 
    def visualize(self, filename="avl_tree"):
        dot = Digraph()
        dot.attr(fontname="Arial Unicode MS")
        dot.node_attr.update(fontname="Arial Unicode MS")
        self._add_nodes(dot, self.root)
        dot.render(filename, format="png", cleanup=True)
        print(f"Tree saved as {filename}.png")

    def _add_nodes(self, dot, node):
        if node is None:
            return
        course_id = node.data.get("id", "")
        title = str(node.data.get("title", ""))[:20]
        # replace non-ascii characters so graphviz can render them
        ##title = title.encode("ascii", "replace").decode("ascii")
        label = f"ID: {course_id}\nTitle: {title}\nSat: {node.key}"
        dot.node(str(node.key), label=label)
        if node.left:
            dot.edge(str(node.key), str(node.left.key))
            self._add_nodes(dot, node.left)
        if node.right:
            dot.edge(str(node.key), str(node.right.key))
            self._add_nodes(dot, node.right)







#######termina lo de graphviz

## MAIN
## MAIN
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog
import io
import contextlib

def launch_interface(avl, data):
    dataset = {int(k): {**v, "id": int(k)} for k, v in data.set_index("id").to_dict("index").items()}

    window = tk.Tk()
    window.title("lab for the big E")
    window.configure(bg="#f5f5f5")
    window.geometry("1200x750")
    
    window.resizable(True, True)

    tk.Label(window, text="ARBÓL AVL LABORATORIO 2 - ESTRUCTURA DE DATOS 2", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    msg_var = tk.StringVar()
    tk.Label(window, textvariable=msg_var, font=("Courier", 10),bg="#f5f5f5", wraplength=1100, justify="left").pack(padx=15, pady=2)

    canvas = tk.Canvas(window, bg="white", relief="groove")
    canvas.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)

    tree_img_ref = None

    def show(text):
        msg_var.set(msg_var.get() + "\n" + text)

    def clear():
        msg_var.set("")

    def update_tree_image():
        nonlocal tree_img_ref
        try:
            img = Image.open("avl_tree.png")
            canvas.update()
            cw, ch = canvas.winfo_width(), canvas.winfo_height()
            img.thumbnail((cw, ch), Image.LANCZOS)
            tree_img_ref = ImageTk.PhotoImage(img)
            canvas.delete("all")
            canvas.create_image(cw // 2, ch // 2, anchor="center", image=tree_img_ref)
        except Exception as e:
            canvas.delete("all")
            canvas.create_text(20, 20, anchor="nw",
                text=f"Tree not available: {e}", fill="gray")
    import builtins
    builtins.print = lambda *args, **kwargs: show(" ".join(str(a) for a in args))
    builtins.input = lambda prompt="": simpledialog.askstring("Input", str(prompt)) or ""
    def capture(fn):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = fn()
        show(buf.getvalue())
        return result

    def node_options_window(node):
        popup = tk.Toplevel(window)
        popup.title(f"Node — ID {node.data.get('id')}")
        popup.geometry("260x300")
        popup.configure(bg="#f5f5f5")
        popup.resizable(False, False)

        tk.Label(popup, text=f"ID: {node.data.get('id')}", font=("Arial", 11, "bold"), bg="#f5f5f5").pack(pady=8)

        def btn(text, cmd):
            tk.Button(popup, text=text, width=30, command=cmd,bg="white", relief="groove",font=("Arial", 10)).pack(pady=2)

        btn("a. Full info",      lambda: [clear(), capture(lambda: avl.get_info(node))])
        btn("b. Level",          lambda: [clear(), show(f"Level: {avl.get_level(node)}")])
        btn("c. Balance factor", lambda: [clear(), show(f"Balance factor: {avl.get_balance_node(node)}")])
        btn("d. Parent",         lambda: [clear(), show(f"Parent: {avl.get_parent(node).data.get('id') if avl.get_parent(node) else 'None'}")])
        btn("e. Grandparent",    lambda: [clear(), show(f"Grandparent: {avl.get_grandparent(node).data.get('id') if avl.get_grandparent(node) else 'None'}")])
        btn("f. Uncle",          lambda: [clear(), show(f"Uncle: {avl.get_uncle(node).data.get('id') if avl.get_uncle(node) else 'None'}")])
        tk.Button(popup, text="Close", width=30, command=popup.destroy,bg="#ffdddd", relief="groove", font=("Arial", 10)).pack(pady=8)

    def select_from_results(results):
        if not results:
            show("No results found.")
            return
        popup = tk.Toplevel(window)
        popup.title("Results")
        popup.geometry("430x300")
        popup.configure(bg="#f5f5f5")

        tk.Label(popup, text=f"{len(results)} result(s) found:",font=("Arial", 11, "bold"), bg="#f5f5f5").pack(pady=6)

        listbox = tk.Listbox(popup, font=("Courier", 10), width=52, height=12)
        listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        for n in results:
            listbox.insert(tk.END,f"ID={n.data.get('id')}  |  {str(n.data.get('title',''))[:38]}")

        def on_select():
            idx = listbox.curselection()
            if idx:
                node_options_window(results[idx[0]])

        tk.Button(popup, text="Open node operations", command=on_select,bg="white", relief="groove", font=("Arial", 10)).pack(pady=5)

    def do_insert():
        clear()
        course_id = simpledialog.askinteger("Insert", "Enter course ID:")
        if course_id is None:
            return
        if course_id not in dataset:
            show("ID not found in dataset.")
            return
        if avl.search_by_id(avl.root, course_id) is not None:
            show(f"ID {course_id} is already in the tree.")
            return
        avl.root = avl.insert_balance(avl.root, dataset[course_id])
        avl.visualize()
        update_tree_image()
        show(f"Course {course_id} inserted.")

    def do_delete_id():
        clear()
        course_id = simpledialog.askinteger("Delete by ID", "Enter course ID:")
        if course_id is None:
            return
        if avl.delete_by_id(course_id):
            update_tree_image()
            show(f"Course {course_id} deleted. Tree saved as avl_tree.png")
        else:
            show("ID not found in tree.")

    def do_delete_sat():
        clear()
        sat = simpledialog.askfloat("Delete by Satisfaction", "Enter satisfaction value:")
        if sat is None:
            return
        if avl.delete_by_key(round(sat, 5)):
            update_tree_image()
            show("Node deleted. Tree saved as avl_tree.png")
        else:
            show("Satisfaction value not found.")

    def do_search_id():
        clear()
        course_id = simpledialog.askinteger("Search by ID", "Enter course ID:")
        if course_id is None:
            return
        result = avl.search_by_id(avl.root, course_id)
        if result:
            show(f"Found: {result.data.get('title','')}")
            node_options_window(result)
        else:
            show("ID not found.")

    def do_search_metric():
        clear()
        metric = simpledialog.askstring("Search by Metric","Enter metric name (e.g. title, rating, num_reviews):")
        if not metric:
            return
        value = simpledialog.askstring("Search by Metric", f"Enter value for '{metric}':")
        if value is None:
            return
        results = avl.search_by_metric(avl.root, metric, value)
        show(f"{len(results)} result(s) found.")
        select_from_results(results)

    def do_delete_metric():
        clear()
        metric = simpledialog.askstring("Delete by Metric", "Enter metric name (e.g. title, rating, num_reviews):")
        if not metric or metric.strip() == "":
            show("No metric entered.")
            return
        if metric not in avl.row_metric_list:
            show(f"Metric '{metric}' does not exist. Valid metrics are:\n{', '.join(avl.row_metric_list)}")
            return
        value = simpledialog.askstring("Delete by Metric", f"Enter value for '{metric}':")
        if not value or value.strip() == "":
            show("No value entered.")
            return
        if avl.delete_by_metric(metric, value):
            update_tree_image()

    def do_positive_reviews():
        clear()
        results = avl.search_positive_reviews()
        show(f"{len(results)} course(s) found.")
        select_from_results(results)

    def do_by_date():
        clear()
        fecha = simpledialog.askstring("Search by Date", "Enter date (YYYY-MM-DD):")
        if not fecha:
            return
        try:
            results = avl.search_by_date(fecha)
            show(f"{len(results)} course(s) created after {fecha}.")
            select_from_results(results)
        except:
            show("Invalid date format.")

    def do_by_lectures():
        clear()
        min_l = simpledialog.askinteger("Lectures Range", "Minimum lectures:")
        if min_l is None:
            return
        max_l = simpledialog.askinteger("Lectures Range", "Maximum lectures:")
        if max_l is None:
            return
        results = avl.search_by_lectures(min_l, max_l)
        show(f"{len(results)} course(s) found.")
        select_from_results(results)

    def do_above_average():
        clear()
        promedio = avl.get_average_reviews()
        show(f"Average reviews: {promedio:.2f}")
        results = avl.search_by_reviews(promedio)
        show(f"{len(results)} course(s) above average.")
        select_from_results(results)

    def do_bfs():
        clear()
        capture(lambda: avl.BFS())

    btn_frame = tk.Frame(window, bg="#f5f5f5")
    btn_frame.pack(pady=8)

    buttons = [
        ("Insert by ID",           do_insert),
        ("Delete by ID",           do_delete_id),
        ("Delete by Satisfaction", do_delete_sat),
        ("Delete by Metric",       do_delete_metric),
        ("Search by ID",           do_search_id),
        ("Search by Metric",       do_search_metric),
        ("Positive Reviews",       do_positive_reviews),
        ("Created After Date",     do_by_date),
        ("Lectures in Range",      do_by_lectures),
        ("Above Avg Reviews",      do_above_average),
        ("BFS",          do_bfs),
    ]

    for i, (text, cmd) in enumerate(buttons):
        tk.Button(btn_frame, text=text, width=22, height=2, command=cmd,bg="white", relief="groove", font=("Arial", 10)).grid(row=i//5, column=i%5, padx=4, pady=4)

    window.mainloop()

avl = AVL()
launch_interface(avl, data)
