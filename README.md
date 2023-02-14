# DeepSpeech 0.9.3

### Sources :
### [readthedoc](https://deepspeech.readthedocs.io/en/v0.9.3/index.html)
### [deepspeech-play book](https://mozilla.github.io/deepspeech-playbook/)
### [commonvoice](https://commonvoice.mozilla.org/)
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
   cd <data_path>

   docker run  -it \
   -v $(pwd)/:/DeepSpeech/data/<dataset_directory> \
   --entrypoint /bin/bash \
   --gpus all \
   mozilla/deepspeech-train:v0.9.3
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
     apt-get -y update 
     apt-get install -y sox
     ```

  5. Format data
       ```bash
       cd /DeepSpeech
       python /bin/import_cv2.py --filter_alphabet <alphabet.txt_path> <dataset_directory>
       #python bin/import_cv2.py --filter_alphabet data/myModel/alphabets.txt data/myModel/
       ```


  - ### **Making train,test,... files for training,testing the model**
    You can use tools dir in the repo for modify and create  your own train,test,.. dataset.
   
    
     1.
```bash
```



## Training a DeepSpeech model in the container
[deepspeech-playbook](https://mozilla.github.io/deepspeech-playbook/TRAINING.html)

[readthedoc](https://deepspeech.readthedocs.io/en/r0.9/TRAINING.html)

[Command-line flags for the training scripts](https://deepspeech.readthedocs.io/en/v0.9.3/Flags.html#training-flags)
```bash
cd data/<dataset_directory>
#cd data/myModel/
python3 ../..DeepSpeech.py \
  --train_files <train_csv> \
   --test_files data/farsi_/clips/test_.csv \
   --audio_sample_rate 32000 \
   --alphabet_config_path data/farsi_/alphabets.txt \
    --checkpoint_dir data/farsi_/checkpoints \
    --export_dir data/farsi_/exoprt_model \
    --reduce_lr_on_plateau true \
    --early_stop true \
    --dropout_rate 0.4 \
    --es_epochs 1 \
    --epochs 5
```
## Scorer - language model for determining which words occur together
[deepspeech-playbook](https://mozilla.github.io/deepspeech-playbook/SCORER.html)
### Building kenlm
```bash
python3 lm_optimizer.py \
    --train_files data/farsi_/clips/train_.csv \
   --test_files data/farsi_/clips/test_.csv \
   --audio_sample_rate 32000 \
   --alphabet_config_path data/farsi_/alphabets.txt \
    --checkpoint_dir data/farsi_/checkpoints \
    --export_dir data/farsi_/exoprt_model \
    --reduce_lr_on_plateau true \
    --early_stop true \
    --dropout_rate 0.4 \
    --es_epochs 1 \
    --epochs 5


#{'lm_alpha': 0.9424157455163411, 'lm_beta': 4.414578333651529}

cd data/lm
python3 generate_lm.py \
  --input_txt ../farsi_/farsi_scorer/alphabet_senteces.txt \
  --output_dir ../farsi_/farsi_scorer/ \
  --top_k 500000 --kenlm_bins /DeepSpeech/native_client/kenlm/build/bin/ \
  --arpa_order 5 --max_arpa_memory "85%" --arpa_prune "0|0|1" \
  --binary_a_bits 255 --binary_q_bits 8 --binary_type trie


curl -L https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/native_client.amd64.cuda.linux.tar.xz -o native_client.amd64.cuda.linux.tar.xz && tar -Jxvf native_client.amd64.cuda.linux.tar.xz

    ./generate_scorer_package \
    --alphabet ../farsi_/alphabets.txt  \
    --lm ../farsi_/farsi_scorer/lm.binary \
    --vocab ../farsi_/farsi_scorer/vocab-500000.txt \
    --package kenlm-farsi.scorer \
    --default_alpha 0.931289039105002 \
    --default_beta 1.1834137581510284 \
    --force_bytes_output_mode True

```

## Deeployment
convert .pb to .pbmm
```bash
cd /DeepSpeech/data/farsi_/exoprt_model
/DeepSpeech/convert_graphdef_memmapped_format --in_graph=output_graph.pb --out_graph=output_graph.pbmm

```
```bash
pip3 install deepspeech

deepspeech --model <pmbm> --scorer <scorer> --audio <my_audio_file.wav>

```
