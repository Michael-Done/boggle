let url = window.location.href
url = url.substring(0, url.indexOf('/', url.indexOf('//') + 2))

let ws = io.connect(url);

ws.on("connect", () => {});

// handle the event sent with ws.send()
ws.on("message", data => {
    console.log(data);
});

ws.on('player_list', plist => {
    document.getElementById('player_list').innerHTML = "";
    for(let p of plist) {
        if(p === player_name){
            document.getElementById('player_list').innerHTML += ('<li><b>' + p + '</b></li>');
        } else {
            document.getElementById('player_list').innerHTML += ('<li>' + p + '</li>');
        }
    }
});

ws.on('game_board', grid => {
    let board_tbody = document.getElementById('game_board')
    board_tbody.innerHTML = ""
    for(let row in grid) {
        let tr = board_tbody.insertRow();
        for(let col in grid[row]) {
            // square = document.getElementById(String(row) + ',' + String(col));
            // square.innerHTML = grid[row][col];
            let cell = tr.insertCell();
            cell.innerHTML = grid[row][col];
        }
    }
});

async function startGame() {
    ws.emit('start_game', {});
}