package main

import (
	"encoding/json"
	"io/ioutil"
	"net/http"
	"strings"
)

type RequestBody struct {
	Stream bool `json:"stream"`
}

type ResponseData struct {
	Id                string `json:"id"`
	Created           int    `json:"created"`
	Model             string `json:"model"`
	SystemFingerprint string `json:"system_fingerprint"`
	Choices           []struct {
		Message struct {
			Content string `json:"content"`
		} `json:"message"`
	} `json:"choices"`
}

func main() {
	http.HandleFunc("/v1/chat/completions", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == "OPTIONS" {
			w.Header().Set("Access-Control-Allow-Origin", "*")
			w.Header().Set("Access-Control-Allow-Headers", "*")
			w.WriteHeader(204)
			return
		}

		if r.Method != "POST" || r.URL.Path != "/v1/chat/completions" {
			http.Error(w, "Not found", 404)
			return
		}

		url := "https://multillm.ai-pro.org/api/openai-completion"
		req, _ := http.NewRequest("POST", url, r.Body)
		req.Header.Set("Content-Type", "application/json")
		client := &http.Client{}
		resp, err := client.Do(req)

		if err != nil {
			http.Error(w, "Unable to reach the backend API", 502)
			return
		}

		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)

		var requestBody RequestBody
		json.Unmarshal(body, &requestBody)

		var responseData ResponseData
		json.Unmarshal(body, &responseData)

		if requestBody.Stream {
			chunks := strings.Split(responseData.Choices[0].Message.Content, " ")
			var events string

			for _, chunk := range chunks {
				event := map[string]interface{}{
					"id":                responseData.Id,
					"object":            "chat.completion.chunk",
					"created":           responseData.Created,
					"model":             responseData.Model,
					"system_fingerprint": responseData.SystemFingerprint,
					"choices": []map[string]interface{}{
						{
							"index": 0,
							"delta": map[string]string{"content": chunk + " "},
							"logprobs": nil,
							"finish_reason": nil,
						},
					},
				}
				eventJson, _ := json.Marshal(event)
				events += "data: " + string(eventJson) + "\n\n"
			}

			w.Header().Set("Content-Type", "text/event-stream")
			w.Header().Set("Cache-Control", "no-cache")
			w.Header().Set("Connection", "keep-alive")
			w.Write([]byte(events))
		} else {
			w.Write(body)
		}
	})

	http.ListenAndServe(":8080", nil)
}
