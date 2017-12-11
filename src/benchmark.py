'''
Use settings.ini to configure the benchmark.
'''

import configparser
import glob
import os
import transcribe
import metrics
import time

def main():

    # Load setting file
    settings = configparser.ConfigParser()
    settings.read("settings.ini")

    asr_systems = settings.get('general','asr_systems').split(',')
    data_folder = settings.get('general','data_folder')

    print('asr_systems: {0}'.format(asr_systems))
    print('data_folder: {0}'.format(data_folder))
    speech_filepaths = glob.glob(os.path.join(data_folder, '*.wav'))

    if settings.getboolean('general','transcribe'):
        # Transcribe
        print('\n### Call the ASR engines to compute predicted transcriptions')
        for speech_file_number, speech_filepath in enumerate(speech_filepaths):
            #if not 'AOLLFPCWXJVA6_1369_SU_BARU.wav' in speech_filepath: continue
            #if speech_file_number >= 100: break
            for asr_system in asr_systems:
                transcription = transcribe.transcribe(speech_filepath,asr_system,settings,save_transcription=True)
            #time.sleep(5)   # Delay in seconds

    if settings.getboolean('general','evaluate_transcriptions'):
        # Evaluate transcriptions
        print('\n### Final evaluation of all the ASR engines based on their predicted jurisdictions')
        for asr_system in asr_systems:
            all_predicted_transcription_filepath = 'all_predicted_transcriptions_' + asr_system + '.txt'
            all_gold_transcription_filepath = 'all_gold_transcriptions_' + asr_system + '.txt'

            number_of_tokens_in_gold = 0
            number_of_edits = 0
            for speech_filepath in speech_filepaths:
                #if 'AYFAOYFBISRF3_6850_NUMBER_ONE' in speech_filepath: break
                if 'A1A84EAZZI6YE_19728_LIGHTEN_SOME_OF_THE_BURN' in speech_filepath: break
                predicted_transcription_filepath_base = '.'.join(speech_filepath.split('.')[:-1]) + '_'  + asr_system
                predicted_transcription_filepath_text = predicted_transcription_filepath_base  + '.txt'
                predicted_transcription = open(predicted_transcription_filepath_text, 'r').read()

                gold_transcription_filepath_base = '.'.join(speech_filepath.split('.')[:-1]) + '_'  + 'gold'
                gold_transcription_filepath_text = gold_transcription_filepath_base  + '.txt'
                gold_transcription = open(gold_transcription_filepath_text, 'r').read()
                gold_transcription = metrics.format_text(gold_transcription, lower_case=True, remove_punctuation=True,write_numbers_in_letters=True)
                predicted_transcription = metrics.format_text(predicted_transcription, lower_case=True, remove_punctuation=True,write_numbers_in_letters=True)

                print('\npredicted_transcription\t: {0}'.format(predicted_transcription))
                print('gold_transcription\t: {0}'.format(gold_transcription))
                wer = metrics.wer(gold_transcription.split(' '), predicted_transcription.split(' '))
                print('wer: {0}'.format(wer))
                #wer = metrics.wer('blue hydrangea bouquet', 'blue had range of okay')
                #print('wer: {0}'.format(wer))

                #if len(predicted_transcription) == 0: continue

                number_of_tokens_in_gold += len(gold_transcription.split(' '))
                number_of_edits += wer
                #if number_of_tokens_in_gold > 1000: break

            wer = number_of_edits / number_of_tokens_in_gold
            print('\nGlobal WER based on the all predicted transcriptions:')
            print('{3}\twer: {0:.5f}% (number_of_edits = {1}; number_of_tokens_in_gold = {2})'.format(wer*100, number_of_edits, number_of_tokens_in_gold,asr_system))

if __name__ == "__main__":
    main()
    #cProfile.run('main()') # if you want to do some profiling