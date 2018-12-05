from database import OpenimageDB, CocoDB, ImageNetDB


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

    label_map = "/Users/Andrea/Documents/datasets/my_label_map.pbtxt"

    # OpenImage database: START

    print("\n********** OpenImage **********")

    # for Linux
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

    # OpenImage database: END

    # COCO database: START

    print("\n********** COCO **********")

    # for Linux
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

    # COCO database: END

    # ImageNet database: START

    # print(\n********** ImageNet **********")
    #
    # in_path = "/home/user/datasets/imagenet/original_imagenet"
    # out_path = "/home/user/datasets/imagenet/my_imagenet"
    #
    # database = ImageNetDB(in_path, out_path)
    # database.img_selector()

    # ImageNet database: END


if __name__ == '__main__':
    main()
