# DeepSpeech 0.9.3

## Sources
	
- ### [readthedoc](https://deepspeech.readthedocs.io/en/v0.9.3/index.html)
- ### [deepspeech-play book](https://mozilla.github.io/deepspeech-playbook/)
- ### [commonvoice](https://commonvoice.mozilla.org/)


## Installation

1. ### Install docker

2. ### Install the nvidia-container-toolkit
	[nvidia-container-toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker) 



3. ### Setting up your environment for training using DeepSpeech 
	[link](https://mozilla.github.io/deepspeech-playbook/ENVIRONMENT.html)
	load image locally

	Pull image from dockerhub :
	```bash
	docker pull mozilla/deepspeech-train:v0.9.3
	```
4. ### Run Docker Container
	```bash
	$ cd <dataset_directory_path>
	$ ls
	alphabets.txt  clips  invalidated.tsv  other.tsv  reported.tsv  validated.tsv

	$ docker run  -it \
	-v $(pwd)/:/DeepSpeech/data/<dataset_directory> \
	--entrypoint /bin/bash \
	--gpus all \
	mozilla/deepspeech-train:v0.9.3
	
	#########################
	$ docker run  -it \
	-v $(pwd)/:/DeepSpeech/data/farsi_model \
	--entrypoint /bin/bash \
	--gpus all \
	mozilla/deepspeech-train:v0.9.3 
	
	________                               _______________                
	___  __/__________________________________  ____/__  /________      __
	__  /  _  _ \_  __ \_  ___/  __ \_  ___/_  /_   __  /_  __ \_ | /| / /
	_  /   /  __/  / / /(__  )/ /_/ /  /   _  __/   _  / / /_/ /_ |/ |/ / 
	/_/    \___//_/ /_//____/ \____//_/    /_/      /_/  \____/____/|__/


	WARNING: You are running this container as root, which can cause new files in
	mounted volumes to be created as the root user on your host machine.

	To avoid this, run the container by specifying your user's userid:

	$ docker run -u $(id -u):$(id -g) args...

	
	```

## Data preparation 
[Deepspeech-palybook](https://mozilla.github.io/deepspeech-playbook/DATA_FORMATTING.html)
- ### Formating data for CommonVoice datasets
  [common voice website](https://voice.mozilla.org/data)

  [readthedoc](https://deepspeech.readthedocs.io/en/v0.9.3/TRAINING.html#common-voice-training-data)
	1. convert all audio files to .wav using [sound convertor](https://ubuntuhandbook.org/index.php/2021/03/install-soundconverter-4-0-0-ubuntu-20-04/).
  	2. Replace the  **import_cv2.py** file in the repository with  **/DeepSpeech/bin/import_cv2.py**.
	3. Add your desired alphabet.txt in the dataset directory (Persian's alphabet is existed in repo)
	4. install **Sox**
		```bash
		$ apt-get -y update 
		$ apt-get install -y sox
		```

  	5. Format data
		```bash
		cd /DeepSpeech
		python /bin/import_cv2.py --filter_alphabet <alphabet.txt_path> <dataset_directory>

		#########################
		cd /DeepSpeech
		python bin/import_cv2.py --filter_alphabet data/farsi_model/alphabets.txt data/farsi_model/
		```


- ### Making train,validate,test files for training,validating,testing the model
	You can use tools dir in the repo for modify and create  your own train,test,.. dataset.

	in **util/create_train_test.py** python module you can make your train and test .csv file.
	
	
	```bash
	$ python utils/create_train_test.py -h
	usage: create_train_test.py [-h] [--dataset_path DATASET_PATH]

	Description: Input-> CSV Dataset. | OUTPUT-> Creates a test.csv & train.csv beside the Input dataset.

	optional arguments:
		-h, --help            show this help message and exit
		--dataset_path DATASET_PATH
    			Path of the csv dataset.

	## E.g
	$ python tools/create_train_test.py --dataset_path  ./dataset.csv
	train_.csv creats at /home/arm0n/Documents/persian_deepspeech/train_.csv
	test_.csv creats at /home/arm0n/Documents/persian_deepspeech/test_.csv
	validate_.csv creats at /home/arm0n/Documents/persian_deepspeech/validate_.csv
	```



## Training a DeepSpeech model in the container
-  Sources
	
	[deepspeech-playbook](https://mozilla.github.io/deepspeech-playbook/TRAINING.html)

	[readthedoc](https://deepspeech.readthedocs.io/en/r0.9/TRAINING.html)

	[Command-line flags for the training scripts](https://deepspeech.readthedocs.io/en/v0.9.3/Flags.html#training-flags)
- Start training
	```bash
	cd data/farsi_model/
	python3 DeepSpeech.py \
  		--train_files data/farsi_model/clips/train_.csv \
  		--dev_files data/farsi_model/clips/validate_.csv \
  		--test_files data/farsi_model/clips/test_.csv \
  		--audio_sample_rate 32000 \
  		--checkpoint_dir data/farsi_model/checkpoints \
  		--export_dir data/farsi_model/exported_model \
  		--export_tflite data/farsi_model/exported_model_tflite \
  		--reduce_lr_on_plateau true \
  		--early_stop true \
	```
## Scorer - language model for determining which words occur together
[deepspeech-playbook](https://mozilla.github.io/deepspeech-playbook/SCORER.html)
### Building kenlm
```bash
python3 lm_optimizer.py \
	--train_files data/farsi_model/clips/train_.csv \
  	--dev_files data/farsi_model/clips/validate_.csv \
  	--test_files data/farsi_model/clips/test_.csv \
  	--audio_sample_rate 32000 \
  	--checkpoint_dir data/farsi_model/checkpoints \
  	--export_dir data/farsi_model/exported_model \
  	--export_tflite data/farsi_model/exported_model_tflite \
  	--reduce_lr_on_plateau true \
  	--early_stop true \


#{'lm_alpha': 0.9424157455163411, 'lm_beta': 4.414578333651529}

cd data/lm
python3 generate_lm.py \
  --input_txt ../farsi_model/farsi_scorer/alphabet_senteces.txt \
  --output_dir ../farsi_model/farsi_scorer/ \
  --top_k 500000 --kenlm_bins /DeepSpeech/native_client/kenlm/build/bin/ \
  --arpa_order 5 --max_arpa_memory "85%" --arpa_prune "0|0|1" \
  --binary_a_bits 255 --binary_q_bits 8 --binary_type trie


curl -L https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/native_client.amd64.cuda.linux.tar.xz -o native_client.amd64.cuda.linux.tar.xz && tar -Jxvf native_client.amd64.cuda.linux.tar.xz

mkdir data/farsi_model/farsi_scorer

./generate_scorer_package \
	--alphabet ../farsi_model/alphabets.txt  \
	--lm ../farsi_model/farsi_scorer/lm.binary \
	--vocab ../farsi_model/farsi_scorer/vocab-500000.txt \
	--package kenlm-farsi.scorer \
	--default_alpha 0.931289039105002 \
	--default_beta 1.1834137581510284 \
	--force_bytes_output_mode True

```
## Deployment
convert .pb to .pbmm
```bash
cd /DeepSpeech/data/farsi_model/exoprt_model

/DeepSpeech/convert_graphdef_memmapped_format --in_graph=output_graph.pb --out_graph=output_graph.pbmm

```
```bash
pip3 install deepspeech

deepspeech --model <pmbm> --scorer <scorer> --audio <my_audio_file.wav>

```
