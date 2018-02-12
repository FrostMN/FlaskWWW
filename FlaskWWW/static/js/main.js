window.setTimeout(hide_flash, 1000);

function toggle_details(id) {
    var event = document.getElementById(id);
    if (event.style.display === "none") {
        event.style.display = "block";
    } else {
        event.style.display = "none";
    }
}

function show_modal(id) {
    var modal = document.getElementById(id);
    modal.style.display = "block";
}

function closeModal(obj) {
    var element = obj;
    while (element.className !== 'modal') {
        element = element.parentNode
    }
    element.style.display = "none";
}

function hide_flash() {
    var flashed = document.getElementById("flashed");
    if (flashed !== null) {
        fade(flashed);
    }
}

// found this function at https://stackoverflow.com/questions/6121203/how-to-do-fade-in-and-fade-out-with-javascript-and-css
function fade(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1){
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
}

function populateDays() {
    var month = document.getElementById("month").value;
    var days = document.getElementById("days");
    var year = document.getElementById("year").value;

    while (days.firstChild) {
        days.removeChild(days.firstChild);
    }

    switch (month) {
        case "1":
            setDaysInMonth(31, days);
            break;
        case "2":
            if ((year % 4) === 0 ) {
                setDaysInMonth(29, days);
            } else {
                setDaysInMonth(28, days);
            }
            break;
        case "3":
            setDaysInMonth(28, days);
            break;
        case "4":
            setDaysInMonth(30, days);
            break;
        case "5":
            setDaysInMonth(31, days);
            break;
        case "6":
            setDaysInMonth(30, days);
            break;
        case "7":
            setDaysInMonth(31, days);
            break;
        case "8":
            setDaysInMonth(31, days);
            break;
        case "9":
            setDaysInMonth(30, days);
            break;
        case "10":
            setDaysInMonth(31, days);
            break;
        case "11":
            setDaysInMonth(30, days);
            break;
        default:
            setDaysInMonth(31, days);
    }
}

function setDaysInMonth(days_in_month, days) {
    for (var i = 1; i <= days_in_month; i++) {
        var d = document.createElement("option");
        d.innerHTML = i;
        d.value = i;
        days.appendChild(d);
    }
}

function updateItemCount(event_id, item_id, update_url, key) {
    // alert("Event: " + event_id + ", Item: " + item_id);
    // var update_url = update_url;
    // alert({{ config["ITEMS_URL"] }})

    var count_id = "count_" + event_id + "_" + item_id;
    // alert(count_id);
    var count = document.getElementById(count_id).value;
    // alert(count);
    var full_update_url = update_url + "/api/v1/" + key + "/items/" + item_id;
    // alert(update_url);
    var xlr = new XMLHttpRequest();

    xlr.open('POST', full_update_url, true);

    var post_data = "event_id=" + event_id + "&item_id=" + item_id + "&count=" + count;

    xlr.send(post_data)
}


