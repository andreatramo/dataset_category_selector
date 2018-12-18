from coco_db import CocoDB
import tensorflow as tf

tf.flags.DEFINE_string('input_label_map', "/home/andreatramo/datasets/coco/my_coco_label_map.pbtxt",
                       'Path to the label map proto')

tf.flags.DEFINE_string('input_train_annotations', "/home/andreatramo/datasets/coco/coco_original/annotations/annotations_trainval2017/annotations/instances_train2017.json",
                       'Path to CSV containing train image bounding box annotations')
tf.flags.DEFINE_string('input_val_annotations', "/home/andreatramo/datasets/coco/coco_original/annotations/annotations_trainval2017/annotations/instances_val2017.json",
                       'Path to CSV containing validation image bounding box annotations')
tf.flags.DEFINE_string('input_test_annotations', "/home/andreatramo/datasets/coco/coco_original/annotations/image_info_test2017/annotations/image_info_test-dev2017.json",
                       'Path to CSV containing test image bounding box annotations')

tf.flags.DEFINE_string('input_train_dir', "/home/andreatramo/datasets/coco/coco_original/images/train2017",
                       'Path to the train image directory')
tf.flags.DEFINE_string('input_val_dir', "/home/andreatramo/datasets/coco/coco_original/images/val2017",
                       'Path to the validation image directory')
tf.flags.DEFINE_string('input_test_dir', "/home/andreatramo/datasets/coco/coco_original/images/test2017",
                       'Path to the test image directory')

tf.flags.DEFINE_string('output_dir', "/home/andreatramo/datasets/openimage/my_openimage",
                       'Path to the output directory')

FLAGS = tf.flags.FLAGS


def main():

    if FLAGS.database_type != "coco":
        print("UNCORRECT DATASET: use COCO dataset!")
        return

    # check if there are all the input
    required_flags = [
        'input_label_map',
        'input_train_annotations', 'input_val_annotations', 'input_test_annotations',
        'input_train_dir', 'input_val_dir', 'input_test_dir',
        'output_dir'
    ]
    for flag_name in required_flags:
        if not getattr(FLAGS, flag_name):
            raise ValueError('Flag --{} is required'.format(flag_name))

    print("\n********** COCO **********")

    input_file = {0: [FLAGS.input_train_annotations, FLAGS.input_train_dir, "train"],
                  1: [FLAGS.input_val_annotations, FLAGS.input_val_dir, "validation"],
                  2: [FLAGS.input_test_annotations, FLAGS.input_test_dir, "test"]}

    for i in range(3):
        now_input = [FLAGS.input_label_map,
                     input_file[i][0],
                     input_file[i][1],
                     input_file[i][2]]
        database = CocoDB(now_input, FLAGS.output_dir)
        database.img_selector()
        print("[ " + input_file[i][2] + " ]")
        print("    Number of object found: " + str(database.get_num_object_found()))
        print("    Number of images not found: " + str(database.get_img_not_found()))

    return


if __name__ == '__main__':
    main()
