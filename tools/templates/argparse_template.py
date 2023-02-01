import argparse

def hello_world():
    """ Hello world, that's all folks. Sorry, Move along. """
    hello_world = print('Hello world! What an exciting time to be alive!')

    return hello_world

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hello-world', action='store_true', required=False)
    parser.add_argument('--input-dir', type=str, required=False)
    parser.add_argument('--output-dir', type=str, required=False)
    args = parser.parse_args()

    # Oh, hello!
    if args.hello_world:
        hello_world()
    else:
        print('Nothing to see here. Move along.')