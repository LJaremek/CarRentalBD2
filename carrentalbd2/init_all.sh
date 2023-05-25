#!/bin/bash
conda create --name carRental python=3.11
conda activate carRental
conda install postgresql
bash -i ./init.sh postgres_db admin1 haslo1
