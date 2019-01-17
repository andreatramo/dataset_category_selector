from database import Database
import csv
import tensorflow as tf
from labeled_image import LabeledImage
from PIL import Image


class OpenimageDB(Database):

    def __init__(self, input_file_path, output_file_path):
        super(OpenimageDB, self).__init__(input_file_path, output_file_path)
        self.read_obj_list(input_file_path[0])

    def img_selector(self):

        directory_name = self.input_file[3]

        print("   START: " + directory_name)

        print("      1. Loading csv file...")

        with open(self.input_file[0], 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            print("      2. Computing categories and images...")

            # Declare a dictionary
            img_dict = dict()

            for row in csv_reader:

                # we jump the first line with the label name
                if row[2] == "LabelName":
                    continue

                idx = self.convert_label2idx(row[2])

                # double check
                if self.is_my_obj(idx) and self.my_obj_list[idx-1].get_num() < self.my_obj_list[idx-1].MAX_OBJ_NUM:

                    image_path = self.input_file[2] + "/" + row[0] + ".jpg"

                    # if the image is yet in the dictionary
                    if row[0] in img_dict:
                        labeled_img = img_dict[row[0]]
                        exist = True
                    else:
                        labeled_img = LabeledImage()
                        with tf.gfile.Open(image_path, 'rb') as image_file:
                            exist = True

                            img = Image.open(image_path)
                            labeled_img.width, labeled_img.height = img.size
                            img.close()

                            labeled_img.filename = str.encode(row[0])
                            labeled_img.encoded = image_file.read()

                            img_dict[row[0]] = labeled_img

                    labeled_img.xmins.append(float(row[4]))
                    labeled_img.xmaxs.append(float(row[5]))
                    labeled_img.ymins.append(float(row[6]))
                    labeled_img.ymaxs.append(float(row[7]))

                    labeled_img.is_occluded.append(int(row[8]))
                    labeled_img.is_truncated.append(int(row[9]))
                    labeled_img.is_group_of.append(int(row[10]))
                    labeled_img.is_depicted.append(int(row[11]))
                    labeled_img.is_inside.append(int(row[12]))

                    labeled_img.text.append(str.encode(row[2]))
                    labeled_img.label.append(idx)

                    # add line to the new file
                    if exist:
                        # update statistics
                        self.my_obj_list[idx-1].update_num()
                    else:
                        self.img_not_found += 1

        print("   END: " + directory_name)

        return img_dict
