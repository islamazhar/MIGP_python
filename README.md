<h1 align="center">MIGP (Might I Get Pwned)</h1>

# Description
MIGP (Might I Get Pwned) is a next generation password breach altering service to stop *credential tweaking attack*. This repository contains the code we used to for the security simulations and performance analysis, the results of which are recorded in the paper published in USENIX Security 2022. For details please refer to [our paper](https://arxiv.org/pdf/2109.14490.pdf).


## Setting the environment
- For cypto operations on `spec256k`, we used [petlib](https://github.com/gdanezis/petlib) library, and for expensive hashing we used the 
[this](https://argon2-cffi.readthedocs.io/en/stable/api.html) argon2 implementation. Please Install `petlib` following the instructions from [here](https://github.com/gdanezis/petlib).
- Create a vitrual environment `virtualenv MIGP_env` and activate the environment `source MIGP_env/bin/activate`
- Install all required dependencies using `pip3 install -r requirements.txt`    
## Downloading required files
TODO:
Since the files required to run the experiments are sensitve password leaks from 2019, we ask the reviwers to download the zipped file from the secret link provided in hotcrp and unzip them in a folder. In future we will request other researchers to fill up a form and then upon examination approved requests  will get access those sensitve leaks with proper discration.
## Security simulation
### Producing Figure 8
The security simulation is computationally expensive. It some of the runs took days. Therefore it is seperated into three phases. The output of the one phases is saved as numpy arrays and used in the next phases. We have provided output of the first and second phase as numpy arrays so that if reviwers wish to reproduce Figure 8 quickly they can go to thrid phase and run the `script.sh`. 
- First Phase:
    We first generate $k$ variations of each password and saved them as numpy arrays using the command `python3 get_vairations.py --bl <bl> --k <k>`. Here  `bl` = number of blocklisted password $\in (0, 10, 100, 1000, 10000)$, and k = number of password variations to consider $\in (10, 100)$. The output of run is saved as a numpy array having the following 
    naming convention `varations.{qc}.{bl}.pws`
- Second Phase:
    Using the variations of passwords  we generate top `qc` $\in (10, 100, 100)$ guess using he command `python3 get_guess_ranks.py --bl <bl> --k <k> --qc <qc>`. 
- Third Phase:
    Now that we have the top `qc` guesses, we can calcuate the attack success rates using target passwords. To achieve this do the following steps.
    - go to security_simuation folder `cd security_simulation` 
    - Point `breach_fname` to the location where `mixed_full_leak_data_40_1_with-pws-counts.txt` file is.
    - Point `target_fname` to the location where `target_pws_25000.S2.0txt` file. 
    - Run `bash script.sh <number_of_threads> <ql>` to generate each column of Figure 6. Note as previously mentioned it takes a lot of time to run the simulation espcially for `qc=1000`. Hence we recommand the reviwers to run not more than three threads at a time for `qc=1000` depending on machine configuration. 
    For our linux machine if we run more than three threads it shows memory out of error. For `qc=10` runs fairely quickly and for `qc=100` it may take more than 1 hour. 

### Producing Figure 9:
  - go to Figure 9 folder under security_simulation `cd Figure_9`
  - run `bash script.sh`. You can a new a `Figure_9.jpg`.

## Peformance simulation
### Protocol implementation on Figure 2:
- Server side: cd to `performance_simulation/MIGP_server` and type `python3 MIGP_server.py`. By default rate limiting protection is off and prefix length 20 is used. To run the server with rate limiting option on type `python3 MIGP_server.py --rate_limitaintg 1`
- Client side: After the server has completed preloading open a new terminal and cd to `performance_simulation/MIGP_server` and type the following commands
    - `python3 post_client_MIGP.py  --username <username> --password <password to  check> --prefix_length <prefix_length set on the server> --rate_limiting <limiting option set on the server>`

For example if server is run for default options using `python3 MIGP_server.py` using the following commands to get different results on the client-side terminal.

```sh
python3 post_client_MIGP.py --username Alice --password 123456 # will give exact password matching
python3 post_client_MIGP.py --username Alice --password 123456$ # will give similar password matching
python3 post_client_MIGP.py --username Alice --password <any other passwords> $ # will give not present in the leak
```
Here we simpliy assume user `Alice` password `123456` has been leaked and `123456$` is similar password (line 91, 92 in MIGP_server.py)
### Peformance of evaluation reported in Figure 12.
We provide a bash script to reproduce Figure #12. Results may differ as the reported values are from EC2 instances in WAN conncetion (refer to the paper for details).
cd to performance simulation and run `bash script.sh`. This script will send API request to EC2 instancess running MIGP/IDB server's API. we Note you may have to install `go` since WR-19 and WR-20 code borrow from the original authors is in go.  
# CloudFlare version of MIGP.
https://github.com/cloudflare/migp-go
# Contact
We are always looking for ways to improve our codes. For any bugs please email at: [mislam9@wisc.edu](mailto:mislam9@wisc.edu)
# Citations
If you use any part of our code or paper please cite our paper. 
```
@inproceedings{pal2021might,
  title={{Might I Get Pwned: A Second Generation Password Breach Alerting Service}},
  author={Pal, Bijeeta and Islam, Mazharul and Sanusi, Marina and Valenta, Luke and Wood, Chris and Whalen, Tara and Sullivan, Nick and Ristenpart, Thomas and Chatterjee, Rahul},
  booktitle={31th $\{$USENIX$\}$ Security Symposium ($\{$USENIX$\}$ Security 22)},
  year={2022},
  organization={USENIX}
}
