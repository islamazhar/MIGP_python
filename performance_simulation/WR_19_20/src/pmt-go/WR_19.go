package main

import (
	"flag"
	"fmt"
	"runtime"
	"strconv"
	"time"

	pmt "pmt-go/pmtBfElgamal" // Choose Bloom-PMT
)

func main() {

	//////////////////  ARGUMENTS  /////////////////

	var setSize int
	var numThreads, params, rateLimiting int
	var pointCompression bool
	var pwd2check string
	var suffix string

	paramPtr := flag.Int("keyLength", 256, "224, 256, 384 or 512")
	setSizePtr := flag.Int("setSize", 1024, "an int")
	numThreadsPtr := flag.Int("numThreads", 2, "an int")
	rateLimitingPtr := flag.Int("rateLimiting", 1, "an int")
	pointCompressionPtr := flag.Bool("enablePC", false, "true or false")
	pwd2checkPtr := flag.String("requesterInput", "Simba", "a string") // "Simba" will result in a positive response

	flag.Parse()

	params = *paramPtr
	setSize = *setSizePtr
	numThreads = *numThreadsPtr
	pointCompression = *pointCompressionPtr
	pwd2check = *pwd2checkPtr
	rateLimiting  = *rateLimitingPtr

	if runtime.NumCPU() <=numThreads {
		numThreads = runtime.NumCPU()
	}
	if rateLimiting == 0 {
		suffix = "w/o rate limit" 
	} else {
		suffix = "w/ rate limit" 
	}

	//fmt.Printf("\n============ \n[OS] # of threads >>> %d/%d\n", numThreads, runtime.NumCPU())
	//fmt.Println("[ECC] Point Compression >>>", pointCompression)
	//fmt.Printf("[PMT] Checking membership >>> %s\n", pwd2check)

	//////////////////  PROTOCOL OFFLINE PHASE  /////////////////

	/*  Requester/Receiver Offline Phase */
	pk, _ , reqData := pmt.ReqInit(params, setSize, numThreads, pointCompression) // Key generation and parameter initialization
	queryCTs := pmt.ReqEncryptConstants(pk, reqData) // Precomputes ciphertexts of constants, e.g., 0 or 1.


	/*  Responder/Sender Offline Phase */
	responderSet := make([]string, setSize) // Initializes an empty set
	responderSet[0] = "Simba" // Adds "Simba" as the target string
	for i := 1; i < setSize; i++ {
		responderSet[i] = "Simba" + strconv.Itoa(i) // Fills the set with variants to meet the specified set size
	}
	respFilter := pmt.RespFilterGen(responderSet) // Drops the set into a filter (i.e., a Bloom filter or a cuckoo filter)

	//////////////////  PROTOCOL ONLINE PHASE  /////////////////

	/*  Requester/Receiver Online Phase I: Query Generation */
	timeQueryGenStart := makeTimestamp()
	queryMessage := pmt.QueryGen(pk, []byte(pwd2check), reqData, queryCTs) // Query generation based on input element
	queryMessageBytes:= pmt.EncodeQuery(queryMessage) // Encodes query message into bytes
	queryMessageSize := len(queryMessageBytes) // Gets message size in bytes
	timeQueryGenEnd := makeTimestamp()


	/*  Responder/Sender Online Phase I: Response Generation */
	timeRespGenStart := makeTimestamp()
	rcvQueryMessage := pmt.DecodeQuery(queryMessageBytes) // Decodes query message from bytes
	responseMessage := pmt.ResponseGen(rcvQueryMessage, respFilter) // Generates response based on query
	responseMessageBytes := pmt.EncodeResponse(responseMessage) // Encodes response message to bytes
	timeRespGenEnd := makeTimestamp()


	/*  Requester/Receiver Online Phase II: Response Decryption */
	timeRespDecStart := makeTimestamp()
	_ = pmt.DecodeResponse(responseMessageBytes) // Decodes response message from bytes
	// result := pmt.ResponseDecrypt(pk, sk, reqData, rcvResponseMessage) // Decrypt response to get the result
	responseMessageSize := len(responseMessageBytes) // gets response message size in bytes
	timeRespDecEnd := makeTimestamp()


	//////////////////  PRINTING  /////////////////


	queryGenTime := timeQueryGenEnd - timeQueryGenStart
	if rateLimiting == 1 {
		queryGenTime += 97 // Adding 97 ms time to apply argon2 hash. 
	}
	responseGenTime := timeRespGenEnd - timeRespGenStart
	responseDecTime := timeRespDecEnd - timeRespDecStart

	// fmt.Printf("[R] >>> QueryGen takes %.4f s\n", float32(queryGenTime)/1000000.0)
	fmt.Printf("Query Prep. %s\t%.2f\n",suffix, float32(queryGenTime)) // ms
	fmt.Printf("B/w (MB)\t%.2f\n",(float32(queryMessageSize) + float32(responseMessageSize))/1000000) // MB
	// fmt.Printf("[S] Query message size >>> %.2f KB\n", float32(queryMessageSize)/1000.0)
	fmt.Printf("API call\t%.2f\n",float32(responseGenTime)) // ms
	// fmt.Printf("[S] >>> ResponseGen takes %.4f s\n", float32(responseGenTime)/1000000.0)

	//fmt.Printf("[S] Response message size >>> %.2f KB\n", float32(responseMessageSize)/1000.0)
	// fmt.Printf("[R] >>> ResponseDec takes %.4f s\n", float32(responseDecTime)/1000000.0)
	fmt.Printf("Finalize\t%.2f\n",float32(responseDecTime)) // ms
	total := responseDecTime + responseGenTime + queryGenTime
	fmt.Printf("total_%s\t%.2f\n",suffix, float32(total)) // ms
	// fmt.Println("[R] >>> Result: ", result) // PMT result
}

func makeTimestamp() int64 {
	return time.Now().UnixNano() / int64(time.Millisecond)
}
