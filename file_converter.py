import sys
import subprocess

def main():
    """
    Converts files from one format to another.
    - Usage: python convert_files.py <original> <converted>
    - Requires ffmpeg.
    """
    num_args = len(sys.argv)
    if num_args != 3:
        print("Usage: python convert_files.py <original> <converted>")
        return
    
    original_file_name = sys.argv[1]
    converted_file_name = sys.argv[2]

    command = ['ffmpeg', '-i', original_file_name, converted_file_name]
    try:
        subprocess.run(command, check=True)
        print("File converted successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error converting file: {e}")

    pass

if __name__ == "__main__":
    main()