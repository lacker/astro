# Help, I want a Python environment where Blimpy and so on just work!

Okay, try this. I promise it works on the `blpc` machines.

If it doesn't work, you can bug me (Kevin Lacker) on Slack to fix your python environment.

First, install miniconda3 in your home directory.

Second, follow these steps.

```
conda env create -f /home/obs/obs_bin/pipeline/environment.yml
conda activate pipeline
pip uninstall h5py
pip install --no-binary=h5py h5py
```

Now everything should work. You are using a conda environment named "pipeline".

In the future, you have to type `conda activate pipeline` to enable this Python environment - the default one is different.
