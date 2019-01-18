import tensorflow as tf


def int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def int64_list_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def bytes_list_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=value))


def float_list_feature(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))


def create_tf_example(example):

    height = example.height  # Image height
    width = example.width  # Image width
    filename = example.filename  # Filename of the image. Empty if image is not from file
    encoded_image_data = example.encoded  # Encoded image bytes
    image_format = example.format  # b'jpeg' or b'png'

    xmins = example.xmins  # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = example.xmaxs  # List of normalized right x coordinates in bounding box (1 per box)
    ymins = example.ymins  # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = example.ymaxs  # List of normalized bottom y coordinates in bounding box (1 per box)

    is_occluded = example.is_occluded
    is_truncated = example.is_truncated
    is_group_of = example.is_group_of
    is_depicted = example.is_depicted
    is_inside = example.is_inside

    classes_text = example.text  # List of string class name of bounding box (1 per box)
    classes = example.label  # List of integer class id of bounding box (1 per box)

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': int64_feature(height),
        'image/width': int64_feature(width),
        'image/filename': bytes_feature(filename),
        'image/source_id': bytes_feature(filename),
        'image/encoded': bytes_feature(encoded_image_data),
        'image/format': bytes_feature(image_format),
        'image/object/bbox/xmin': float_list_feature(xmins),
        'image/object/bbox/xmax': float_list_feature(xmaxs),
        'image/object/bbox/ymin': float_list_feature(ymins),
        'image/object/bbox/ymax': float_list_feature(ymaxs),
        'image/object/bbox/is_occluded': int64_list_feature(is_occluded),
        'image/object/bbox/is_truncated': int64_list_feature(is_truncated),
        'image/object/bbox/is_group_of': int64_list_feature(is_group_of),
        'image/object/bbox/is_depicted': int64_list_feature(is_depicted),
        'image/object/bbox/is_inside': int64_list_feature(is_inside),
        'image/object/class/is_inside': bytes_list_feature(classes_text),
        'image/object/class/label': int64_list_feature(classes),
    }))
    return tf_example


def write_tfrecord(path, examples):
    # Initiating the writer and creating the tfrecords file.
    writer = tf.python_io.TFRecordWriter(path)
    for example in examples:
        tf_example = create_tf_example(example)
        # Writing the serialized example.
        writer.write(tf_example.SerializeToString())
    writer.close()



