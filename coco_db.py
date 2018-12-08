from database import Database
import json
import os


class CocoDB(Database):

    class MyCocoObject(Database.MyObject):

        def __init__(self, idx, label, name, coco_id):
            super(CocoDB.MyCocoObject, self).__init__(idx, label, name)
            self.coco_id = coco_id

        def get_coco_id(self):
            return self.coco_id

    def __init__(self, input_file_path, output_file_path):
        super(CocoDB, self).__init__(input_file_path, output_file_path)
        self.read_obj_list(input_file_path[0])

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
                if self.is_my_obj(category['id']):
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
                self.copy_image(self.input_file[i], images_out_path)
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
                idx = self.convert_cocoid2id(annotation['category_id'])
                # if self.is_my_obj(idx):
                if idx > 0:
                    # add the object to the selected list
                    selected_annotations.append(annotation)
                    # update object_found array
                    self.my_obj_list[idx].update_num()
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

    def read_obj_list(self, file_path):
        # example:

        # item
        # {
        #     name: "/m/0d4v4"
        #     id: 13
        #     coco_id: 56
        #     display_name: "window"
        # }

        with open(file_path, 'r') as txt_file:
            line = txt_file.readline()
            while line:
                label = txt_file.readline().split("\"")[1]
                idx = int(txt_file.readline().split(" ")[3].split("\n")[0])
                coco_idx = int(txt_file.readline().split(" ")[3].split("\n")[0])
                name = txt_file.readline().split("\"")[1]

                self.my_obj_list.append(self.MyCocoObject(idx, label, name, coco_idx))
                txt_file.readline()
                line = txt_file.readline()

    def convert_cocoid2id(self, coco_idx):
        for my_obj in self.my_obj_list:
            if coco_idx == my_obj.get_coco_id():
                return my_obj.get_id()
        return -1
