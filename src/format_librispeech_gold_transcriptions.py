'''
Create the gold transcription files for the LibriSpeech test-clean and LibriSpeech test-other datasets

wget http://www.openslr.org/resources/12/test-clean.tar.gz
wget http://www.openslr.org/resources/12/test-other.tar.gz
'''

import glob
import os
import shutil
import utils

def main():
    for dataset in ['test-clean', 'test-other']:

        # Copy files
        data_folder = os.path.join('..','data','LibriSpeech', dataset)
        print('data_folder: {0}'.format(data_folder))
        destination_data_folder = os.path.join('..', 'data','librispeech-{0}'.format(dataset))
        utils.create_folder_if_not_exists(destination_data_folder)
        speech_filepaths = utils.get_all_filepaths(data_folder, 'flac')
        transcript_filepaths = utils.get_all_filepaths(data_folder, 'txt')
        print('speech_filepaths: {0}'.format(speech_filepaths))
        for filepath in speech_filepaths + transcript_filepaths:
            destination_filepath = os.path.join(destination_data_folder, os.path.basename(filepath))
            shutil.copyfile(filepath, destination_filepath)

        # Generate gold transcripts
        transcription_filepaths = glob.glob(os.path.join(destination_data_folder,'*.txt'))
        for transcription_filepath in transcription_filepaths:
            print('transcription_filepath: {0}'.format(transcription_filepath))
            transcription_file = open(transcription_filepath,'r')
            for transcription_line in transcription_file:
                transcription_line = transcription_line.strip()
                speech_file_id = transcription_line.split(' ')[0]
                transcription = ' '.join(transcription_line.split(' ')[1:])
                with open(os.path.join(destination_data_folder,'{0}_gold.txt'.format(speech_file_id)),'w') as file:
                    file.write(transcription)

            transcription_file.close()
            os.remove(transcription_filepath)

if __name__ == "__main__":
    main()
    #cProfile.run('main()') # if you want to do some profiling