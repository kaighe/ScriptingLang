var base_url = "https://207.81.219.142:1945/run/"
//var base_url = "https://192.168.1.200:1945/run/"
var running = false
var button_element = document.getElementsByClassName("run-button")[0];
var input_element = document.getElementById("input");
var output_element = document.getElementById("output");

function run_code(){
    code = input_element.value;
    code_url = encodeURIComponent(code);

    if(!running){
        running = true
        button_element.classList.add("running")
        button_element.innerText = "Running..."
        console.log(code_url)
        
        fetch(base_url + code_url, {
            mode: 'cors'
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            output_element.innerText = data.out
            running = false
            button_element.classList.remove("running")
            button_element.innerText = "Run"
            output_element.scrollTo(0, output_element.scrollHeight);
        }).catch(function(err) {
            base_url = "https://192.168.1.200:1945/run/"
            fetch(base_url + code_url, {
                mode: 'cors'
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                output_element.innerText = data.out
                running = false
                button_element.classList.remove("running")
                button_element.innerText = "Run"
                output_element.scrollTo(0, output_element.scrollHeight);
            }).catch(function(err) {
                alert("Servers are currently down.");
            });
        });
    }
}