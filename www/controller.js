function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

function client_id(set_value = undefined){
    dom_id = $("#client_id");
    if (set_value != undefined) {
        // Setting value
        if (dom_id.length == 0) {
            return $('<input>', {
                type: 'hidden',
                id: 'client_id',
                name: 'client_id',
                value: set_value
            }).appendTo($("body"))
        } else {
            return dom_id.value(set_value);
        }
  } else {
    // getting value
    return (dom_id.length != 0) ? dom_id.val() : undefined;
  }
}

function encapsulate(msg) {
    if (!msg.type){ msg.type= "controller"; }
    return JSON.stringify(msg);
}

function signOut() {
    gapi.load('auth2', () => {
        var auth2 = gapi.auth2.getAuthInstance();
        auth2.signOut().then(function () {
            $("#sessions").hide();
        });
    });
}

function addRow(id, uuid){
    let btnClass = (uuid == 'all') ? 'btn-primary' : 'btn-secondary';
    let buttons = ['mic', 'camera', 'cc', 'leave'].map(v =>
        '<button class="btn '+ btnClass +'" value="'+ uuid +'">'+ v +'</button>'
    );
    let row = (
      '<tr>'+
      '<th scope="col">' + id + '</th><td>' +
      '<div class="btn-group">' +
       buttons.join('') +
      '</div>' +
      '</td></tr>'
    );
    $('#sessions tbody').append(row);
}

function populate_control_table(event, _socket) {
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


function handleMsg(event) {
    var _socket = this;
    let resp = JSON.parse(event.data);
    if (!client_id()) {
        if ("client_id" in resp) {
            gapi.load('auth2', () => {
                gapi.auth2.init(resp).then(() => {
                    client_id(resp.client_id);
                    gapi.signin2.render('myGoogleButton',
                    {
                        'scope': 'profile email',
                        'width': 240,
                        'height': 40,
                        'longtitle': true,
                        'theme': 'dark',
                        'onsuccess': (googleUser) => {
                            var id_token = googleUser.getAuthResponse().id_token;
                            $("#sessions").show();
                            _socket.send(encapsulate({token:id_token}));
                        },
                        'onfailure': () => {
                            $("#sessions").hide();
                        }
                    });
                })
            });
        } else {
            // No web application client_id specified -- go into controller,
            // without user access controls
            $("#sessions").show();
            _socket.send(encapsulate({}));
        }
    }
    populate_control_table(event, _socket);
}

function googleInit(){
    function createSocket(addresses){
        head = addresses.shift();
        var _socket = new WebSocket(head);
        _socket.onerror=function(){
            createSocket(addresses);
        }
        _socket.onmessage = handleMsg;
        _socket.onopen = function(event) {
            let msg = { type: "get_client_id" };
            this.send(encapsulate(msg));
        }
    }
    createSocket([
        'wss://' + location.host + "/websocket",    // use this for production
        'ws://localhost:8001'                       // use this for testing
    ]);
    $("#sign-out").click(signOut);
};
