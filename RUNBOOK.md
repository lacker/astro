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

## Log in

You need two accounts, a GB account and a UCB account.

First the GB account:

`ssh ssh.gb.nrao.edu`

Then the UCB account:

`ssh bl-head`

## Splicing

If we splice from `datax2` then there won't be contention with observing.

First we need to check how much space is available in different places
to make decisions.

* ssh into bls0
* `su obs`
* `df -h --total /mnt_bls*/datax*`
* Pick the one with the most space that isn't `bls9` which is for
  "special projects". We'll put output there.
* ssh into bls{n}
* `su obs`
* `all_df_bg` shows you usage for `blc{x}{x}` machines. Find one that's
  getting full. We'll take input files from there.
* Pick one of the
  `/mnt_blc{hostn}/datax2/dibas.{date}/{sessionid}/GUPPI/BLP{hostn}`
  directories. Each directory is a session.
* cd into it
* `su root`
* `/home/obs/bin/do_anyspec_collate . /datax{n}/collate |& tee -a collate.out`

