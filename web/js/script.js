document.getElementById("btn-selectFolder").addEventListener("click", function() {
    eel.select_folder()(function(response)

    {
        let selected_files = response[0];
        let root = response[1];
        eel.process_selected_files(selected_files, root)(function(results) {
            console.log(results);
            display(results);
        });
    });
})

var existingItems=new Array();

function display(results) {
    //prevent repetition and sort
    for (var i = 0; i < results.length; i++) {
        let result = results[i];
        let exists = false;
        for (var j = 0; j < existingItems.length; j++) {
            if (existingItems[j][0] == result[0]) { // existingItems[0] and result[0] are the names of the files
                exists = true;
                break;
            }
        }
        if (!exists) {
            var place = find_place(result[1]); // results[1] is the score of the given music
            existingItems.splice(place, 0, result); // the results are sorted by score
        }
    }

    //display all results
    var outList = document.getElementById("outList");
    outList.innerHTML = '';
    existingItems.forEach(function(item) {
        var li = document.createElement("li");
        li.className = "result-list-item"
        li.textContent = item[1] + "   " + item[0];
        outList.appendChild(li);
    });
}

function find_place(scoreInt) {
    for (var i = 0; i < existingItems.length; i++) {
        if (scoreInt >= existingItems[i][1]) {return i}
    }
    return existingItems.length;
}
