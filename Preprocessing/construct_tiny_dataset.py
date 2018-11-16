import json
import os.path

import os, random, shutil

# ori_json_path = "/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/src_dataset/caption_validation_annotation.json"
# pic_path=""
# with open(ori_json_path, "r") as f:
#     load_json_dic = json.load(f)
# id_caption = dict([(x['image_id'], x['caption']) for x in load_json_dic])
# print(id_caption)


def move_n_pic(n, src_path, dst_path):
    print('from : ' + src_path)
    print('to: ' + dst_path)
    src_dir = os.listdir(src_path)
    sample = random.sample(src_dir, n)
    print(sample)

    for name in sample:
        # shutil.copyfile(src_path + name, dst_path + name)
        shutil.move(src_path + name, dst_path + name)
    print("move %d files successfully", n)


def construct_json(src_json, pic_path, output_json):
    new_id_caption= []
    count = 0
    # load json data into python dic
    with open(src_json, "r") as f:
        load_json_dic = json.load(f)
        id_caption = dict([(x['image_id'], x['caption']) for x in load_json_dic])
    print("load source json succeed")
    for image_id in os.listdir(pic_path):
        caption = id_caption[image_id]
        new_id_caption.append(
            {
                "image_id": image_id,
                "caption": caption
            },
        )
        count = count + 1
    new_id_caption = json.dumps(new_id_caption).encode('utf-8')
    data = json.loads(new_id_caption)
    with open(output_json, 'w') as f:
        json.dump(data, f)
    print("wrotten %d items into json", count)


if __name__ == '__main__':
    src_path = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/src_dataset/images/'
    train_set = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/train_set/images/'
    validation_set = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/validation_set/images/'
    test_set = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/test_set/images/'
    src_json = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/src_dataset/caption_validation_annotation.json'
    train_json = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/train_set/train.json'
    validation_json = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/validation_set/validation.json'
    test_json = '/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/test_set/test.json'

   # move_n_pic(n=20000, src_path=src_path, dst_path=train_set)
    #move_n_pic(n=8000, src_path=src_path, dst_path=validation_set)
    # move_n_pic(n=2000, src_path=src_path, dst_path=test_set)
    #
    construct_json(src_json, train_set, train_json)
    construct_json(src_json, validation_set, validation_json)
    construct_json(src_json, test_set, test_json)
