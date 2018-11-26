import numpy as np
import json
import csv
from shutil import copy, copytree
import os


class Database(object):

    def __init__(self, input_file_path, output_file_path):

        self.input_file = input_file_path
        self.output_dir = output_file_path
        # 0.Desk, 1.Mouse, 2.Keyboard, 3.Mug, 4.Office_supplies, 5.Monitor, 6.Window
        self.num_object_found = np.zeros(7)
        self.img_not_found = 0

    def get_num_object_found(self):
        return self.num_object_found

    def get_img_not_found(self):
        return self.img_not_found

    def copy_image(self, src, dst):

        if not os.path.exists(dst):
            os.makedirs(dst)
        # if the image doesn't exist, it is not added to selected_images
        try:
            copy(src, dst)
        except OSError:
            self.img_not_found += 1
            return False

        return True


class OpenimageDB(Database):

    def img_selector(self):

        # labels of the object we are looking for:
        # /m/01y9k5 (Desk), /m/020lf (mouse), /m/01m2v (Computer keyboard), /m/02jvh9 (Mug),
        # /m/02rdsp (Office supplies), /m/02522 (Computer monitor), /m/0d4v4 (Window)
        my_categories = ["/m/01y9k5", "/m/020lf", "/m/01m2v", "/m/02jvh9", "/m/02rdsp", "/m/02522", "/m/0d4v4"]

        # compute label_map file
        selected_label = ""

        with open(self.input_file[0], 'r') as txtfile:
            line = txtfile.readline()
            while line:
                line = txtfile.readline()
                category_name = line.split(" ")[3].split("\"")[1]
                if category_name in my_categories:
                    selected_label += "item {\n" + line + txtfile.readline() + txtfile.readline() + txtfile.readline()
                else:
                    txtfile.readline()
                    txtfile.readline()
                    txtfile.readline()

                line = txtfile.readline()

        file_name = self.input_file[0].split("/")
        new_label_map = self.output_dir + "/annotations/new_" + file_name[len(file_name)-1]
        if not os.path.exists(self.output_dir + "/annotations"):
            os.makedirs(self.output_dir + "/annotations")
        with open(new_label_map, 'w+') as outfile:
            outfile.write(selected_label)

        # we do this procedure for train and validation and test annotations/images
        for i in range(3):

            directory_name = self.input_file[i + 7].split("/")

            print("   START: " + directory_name[len(directory_name)-1])

            print("      1. Loading csv file...")

            # take only the box line we need
            selected_box = ''

            with open(self.input_file[i+1], 'r') as csvfile:
                csv_reader = csv.reader(csvfile)

                print("      2. Computing categories and images...")

                for row in csv_reader:
                    if row[1] in my_categories:
                        # copy image if exist
                        image_path = self.input_file[i+7] + "/" + row[0] + ".jpg"
                        copied = self.copy_image(image_path, self.output_dir + "/images/" + directory_name[len(directory_name)-1])
                        # add line to the new file
                        if copied:
                            selected_box += ','.join(row) + "\n"
                            # update statistics
                            self.update_found_object(row[1])
                        else:
                            self.img_not_found += 1

            file_name = self.input_file[i+1].split("/")
            new_box_file = self.output_dir + "/annotations/new_" + file_name[len(file_name)-1]
            if not os.path.exists(self.output_dir + "/annotations"):
                os.makedirs(self.output_dir + "/annotations")
            with open(new_box_file, 'w+') as outfile:
                outfile.write(selected_box)

            print("      3. Computing verification...")

            # take only the verification line we need
            selected_verification = ''

            with open(self.input_file[i + 4], 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if row[2] in my_categories:
                        # add line to the new file
                        selected_verification += ','.join(row) + "\n"

            file_name = self.input_file[i + 4].split("/")
            new_verification_file = self.output_dir + "/annotations/new_" + file_name[len(file_name) - 1]
            if not os.path.exists(self.output_dir + "/annotations"):
                os.makedirs(self.output_dir + "/annotations")
            with open(new_verification_file, 'w+') as outfile:
                outfile.write(selected_verification)

            print("   END: " + directory_name[len(directory_name)-1])

    def update_found_object(self, category_id):

        # /m/01y9k5 (Desk), /m/020lf (mouse), /m/01m2v (Computer keyboard), /m/02jvh9 (Mug),
        # /m/02rdsp (Office supplies), /m/02522 (Computer monitor), /m/0d4v4 (Window)

        # 0.Desk, 1.Mouse, 2.Keyboard, 3.Mug, 4.Office_supplies, 5.Monitor, 6.Window

        switcher = {
            "/m/01y9k5": 0,
            "/m/020lf": 1,
            "/m/01m2v": 2,
            "/m/02jvh9": 3,
            "/m/02rdsp": 4,
            "/m/02522": 5,
            "/m/0d4v4": 6,
        }

        my_obj = switcher.get(category_id, -1)
        if my_obj >= 0:
            self.num_object_found[my_obj] += 1


class CocoDB(Database):

    def img_selector(self):

        # labels of the object we are looking for:
        # 47(cup), 67(dining table), 72(tv), 74(mouse), 76(keyboard)
        my_categories = [47, 67, 72, 74, 76]

        # we do this procedure for train and validation and test annotations/images
        for i in range(3):

            # directory name could be: train..., valid... or test..
            directory_name = self.input_file[i].split("/")
            # path where we are going to save the selected images
            images_out_path = self.output_dir + '/images/' + directory_name[len(directory_name)-1]

            print("   START: " + directory_name[len(directory_name)-1])

            selected_datas = {}

            print("      1. Loading json file...")

            # open json file
            with open(self.input_file[i+3]) as annotation_file:
                datas = json.load(annotation_file)

            # name of the original json file
            file_name = self.input_file[i+3].split("/")
            # path where we are going to save the new json file
            annotations_out_path = self.output_dir + "/annotations/new_" + file_name[len(file_name)-1]

            # copy all the info
            selected_datas['info'] = datas['info']
            # copy all the licenses
            selected_datas['licenses'] = datas['licenses']

            print("      2. Computing categories...")

            # copy only the used categories
            selected_categories = []
            categories_data = datas['categories']
            for category in categories_data:
                if category['id'] in my_categories:
                    selected_categories.append(category)
            selected_datas['categories'] = selected_categories

            # copy only the used annotations and the used images
            selected_annotations = []
            selected_images = []

            try:
                annotations_datas = datas['annotations']
                print("      3. Computing annotations and images...")
            except:
                selected_datas['images'] = datas['images']
                # copy all the image in the directory
                copytree(self.input_file[i], images_out_path)
                # write the json file
                if not os.path.exists(self.output_dir + "/annotations"):
                    os.makedirs(self.output_dir + "/annotations")
                with open(annotations_out_path, 'w+') as outfile:
                    json.dump(selected_datas, outfile)
                print("   END: " + directory_name[len(directory_name) - 1])
                continue

            images_datas = datas['images']

            for annotation in annotations_datas:
                # check if is one of mine objects
                if annotation['category_id'] in my_categories:
                    # add the object to the selected list
                    selected_annotations.append(annotation)
                    # update object_found array
                    self.update_found_object(annotation['category_id'])
                    # copy the image in the new location
                    for image in images_datas:
                        if image['id'] == annotation['image_id']:
                            image_path = self.input_file[i] + "/" + image['file_name']
                            copied = self.copy_image(image_path, images_out_path)
                            # add line to the new file
                            if copied:
                                selected_images.append(image)
                            else:
                                self.img_not_found += 1

            selected_datas['annotations'] = selected_annotations
            selected_datas['images'] = selected_images

            # write the json file
            if not os.path.exists(self.output_dir + "/annotations"):
                os.makedirs(self.output_dir + "/annotations")
            with open(annotations_out_path, 'w+') as outfile:
                json.dump(selected_datas, outfile)

            print("   END: " + directory_name[len(directory_name)-1])

    def update_found_object(self, category_id):

        # 0.Desk, 1.Mouse, 2.Keyboard, 3.Mug, 4.Office_supplies, 5.Monitor, 6.Window
        # 47(cup), 67(dining table), 72(tv), 74(mouse), 76(keyboard)

        switcher = {
            47: 3,
            67: 0,
            72: 5,
            74: 1,
            76: 2
        }

        my_obj = switcher.get(category_id, -1)
        if my_obj >= 0:
            self.num_object_found[my_obj] += 1


class ImageNetDB(Database):

    def img_selector(self):
        pass
