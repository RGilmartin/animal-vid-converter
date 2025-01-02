import ffmpeg # type: ignore
import os
import subprocess

def collect_mp4(base_dir):
        """Walks through the given directory and creates a 2d array of all mp4 files in subdirectories

        Args:
            base_dir (string): the absolute path of the base directory to walk

        Returns:
            string[][]: A 2d array of the returned files and their relation
        """
        folder_mp4_mapping = {}
        index = 0
        for root, dirs, files in os.walk(base_dir):
            #skip base folder, only process subfolders
            if root == base_dir:
                continue
            #add mp4 files to list
            abs_files = []
            for file in files: 
                abs_files.append(os.path.normpath(root)+"\\"+file)
            mp4_files = abs_files
            #add mp4 files to map if there are any 
            if mp4_files:
                folder_mp4_mapping[os.path.basename(os.path.normpath(root))] = mp4_files
            index+=1
        return folder_mp4_mapping
    
def compress_files(files): 
    
    success = True

    if files: 
        for input_file in files: 
            try:
                dir, filename = os.path.split(input_file)
                new_filename = f"compressed_{filename}"
                output_file = os.path.join(dir, new_filename)
                in_file = os.path.normpath(input_file)
                # Build and execute the FFmpeg command
                
                command = ['ffmpeg', '-y', '-i', in_file, '-b:a', '128k', '-crf', '24', '-preset', 'veryfast', '-vcodec', 'libx264', output_file]
                subprocess.call(command, shell=True)
                
                print(f"Conversion successful: {output_file}")
            except ffmpeg.Error as e:
                print(f"Error during conversion: {e}")
                success = False
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                success = False
                
    return success