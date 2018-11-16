# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
r"""Generate captions for images using default beam search parameters."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
#import json


import tensorflow as tf

import configuration
import inference_wrapper
from inference_utils import caption_generator
from inference_utils import vocabulary

FLAGS = tf.flags.FLAGS

tf.flags.DEFINE_string(
    "checkpoint_path",
    "/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/model/",
    "Model checkpoint file or directory containing a model checkpoint file.")
tf.flags.DEFINE_string(
    "vocab_file",
    "/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/data/vocabulary.txt",
    "Text file containing the vocabulary.")
tf.flags.DEFINE_string(
    "input_files",
    "/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/test_set/images/0a3ae4b374fdfa9809bb0b46eb960ead32b22cd4.jpg",
    "File pattern or comma-separated list of file patterns of image files.")
# tf.flags.DEFINE_string(
#     "captions_file",
#     "/Users/yangyuxuan/workspace/PyCharm/Inception_v4_Mult_LSTM/test_set/model_output.json",
#     "Test captions JSON file.")

tf.logging.set_verbosity(tf.logging.INFO)


def main(_):
    # Build the inference graph.
    g = tf.Graph()
    with g.as_default():
        model = inference_wrapper.InferenceWrapper()
        print("start loading model from checkpoint... ")
        restore_fn = model.build_graph_from_config(configuration.ModelConfig(),
                                                   FLAGS.checkpoint_path)
        print("load model completed")
    g.finalize()

    # Create the vocabulary.
    vocab = vocabulary.Vocabulary(FLAGS.vocab_file)

    filenames = []
    for file_pattern in FLAGS.input_files.split(","):
        filenames.extend(tf.gfile.Glob(file_pattern))
    tf.logging.info("Running caption generation on %d files matching %s",
                    len(filenames), FLAGS.input_files)

    with tf.Session(graph=g) as sess:
        # Load the model from checkpoint.
        restore_fn(sess)

        # Prepare the caption generator. Here we are implicitly using the default
        # beam search parameters. See caption_generator.py for a description of the
        # available beam search parameters.
        generator = caption_generator.CaptionGenerator(model, vocab)
        # image_id_caption = []
        for filename in filenames:
            with tf.gfile.GFile(filename, "rb") as f:
                image = f.read()
            captions = generator.beam_search(sess, image)
            print("Captions for image %s:" % os.path.basename(filename))
            for i, caption in enumerate(captions):
                # Ignore begin and end words.
                sentence = [vocab.id_to_word(w)
                            for w in caption.sentence[1:-1]]
                sentence = "".join(sentence)
                print("  %d) %s (p=%f)" %
                      (i, sentence, math.exp(caption.logprob)))
                # if not i:
                #     image_id_caption.append(
                #         {
                #             "image_id": filename.split('/')[-1],
                #             "caption": sentence
                #         },)
        # image_id_caption = json.dumps(image_id_caption).encode('utf-8')
        # data = json.loads(image_id_caption)
        # with open(FLAGS.captions_file, 'w') as f:
        #     json.dump(data, f)
        # print("Saving captions file to path %s" % FLAGS.captions_file)


if __name__ == "__main__":
    tf.app.run()
