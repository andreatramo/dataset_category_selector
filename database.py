import json
import csv
from shutil import copy, copytree
import os


class Database(object):

    NUM_OBJECT = 13

    class MyObject:

        def __init__(self, id, label, name):
            self.id = id
            self.label = label
            self.name = name
            self.num = 0

        def get_id(self):
            return self.id

        def update_num(self):
            self.num += 1

        def get_num(self):
            return self.num

    def __init__(self, input_file_path, output_file_path):

        self.my_obj_list = []
        self.read_obj_list(input_file_path[0])
        self.input_file = input_file_path[1:]
        self.output_dir = output_file_path
        self.img_not_found = 0

    def get_num_object_found(self):
        return self.my_obj_list

    def get_img_not_found(self):
        return self.img_not_found

    def copy_image(self, src, dst):

        if not os.path.exists(dst):
            os.makedirs(dst)
        try:
            copy(src, dst)
        except OSError:
            self.img_not_found += 1
            return False

        return True

    def read_obj_list(self, file_path):

        # example:

        # item
        # {
        #     name: "/m/0d4v4"
        #     id: 11
        #     display_name: "window"
        # }

        with open(file_path, 'r') as txtfile:
            line = txtfile.readline()
            while line:
                label = txtfile.readline().split("\"")[1]
                idx = int(txtfile.readline().split(" ")[3].split("\n")[0])
                name = txtfile.readline().split("\"")[1]

                self.my_obj_list.append(self.MyObject(idx, label, name))
                txtfile.readline()
                line = txtfile.readline()

    def is_in(self, idx):

        length = len(self.my_obj_list)
        if 0 < idx < 13 and length > 0:
            for i in range(length):
                if idx == self.my_obj_list[i]:
                    return True
        return False


class OpenimageDB(Database):

    def img_selector(self):

        # we do this procedure for train and validation and test annotations/images
        for i in range(3):

            directory_name = self.input_file[i + 6].split("/")

            print("   START: " + directory_name[len(directory_name)-1])

            print("      1. Loading csv file...")

            # take only the box line we need
            selected_box = ''

            with open(self.input_file[i], 'r') as csvfile:
                csv_reader = csv.reader(csvfile)

                print("      2. Computing categories and images...")

                for row in csv_reader:
                    if self.is_in(row[1]):
                        # copy image if exist
                        image_path = self.input_file[i+6] + "/" + row[0] + ".jpg"
                        copied = self.copy_image(image_path, self.output_dir + "/images/" + directory_name[len(directory_name)-1])
                        # add line to the new file
                        if copied:
                            selected_box += ','.join(row) + "\n"
                            # update statistics
                            self.my_obj_list[row[1]].update_num()
                        else:
                            self.img_not_found += 1

            file_name = self.input_file[i].split("/")
            new_box_file = self.output_dir + "/annotations/new_" + file_name[len(file_name)-1]
            if not os.path.exists(self.output_dir + "/annotations"):
                os.makedirs(self.output_dir + "/annotations")
            with open(new_box_file, 'w+') as outfile:
                outfile.write(selected_box)

            print("      3. Computing verification...")

            # take only the verification line we need
            selected_verification = ''

            with open(self.input_file[i + 3], 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    if self.is_in(row[2]):
                        # add line to the new file
                        selected_verification += ','.join(row) + "\n"

            file_name = self.input_file[i + 3].split("/")
            new_verification_file = self.output_dir + "/annotations/new_" + file_name[len(file_name) - 1]
            if not os.path.exists(self.output_dir + "/annotations"):
                os.makedirs(self.output_dir + "/annotations")
            with open(new_verification_file, 'w+') as outfile:
                outfile.write(selected_verification)

            print("   END: " + directory_name[len(directory_name)-1])


class CocoDB(Database):

    def img_selector(self):

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
                if self.is_in(category['id']):
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
                if self.is_in(annotation['category_id']):
                    # add the object to the selected list
                    selected_annotations.append(annotation)
                    # update object_found array
                    self.my_obj_list[annotation['category_id']].update_num()
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


class ImageNetDB(Database):

    def img_selector(self):
        pass
