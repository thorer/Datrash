# Object detection Datrash Model
Object_detection

# Présentation
Dans le cardre d'un Master Camp, nous avons souhaité développer un outil de détection de déchets à l'aide d'une intelligence artificielle.
Pour cela, nous avons utilisé une intelligence artificielle basé sur une détection en "boxes" à l'aide de Tensorflow V2.

# Premiers pas : Installation de l'environnement
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

# Deuxième pas : Labéllisation des images.

Maintenant que tout est installé correctement, il faut ensuite préparer son dataset. 
Pour cela nous devrons utiliser LabelImg.py pour labiliser les données.
LabelImg permet de faire des boundings boxes autour des objets désirées.

> LabelImg GitHub

Il faudra ensuite placer environ 80 % des images avec leurs fichiers .xml dans un dossier "train" et 20 % dans un dossier "test".

# Troisième étape : TFRecords et LabelMap

Avec nos images labellisées nous allons créer des Tfrecords pour utiliser notre model. Pohur cela nous ne pouvons passer par des fichiers XML mais des fichiers CSV.
Pour cela on peut exécuter le fichier xml_to_csv.py : 

```bash
python xml_to_csv.py
```

Nous aurons donc deux nouveaux fichier : test_labels.csv et train_labels.csv.
Nous pouvons ensuite passer à la création de nos Tfrecords avec le fichier generate_tfrecords.py.

> Il faudra faire attention à bien modifier une partie du logiciel avec vos propres labels : 

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
Pour générer les TFrecords on peut utiliser cette commande :

```bash
python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record
python generate_tfrecord.py --csv_input=images/test_labels.csv --image_dir=images/test --output_path=test.record
```
> Cela va générer deux fichiers : train.record et test.record

Pour finir avec cette étape, il faut créer un Label_map pour pouvoir entraîner notre modèle choisi.

> Ne pas oublier de garder les mêmes noms de labels et id que dans generate_tfrecords.py 

```bash
item {
    id: 1
    name: 'trash_can'
}
item {
    id: 2
    name: 'trash_cup'
}
item {
    id: 3
    name: 'trash_bag'
}
item {
    id: 4
    name: 'trash_bottle'
}
```

# Quatrième étape : Préparation Training

Pour entraîner votre model, vous devrais en choisir un sur [Tensorflow 2 Detection Model Zoo]
(https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2_detection_zoo.md)
Il faudra ensuite modifier dans votre model le path vers votre label_map ainsi que vos fichier tf.records : 

````bash
train_input_reader: {
  label_map_path: "C:/Users/tomca/Documents/Master_camp3/models/research/training/label_map.pbtxt"
  tf_record_input_reader {
    input_path: "C:/Users/tomca/Documents/Master_camp3/models/research/object_detection/train.record"
  }
}

eval_config: {
  metrics_set: "coco_detection_metrics"
  use_moving_averages: false
  batch_size: 1;
}

eval_input_reader: {
  label_map_path: "C:/Users/tomca/Documents/Master_camp3/models/research/training/label_map.txt"
  shuffle: false
  num_epochs: 1
  tf_record_input_reader {
    input_path: "C:/Users/tomca/Documents/Master_camp3/models/research/object_detection/test.record"
  }
}

````
Je vous conseil également si vous le souhaitez de diminuer le batch_size à 1 ainsi que fine_tune_checkpoint_type en mettant detection.

# Cinquième étape : Training

Pour entraîner le modèle vous pouvez utiliser la commande suivante : 

```bash
python model_main_tf2.py --pipeline_config_path=training/ssd_efficientdet_d0_512x512_coco17_tpu-8.config --model_dir=training --alsologtostderr

```
Si vous souhaitez visualiser pour visualiser vos résultats grâce à Tensorboard :

```bash
tensorboard --logdir=training/train
```
# Sixième étape : Exporter son training

Vous pouvez désormais exporter votre training pour pouvoir l'utiliser : 

```bash
python /content/models/research/object_detection/exporter_main_v2.py \
    --trained_checkpoint_dir training \
    --output_directory inference_graph \
    --pipeline_config_path training/ssd_efficientdet_d0_512x512_coco17_tpu-8.config
```
