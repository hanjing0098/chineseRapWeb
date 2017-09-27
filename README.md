# Hafez: an Interactive Poetry Generation System

This is the code for the whole pipeline and web interface described in [Hafez: an Interactive Poetry Generation System](http://xingshi.me/data/pdf/ACL2017demo.pdf).

For Rhyme Generation Code, please find it [here](https://github.com/Marjan-GH/Topical_poetry)
For RNN with FSA decoding code, please find it [here](https://github.com/isi-nlp/Zoph_RNN/blob/master/README_XING.md)

## Preparation

0. Unzip the RNN model files in `models`:
Due to the model's large size (more than 1GB), please download here: [lyrics.tl.nn.gz](https://drive.google.com/open?id=0B9mEwe4MVv7XVk9OcUhzWGg2bUU) and [lyrics.tl.topdown.nn](https://drive.google.com/open?id=0B9mEwe4MVv7XbTMyMlBZRDFWcTA)

```
cd models
gunzip lyrics.tl.nn.gz
gunzip lyrics.tl.topdown.nn
```
1. Copy the rhyme generation code into the folder `sonnet-project-for-server/`

```
cd sonnet-project-for-server
git clone https://github.com/Marjan-GH/Topical_poetry
```

2. Follow the [instruction](https://github.com/Marjan-GH/Topical_poetry/blob/master/README.md) to start the server for `Rhyme Generation`.


## Generate a 4-line poem from command line

In this section, we describe how to generate a four line poem from command line.

1. Follow the [instruction](https://github.com/Marjan-GH/Topical_poetry/blob/master/README.md) to generate related files given any topic. Here, we pre-generate all the related files about topic `Mountain`, please check `example/4line/` folder:

* `source.txt` the source file 
* `poem.fsa` the FSA file
* `encourage.txt` the encourange words list
* `rhyme.txt` the rhyme words information. (You don't need this in following steps)

2. Run the script:

```
cd example/4line
bash run_standaline.sh
```
It will print the command it actually call:

```
<ROOT_DIR>/exec/ZOPH_RNN_GPU_EXPAND --adjacent-repeat-penalty -2.0 --repeat-penalty -3.0 -L 60 -b 50 --legacy-model 1 -k 1 <ROOT_DIR>/example/4line/../..//models/lyrics.tl.nn <ROOT_DIR>/example/4line/temp.txt --fsa <ROOT_DIR>/example/4line/poem.fsa --encourage-list <ROOT_DIR>/example/4line/encourage.txt --encourage-weight 1.0 --dec-ratio 0.0 100.0 --decode-main-data-files <ROOT_DIR>/example/4line/source.txt
```

After 1-2 minutes (most time spent on loading the model), it will generate the following 4 line poem and print in STDOUT:

```
as long as you can see that you are grassy !
this land is filled with highest elevation ,
we took a ride across the river valley ,
and now i got to find my own location .
```

## Setup Poem Generation Server

In this section, you'll setup a backend to generate the poems and build a series a webpages as the frontend. 

You need a server with GPU and CUDA 8.0 installed.

1. Start the RNN server:
```
cd sh
# start the normal server
bash run_server.sh
# start the interactive server
bash run_server_interactive.sh
```
2. (Optional) You need to register a [google clound datastore](https://cloud.google.com/datastore/) to log all the poems generated by the system.
3. Start the web server:
If you didn't follow step 2, you may need to comments the related lines in `py/client.py`. (Happy Debugging !)
Change the `host` in `py/client.py` to reflect your host address, Then run: 
```
cd sh
bash run_client.sh
```
4. Go to folder `jekyll/poem/data/js/`, for each javascript file, locate the variable `api_host` and change to your host server address. By default, we will use port 8080 for all our API call.
5. Build the webpage:
```
cd jekyll/poem
jekyll build
```
Then the built web pages are in `jekyll/poem/_site/`

## Default Hyper-parameters

### For auto mode
The server starts with: 
```
<ROOT_FOLDER>/exec/ZOPH_RNN_GPU_EXPAND --interactive 1 --adjacent-repeat-penalty -2.0 --repeat-penalty -3.0 -b 50 -L 160 --decode-main-data-files <ROOT_FOLDER>/models/source.fake.txt -k 1 <ROOT_FOLDER>/models/lyrics.tl.nn <ROOT_FOLDER>/run/kbest10010.txt --fsa <ROOT_FOLDER>/models/fsa.fake.txt --print-beam 1 --dec-ratio 0.0 100.0 --encourage-list dummy --encourage-weight 1.0 --legacy-model 1
```
and the client communicate with:
```
k:1 source_file:<ROOT_FOLDER>/fsas/source.txt fsa_file:<ROOT_FOLDER>/fsas/poem.fsa encourage_list_files:<ROOT_FOLDER>/fsas/encourage.txt,<ROOT_FOLDER>/models/curse.txt,<ROOT_FOLDER>/models/mono.txt encourage_weights:1.0,-5.0,-5.0 repetition:0.0 alliteration:0.0 wordlen:0.0
```

### For ensemble mode
The server starts with:
```
<ROOT_FOLDER>/exec/ZOPH_RNN_GPU_EXPAND --interactive 1 --interactive-line 1 --adjacent-repeat-penalty -2.0 --repeat-penalty -3.0 -b 50 -L 160 --decode-main-data-files <ROOT_FOLDER>/models/source.fake.txt <ROOT_FOLDER>/models/source.fake.txt -k 1 <ROOT_FOLDER>/models/lyrics.tl.topdown.nn <ROOT_FOLDER>/models/lyrics.tl.nn <ROOT_FOLDER>/run/kbest10010.txt --fsa <ROOT_FOLDER>/models/fsa.fake.txt --print-beam 1 --dec-ratio 0.0 100.0 --encourage-list dummy --encourage-weight 1.0 --legacy-model 1
```
and the client communicate with:

```
source <source_file>
```
```
words_ensemble word11 word12 word13 ___sep___ word21 word22 word23 ___sep___
```
```
fsaline <fsa_file> encourage_list_files:<ROOT_FOLDER>/fsas/encourage.txt,<ROOT_FOLDER>/models/curse.txt,<ROOT_FOLDER>/models/mono.txt encourage_weights:1.0,-5.0,-5.0 repetition:0.0 alliteration:0.0 wordlen:0.0
```




Any questions, please contact [Xing Shi](mailto:shixing19910105@gmail.com)
