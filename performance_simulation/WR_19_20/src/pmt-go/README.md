# pmt-go

### Bloom-PMT and Cuckoo-PMT

- This repository includes two ElGamal based PMT (private membership test) implementations in Go language (for academic use only).
    - Bloom-PMT: proposed in the paper "[_How to end password reuse on the web_](https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_06A-5_Wang_paper.pdf)" (NDSS '19)
    - Cuckoo-PMT: proposed in the paper "[_Detecting Stuffing of a User’s Credentials at Her Own Accounts_](https://www.usenix.org/system/files/sec20-wang.pdf)" (USENIX Security '20)
    
- Both PMTs need one round of interaction. For Bloom-PMT, a response message includes only one ciphertext. In most cases, Cuckoo-PMT requires smaller query messages 
  and has better overall computation and communication complexity. Both protocols allow checking if keys and ciphertexts are well-formed.

### Switch between two PMTs

- Choose which PMT to use by importing corresponding PMT go file as alias "pmt". For example,
  ```go
  // Choose Bloom-PMT
  import pmt "pmt-go/pmtBfElgamal"
  ```
  or
  ```go
  // Choose Cuckoo-PMT
  import pmt "pmt-go/pmtCfElgamal"
  ```
  
### Point Compression
- Both protocols support point compression (default: disabled). 
  Enabling point compression would decrease each message to about half its original size but increase
  computation costs.

### FPR (False Positive Rates)
- For Bloom-PMT, FPR depends on the number of hash functions (default: 20). By default, the FPR is about 2^{-20}.
- For Cuckoo-PMT, FPR depends on the buck size (default: 16) and the fingerprint size (default: 224). 
  By default, the FPR is about 2^{-219}.

### example.go
- _example.go_ shows an example of PMT usage.
- Usage: 
```bash
go run example.go -keyLength=256 -setSize=4096 -numThreads=1 -enablePC=false -requesterInput="Simba"
```
- Parameters:
  - -keyLength=256: the key length of the underlying ECC-ElGamal is 256 bits. Other options include 224, 384, and 512. (Default: 256)
  - -setSize=1024: the size of the responder/sender's set is 1024. (Default: 1024)
  - -numThreads=2: both parties are allowed to run the protocol with 2 threads. (Default: 2)
  - -enablePC: Point compression for the underlying curve is enabled. (Default: disabled)
  - -requesterInput="Simba": the monitor/responder/sender's input element. (Default: "Simba")
    - In example.go, the target's input set is filled with "Simba" and some other strings starting 
      with "Simba" (e.g., "Simba24") to reach the specified set size. So the set membership holds if the requester/receiver's
      input string is "Simba", while the relation does not hold for any other strings not 
      starting with "Simba".
      
### Citation

```latex
@inproceedings{wang2019:reuse,
  title = {How to end password reuse on the web},
  author = {Wang, Ke Coby and Reiter, Michael K.},
  booktitle = {26\textsuperscript{th} Annual Network and Distributed System Security Symposium},
  publisher = {Internet Society},
  month = {Feb},
  year = {2019}
}
```

```latex
@inproceedings {wang2020:stuffing,
title = {Detecting stuffing of a user's credentials at her own accounts},
author = {Wang, Ke Coby and Reiter, Michael K.},
booktitle = {29\textsuperscript{th} {USENIX} Security Symposium},
publisher = {{USENIX} Association},
month = {Aug},
year = {2020},
}
```