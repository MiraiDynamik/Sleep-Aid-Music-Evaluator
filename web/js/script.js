// Array for music-score pairs
var existingItems=new Array();


//Handle click
document.getElementById("btn-selectFolder").addEventListener("click", click);
function click() {
    eel.select_folder()(function(eel_select_return) {
        let selectedFiles = eel_select_return[0];
        let selectedRoot = eel_select_return[1];

         // Display a spinner
        var spinner_place = document.getElementById("spinnerPlace");
        spinner_place.innerHTML = '<div class="spinner-border text-light mt-2" role="status"></div>';

        // Prevent repeating items
        selectedFiles = selectedFiles.filter(file => !existingItems.some(item => item[0] === file));

        // Process selected files with python
        eel.process_selected_files(selectedFiles, selectedRoot)(function(eel_process_return) {
            console.log(eel_process_return);
            display_results(eel_process_return);

            // Remove the spinner
            spinner_place.innerHTML = '<p class="word text-center m-0">that contains any .mp3 files</p>';
        });
    });
}

// Array for music-score pairs, always exists
var existingItems=new Array();

// Prevent repetition，sort when add item
function display_results(results) {
    for (var i = 0; i < results.length; i++) {
        var place = find_insertion_index(results[i][1]); // results[i][1] is the score of music file i
        existingItems.splice(place, 0, results[i]); // Sort results by score
    }

    // Display all results
    var out_list = document.getElementById("outList");
    out_list.innerHTML = '';
    existingItems.forEach(function(item) {
        var li = document.createElement("li");
        li.className = "result-list-item"
        li.textContent = item[1] + " —— " + item[0];
        out_list.appendChild(li);
    });
}


function find_insertion_index(scoreInt) {
    for (var i = 0; i < existingItems.length; i++) {
        if (scoreInt >= existingItems[i][1]) {return i}
    }
    return existingItems.length;
}
