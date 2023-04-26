import os
import re

def read_tex_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except Exception as e:
        try:
            print(f"\tWARNING: {e} occured, trying latin-1 encoding...")
            with open(file_path, 'r', encoding='latin-1') as file:
                return file.readlines()
        except Exception as e:
            raise Exception(e)

def find_main_tex_file(directory):
    documentclass_pattern = re.compile(r'\\documentclass')

    for root, _, files in os.walk(directory):
        # special case for some old submissions, they are already merged
        
        if len(files)==1:
            print(f"Detected single file for {directory}, please verify that this is correct...")
            file_path = os.path.join(root, files[0])
            return file_path
        
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.tex'):
                with open(file_path, 'r') as tex_file:
                    for line in tex_file:
                        if documentclass_pattern.search(line):
                            return file_path

    raise FileNotFoundError(f"No main .tex file found in the specified directory {directory}")

def process_input_commands(file_lines, file_dir):
    input_pattern = re.compile(r'\\input\{(.+?)\}')
    output_lines = []

    for line in file_lines:
        if not line.strip().startswith('%'):
            while match := input_pattern.search(line):
                input_relative_path = match.group(1).replace('\\', '/')
                input_file_path = os.path.normpath(os.path.join(file_dir, input_relative_path))

                if not input_file_path.endswith('.tex'):
                    input_file_path += '.tex'

                if not os.path.isfile(input_file_path):
                    input_file_path = os.path.normpath(os.path.join(file_dir, '..', input_relative_path))
                    if not input_file_path.endswith('.tex'):
                        input_file_path += '.tex'

                input_file_dir = os.path.dirname(input_file_path)
                input_file_lines = read_tex_file(input_file_path)

                input_file_content = process_input_commands(input_file_lines, input_file_dir)

                line = line[:match.start()] + ''.join(input_file_content) + line[match.end():]

        output_lines.append(line)

    return output_lines

def merge_tex_files(main_tex_path):
    main_tex_dir = os.path.dirname(main_tex_path)
    main_tex_lines = read_tex_file(main_tex_path)

    merged_tex_lines = process_input_commands(main_tex_lines, main_tex_dir)

    return ''.join(merged_tex_lines)