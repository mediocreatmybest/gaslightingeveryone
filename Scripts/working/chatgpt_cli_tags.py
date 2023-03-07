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
    parser.add_argument("--input", type=str, help="directory to search for files", required=True)
    parser.add_argument("--input-extension", default=".tags", type=str, help="file extension to search for")
    parser.add_argument("--output-extension", default=".caption", type=str, help="file extension for output files")
    parser.add_argument("--question", type=str, help="question to prepend to the response", required=True)
    args = parser.parse_args()

    bot = ChatGPT()

    for file_path in search_files(args.input, args.input_extension):
        process_file(file_path, args.output_extension, args.question)
        print(f"\nQ: {args.question}\n")
        print(f"A: {read_file(file_path)}\n")

