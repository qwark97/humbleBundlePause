package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"time"
)

var (
	PYTHON string
	PORT   string
)

func main() {
	loadEnvs()
	http.HandleFunc("/pause", scriptExecutor)
	log.Println(fmt.Sprintf("start at: 127.0.0.1:%s", PORT))
	log.Fatal(http.ListenAndServe(fmt.Sprintf(":%s", PORT), nil))
}

func scriptExecutor(w http.ResponseWriter, _ *http.Request) {
	log.Println("received request")
	w.Header().Set("Content-Type", "application/json")
	resp := response{}
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, PYTHON, "main.py")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		log.Printf("request failed with error: %s\n", err.Error())
		w.WriteHeader(http.StatusInternalServerError)
		resp.Code = http.StatusInternalServerError
		resp.Message = "process failed"
		json.NewEncoder(w).Encode(&resp)
	} else {
		log.Println("request succeeded")
		resp.Code = http.StatusOK
		resp.Message = "humble bundle paused, check mail to confirm"
		json.NewEncoder(w).Encode(&resp)
	}
}

func loadEnvs() {
	PYTHON = os.Getenv("HBP_PYTHON_PATH")
	if PYTHON == "" {
		log.Panicln("Env HBP_PYTHON_PATH is needed")
	}
	PORT = os.Getenv("HBP_PORT")
	if PORT == "" {
		log.Panicln("Env HBP_PORT is needed")
	}

	// below are being used by ran subprocess so must be present
	chromedriver := os.Getenv("HBP_CHROMEDRIVER_PATH")
	if chromedriver == "" {
		log.Panicln("Env HBP_CHROMEDRIVER_PATH is needed")
	}
	profile := os.Getenv("HBP_BROWSER_PROFILE_PATH")
	if profile == "" {
		log.Panicln("Env HBP_BROWSER_PROFILE_PATH is needed")
	}
}

type response struct {
	Code    int    `json:"code"`
	Message string `json:"msg"`
}
