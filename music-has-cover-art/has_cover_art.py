import sys
import os
import eyed3


def has_cover_art(file_path):
    try:
        audiofile = eyed3.load(file_path)
        if audiofile is not None:
            tag = audiofile.tag
            if tag is not None:
                if tag.frame_set.get('APIC') is not None or tag.frame_set.get(3) is not None:
                    return True
                elif tag.frame_set.get('PIC') is not None:
                    return True
                elif tag.images:
                    return True
    except eyed3.core.Eyed3Error:
        print(f"Error processing file: {file_path}")
    return False


def collect_files_without_cover_art(directory_path):
    files_without_cover_art = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.mp3', '.ogg', '.flac')):
                file_path = os.path.join(root, file)
                if not has_cover_art(file_path):
                    # Get the last two folder names and the file name
                    folders = os.path.normpath(file_path).split(os.sep)[-3:]
                    display_path = os.path.join(*folders)
                    print(f"{display_path}: No cover art found. :(")
                    files_without_cover_art.append(display_path)
    return files_without_cover_art


def write_list_to_file(file_list, output_file):
    with open(output_file, 'w') as file:
        for item in file_list:
            file.write("%s\n" % item)


def process_music_directory(music_path, output_file):
    if os.path.exists(music_path):
        if os.path.isdir(music_path):
            result = collect_files_without_cover_art(music_path)
            if result:
                print("Files without cover art:")
                for file_path in result:
                    print(file_path)

                # Write the list to the specified output file
                write_list_to_file(result, output_file)
                print(f"List written to {output_file}")
            else:
                print("All checked files have cover art.")
        else:
            if has_cover_art(music_path):
                print("This music file has cover art!")
            else:
                print("No cover art found. :(")
    else:
        print("Path not found. Check your input.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_music_directory>")
    else:
        music_path = sys.argv[1]
        output_file = "output.txt"
        if sys.argv.__len__() == 3:
            output_file = sys.argv[2]

        process_music_directory(music_path, output_file)
