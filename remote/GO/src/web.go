package src

import (
	"fmt"
	"io/ioutil"
	"net/http"

	mqtt "github.com/eclipse/paho.mqtt.golang"

)

func index(w http.ResponseWriter, r *http.Request) {
	tpl.Execute(w, nil)
}
func handler(client mqtt.Client, topic string) http.HandlerFunc {
	output := ""
	return func (w http.ResponseWriter, r *http.Request) {
		t, _ := ioutil.ReadAll(r.Body)
		val := string(t)
		switch val {
		case "blue":
			output = "pause"
		case "green":
			output = "-20"		
		case "percent":
				output = "%20"
		case "red":
			output = "+5"
		case "yellow":
			output = "Explode"
		default:
			output = val
		}
		fmt.Println(output)
		publish(client, topic, output)
	}
}
func inHandler(press *string) http.HandlerFunc {

	return func (w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, *press)
	}
}
