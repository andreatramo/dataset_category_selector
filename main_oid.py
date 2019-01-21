from openimage_db import OpenimageDB
import tensorflow as tf
from tfrecord_utils import write_tfrecord
import os
import random


tf.flags.DEFINE_string('input_label_map',
                       "/home/andreatramo/datasets/openimage/my_oid_label_map.pbtxt",
                       'Path to the label map proto')

tf.flags.DEFINE_string('input_train_label',
                       "/home/andreatramo/datasets/openimage/openimage_original/annotations/train-annotations-bbox.csv",
                       'Path to CSV containing train image bounding box annotations')
tf.flags.DEFINE_string('input_val_label',
                       None,#"/home/andreatramo/datasets/openimage/openimage_original/annotations/validation-annotations-bbox.csv",
                       'Path to CSV containing validation image bounding box annotations')
tf.flags.DEFINE_string('input_test_label',
                       None,#"/home/andreatramo/datasets/openimage/openimage_original/annotations/test-annotations-bbox.csv",
                       'Path to CSV containing test image bounding box annotations')

tf.flags.DEFINE_string('input_train_dir',
                       "/home/andreatramo/datasets/openimage/openimage_original/images/train",
                       'Path to the train image directory')
tf.flags.DEFINE_string('input_val_dir',
                       None,#"/home/andreatramo/datasets/openimage/openimage_original/images/val",
                       'Path to the validation image directory')
tf.flags.DEFINE_string('input_test_dir',
                       None,#"/home/andreatramo/datasets/openimage/openimage_original/images/test",
                       'Path to the test image directory')

tf.flags.DEFINE_string('output_dir',
                       "/home/andreatramo/datasets/openimage/my_openimage",
                       'Path to the output directory')

tf.flags.DEFINE_string('subdivision_mode', "100",
                       'Instruction about how to divide the data')
FLAGS = tf.flags.FLAGS


def main():

    # check if there are all the input
    required_flags = [
        'input_label_map',
        'output_dir'
    ]
    for flag_name in required_flags:
        if not getattr(FLAGS, flag_name):
            raise ValueError('Flag --{} is required'.format(flag_name))

    step = 0
    input_file = dict()

    if (FLAGS.input_train_label is not None) and (FLAGS.input_train_dir is not None):
        input_file[step] = [FLAGS.input_train_label, FLAGS.input_train_dir, "train"]
        step += 1
    elif (FLAGS.input_train_label is None) ^ (FLAGS.input_train_dir is None):
        raise ValueError('One between train annotations path or train images directory, is not present.')
    if (FLAGS.input_val_label is not None) and (FLAGS.input_val_dir is not None):
        input_file[step] = [FLAGS.input_val_label, FLAGS.input_val_dir, "validation"]
        step += 1
    elif (FLAGS.input_val_label is None) ^ (FLAGS.input_val_dir is None):
        raise ValueError('One between validation annotations path or validation images directory, is not present.')
    if (FLAGS.input_test_label is not None) and (FLAGS.input_test_dir is not None):
        input_file[step] = [FLAGS.input_test_label, FLAGS.input_test_dir, "test"]
        step += 1
    elif (FLAGS.input_test_label is None) ^ (FLAGS.input_test_dir is None):
        raise ValueError('One between test annotations path or test images directory, is not present.')

    if step < 1:
        raise ValueError('No train, test or validation path present. Give in input almost one of them.')

    print("\n********** OpenImage **********")

    images_not_found = 0
    img_list = []

    print("1. Reading csv file...")

    for i in range(step):
        now_input = [FLAGS.input_label_map,
                     input_file[i][0],
                     input_file[i][1],
                     input_file[i][2]]
        database = OpenimageDB(now_input, FLAGS.output_dir)
        img_list += database.img_selector()
        if i == 0:
            object_found = database.get_num_object_found()
        else:
            object_found += database.get_num_object_found()
        images_not_found += database.get_img_not_found()

    # shuffle the entire dataset and divide it in train, test and validation set

    print("\n   Number of object found: " + str(object_found))
    print("   Number of images not found: " + str(images_not_found))

    print("\n2. Image subdivision and tfrecord writing...")

    # shuffle list
    random.shuffle(img_list)

    test_percentage = 0
    val_percentage = 0
    step = 0

    sub_mode = int(FLAGS.subdivision_mode)

    if sub_mode == 111:
        test_percentage = 0.1
        val_percentage = 0.1
        step = 3
    elif sub_mode == 110:
        val_percentage = 0.1
        step = 2
    elif sub_mode == 101:
        test_percentage = 0.1
        step = 2
    elif sub_mode == 11:
        test_percentage = 0.5
        val_percentage = 0.5
        step = 2
    elif sub_mode == 0:
        test_percentage = 0
        val_percentage = 0
        step = 1

    train_percentage = 1 - test_percentage - val_percentage

    train_thr = int(len(img_list)*train_percentage)
    val_thr = int(len(img_list)*val_percentage) + train_thr
    test_thr = int(len(img_list) * test_percentage) + val_thr

    train_img = img_list[:train_thr]
    val_img = img_list[train_thr:val_thr]
    test_img = img_list[val_thr:test_thr]

    # write the images and labels in a TFRecord
    for i in range(step):
        if step == 1:
            tfrecord_path = FLAGS.output_dir + "/" + "my_oid_dataset_1"
            list_to_write = train_img
        else:
            if i == 0 and sub_mode > 100:
                tfrecord_path = FLAGS.output_dir + "/" + "train_oid_dataset_1"
                list_to_write = train_img
            elif (i == 1 and sub_mode > 100) or (i == 0 and 0 < sub_mode < 100):
                tfrecord_path = FLAGS.output_dir + "/" + "val_oid_dataset_1"
                list_to_write = val_img
            elif (i == 2 and sub_mode > 110) or (i == 1 and 0 < sub_mode < 100):
                tfrecord_path = FLAGS.output_dir + "/" + "test_oid_dataset_1"
                list_to_write = test_img

        n = 1
        while os.path.exists(tfrecord_path + ".tfrecord"):
            n += 1
            if n < 11:
                tfrecord_path = tfrecord_path[:len(tfrecord_path) - 1] + str(n)
            else:
                tfrecord_path = tfrecord_path[:len(tfrecord_path) - 2] + str(n)

        tfrecord_path += ".tfrecord" 
        write_tfrecord(tfrecord_path, list_to_write)
    print("      DONE!")

    print("\n   Number of train, validation and test images: "
          "[" + str(train_thr) + ", "
          + str(val_thr - train_thr) + ", "
          + str(test_thr - val_thr) + "]")

    print("********** OpenImage **********")

    return


if __name__ == '__main__':
    main()
