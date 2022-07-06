<h1 align="center">MIGP (Might I Get Pwned)</h1>

## Description
MIGP (Might I Get Pwned) is a next-generation password breach altering service to prevent users from picking passwords that are very similar to their prior leaked passwords; such credentials are vulnerable to [*credential tweaking attacks*](https://pages.cs.wisc.edu/~chatterjee/papers/ppsm.pdf). This repository contains the code we used for the security simulations and performance analysis of MIGP. The paper is published in USENIX Security 2022. For details please refer to [our paper](https://arxiv.org/pdf/2109.14490.pdf).

[Disclaimer] This repository is a proof-of-concept prototype. Please review it carefully before using it for any purposes.


## Setting the environment
- For crypto  operations on `secp256k`,  we used [petlib](https://github.com/gdanezis/petlib) library, and for expensive hashing we used  
[this](https://argon2-cffi.readthedocs.io/en/stable/api.html) argon2 implementation. Please install `petlib` following the instructions from [here](https://github.com/gdanezis/petlib).
- All required packages are listed in the `requirements.txt` file. We encourage creating virtual environments before running the experiments (using `conda` or `virtualenv`). 
- `WR_19` and `WR_20` relies on GO (version 1.15).
## Downloading required data files
Since the files required to run the experiments are sensitive password leaks from 2019, if you need access to datasets please write to us. We can grant access to datasets after properly reviewing the request.
## Similarity simulation
Training the Pass2Path models is computationally expensive. Therefore, we trained these models in GPU and generated the prediction files for required test_files, to run the experiments fast. The code for training the Pass2Path models is in "https://github.com/Bijeeta/credtweak/tree/master/credTweakAttack/".
We also stored the sorted list of rules for Das-R and EDR models, ranked based on the breached dataset.

### Producing Figure 4
To generate the values of fig4, run `bash fig4.sh`

### Producing Figure 5
To generate the values of fig5, run `bash fig5.sh`

### Producing Figure 6
To generate the values of fig6, run `bash fig6.sh`

## Security simulation
Security simulation is computationally expensive. Some of the simulations may took days. Therefore it is separated into three phases. The output of the one phase is saved as NumPy arrays and used in the next phases. 
- `bash  script_step_1.sh`. // This will create password variations. You can skip this one as we already provide the variations file inside `data_files` folder
- `bash script_step_2.sh`. // This creates the top 10^3 guess ranks. We have also generated the guess ranks and balls of each password in the `data_files` folder. [skip if you want] 
- Finally, run `bash script_step_3.sh <n> <qc>` to generate the row corresponding to row  with value `n` and `qc` in Figure 8. The results will be saved in `results/security_sumulation.tsv` file. This part may long time as for n =100 and q_c=10^3 it took us 12 hours to complete the simulation. 
- After the step 3 has been done for each `n` and `qc`, run `python3.8 Figure 8.py`. It should generate Figure 8. If some values for `n` and `qc` the values have not been generated it will show blank. 



## Running the MIGP protocol 
- **MIGP Server**: Navigate to the `performance_simulation/MIGP_server` directory in the terminal and enter `python3 MIGP_server.py`. By default, rate-limiting protection is off and prefix length 20 is used. To run the server with rate-limiting option enter: `python3 MIGP_server.py --rate_limitaintg 1`
- **MIGP Client**: After the server has completed preloading open a new terminal, navigate to `performance_simulation/MIGP_server` and type the following commands
    - `python3 post_client_MIGP.py  --username <username> --password <password to  check> --prefix_length <prefix_length set on the server> --rate_limiting <limiting option set on the server>`

For example, if server is run with default options (without any command line options, `python3 MIGP_server.py`), it initiates the leaked database with only one leak entry `Alice,123456`). Now, you can use the client-side terminal in the following way and should get the following results:

```sh
python3 MIGP_client.py --username Alice --password 123456 # will give exact password matching
python3 MIGP_client.py --username Alice --password 123456$ # will give similar password matching
python3 MIGP_client.py --username Alice --password deercrossing # or any other password, will give not present in the leak
```
Here we simply assume user `Alice` password `123456` has been leaked and `123456$` is a similar password of `123456` vulnerable to credential tweaking attack (line 81 in MIGP_server.py)

# CloudFlare version of MIGP.
https://github.com/cloudflare/migp-go
# Contact
We are always looking for ways to improve our codes. For any bugs please email at: [mislam9@wisc.edu](mailto:mislam9@wisc.edu)
# Citations
If you use any part of our code or paper please cite our paper. 
```
@inproceedings{pal2021might,
  title={{Might I Get Pwned: A Second Generation Password Breach Alerting Service}},
  author={Pal, Bijeeta and Islam, Mazharul and Bohuk, Marina Sanusi and Valenta, Luke and Wood, Chris and Whalen, Tara and Sullivan, Nick and Ristenpart, Thomas and Chatterjee, Rahul},
  booktitle={31th {USENIX} Security Symposium ({USENIX} Security 22)},
  year={2022},
  organization={USENIX}
}
