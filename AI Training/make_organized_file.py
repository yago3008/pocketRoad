import os
import shutil
from scipy.io import loadmat
import numpy as np

# Caminhos
base_path = r"C:\Users\yago.martins.SOOW\Documents\pocketRoad\pocketroad\AI Training\stanford-cars-dataset"
train_path = os.path.join(base_path, "cars_train", "cars_train")
test_path = os.path.join(base_path, "cars_test", "cars_test")
devkit_path = os.path.join(base_path, "car_devkit", "devkit")

# Pasta destino organizada
organized_train = os.path.join(base_path, "train")
organized_test = os.path.join(base_path, "test")

os.makedirs(organized_train, exist_ok=True)
os.makedirs(organized_test, exist_ok=True)

# Carrega nomes das classes
meta_file = os.path.join(devkit_path, "cars_meta.mat")
meta = loadmat(meta_file)
class_names = [str(c[0]) for c in meta['class_names'][0]]  # lista de strings dos modelos

# Função para organizar treino
def organize_train(mat_file, images_folder, dest_folder):
    data = loadmat(mat_file)['annotations'][0]
    for entry in data:
        filename = entry['fname'][0].strip()
        class_id = entry['class'][0]
        if isinstance(class_id, (list, tuple, np.ndarray)):
            class_id = class_id[0]
        model_name = class_names[class_id - 1]
        class_folder = os.path.join(dest_folder, model_name)
        os.makedirs(class_folder, exist_ok=True)
        src = os.path.join(images_folder, filename)
        dst = os.path.join(class_folder, filename)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copiado {filename} para {class_folder}")
        else:
            print(f"Arquivo não encontrado, pulando: {src}")

# Função para organizar teste (sem classes)
def organize_test(mat_file, images_folder, dest_folder):
    data = loadmat(mat_file)['annotations'][0]
    for entry in data:
        filename = entry['fname'][0].strip()
        class_id = entry['class'][0]
        if isinstance(class_id, (list, tuple, np.ndarray)):
            class_id = class_id[0]

        model_name = class_names[class_id - 1]  # converte ID para nome do modelo
        class_folder = os.path.join(dest_folder, model_name)
        os.makedirs(class_folder, exist_ok=True)

        src = os.path.join(images_folder, filename)
        dst = os.path.join(class_folder, filename)

        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copiado {filename} para {class_folder}")
        else:
            print(f"Arquivo não encontrado, pulando: {src}")

# Executa organização
#train_mat = os.path.join(devkit_path, "cars_train_annos.mat")
#organize_train(train_mat, train_path, organized_train)

test_mat = os.path.join(devkit_path, "cars_test_annos.mat")
organize_test(test_mat, test_path, organized_test)

print("Organização concluída!")
