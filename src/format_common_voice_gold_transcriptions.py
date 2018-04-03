'''
Create the gold transcription files for the Common Voice dataset
wget https://common-voice-data-download.s3.amazonaws.com/cv_corpus_v1.tar.gz
'''

import glob
import os
import pandas as pd

def main():
    data_folder = os.path.join('..','data','cv-valid-test')
    df = pd.read_csv('cv-valid-test.csv')

    for index, row in df.iterrows():
        speech_filepath = row['filename']
        print('speech_filepath: {0}'.format(speech_filepath))
        speech_filename = speech_filepath.split('/')[-1][:-4]
        print('speech_filename: {0}'.format(speech_filename))
        gold_transcription_filepath_text = os.path.join(data_folder, speech_filename + '_gold.txt')
        gold_transcription_file = open(gold_transcription_filepath_text, 'w')

        gold_transcription = row['text']
        print('os.path.basename(speech_filepath): {0}'.format(os.path.basename(speech_filepath)))
        print('gold_transcription: {0}'.format(gold_transcription))
        gold_transcription_file.write(gold_transcription)
        gold_transcription_file.close()

if __name__ == "__main__":
    main()
    #cProfile.run('main()') # if you want to do some profiling