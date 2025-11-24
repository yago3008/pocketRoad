from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import os

# Inicializa a API
api = KaggleApi()
api.authenticate()

# ID do dataset que você quer baixar
dataset = "eduardo4jesus/stanford-cars-dataset"

# Caminho onde será salvo
download_path = "C:/Users/yago.martins.SOOW/Documents/pocketRoad/pocketroad/AI Training/stanford-cars-dataset"

# Cria a pasta se não existir
os.makedirs(download_path, exist_ok=True)

# Faz o download do dataset (zip)
api.dataset_download_files(dataset, path=download_path, unzip=True)

print("Download e extração concluídos!")
