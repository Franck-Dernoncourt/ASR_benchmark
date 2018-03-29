'''
Use settings.ini to configure the benchmark.
'''

import configparser
import glob
import os
import transcribe
import metrics
import time
import collections
import shutil

def main():

    # Load setting file
    settings = configparser.ConfigParser()
    settings_filepath = 'settings.ini'
    settings.read(settings_filepath)

    asr_systems = settings.get('general','asr_systems').split(',')
    data_folder = settings.get('general','data_folder')
    speech_file_type = settings.get('general','speech_file_type')
    if speech_file_type not in ['flac', 'mp3', 'ogg', 'wav']:
        raise ValueError('You have set speech_file_type to be "{0}" in {1}. This is invalid. speech_file_type should be flac, ogg, mp3, or wav.'.
                         format(speech_file_type,settings_filepath))

    print('asr_systems: {0}'.format(asr_systems))
    print('data_folder: {0}'.format(data_folder))
    speech_filepaths = sorted(glob.glob(os.path.join(data_folder, '*.{0}'.format(speech_file_type))))

    if settings.getboolean('general','transcribe'):

        # Make sure there are files to transcribe
        if len(speech_filepaths) <= 0:
            raise ValueError('There is no file with the extension "{0}"  in the folder "{1}"'.
                             format(speech_file_type,data_folder))

        # Transcribe
        print('\n### Call the ASR engines to compute predicted transcriptions')
        for speech_file_number, speech_filepath in enumerate(speech_filepaths):

            # Convert the speech file from FLAC/MP3/Ogg to WAV
            if speech_file_type in ['flac', 'mp3', 'ogg']:
                from pydub import AudioSegment
                print('speech_filepath: {0}'.format(speech_filepath))
                sound = AudioSegment.from_file(speech_filepath, format=speech_file_type)
                new_speech_filepath = speech_filepath[:-len(speech_file_type)-1]+'.wav'
                sound.export(new_speech_filepath, format="wav")
                speech_filepath = new_speech_filepath


            # Transcribe the speech file
            all_transcription_skipped = True
            for asr_system in asr_systems:
                transcription, transcription_skipped = transcribe.transcribe(speech_filepath,asr_system,settings,save_transcription=True)
                all_transcription_skipped = all_transcription_skipped and transcription_skipped

            # If the speech file was converted from FLAC/MP3/Ogg to WAV, remove the WAV file
            if speech_file_type in ['flac', 'mp3', 'ogg']:
                os.remove(new_speech_filepath)

            if not all_transcription_skipped:
                time.sleep(settings.getint('general','delay_in_seconds_between_transcriptions'))

    if settings.getboolean('general','evaluate_transcriptions'):
        # Evaluate transcriptions
        all_texts = {}
        print('\n### Final evaluation of all the ASR engines based on their predicted jurisdictions')

        for asr_system in asr_systems:
            all_texts[asr_system] = {}

            all_predicted_transcription_filepath = 'all_predicted_transcriptions_' + asr_system + '.txt'
            all_gold_transcription_filepath = 'all_gold_transcriptions.txt'
            all_predicted_transcription_file = open(all_predicted_transcription_filepath, 'w')
            all_gold_transcription_filepath = open(all_gold_transcription_filepath, 'w')

            number_of_tokens_in_gold = 0
            number_of_empty_predicted_transcription_txt_files = 0
            number_of_missing_predicted_transcription_txt_files = 0
            edit_types = ['corrects', 'deletions', 'insertions', 'substitutions', 'changes']
            number_of_edits = {}

            for edit_type in edit_types:
                number_of_edits[edit_type] = 0

            for speech_filepath in speech_filepaths:
                predicted_transcription_filepath_base = '.'.join(speech_filepath.split('.')[:-1]) + '_'  + asr_system
                predicted_transcription_txt_filepath = predicted_transcription_filepath_base  + '.txt'

                if not os.path.isfile(predicted_transcription_txt_filepath):
                    number_of_missing_predicted_transcription_txt_files += 1
                    predicted_transcription = ''
                else:
                    predicted_transcription = open(predicted_transcription_txt_filepath, 'r').read().strip()
                    if len(predicted_transcription) == 0:
                        print('predicted_transcription_txt_filepath {0} is empty'.format(predicted_transcription_txt_filepath))
                        number_of_empty_predicted_transcription_txt_files += 1

                gold_transcription_filepath_base = '.'.join(speech_filepath.split('.')[:-1]) + '_'  + 'gold'
                gold_transcription_filepath_text = gold_transcription_filepath_base  + '.txt'
                gold_transcription = open(gold_transcription_filepath_text, 'r').read()
                gold_transcription = metrics.format_text(gold_transcription, lower_case=True, remove_punctuation=True,write_numbers_in_letters=True)
                predicted_transcription = metrics.format_text(predicted_transcription, lower_case=True, remove_punctuation=True,write_numbers_in_letters=True)

                all_predicted_transcription_file.write('{0}\n'.format(predicted_transcription))
                all_gold_transcription_filepath.write('{0}\n'.format(gold_transcription))
                #print('\npredicted_transcription\t: {0}'.format(predicted_transcription))
                #print('gold_transcription\t: {0}'.format(gold_transcription))
                wer = metrics.wer(gold_transcription.split(' '), predicted_transcription.split(' '))
                #print('wer: {0}'.format(wer))

                if len(predicted_transcription) == 0: continue

                number_of_tokens_in_gold += len(gold_transcription.split(' '))
                for edit_type in edit_types:
                    number_of_edits[edit_type] += wer[edit_type]

            all_predicted_transcription_file.close()
            all_gold_transcription_filepath.close()

            wer = number_of_edits['changes'] / number_of_tokens_in_gold
            #print('\nGlobal WER based on the all predicted transcriptions:')
            #print('{3}\twer: {0:.5f}% ({1}; number_of_tokens_in_gold = {2})'.format(wer*100, number_of_edits, number_of_tokens_in_gold,asr_system))
            print('{5}\twer: {0:.5f}% \t(deletions: {1}\t; insertions: {2}\t; substitutions: {3}\t; number_of_tokens_in_gold = {4})'.
                  format(wer*100, number_of_edits['deletions'], number_of_edits['insertions'], number_of_edits['substitutions'], number_of_tokens_in_gold,asr_system))
            print('Number of speech files: {0}'.format(len(speech_filepaths)))
            print('Number of missing predicted prescription files: {0}'.format(number_of_missing_predicted_transcription_txt_files))
            print('Number of empty predicted prescription files: {0}'.format(number_of_empty_predicted_transcription_txt_files))


if __name__ == "__main__":
    main()
    #cProfile.run('main()') # if you want to do some profiling