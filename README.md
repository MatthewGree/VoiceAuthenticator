## Voice Authenticator

Download data from https://huggingface.co/datasets/ProgramComputer/voxceleb and place it inside the data folder.

The data folder should contain two directories:

* `vox1_dev_wav`
* `vox1_test_wav`

Each of those folders should have the following structure:

* `wav `folder ↓
    * many directories named like `idXYZPQ` ↓
        * many directories with random names ↓
            * `*.wav` files

The data folder should also contain a vox1_vox1_meta.csv. It's tracked by git, so it should be there by default.

Project stages are contained in jupyter notebooks in the root directory for easy
access and code edition.

Stages:

1. [annotate_audio_files](annotate_audio_files.ipynb) - checks audio files from the VoxCeleb1 dataset and creates
   a `annotations_with_metadata.json` file in the data folder, which contains all the relevant information for each
   audio recording - it's path, user_id, train/test split etc.

