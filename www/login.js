function handleMsg(event) {
    var _socket = this;
    let resp = JSON.parse(event.data);
    if ("client_id" in resp) {
        gapi.load('auth2', () => {
            gapi.auth2.init(resp).then(() => {
                gapi.signin2.render('myGoogleButton',
                {
                    'scope': 'profile email',
                    'width': 240,
                    'height': 40,
                    'longtitle': true,
                    'theme': 'dark',
                    'onsuccess': (googleUser) => {
                        var id_token = googleUser.getAuthResponse().id_token;
                        document.cookie = "gapi_token=" + id_token + "; SameSite=Lax";
                        window.location.href = "controller.html"
                    },
                    'onfailure': () => {}
                });
            })
        });
    } else {
        // No web application client_id specified -- go into controller,
        // without user access controls
        document.cookie = "gapi_token=; SameSite=Lax";
        window.location.href = "controller.html"
    }
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
            this.send(JSON.stringify(msg));
        }
    }
    createSocket([
        'wss://' + location.host + "/websocket",    // use this for production
        'ws://localhost:8001'                       // use this for testing
    ]);
};
