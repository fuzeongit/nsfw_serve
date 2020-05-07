from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import os
from os import listdir
from os.path import isfile, join

import numpy as np
import tensorflow as tf
from tensorflow import keras

from nsfw_serve import settings

model = tf.keras.models.load_model(settings.BASE_DIR + "/nsfw_mobilenet2.224x224.h5")

IMAGE_DIM = 224


def load_images(image_paths, image_size):
    loaded_images = []
    loaded_image_paths = []

    if os.path.isdir(image_paths):
        print('wut')
        parent = image_paths
        image_paths = [join(parent, f) for f in listdir(image_paths) if isfile(join(parent, f))]
    else:
        print('wut1')
        image_paths = [image_paths]

    for i, img_path in enumerate(image_paths):
        try:
            image = keras.preprocessing.image.load_img(img_path, target_size=image_size)
            image = keras.preprocessing.image.img_to_array(image)
            image /= 255
            loaded_images.append(image)
            loaded_image_paths.append(img_path)
        except Exception as ex:
            print(i, img_path, ex)

    return np.asarray(loaded_images), loaded_image_paths


def main(image_path):
    images, image_paths = load_images(image_path,
                                      (IMAGE_DIM, IMAGE_DIM))

    model_predicts = model.predict(images)

    predicts = np.argsort(model_predicts, axis=1).tolist()

    probs = []

    categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    for i, single_preds in enumerate(predicts):
        single_probs = []
        for j, pred in enumerate(single_preds):
            single_probs.append(model_predicts[i][pred])
            predicts[i][j] = categories[pred]

        probs.append(single_probs)

    list = []

    for i, loaded_image_path in enumerate(image_paths):
        list.append({
            'url': loaded_image_path,
            'probability': {}
        })
        for _ in range(len(predicts[i])):
            list[i]["probability"][predicts[i][_]] = str(probs[i][_])

    return json.dumps(list, sort_keys=True, indent=2)
