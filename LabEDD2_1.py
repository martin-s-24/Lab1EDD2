import pandas as pd
data = pd.read_csv("/Users/martin/LabsEDD2/dataset_courses_with_reviews.csv")
class Node:
    def __init__(self, data):
        self.data = data
        self.key = Node.satisfaction(data)
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

    def get_height(self, node):
        if node: 
            return node.height
        else: 
            return 0

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

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

    def delete(self, nodo):
        if nodo is None:
            return None
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
            nodo.left = self.delete(nodo.left)

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