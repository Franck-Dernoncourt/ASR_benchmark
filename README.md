

# Speech Recognition Benchmark

[![Build Status](https://travis-ci.org/Franck-Dernoncourt/ASR_benchmark.svg?branch=master)](https://travis-ci.org/Franck-Dernoncourt/ASR_benchmark)

The Speech Recognition Benchmark is a program that assesses and compares the performances of automated speech recognition (ASR) APIs. It runs on Mac OS X, Microsoft Windows and Ubuntu. It currently supports the following ASR APIs: Google, Google Cloud, Houndify, IBM Watson, Microsoft (a.k.a. Bing), Speechmatics and Wit.


 ## Table of Contents

<!-- toc -->

* [Installation](#installation)
* [Usage](#usage)
* [Benchmark results](#benchmark-results)
* [Corpora](#corpora)
* [License](#license)
* [Citation](#citation)

<!-- tocstop -->

## Installation

The Speech Recognition Benchmark requires Python 3, as well as a few Python packages that you may install running `pip install -r requirements.txt`

The configuration file [`src/settings.ini`](src/settings.ini) contains all the parameters that you may wish to change. 

## Usage

Run `cd src; python benchmark.py`

## Benchmark results

Below are some benchmark results presenting the [word error rates](https://en.wikipedia.org/wiki/Word_error_rate) expressed in percentage for several ASR APIs on the following 5 corpora: CV = [Common Voice](https://voice.mozilla.org) (total length: 4:58:32, divided into 3995 speech files); F = Fotolia (4:28:05, 3184); IER = Image Edit Requests (2:29:09, 1289); LS-c = [LibriSpeech](http://www.openslr.org/12) clean (1:53:37, 870); LS-o = LibriSpeech other (5:20:29, 2939). These 5 corpora are all in English. For each of these corpora, we only use the official test set.

Important note: CV, LS-c, and LS-o are public corpora so it is very much possible that some ASRs have been trained on it, making the word error rates lower then they should be. On the contrary, F and IER are private corpora. Also, different APIs may differ on how well they handle languages other than English, speaker accents, background noise, etc. Consequently, you may want to perform the benchmark on a corpus that reflects your use case (in which case you are very welcome to share your results here).


| ASR API      | Date |CV | F | IER | LS-c | LS-o |
| :---         | :---: | :---: | :---: | :---: | :---: | :---: | 
| Human        |  |  | | | [5.8](https://arxiv.org/pdf/1512.02595v1.pdf#page=18) | [12.7](https://arxiv.org/pdf/1512.02595v1.pdf#page=18)
| Google       | 2018-03-30 | 23.2 | 24.2| 16.6| 12.1| 28.8
| Google Cloud | 2018-03-30 | 23.3 | 26.3| 18.3| 12.3| 27.3
| IBM          | 2018-03-30 | 21.8 | 47.6| 24.0|  9.8| 25.3     
| Microsoft    | 2018-03-30 | 29.1 | 28.1| 23.1| 18.8| 35.9
| Speechmatics | 2018-03-30 | 21.2*| 31.9*| 21.4|  7.3| 19.4
| Wit.ai       | 2018-03-30 | 35.6 | 54.2| 37.4| 19.2| 41.7

(* means only a subset of the corpus had been used to compute the word error rate)


## Corpora

For convenience, we provide two scripts to format the Common Voice and LibriSpeech corpora so that the ASR benchmark can be run on them.

Bash script to format Common Voice (requires ~25 GB disk space):

```
# cv_corpus_v1.tar.gz is 12 GB
wget https://common-voice-data-download.s3.amazonaws.com/cv_corpus_v1.tar.gz
tar -xvf cv_corpus_v1.tar.gz
mkdir cv-valid-test
mv cv_corpus_v1/cv-valid-test cv-valid-test
mv cv_corpus_v1/cv-valid-test.csv cv-valid-test
rm -Rf  cv_corpus_v1
rm cv_corpus_v1.tar.gz
cd  ../src 
# format_common_voice_gold_transcriptions.py requires the pandas package, which can be installed with: pip install pandas
python format_common_voice_gold_transcriptions.py
``` 

Bash script to format LibriSpeech (requires ~1.5 GB disk space):
``` 
cd data
mkdir librispeech-test-clean
mkdir librispeech-test-other
mkdir librispeech-temp
cd librispeech-temp
# test-clean.tar.gz is 346 MB, test-other.tar.gz is 328 MB
wget http://www.openslr.org/resources/12/test-clean.tar.gz
wget http://www.openslr.org/resources/12/test-other.tar.gz
tar -xvf test-clean.tar.gz
tar -xvf test-other.tar.gz  
mv LibriSpeech ..
cd  ..
rm -Rf LibriSpeech
rm test-clean.tar.gz
rm test-other.tar.gz
cd  ../src
python format_librispeech_gold_transcriptions.py
``` 


## License

Some code snippets were taken from external sources:
- in [`src/asr_speechmatics.py`](src/asr_speechmatics.py), most of the code comes from https://github.com/speechmatics/speechmatics_python (author: [TomSpeechmatics](https://github.com/TomSpeechmatics), no license specified).
- in [`src/transcribe.py`](src/transcribe.py), some code was adapted from https://github.com/Uberi/speech_recognition (made available under the 3-clause BSD license). For more licensing information. see the SpeechRecognition README.
- in [`src/metrics.py`](src/metrics.py), the functions to compute the word error rate mostly comes from [http://progfruits.blogspot.com/2014/02/word-error-rate-wer-and-word.html](https://web.archive.org/web/20171215025927/http://progfruits.blogspot.com/2014/02/word-error-rate-wer-and-word.html) (author: [SpacePineapple](https://web.archive.org/web/20180401185957/https://www.blogger.com/profile/12691129381793481173), no license specified) and https://martin-thoma.com/word-error-rate-calculation (author: [Martin Thoma](https://github.com/MartinThoma), no license specified).

The rest of the code is made available under the [CC BY-NC 4.0 license](https://creativecommons.org/licenses/by-nc/4.0/).

## Citation

If you use this code in your publications, please cite:

```
@misc{ASRbenchmark2018,
  author = {Franck Dernoncourt, Trung Bui, Walter Chang},
  title = {A Framework for Speech Recognition Benchmarking},
  year = {2018},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Franck-Dernoncourt/ASR_benchmark}},
}
```
