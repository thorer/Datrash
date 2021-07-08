# Object detection Datrash Model
Object_detection

# Présentation
Dans le cardre d'un Master Camp, nous avons souhaité développer un outil de détection de déchets à l'aide d'une intelligence artificielle.
Pour cela, nous avons utilisé une intelligence artificielle basé sur une détection en "boxes" à l'aide de Tensorflow V2.

# Premiers pas 
> Pour le projet nous utiliserons Python version 3.8 localement et avec anaconda.
> Pour débuter ce projet, le premier élément est de créer un environnement virtuel de travail aec python : 

```bash
python -m venv " nom de l'environnement "
```
Dans un deuxième temps nous devrons cloner Tensorflow pour l'utiliser dans son dossier de projet:

```bash
git clone https://github.com/tensorflow/models.git
```
Il faudra ensuite activé son environnement de travail et installer toutes les bibliotèques.

> Activer l'environnement : 

```bash
.\nom de l_environnement\Scripts\activate # Windows 
```
> Installer les dépendances : 
> Installation de protocol buffer (manipulation possible sur Windows) avec la dernière version sur : 
 
 https://github.com/protocolbuffers/protobuf/releases
 
> Puis compiler protos dans votre dossier models/research : 
```bash
protoc object_detection/protos/*.proto --python_out=.
```
> Il faut ensuite copier le setup.py dans le dossier object_detection/packages/tf2/setup.py
> dans votre dossier courant research : 
```bash
python -m pip install .
```
> Pour vérifier si tout a bien été installer il faut exécuter la lige suivante :
```bash
python object_detection/builders/model_builder_tf2_test.py
```

# Deuxième pas 

Maintenant que tout est installé correctement, il faut ensuite préparer son dataset. 
Pour cela nous devrons utiliser LabelImg.py pour labiliser les données.
LabelImg permet de faire des boundings boxes autour des objets désirées.

> LabelImg GitHub

Il faudra ensuite placer environ 80 % des images avec leurs fichiers .xml dans un dossier "train" et 20 % dans un dossier "test".

# Troisième étape

Avec nos images labellisées nous allons créer des Tfrecords pour utiliser notre model. Pohur cela nous ne pouvons passer par des fichiers XML mais des fichiers CSV.
Pour cela on peut exécuter le fichier xml_to_csv.py : 

```bash
python xml_to_csv.py
```

Nous aurons donc deux nouveaux fichier : test_labels.csv et train_labels.csv.
Nous pouvons ensuite passer à la creéation de nos Tfrecords avec le fichier generate_tfrecords.py.

```bash
python generate_tfrecords.py
```
> Il faudra faire attention à bien modfifier une partie du logiciel avec vos propres labels : 

```bash
def class_text_to_int(row_label):
    if row_label == 'trash_can':
        return 1
    elif row_label == 'trash_cup':
        return 2
    elif row_label == 'trash_bag':
        return 3
    elif row_label == 'trash_bottle':
        return 4
    else:
        return None
```
