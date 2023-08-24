import argparse
from func import concat_files

def parse_args():
    parser = argparse.ArgumentParser(description='Merge text files together')
    parser.add_argument('--input-dir', type=str, help='Path to input directory with caption files', required=True)
    parser.add_argument('--output-dir', type=str, help='Save to an alternative directory')
    parser.add_argument('--input-ext', type=str, help='Comma-separated list of file extensions to merge', default='caption,tags')
    parser.add_argument('--output-ext', type=str, help='Output file extension', default='txt')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    extensions = args.input_ext.split(',')
    concat_files(args.input_dir, args.output_dir, extensions, args.output_ext)