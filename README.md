

# Speech Recognition Benchmark

The Speech Recognition Benchmark is program that assesses and compares the performances of automated speech recognition (ASR) APIs. It runs on Mac OS X, Microsoft Windows and Ubuntu. It currently supports the following ASR APIs: Google, Google Cloud, Houndify, IBM Watson, Microsoft (a.k.a. Bing), Speechmatics and Wit.

## Installation

The Speech Recognition Benchmark requires Python 3, as well as a few Python packages that you may install running `pip install -r requirements.txt`

The configuration file [`src/settings.ini`](src/settings.ini) contains all the parameters that you may wish to change. Some ASR APIs require credentials for the user to be able to query them.



## Usage

Run `cd src; python benchmark.py`

## Benchmark results

Below are some benchmark results presenting the [word error rates](https://en.wikipedia.org/wiki/Word_error_rate) expressed in percentage for several ASR APIs on the following 5 corpora: CV = Common Voice (total length: 4:58:32, divided into 3995 speech files); F = Fotolia (4:28:05, 3184); IER = Image Edit Requests (2:29:09, 1289); LS-c = LibriSpeech clean (1:53:37, 870); LS-o = LibriSpeech other (5:20:29, 2939). These 5 corpora are all in English.

Important note: CV, LS-c, and LS-o are public corpora so it is very much possible that some ASRs have been trained on it, making the word error rates lower then they should be. On the contrary, F and IER are private corpora. Also, different APIs may differ on how well they handle languages other than English, speaker accents, background noise, etc. Consequently, you may want to perform the benchmark on a corpus that reflects your use case (in which case you are very welcome to share your results here).


| ASR API      | Date |CV | F | IER | LS-c | LS-o |
| :---         | :---: | :---: | :---: | :---: | :---: | :---: | 
| Human        |  |  | | | [5.8](https://arxiv.org/pdf/1512.02595v1.pdf#page=18) | [12.7](https://arxiv.org/pdf/1512.02595v1.pdf#page=18)
| Google       | 2018-03-30 | 23.2 | 24.2| 16.6| 12.1| 28.6
| Google Cloud | 2018-03-30 | 23.3 | 26.3| 18.3| 12.3| 27.3
| IBM          | 2018-03-30 | 21.8 | 47.6| 24.0|  9.8| 25.3     
| Microsoft    | 2018-03-30 | 29.1 | 28.1| 23.1| 18.8| 35.5
| Speechmatics | 2018-03-30 | 21.2*| 31.9*| 21.4|  7.3| 19.4
| Wit.ai       | 2018-03-30 | 35.6 | 54.2| 37.9| 19.2| 41.7

(* means only a subset of the corpus had been used to compute the word error rate)
