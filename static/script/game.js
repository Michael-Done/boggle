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
        tr.className = 'board_row'
        for(let col in grid[row]) {
            let cell = tr.insertCell();
            cell.className = 'board_cell'
            cell.innerHTML = grid[row][col];
        }
    }
});

ws.on('settings', settings => {
    document.getElementById('round_timer').value = settings['round_timer'];
    document.getElementById('board_size').value = settings['board_size'];
    document.getElementById('word_length').value = settings['word_length'];
});

function changeSettings() {
    let settings = {
        'round_timer' : document.getElementById('round_timer').value,
        'board_size' : document.getElementById('board_size').value,
        'word_length' : document.getElementById('word_length').value
    }
    ws.emit('set_settings', settings);
}

function startGame() {
    ws.emit('start_game');
}

function submitWord(event) {
    if (event.keyCode == 13) {
        field = document.getElementById('player_text_input')
        ws.emit('add_word', field.value)
    }
}