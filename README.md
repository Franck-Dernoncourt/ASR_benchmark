

# Speech Recognition Benchmark

The Speech Recognition Benchmark is program that assesses and compares the performances of automated speech recognition (ASR) engines. It runs on Mac OS X, Microsoft Windows and Ubuntu. It currently supports the following ASR engines: Google, Google Cloud, Houndify, IBM Watson, Microsoft (a.k.a. Bing), Speechmatics and Wit.

## Installation

The Speech Recognition Benchmark requires Python 3, as well as a few Python packages that you may install running `pip install -r requirements.txt`

The configuration file `settings.ini` contains all the parameters that you may wish to change. Some ASR engines require credentials for the user to be able to query it.



## Usage

Run `python benchmark.py`