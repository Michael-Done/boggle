async function startGame() {
    const data = {
        "round_timer": 60*3
    }

    const response = await fetch("/" + String(game_id), {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json"
      }
    })
}

async function sendAlive() {
    const data = {
        "player_name" : player_name,
        "game_id" : game_id,
        "status" : "active"
    }
  
    const response = await fetch("/" + String(game_id), {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json"
      }
    })
}

async function recieveJson(response) {
    if(response.ok) {
        let json = await response.json();
        console.log(json.board);
        if(json.board) {
            let r = 0
            let c = 0
            for(let row of json.board) {
                for(let square of row) {
                    console.log(String(r) + "," + String(c));
                    let el = document.getElementById(String(r) + "," + String(c));
                    el.innerHTML = square;
                    c += 1
                }
                c = 0
                r += 1
            }
        }
    }
}

sendAlive();
setInterval(sendAlive, 3000);