let url = window.location.href
url = url.substring(0, url.indexOf('/', url.indexOf('//') + 2))

let ws = io.connect(url);
let pingID;

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

ws.on('start_round', () => {
    pingID = setInterval(function(){ws.emit('ping_game')}, 500);
    disableSettings(true);

    document.getElementById('player_text_input').disabled = false;
    document.getElementById('player_text_input').focus();
    document.getElementById('player_text_input').select();
});

ws.on('end_round', () => {
    clearInterval(pingID);
    disableSettings(false);
    document.getElementById('player_text_input').disabled = true;
});

ws.on('timer', time => {
    document.getElementById('timer').innerHTML = time;
});

ws.on('invalid_word', msg => {
    setWordMsg(msg);
});

ws.on('word_list', words => {
    word_list = document.getElementById('word_list');
    word_list.innerHTML = "";

    for(let word of words) {
        word_list.innerHTML += ('<li>' + word + '</li>');
    }
})

function submitWord(event) {
    if (event.keyCode == 13) {
        field = document.getElementById('player_text_input')
        ws.emit('add_word', field.value)
        field.value = "";
    }
}

function formatInput() {
    field = document.getElementById("player_text_input");
    field.value = field.value.trim().toLowerCase();
}

let word_msg_opacity = 1;
let word_msg_timer;
function setWordMsg(msg) {
    let element = document.getElementById('word_msg')
    element.innerHTML = msg
    word_msg_opacity = 1;  // initial opacity
    clearInterval(word_msg_timer);
    word_msg_timer = setInterval(function () {
        if (word_msg_opacity <= 0.1){
            clearInterval(word_msg_timer);
        }
        element.style.opacity = word_msg_opacity;
        element.style.filter = 'alpha(opacity=' + word_msg_opacity * 100 + ")";
        word_msg_opacity -= word_msg_opacity * 0.1;
    }, 150);
}

function disableSettings(disabled) {
    document.getElementById('round_timer').disabled = disabled;
    document.getElementById('board_size').disabled = disabled;
    document.getElementById('word_length').disabled = disabled;
    document.getElementById('start_button').disabled = disabled;
}

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