function sendAlive() {
    let xhr = new XMLHttpRequest();
    let url = "status";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    var data = JSON.stringify({
        "player_name" : player_name,
        "game_id" : game_id,
        "status" : "active"
    });
    xhr.send(data);
}

sendAlive();
setInterval(sendAlive, 3000);