from database import Database
import csv, sys
import tensorflow as tf
from labeled_image import LabeledImage
from PIL import Image


class OpenimageDB(Database):

    def __init__(self, input_file_path, output_file_path):
        super(OpenimageDB, self).__init__(input_file_path, output_file_path)
        self.read_obj_list(input_file_path[0])

    def img_selector(self):

        directory_name = self.input_file[2]

        print("START: " + directory_name)
        print("   1. Loading csv file...")

        with open(self.input_file[0], 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            print("      DONE!")
            print("   2. Computing labels and images...")

            # Declare a list
            img_list = []
            precedent_img = ""

            now_time = 0
            i = 0
            total_time = 14610230  # number computed using: sum(1 for line in csv_file)

            for row in csv_reader:
                percentage_time = int(100 * now_time / total_time)
                if percentage_time != i:
                    i = percentage_time
                    sys.stdout.write("\r" + "      On working: " + str(int(percentage_time)) + " %")
                    sys.stdout.flush()
                now_time += 1

                # we jump the first line with the label name
                if row[2] == "LabelName":
                    continue

                idx = self.convert_label2idx(row[2])

                # double check
                if self.is_my_obj(idx) and self.my_obj_list[idx-1].get_num() < self.my_obj_list[idx-1].MAX_OBJ_NUM:

                    image_path = self.input_file[1] + "/" + row[0] + ".jpg"

                    # if the image is yet in the list
                    # new_img = self.get_img(row[0])

                    # if the image is new
                    if row[0] != precedent_img:
                        labeled_img = LabeledImage()
                        with tf.gfile.Open(image_path, 'rb') as image_file:
                            exist = True

                            img = Image.open(image_path)
                            labeled_img.width, labeled_img.height = img.size
                            img.close()

                            labeled_img.filename = str.encode(row[0])
                            labeled_img.encoded = image_file.read()

                            img_list.append(labeled_img)

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

                    precedent_img = row[0]

                    # add line to the new file
                    if exist:
                        # update statistics
                        self.my_obj_list[idx-1].update_num()
                    else:
                        self.img_not_found += 1
        sys.stdout.write("\r" + "      DONE!")
        sys.stdout.flush()
        # print("END: " + directory_name)

        return img_list
