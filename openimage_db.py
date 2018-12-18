from database import Database
import csv
import os


class OpenimageDB(Database):

    def __init__(self, input_file_path, output_file_path):
        super(OpenimageDB, self).__init__(input_file_path, output_file_path)
        self.read_obj_list(input_file_path[0])

    def img_selector(self):

        directory_name = self.input_file[3]

        print("   START: " + directory_name)

        print("      1. Loading csv file...")

        # take only the box lines we need
        selected_box = ''

        with open(self.input_file[0], 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            print("      2. Computing categories and images...")

            for row in csv_reader:
                if row[2] == "LabelName":
                    selected_box += ','.join(row) + "\n"
                    continue
                idx = self.convert_label2idx(row[2])
                if self.is_my_obj(idx) and self.my_obj_list[idx-1].get_num() < self.my_obj_list[idx-1].MAX_OBJ_NUM:
                    # copy image if exist
                    image_path = self.input_file[2] + "/" + row[0] + ".jpg"
                    copied = self.copy_image(image_path, self.output_dir + "/images/" + directory_name)
                    # add line to the new file
                    if copied:
                        selected_box += ','.join(row) + "\n"
                        # update statistics
                        self.my_obj_list[idx-1].update_num()
                    else:
                        self.img_not_found += 1

        file_name = self.input_file[0].split("/")
        new_box_file = self.output_dir + "/annotations/new_" + file_name[len(file_name)-1]
        if not os.path.exists(self.output_dir + "/annotations"):
            os.makedirs(self.output_dir + "/annotations")
        with open(new_box_file, 'w+') as outfile:
            outfile.write(selected_box)

        print("      3. Computing verification...")

        # take only the verification line we need
        selected_verification = ''

        with open(self.input_file[1], 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if row[2] == "LabelName":
                    selected_box += ','.join(row) + "\n"
                    continue
                idx = self.convert_label2idx(row[2])
                if self.is_my_obj(idx):
                    # add line to the new file
                    selected_verification += ','.join(row) + "\n"

        file_name = self.input_file[1].split("/")
        new_verification_file = self.output_dir + "/annotations/new_" + file_name[len(file_name) - 1]
        if not os.path.exists(self.output_dir + "/annotations"):
            os.makedirs(self.output_dir + "/annotations")
        with open(new_verification_file, 'w+') as outfile:
            outfile.write(selected_verification)

        print("   END: " + directory_name)
