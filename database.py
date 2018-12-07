from shutil import copy, copytree
import os


class Database(object):

    class MyObject:

        def __init__(self, id, label, name):
            self.id = id
            self.label = label
            self.name = name
            self.num = 0

        def get_id(self):
            return self.id

        def get_label(self):
            return self.label

        def get_num(self):
            return self.num

        def update_num(self):
            self.num += 1

    def __init__(self, input_file_path, output_file_path):
        self.my_obj_list = []
        self.read_obj_list(input_file_path[0])
        self.input_file = input_file_path[1:]
        self.output_dir = output_file_path
        self.img_not_found = 0

    def get_num_object_found(self):
        obj_found = []
        for my_obj in self.my_obj_list:
            obj_found.append(my_obj.get_num())
        return obj_found

    def get_img_not_found(self):
        return self.img_not_found

    def copy_image(self, src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)
        try:
            copy(src, dst)
        except FileNotFoundError:
            self.img_not_found += 1
            return False
        except IsADirectoryError:
            copytree(src, dst)
            return True

        return True

    def read_obj_list(self, file_path):
        # example:

        # item
        # {
        #     name: "/m/0d4v4"
        #     id: 13
        #     display_name: "window"
        # }

        with open(file_path, 'r') as txt_file:
            line = txt_file.readline()
            while line:
                label = txt_file.readline().split("\"")[1]
                idx = int(txt_file.readline().split(" ")[3].split("\n")[0])
                name = txt_file.readline().split("\"")[1]

                self.my_obj_list.append(self.MyObject(idx, label, name))
                txt_file.readline()
                line = txt_file.readline()

    def is_my_obj(self, idx):
        if type(idx) is int:
            length = len(self.my_obj_list)
            if 0 < idx < length+1 and length > 0:
                for i in range(length):
                    if idx == self.my_obj_list[i].get_id():
                        return True
        return False

    def convert_label2idx(self, label):
        for my_obj in self.my_obj_list:
            if my_obj.label == label:
                return my_obj.get_id()
        return -1

    def convert_idx2label(self, idx):
        for my_obj in self.my_obj_list:
            if my_obj.idx == idx:
                return my_obj.label
        return "None"
