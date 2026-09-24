import argparse
import sys
from datetime import datetime

import file_handling
from file_handling import parse_path_arg
import grid_info as grid_i
from process_input import process_input


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='OpenMCR: An accurate and simple exam bubble sheet reading tool.\n'
                                                 'Reads sheets from input folder, process and saves result in output folder.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_folder',
                        help='Path to a folder containing scanned input sheets.\n'
                             'Ignores subfolders.',
                        type=parse_path_arg)
    parser.add_argument('output_folder',
                        help='Path to a folder to save result to.',
                        type=parse_path_arg)
    parser.add_argument('--anskeys',
                        help='CSV file containing one answer key for scoring.',
                        type=parse_path_arg)
    parser.add_argument('--variant',
                        default='150',
                        choices=['150'],
                        help='Answer sheet format: 150 questions (the organization standard).')
    parser.add_argument('-ml', '--multiple',
                        action='store_true',
                        help='Convert multiple answers in a question to F, instead of [A|B].')
    parser.add_argument('-e', '--empty',
                        action='store_true',
                        help='Save empty answers as G. By default, they will be saved as blank values.')
    parser.add_argument('-s', '--sort',
                        action='store_true',
                        help="Sort output by Examinee ID")
    parser.add_argument('-d', '--debug',
                        action='store_true',
                        help='Turn debug mode on. Additional directory with debug data will be created.')
    parser.add_argument('--mcta',
                        action='store_true',
                        help='Output additional files for Multiple Choice Test Analysis.')
    parser.add_argument('--disable-timestamps',
                        action='store_true',
                        help='Disable timestamps in file names. Useful when consistent file names are required. Existing files will be overwritten without warning!')

    # prints help and exits when called w/o arguments
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    image_paths = file_handling.filter_images(file_handling.list_file_paths(args.input_folder))
    output_folder = args.output_folder
    multi_answers_as_f = args.multiple
    empty_answers_as_g = args.empty
    keys_file = args.anskeys
    arrangement_file = None
    sort_results = args.sort
    output_mcta = args.mcta
    debug_mode_on = args.debug
    form_variant = grid_i.form_150q
    files_timestamp = datetime.now().replace(microsecond=0) if not args.disable_timestamps else None
    print(arrangement_file)
    process_input(image_paths,
                  output_folder,
                  multi_answers_as_f,
                  empty_answers_as_g,
                  keys_file,
                  arrangement_file,
                  sort_results,
                  output_mcta,
                  debug_mode_on,
                  form_variant,
                  None,
                  files_timestamp)
