import argparse
from os import path

def add_arguments(parser):
  parser.register('type', 'bool', lambda v: v.lower() == 'true')

  parser.add_argument('--input_base_path', type=str, help='Base path for input files')
  parser.add_argument('--output_base_path', type=str, help='Base path for output files')
  parser.add_argument('--src_input_name', type=str, help='Input file of source language (training)')
  parser.add_argument('--tgt_input_name', type=str, help='Input file of target language (training)')
  parser.add_argument('--merge_vocab', type='bool', help='Whether only one vocab file should be created')
  parser.add_argument('--src_vocab_name', type=str, help='Output file of source language')
  parser.add_argument('--tgt_vocab_name', type=str, default='', help='Output file of target language')
  parser.add_argument('--unk_token', type=str, default='<unk>', help='Token for unknown')
  parser.add_argument('--sos_src', type=str, default='<s>', help='Token for start of sentence in source')
  parser.add_argument('--sos_tgt', type=str, default='</s>', help='Token for end of sentence in source')
  parser.add_argument('--eos_src', type=str, default='<s>', help='Token for start of sentence in target')
  parser.add_argument('--eos_tgt', type=str, default='</s>', help='Token for end of sentence in target')

def create_vocab(input_path, output_path, append=False, shared_set = None, preload_words=list()):
  if shared_set is None:
    shared_set = set()

  if not append:
    with open(output_path, 'w') as output_file:
      for word in preload_words:
        add_word(word, shared_set, output_file)

  with open(input_path, 'r') as input_file:
    with open(output_path, 'a') as output_file:
      for line in input_file:
        words = line.split(' ')
        for word in words:
          add_word(word, shared_set, output_file)

def add_word(word, word_set, file):
  word = word.strip('\n')
  if word not in word_set:
    word_set.add(word)
    file.write(word + '\n')

def main(FLAGS):
  src_file_path = path.join(FLAGS.input_base_path, FLAGS.src_input_name)
  tgt_file_path = path.join(FLAGS.input_base_path, FLAGS.tgt_input_name)
  print('Source path: %s; Target path: %s' % (src_file_path, tgt_file_path))
  preload_words = [
    FLAGS.unk_token,
    FLAGS.sos_src,
    FLAGS.sos_tgt,
    FLAGS.eos_src,
    FLAGS.eos_tgt
  ]
  print('Preload words:', preload_words)
  if FLAGS.merge_vocab:
    vocab_path = path.join(FLAGS.output_base_path, FLAGS.src_vocab_name)
    print('Shared vocab path', vocab_path)

    shared_set = set()

    create_vocab(input_path=src_file_path, output_path=vocab_path, append=False, shared_set=shared_set, preload_words=preload_words)
    create_vocab(input_path=tgt_file_path, output_path=vocab_path, append=True, shared_set=shared_set)
  else:
    src_vocab_path = path.join(FLAGS.output_base_path, FLAGS.src_vocab_name)
    tgt_vocab_path = path.join(FLAGS.output_base_path, FLAGS.tgt_vocab_name)
    print('Source vocab path: %s; Target vocab path: %s' % (src_vocab_path, tgt_vocab_path))

    create_vocab(input_path=src_file_path, output_path=src_vocab_path, append=False, shared_set=None)
    create_vocab(input_path=tgt_file_path, output_path=tgt_vocab_path, append=False, shared_set=None)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  add_arguments(parser)
  FLAGS, unparsed = parser.parse_known_args()
  main(FLAGS)
