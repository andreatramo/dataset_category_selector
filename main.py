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

    label_map = "/home/user/datasets/my_label_map.pbtxt"

    # OpenImage database: START

    print("\n********** OpenImage **********")

    train_box = "/home/user/datasets/openimage/original_openimage/annotations/train-annotations-bbox.csv"
    val_box = "/home/user/datasets/openimage/original_openimage/annotations/validation-annotations-bbox.csv"
    test_box = "/home/user/datasets/openimage/original_openimage/annotations/test-annotations-bbox.csv"
    train_verification = "/home/user/datasets/openimage/original_openimage/annotations/train-annotations-human-" \
                         "imagelabels-boxable.csv"
    val_verification = "/home/user/datasets/openimage/original_openimage/annotations/validation-annotations-human-" \
                       "imagelabels-boxable.csv"
    test_verification = "/home/user/datasets/openimage/original_openimage/annotations/test-annotations-human-" \
                        "imagelabels-boxable.csv"
    train_image_dir = "/home/user/datasets/openimage/original_openimage/images/train"
    val_image_dir = "/home/user/datasets/openimage/original_openimage/images/validation"
    test_image_dir = "/home/user/datasets/openimage/original_openimage/images/test"
    output_dir = "/home/user/datasets/openimage/my_openimage"

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

    train_image_dir = "/home/user/cocoapi/coco/images/train2017"
    val_image_dir = "/home/user/cocoapi/coco/images/val2017"
    test_image_dir = "/home/user/cocoapi/coco/images/test2017"
    train_annotations_file = "/home/user/cocoapi/coco/annotations/annotations_trainval2017/annotations/instances_" \
                             "train2017.json"
    val_annotations_file = "/home/user/cocoapi/coco/annotations/annotations_trainval2017/annotations/instances_" \
                           "val2017.json"
    testdev_annotations_file = "/home/user/cocoapi/coco/annotations/image_info_test2017/annotations/image_info_" \
                               "test-dev2017.json"
    output_dir = "/home/user/datasets/coco/my_coco"

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
