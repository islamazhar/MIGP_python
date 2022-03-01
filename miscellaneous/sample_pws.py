from pathlib import Path
# coding: utf-8
#!/usr/bin/env python3

import sys
sys.path.append("..")
import argparse 
from miscellaneous.utilities import filter_ws



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bl', action='store', dest='bl', type=int, default=-1,
                        help='number of blocklisted passwords')
    return parser.parse_args()

opt = parse_args()

DIR = Path("/pwdata/mazharul/password_research_dataset_Jan/")
breach_fname = f'mixed_full_leak_data_40_2_with-pws-counts_{opt.bl}.txt' if opt.bl > 0 else f'mixed_full_leak_data_40_2_with-pws-counts.txt'
fname = DIR / breach_fname

limit = -1
# filename='/pwdata/mazharul/new_mixed_full/mixed_full_leak_data_40_2.txt'
# cut -d$'\t' -f 2- $filename | tr '\t' '\n' | sort -t$'\t' | uniq -c | sed -E 's/^ *//; s/ /\t/' | sort -nrk1 > pwdata/mazharul/password_research_dataset_Jan/mixed_full_leak_data_40_2_with-pws-counts.txt 
from pwmodel import readpw
pwm = readpw.Passwords(pass_file=fname,limit=int(limit))
l = list(pwm.sample_pws(25000))
out_fname = DIR/f'target_pws_25000.S2.{opt.bl}txt'  if opt.bl > 0 else f'target_pws_25000.S2.txt'
with open(out_fname, 'w') as f:
    for pw in l:  
        f.write(pw+'\n')
           

            
     
    
