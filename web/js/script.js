document.getElementById("btn-selectFolder").addEventListener("click", click);

//Handle click
function click() {
    eel.select_folder()(function(eel_select_return) {
        let selected_files = eel_select_return[0];
        let root = eel_select_return[1];

        //Display a spinner
        var spinner_place = document.getElementById("spinnerPlace");
        spinner_place.innerHTML = '<div class="spinner-border text-light mt-2" role="status"></div>';

        // Process selected files with python
        eel.process_selected_files(selected_files, root)(function(eel_process_return) {
            console.log(eel_process_return);
            display(eel_process_return);
            //Remove the spinner
            spinner_place.innerHTML = '<p class="word text-center m-0">that contains any .mp3 files</p>';
        });
    });
}

//Array for music-score pairs, always exists
var existingItems=new Array();

//Prevent repetition，sort when add item
function display(results) {
    for (var i = 0; i < results.length; i++) {
        let result = results[i];
        let exists = false;
        // Check repeating items, existingItems[0] and result[0] are the names of the files
        for (var j = 0; j < existingItems.length; j++) {
            if (existingItems[j][0] == result[0]) {
                exists = true;
                break;
            }
        }
        if (!exists) {
            var place = find_place(result[1]); // results[1] is the score of the given music
            existingItems.splice(place, 0, result); // Sort results by score
        }
    }

    //Display all results
    var out_list = document.getElementById("outList");
    out_list.innerHTML = '';
    existingItems.forEach(function(item) {
        var li = document.createElement("li");
        li.className = "result-list-item"
        li.textContent = item[1] + " —— " + item[0];
        out_list.appendChild(li);
    });
}

function find_place(scoreInt) {
    for (var i = 0; i < existingItems.length; i++) {
        if (scoreInt >= existingItems[i][1]) {return i}
    }
    return existingItems.length;
}
