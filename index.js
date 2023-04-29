var base_url = "https://207.81.219.142:1945/run/"
//var base_url = "https://192.168.1.200:1945/run/"
var running = false

function run_code(){
    input = document.getElementById("input");
    code = input.value;
    code_url = encodeURIComponent(code);

    if(!running){
        running = true
        console.log(code_url)
        
        fetch(base_url + code_url, {
            mode: 'cors'
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            output = document.getElementById("output");
            output.innerText = data.out
            running = false
        }).catch(function(err) {
            base_url = "https://192.168.1.200:1945/run/"
            fetch(base_url + code_url, {
                mode: 'cors'
            }).then(function(response) {
                return response.json();
            }).then(function(data) {
                output = document.getElementById("output");
                output.innerText = data.out
                running = false
            }).catch(function(err) {
                alert("Servers are currently down.");
            });
        });
    }
}