from datetime import  datetime 
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


## MAIN
def main():
    avl = AVL()

    while True:
        print("\n----- MENU -----")
        print("1.  Insertar curso por ID")
        print("2.  Eliminar por ID")
        print("3.  Eliminar por métrica (satisfacción)")
        print("4.  Buscar por ID")
        print("5.  Buscar por métrica")
        print("6.  Buscar: reseñas positivas > negativas + neutras")
        print("7.  Buscar: fecha de creación posterior a una fecha")
        print("8.  Buscar: rango de clases")
        print("9.  Buscar: reseñas > promedio")
        print("10. Recorrido por niveles")
        print("11. Salir")
        option = input("Elige una opción: ").strip()

        if option == "1":
            try:
                course_id = int(input("ID del curso: "))
                found = False
                for ind, row in data.iterrows():
                    if row["id"] == course_id:
                        avl.root = avl.insert_balance(avl.root, row)
                        print("Curso insertado correctamente.")
                        found = True
                        break
                if not found:
                    print("ID no encontrado en el dataset.")
            except:
                print("ID inválido.")

        elif option == "2":
            try:
                course_id = int(input("ID del curso a eliminar: "))
                if avl.delete_by_id(course_id):
                    print("Curso eliminado.")
                else:
                    print("ID no encontrado en el árbol.")
            except:
                print("ID inválido.")

        elif option == "3":
            try:
                key = round(float(input("Valor de satisfacción: ")), 5)
                if avl.delete_by_key(key):
                    print("Nodo eliminado.")
                else:
                    print("Valor no encontrado.")
            except:
                print("Valor inválido.")

        elif option == "4":
            try:
                course_id = int(input("ID del curso: "))
                node = avl.search_by_id(avl.root, course_id)
                if node:
                    print("Curso encontrado:")
                    avl.get_info(node)
                    operaciones_nodo(avl, node)
                else:
                    print("Curso no encontrado.")
            except:
                print("ID inválido.")

        elif option == "5":
            metric = input("Métrica (ej: rating, title, num_reviews...): ").strip()
            value  = input("Valor: ").strip()
            results = avl.search_by_metric(avl.root, metric, value)
            if results:
                _mostrar_resultados(avl, results)
            else:
                print("No se encontraron resultados.")

        elif option == "6":
            results = avl.search_positive_reviews()
            if results:
                _mostrar_resultados(avl, results)
            else:
                print("No se encontraron resultados.")

        elif option == "7":
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            try:
                results = avl.search_by_date(fecha)
                if results:
                    _mostrar_resultados(avl, results)
                else:
                    print("No se encontraron resultados.")
            except:
                print("Formato de fecha inválido.")

        elif option == "8":
            try:
                min_l = int(input("Mínimo de clases: "))
                max_l = int(input("Máximo de clases: "))
                results = avl.search_by_lectures(min_l, max_l)
                if results:
                    _mostrar_resultados(avl, results)
                else:
                    print("No se encontraron resultados.")
            except:
                print("Valores inválidos.")

        elif option == "9":
            promedio = avl.get_average_reviews()
            print(f"Promedio de reseñas totales: {promedio:.2f}")
            results = avl.search_by_reviews(promedio)
            if results:
                _mostrar_resultados(avl, results)
            else:
                print("No se encontraron resultados.")

        elif option == "10":
            avl.BFS()

        elif option == "11":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida.")


def _mostrar_resultados(avl, results):
    print(f"\n{len(results)} resultado(s) encontrado(s):")
    i = 1
    for n in results:
        print(f"  {i}. ID: {n.data['id']} | Sat: {n.key} | {n.data.get('title','')[:50]}")
        i += 1
    sel = input("\n¿Operar sobre algún nodo? (número o Enter para saltar): ").strip()
    if sel.isdigit():
        idx = int(sel) - 1
        if 0 <= idx < len(results):
            operaciones_nodo(avl, results[idx])


def operaciones_nodo(avl, node):
    while True:
        print("\n-- Operaciones sobre el nodo --")
        print("a. Info completa")
        print("b. Nivel")
        print("c. Factor de balance")
        print("d. Padre")
        print("e. Abuelo")
        print("f. Tío")
        print("g. Volver")
        op = input("Elige: ").strip().lower()

        if op == "a":
            avl.get_info(node)

        elif op == "b":
            nivel = avl.get_level(node)
            print(f"Nivel: {nivel}")

        elif op == "c":
            balance = avl.get_balance(node)
            print(f"Factor de balance: {balance}")

        elif op == "d":
            padre = avl.get_parent(node)
            if padre is None:
                print("No tiene padre (es la raíz).")
            else:
                print(f"Padre: ID {padre.data['id']} | Sat {padre.key}")

        elif op == "e":
            abuelo = avl.get_grandparent(node)
            if abuelo is None:
                print("No tiene abuelo.")
            else:
                print(f"Abuelo: ID {abuelo.data['id']} | Sat {abuelo.key}")

        elif op == "f":
            tio = avl.get_uncle(node)
            if tio is None:
                print("No tiene tío.")
            else:
                print(f"Tío: ID {tio.data['id']} | Sat {tio.key}")

        elif op == "g":
            break

        else:
            print("Opción inválida.")


main()
