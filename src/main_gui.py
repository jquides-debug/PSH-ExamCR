import tkinter as tk
from datetime import datetime

import file_handling
import grid_info as grid_i
import user_interface
from process_input import process_input


def main():
    user_input = user_interface.MainWindow()
    while user_input.wait_for_batch():
        try:
            image_paths = file_handling.filter_images(
                file_handling.list_file_paths(user_input.input_folder))
            progress_tracker = user_input.create_and_pack_progress(len(image_paths))
            process_input(
                image_paths,
                user_input.output_folder,
                user_input.multi_answers_as_f,
                user_input.empty_answers_as_g,
                user_input.keys_file,
                user_input.arrangement_map,
                user_input.sort_results,
                user_input.output_mcta,
                user_input.debug_mode,
                grid_i.form_150q,
                progress_tracker,
                datetime.now())
        except tk.TclError:
            if not user_input.cancelled:
                raise
        finally:
            if not user_input.cancelled:
                user_input.reset_for_next_batch()
        if user_input.cancelled:
            break


if __name__ == "__main__":
    main()
