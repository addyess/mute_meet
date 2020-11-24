function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function encapsulate(msg) {
    let token = getCookie("gapi_token");
    if (token) { msg.token = token; }
    return JSON.stringify(msg);
}


function addRow(id, uuid){
    let btnClass = (uuid == 'all') ? 'btn-outline-primary' : 'btn-outline-secondary';
    let buttons = ['mic', 'camera', 'cc', 'leave'].map(v =>
        '<button class="btn '+ btnClass +'" value="'+ uuid +'">'+ v +'</button>'
    );
    let row = (
      '<tr>'+
      '<th scope="col">' + id + '</th><td>' +
      '<div class="btn-group btn-group-toggle" data-toggle="buttons">' +
       buttons.join('') +
      '</div>' +
      '</td></tr>'
    );
    $('#sessions tbody').append(row);
}

function handleMsg(event) {
    var _socket = this;
    let resp = JSON.parse(event.data);
    let sessions = resp["meet-sessions"] || [];

    $('#sessions tbody').empty();
    if (sessions.length){ addRow('ALL', 'all'); }
    sessions.forEach(function(session, idx){
        addRow(session.id, session.uuid);
    });

    $('#sessions button').click(function(){
        let uuid = $(this).attr('value');
        let device = $(this).text();
        if (uuid == "all") {
            uuid = resp['meet-sessions'].map(v => v.uuid);
        } else {
            uuid = [uuid];
        }

        uuid.forEach(function(uuid){
            let msg = encapsulate({
                type: "controller",
                action: {
                    device: device,
                    uuid: uuid,
                }
            })
            _socket.send(msg);
        });
    })
}

$(document).ready(() => {
    function createSocket(addresses){
        head = addresses.shift();
        var _socket = new WebSocket(head);
        _socket.onerror=function(){
            createSocket(addresses);
        }
        _socket.onmessage = handleMsg;
        _socket.onopen = function(event) {
            let msg = { type: "controller" };
            this.send(encapsulate(msg));
        }
    }
    createSocket([
        'wss://' + location.host + "/websocket",
        'ws://localhost:8001'
    ]);
});
