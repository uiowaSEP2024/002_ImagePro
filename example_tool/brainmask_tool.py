import argparse


def main():
    parser = argparse.ArgumentParser(description='Process input and output directory paths.')

    # Define the input directory argument
    parser.add_argument('-i', '--input_dir_path', required=True,
                        help='Path to the input directory')

    # Define the output directory argument
    parser.add_argument('-o', '--output_dir_path', required=True,
                        help='Path to the output directory')

    # Parse the arguments
    args = parser.parse_args()

    # You can now use args.input_dir_path and args.output_dir_path
    # For example, print them:
    print("Input Directory:", args.input_dir_path)
    print("Output Directory:", args.output_dir_path)


if __name__ == "__main__":
    main()
