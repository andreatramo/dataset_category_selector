class LabeledImage(object):

    def __init__(self):

        self.height = -1
        self.width = -1
        self.filename = ""
        self.source_id = -1
        self.encoded = -1
        self.format = str.encode('jpeg')

        self.xmins = []
        self.xmaxs = []
        self.ymins = []
        self.ymaxs = []

        self.is_occluded = []
        self.is_truncated = []
        self.is_group_of = []
        self.is_depicted = []
        self.is_inside = []

        self.text = []
        self.label = []

    # def set_height(self, val):
    #     self.height = val
    #
    # def set_width(self, val):
    #     self.width = val
    #
    # def set_filename(self, val):
    #     self.filename = val
    #
    # def set_source_id(self, val):
    #     self.source_id = val
    #
    # def set_encoded(self, val):
    #     self.encoded = val
    #
    # def set_format(self, val):
    #     self.format = val
    #
    # def set_xmin(self, val):
    #     self.xmin = val
    #
    # def set_xmax(self, val):
    #     self.xmax = val
    #
    # def set_ymin(self, val):
    #     self.ymin = val
    #
    # def set_ymax(self, val):
    #     self.ymax = val
    #
    # def set_text(self, val):
    #     self.text = val
    #
    # def set_label(self, val):
    #     self.label = val
    #
    # def get_height(self):
    #     return self.height
    #
    # def get_width(self):
    #     return self.width
    #
    # def get_filename(self):
    #     return self.filename
    #
    # def get_source_id(self):
    #     return self.source_id
    #
    # def get_encoded(self):
    #     return self.encoded
    #
    # def get_format(self):
    #     return self.format
    #
    # def get_xmin(self):
    #     return self.xmin
    #
    # def get_xmax(self):
    #     return self.xmax
    #
    # def get_ymin(self):
    #     return self.ymin
    #
    # def get_ymax(self):
    #     return self.ymax
    #
    # def get_text(self):
    #     return self.text
    #
    # def get_label(self):
    #     return self.label
