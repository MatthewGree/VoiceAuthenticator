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
