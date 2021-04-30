# Runbook for BL pipeline ops at Green Bank

This document explains how to run part of the Green Bank pipeline. The
goal is to automate these steps. For more pipeline information check
[Matt's data wrangling
memo](https://github.com/UCBerkeleySETI/bl_docs/tree/master/027_data_wrangling_status_apr_2021).

Overall the pipeline has these steps:

1. Capturing raw data
2. Reducing the data from `.raw` to `.fil`
3. Splicing the data to combine `.fil` files
4. "Chaining" which converts `.fil` to `.h5`
5. Copying the data to the Berkeley datacenter

Steps 1 and 2 are done by the observer. This doc covers steps 3-5.

GOAL: skip the splicing step.

## Log in

You need two accounts, a GB account and a UCB account.

First the GB account:

`ssh ssh.gb.nrao.edu`

Then the UCB account:

`ssh bl-head`

## Environment

In general the pipeline runs as `obs` and the Python orchestration code is in `~/bin/pipeline`:

* `su obs`
* `conda activate pipeline`
* `cd ~/bin/pipeline`

## Status

To operate the pipeline status server, from two separate terminals run:

* `./status.py`
* `~/ngrok http 8080`

## Analyzing disk space

* ssh into bls0
* `df -h --total /mnt_bls*/datax*`
* Pick the one with the most space that isn't `bls9` which is for
  "special projects". We'll put output there.
* ssh into bls{n}
* `all_df_bg` shows you usage for `blc{x}{x}` machines. Find one that's
  getting full. We'll take input files from there.
* Pick one of the
  `/mnt_blc{hostn}/datax2/dibas.{date}/{sessionid}/GUPPI/BLP{hostn}`
  directories. Each directory is a session.
* You need to pick a directory that has not yet been spliced. One sign
  that splicing has already run is when there is a `.done` file
  without a corresponding `.fil` file.
  
## Conversion

Some misc rules:

* Only use the `datax2` disks on the blc machines
* Stay off bls6 and bls9
* Don't put more stuff on a bls disk with less than 1T free space
* Only process sessions that are from 17B and earlier
* I should process a whole session at a time, so that we don't subsequently try to splice it

Go to the bls machine we're using:

`ssh bls0`

Move:

`/mnt_blc03/datax2/dibas.20170329/AGBT17A_999_35/GUPPI/BLP03/blc03_guppi_57841_70863_B0329+54_0021.gpuspec.0000.fil`

To:

`/datax3/pipeline/AGBT17A_999_35/blc03`

* Deal with root ownership, it should be obs

Fix it up:

`/home/obs/bin/chain_fixup blc03_guppi_57841_70863_B0329+54_0021.gpuspec.0000.fil`

Convert to h5:

`fil2h5 blc03_guppi_57841_70863_B0329+54_0021.gpuspec.0000.fil`

* That creates the h5, but there's still a fil in there.
* Append `.x2h` to the fil file for theoretical deletion later
