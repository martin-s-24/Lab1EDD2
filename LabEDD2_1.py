from platform import node, nodeimport datetime
import pandas as pd
data = pd.read_csv("/Users/martin/LabsEDD2/dataset_courses_with_reviews.csv")
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
        sat = rating * 0.7 + ((5 * pos + 3 * neu + neg) / num) * 0.3
        return round(sat, 5)


class AVL:
    def __init__(self):
        self.root = None

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
        return True

    def delete_by_key(self, key):
        p, padre = self.search_generic(key)
        if p is None:
            return False  # no existe
        self.root = self.delete(self.root, key)
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
            if balance > 1 and self.get_balance(nodo.left) < 0:
                return self.left_right_rotation(nodo)
            # Caso derecha-derecha
            if balance < -1 and self.get_balance(nodo.right) <= 0:
                return self.left_rotation(nodo)
            # Caso derecha-izquierda
            if balance < -1 and self.get_balance(nodo.right) > 0:
                return self.right_left_rotation(nodo)

            return nodo

    def search_positive_reviews(self, nodo, result=None):
        if result is None:
            result = []
        if nodo is not None:
            if nodo.data["positive_reviews"] > nodo.data["negative_reviews"] + nodo.data["neutral_reviews"]:
                result.append(nodo)
            self.search_positive_reviews(nodo.left, result)
            self.search_positive_reviews(nodo.right, result)
        return result

    def search_by_date(self, fecha, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        if node is not None:
            fecha_dada = datetime.strptime(fecha, "%Y-%m-%d") #strptime convierte un string a un objeto datetime.
            fecha_nodo = datetime.strptime(node.data["created"][:10], "%Y-%m-%d")
            if fecha_nodo > fecha_dada:
                result.append(node)
            self.search_by_date(fecha, node.left, result)
            self.search_by_date(fecha, node.right, result)
        return result

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
            print(f"{i}. {node.key} | {node.data.get('title', '')}")
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

    def get_level(self, node, current=None, level=1):
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
