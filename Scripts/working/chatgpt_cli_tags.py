import argparse
import os

from chatgpt_wrapper import ChatGPT


def search_files(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                yield os.path.join(root, file)


def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


def write_file(file_path, content, extension):
    new_file_path = os.path.splitext(file_path)[0] + extension
    with open(new_file_path, "w") as f:
        f.write(content)


def process_file(file_path, extension, question):
    original_content = read_file(file_path)
    response = bot.ask(question + " " + original_content)
    write_file(file_path, response, extension)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A command line bot")
    parser.add_argument("directory", type=str, help="directory to search for files")
    parser.add_argument("extension", type=str, help="file extension to search for")
    parser.add_argument("output_extension", type=str, help="file extension for output files")
    parser.add_argument("question", type=str, help="question to prepend to the response")
    args = parser.parse_args()

    bot = ChatGPT()

    for file_path in search_files(args.directory, args.extension):
        process_file(file_path, args.output_extension, args.question)
