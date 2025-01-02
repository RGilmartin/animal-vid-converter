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
                pass
            except ffmpeg.Error as e:
                print(f"Error during conversion: {e}")
                success = False
            except Exception as e:
                print(f"An unexpected error occurred: {str(e)}")
                success = False
    
        dir, filename = os.path.split(files[0])
        stitch_videos_in_folder(dir,os.path.dirname(dir))
                
    return success

def stitch_videos_in_folder(folder_path, output_path):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    
    print(os.listdir(folder_path))
    
    # Get all MP4 files in the folder
    video_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.MP4') and 'compressed_' in f]
    print(video_files)
    # Ensure there are videos to stitch
    if len(video_files) < 2:
        raise ValueError("At least two videos are required to stitch.")

    # Create a temporary file to list the videos
    concat_file = os.path.join(folder_path, "concat_list.txt")
    with open(concat_file, "w") as f:
        for video in video_files:
            f.write(f"file '{video}'\n")
    
    # Use FFmpeg to stitch videos
    try:
        print(ffmpeg.input(concat_file, format="concat", safe=0).output(output_path, c="copy").compile())
        command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', f'{folder_path}\\concat_list.txt', '-c', 'copy', f'{output_path}\\{os.path.basename(folder_path)}.mp4']
        subprocess.call(command, shell=True)
        print(f"Successfully stitched videos into: {output_path}")
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode()}")
    finally:
        # Clean up the temporary concat file
        if os.path.exists(concat_file):
            os.remove(concat_file)