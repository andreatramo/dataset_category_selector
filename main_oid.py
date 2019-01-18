from openimage_db import OpenimageDB
import tensorflow as tf
from tfrecord_utils import TFRecordWriter
import os
import random


tf.flags.DEFINE_string('input_label_map', "/home/andreatramo/datasets/openimage/my_oid_label_map.pbtxt",
                       'Path to the label map proto')

tf.flags.DEFINE_string('input_train_box', "/home/andreatramo/datasets/openimage/openimage_original/annotations/train-annotations-bbox.csv",
                       'Path to CSV containing train image bounding box annotations')
tf.flags.DEFINE_string('input_val_box', "/home/andreatramo/datasets/openimage/openimage_original/annotations/validation-annotations-bbox.csv",
                       'Path to CSV containing validation image bounding box annotations')
tf.flags.DEFINE_string('input_test_box', "/home/andreatramo/datasets/openimage/openimage_original/annotations/test-annotations-bbox.csv",
                       'Path to CSV containing test image bounding box annotations')

tf.flags.DEFINE_string('input_train_verification', "/home/andreatramo/datasets/openimage/openimage_original/annotations/train-annotations-human-imagelabels-boxable.csv",
                       'Path to CSV containing train image-level labels annotations')
tf.flags.DEFINE_string('input_val_verification', "/home/andreatramo/datasets/openimage/openimage_original/annotations/validation-annotations-human-imagelabels-boxable.csv",
                       'Path to CSV containing validation image-level labels annotations')
tf.flags.DEFINE_string('input_test_verification', "/home/andreatramo/datasets/openimage/openimage_original/annotations/test-annotations-human-imagelabels-boxable.csv",
                       'Path to CSV containing test image-level labels annotations')

tf.flags.DEFINE_string('input_train_dir', "/home/andreatramo/datasets/openimage/openimage_original/images/train",
                       'Path to the train image directory')
tf.flags.DEFINE_string('input_val_dir', "/home/andreatramo/datasets/openimage/openimage_original/images/val",
                       'Path to the validation image directory')
tf.flags.DEFINE_string('input_test_dir', "/home/andreatramo/datasets/openimage/openimage_original/images/test",
                       'Path to the test image directory')

tf.flags.DEFINE_string('output_dir', "/home/andreatramo/datasets/openimage/my_openimage",
                       'Path to the output directory')

FLAGS = tf.flags.FLAGS


def main():

    # check if there are all the input
    required_flags = [
        'input_label_map',
        'input_train_box', 'input_val_box', 'input_test_box',
        'input_train_verification', 'input_val_verification', 'input_test_verification',
        'input_train_dir', 'input_val_dir', 'input_test_dir',
        'output_dir'
    ]
    for flag_name in required_flags:
        if not getattr(FLAGS, flag_name):
            raise ValueError('Flag --{} is required'.format(flag_name))

    print("\n********** OpenImage **********")

    input_file = {0: [FLAGS.input_train_box, FLAGS.input_train_verification, FLAGS.input_train_dir, "train"],
                  1: [FLAGS.input_val_box, FLAGS.input_val_verification, FLAGS.input_val_dir, "validation"],
                  2: [FLAGS.input_test_box, FLAGS.input_test_verification, FLAGS.input_test_dir, "test"]}

    images_not_found = 0

    step = 3
    img_list = []

    for i in range(step):
        now_input = [FLAGS.input_label_map,
                     input_file[i][0],
                     input_file[i][1],
                     input_file[i][2],
                     input_file[i][3]]
        database = OpenimageDB(now_input, FLAGS.output_dir)
        img_list += database.img_selector()
        if i == 0:
            object_found = database.get_num_object_found()
        else:
            object_found += database.get_num_object_found()
        images_not_found += database.get_img_not_found()

    # shuffle the entire dataset and divide it in train, test and validation set

    # shuffle list
    random.shuffle(img_list)

    train_percentage = 0.8
    val_percentage = 0.1
    test_percentage = 1 - train_percentage - val_percentage

    train_thr = int(len(img_list)*train_percentage)
    val_thr = int(len(img_list)*val_percentage)
    test_thr = int(len(img_list) * test_percentage)

    train_img = img_list[:train_thr]
    val_img = img_list[train_thr:val_thr]
    test_img = img_list[val_thr:]

    # write the images and labels in a TFRecord
    for i in range(3):
        if i == 0:
            tfrecord_path = FLAGS.output_dir + "/" + "train_oid_dataset.tfrecord_1"
            list_to_write = train_img
        if i == 1:
            tfrecord_path = FLAGS.output_dir + "/" + "val_oid_dataset.tfrecord_1"
            list_to_write = val_img
        if i == 2:
            tfrecord_path = FLAGS.output_dir + "/" + "test_oid_dataset.tfrecord_1"
            list_to_write = test_img

        n = 1
        while os.path.exists(tfrecord_path):
            n += 1
            tfrecord_path = tfrecord_path[:len(tfrecord_path) - 1] + str(n)

        writer = TFRecordWriter(tfrecord_path)
        writer.write_tfrecord(list_to_write)
        writer.close_tfrecord()

    print("Number of object found: " + str(object_found))
    print("Number of images not found: " + str(images_not_found))

    return


if __name__ == '__main__':
    main()
