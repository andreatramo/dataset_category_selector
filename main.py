from openimage_db import OpenimageDB
from coco_db import CocoDB
from imagenet_db import ImageNetDB
# import tensorflow as tf
#
# tf.flags.DEFINE_string('input_box_annotations_csv', None,
#                        'Path to CSV containing image bounding box annotations')
# tf.flags.DEFINE_string('input_images_directory', None,
#                        'Directory containing the image pixels '
#                        'downloaded from the OpenImages GitHub repository.')
# tf.flags.DEFINE_string('input_image_label_annotations_csv', None,
#                        'Path to CSV containing image-level labels annotations')
# tf.flags.DEFINE_string('input_label_map', None, 'Path to the label map proto')
# tf.flags.DEFINE_string('output_tf_record_path_prefix', None,
#                        'Path to the output TFRecord. The shard index and the number of shards '
#                        'will be appended for each output shard.')
# tf.flags.DEFINE_integer('num_shards', 100, 'Number of TFRecord shards')
#
# FLAGS = tf.flags.FLAGS

def main():

    # object list:
    #  - Book
    #  - Bookcase
    #  - Chair
    #  - Desk
    #  - Door
    #  - Filing Cabinet
    #  - Keyboard
    #  - Monitor
    #  - Mouse
    #  - Mug
    #  - Plant
    #  - Telephone
    #  - Window

    database_type = "coco"

    if database_type == "openimage":

        # # check if there are all the input
        # required_flags = [
        #     'input_box_annotations_csv', 'input_images_directory', 'input_label_map',
        #     'output_tf_record_path_prefix'
        # ]
        # for flag_name in required_flags:
        #     if not getattr(FLAGS, flag_name):
        #         raise ValueError('Flag --{} is required'.format(flag_name))
        #
        # x = FLAGS.input_label_map

        # OpenImage database: START

        print("\n********** OpenImage **********")

        # for Linux
        # label_map = "/home/andreatramo/datasets/openimage/my_oid_label_map.pbtxt"
        # train_box = "/home/andreatramo/datasets/openimage/openimage_original/annotations/train-annotations-bbox.csv"
        # val_box = "/home/andreatramo/datasets/openimage/openimage_original/annotations/validation-annotations-bbox.csv"
        # test_box = "/home/andreatramo/datasets/openimage/openimage_original/annotations/test-annotations-bbox.csv"
        # train_verification = "/home/andreatramo/datasets/openimage/openimage_original/annotations/train-annotations-human-" \
        #                      "imagelabels-boxable.csv"
        # val_verification = "/home/andreatramo/datasets/openimage/openimage_original/annotations/validation-annotations-human-" \
        #                    "imagelabels-boxable.csv"
        # test_verification = "/home/andreatramo/datasets/openimage/openimage_original/annotations/test-annotations-human-" \
        #                     "imagelabels-boxable.csv"
        # train_image_dir = "/home/andreatramo/datasets/openimage/openimage_original/images/train"
        # val_image_dir = "/home/andreatramo/datasets/openimage/openimage_original/images/validation"
        # test_image_dir = "/home/andreatramo/datasets/openimage/openimage_original/images/test"
        # output_dir = "/home/andreatramo/datasets/openimage/my_openimage"

        # for MAC
        label_map = "/Users/Andrea/Documents/datasets/openimage/my_oid_label_map.pbtxt"
        train_box = "/Users/Andrea/Documents/datasets/openimage/openimage_original/annotations/train-annotations-bbox.csv"
        val_box = "/Users/Andrea/Documents/datasets/openimage/openimage_original/annotations/validation-annotations-bbox.csv"
        test_box = "/Users/Andrea/Documents/datasets/openimage/openimage_original/annotations/test-annotations-bbox.csv"
        train_verification = "/Users/Andrea/Documents/datasets/openimage/openimage_original/annotations/train-annotations-human-" \
                             "imagelabels-boxable.csv"
        val_verification = "/Users/Andrea/Documents/datasets/openimage/openimage_original/annotations/validation-annotations-human-" \
                           "imagelabels-boxable.csv"
        test_verification = "/Users/Andrea/Documents/datasets/openimage/openimage_original/annotations/test-annotations-human-" \
                            "imagelabels-boxable.csv"
        train_image_dir = "/Users/Andrea/Documents/openimage/openimage_original/images/train"
        val_image_dir = "/Users/Andrea/Documents/datasets/openimage/openimage_original/images/validation"
        test_image_dir = "/Users/Andrea/Documents/datasets/openimage/openimage_original/images/test"
        output_dir = "/Users/Andrea/Documents/datasets/openimage/my_openimage"

        input_file = [label_map,
                      train_box, val_box, test_box,
                      train_verification, val_verification, test_verification,
                      train_image_dir, val_image_dir, test_image_dir]

        database = OpenimageDB(input_file, output_dir)
        database.img_selector()

        print("Number of object found: " + str(database.get_num_object_found()))
        print("Number of images not found: " + str(database.get_img_not_found()))

        return

        # OpenImage database: END

    if database_type == "coco":

        # COCO database: START

        print("\n********** COCO **********")

        # for Linux
        # label_map = "/home/andreatramo/datasets/coco/my_coco_label_map.pbtxt"
        # train_image_dir = "/home/andreatramo/datasets/coco/coco_original/images/train2017"
        # val_image_dir = "/home/andreatramo/datasets/coco/coco_original/images/val2017"
        # test_image_dir = "/home/andreatramo/datasets/coco/coco_original/images/test2017"
        # train_annotations_file = "/home/andreatramo/datasets/coco/coco_original/annotations/annotations_trainval2017/" \
        #                          "annotations/instances_train2017.json"
        # val_annotations_file = "/home/andreatramo/datasets/coco/coco_original/annotations/annotations_trainval2017/" \
        #                        "annotations/instances_val2017.json"
        # testdev_annotations_file = "/home/andreatramo/datasets/coco/coco_original/annotations/image_info_test2017/" \
        #                            "annotations/image_info_test-dev2017.json"
        # output_dir = "/home/andreatramo/datasets/coco/my_coco"

        # for MAC
        label_map = "/Users/Andrea/Documents/datasets/coco/my_coco_label_map.pbtxt"
        train_image_dir = "/Users/Andrea/Documents/datasets/coco/coco_original/images/train2017"
        val_image_dir = "/Users/Andrea/Documents/datasets/coco/coco_original/images/val2017"
        test_image_dir = "/Users/Andrea/Documents/datasets/coco/coco_original/images/test2017"
        train_annotations_file = "/Users/Andrea/Documents/datasets/coco/coco_original/annotations/instances_train2017.json"
        val_annotations_file = "/Users/Andrea/Documents/datasets/coco/coco_original/annotations/instances_val2017.json"
        testdev_annotations_file = "/Users/Andrea/Documents/datasets/coco/coco_original/annotations/image_info_test-dev2017.json"
        output_dir = "/Users/Andrea/Documents/datasets/coco/my_coco"

        input_file = [label_map,
                      train_image_dir, val_image_dir, test_image_dir,
                      train_annotations_file, val_annotations_file, testdev_annotations_file]

        database = CocoDB(input_file, output_dir)
        database.img_selector()

        print("Number of object found: " + str(database.get_num_object_found()))
        print("Number of images not found: " + str(database.get_img_not_found()))

        return

        # COCO database: END

    if database_type == "imagenet":

        # ImageNet database: START

        print("\n********** ImageNet **********")

        in_path = "/home/user/datasets/imagenet/original_imagenet"
        out_path = "/home/user/datasets/imagenet/my_imagenet"

        database = ImageNetDB(in_path, out_path)
        database.img_selector()

        print("Number of object found: " + str(database.get_num_object_found()))
        print("Number of images not found: " + str(database.get_img_not_found()))

        return

        # ImageNet database: END


if __name__ == '__main__':
    main()
