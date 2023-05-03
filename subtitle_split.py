import os
import re

subs_path = 'subtitles/raw'
cn_subs_path = 'chinese_subtitles'
en_subs_path = 'english_subtitles'

def extract_timeline_and_content(input_file):
    # Read the input file and create a dictionary of subtitles with timeline keys
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    subtitles_dict = {}
    for i, line in enumerate(lines):
        line = line.strip()
        if re.match(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', line):
            timeline = line
            chinese = lines[i + 1].strip()
            english = lines[i + 2].strip()
            subtitles_dict[timeline] = {"chinese": chinese, "english": english}

    return subtitles_dict

def write_chinese_subtitles(subtitles_dict, output_file):
    # Write Chinese subtitles to output_file
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, (timeline, content) in enumerate(subtitles_dict.items()):
            f.write(f"{idx + 1}\n{timeline}\n{content['chinese']}\n\n")

def write_english_subtitles(subtitles_dict, output_file):
    # Write English subtitles to output_file
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, (timeline, content) in enumerate(subtitles_dict.items()):
            f.write(f"{idx + 1}\n{timeline}\n{content['english']}\n\n")

def process_filename(filename):
    # Generate Chinese and English output filenames
    basename, ext = os.path.splitext(filename)
    return basename + "_chinese" + ext, basename + "_english" + ext

def process_files():
    # Create output directories if they don't exist
    os.makedirs(cn_subs_path, exist_ok=True)
    os.makedirs(en_subs_path, exist_ok=True)

    # Iterate through all SRT files in the subtitles directory
    for filename in os.listdir(subs_path):
        if filename.endswith(".srt") and not filename.endswith("_chinese.srt") and not filename.endswith("_english.srt"):
            print(f"Processing {filename}")
            input_file = os.path.join(subs_path, filename)
            subtitles_dict = extract_timeline_and_content(input_file)
            chinese_output, english_output = process_filename(filename)
            write_chinese_subtitles(subtitles_dict, os.path.join(cn_subs_path, chinese_output))
            write_english_subtitles(subtitles_dict, os.path.join(en_subs_path, english_output))
            print(f"Generated {chinese_output} and {english_output}\n")

# Traverse all subtitle files under current directory and generate Chinese and English subtitles.
process_files()