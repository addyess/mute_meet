var socket = null;
(function(){
    if (socket === null){
        class UIElement {
            constructor (onLabel, offLabel) {
                this.onLabel = onLabel;
                this.offLabel = offLabel;
            }
            on() {
                let button = this.getButton(this.onLabel);
                button && button.click();
                return button != null;
            }

            off() {
                let button = this.getButton(this.offLabel);
                button && button.click();
                return button;
            }

            toggle() {
                if (this.off() == null){
                    this.on();
                }
            }
        }

        class Muter extends UIElement {
            constructor(device, key) {
                let ctrlKey = '(ctrl + ' + key + ')';
                let onLabel = '[aria-label="Turn on ' + device + ' ' + ctrlKey +'"]';
                let offLabel = '[aria-label="Turn off '+ device + ' ' + ctrlKey +'"]';
                super(onLabel, offLabel);
            }
            getButton(label) {
                return document.querySelector(label);
            }
        }

        class CCMuter extends UIElement {
            constructor() {
                super("Turn on captions", "Turn off captions");
            }
            getButton(label) {
                let xpath = "//div[contains(text(),'captions')]";
                return document.evaluate(xpath, document, null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            }
        }

        var micButton = new Muter("microphone", "d");
        var camButton = new Muter("camera", "e");
        var ccButton = new CCMuter();
        eval(document.querySelector('#_ij').innerText);
        var email = window.IJ_values.filter(v => (typeof(v) == "string" && v.includes("@")));
        create_socket = function(ws_host) {
            if (socket != null) { socket.close(); }
            socket = new WebSocket(ws_host);
            socket.onmessage = function(event) {
                let resp = JSON.parse(event.data);
                if (resp.toggle == "mic") { micButton.toggle(); }
                else if (resp.toggle == "camera") { camButton.toggle(); }
                else if (resp.toggle == "cc") { ccButton.toggle(); }
            };
            socket.onclose = function(event) {
                let msg = {"logout": true};
                this.send(JSON.stringify(msg));
            };
            socket.onopen = function(event) {
                let msg = { type: "extension", user: email };
                this.send(JSON.stringify(msg));
            };
        };
        chrome.storage.sync.get(['ws_host'], function(result){
            create_socket(result['ws_host']);
        });
        chrome.storage.onChanged.addListener( function(changes){
            for (var key in changes){
                if (key == "ws_host"){
                    create_socket(changes[key].newValue);
                }
            }
        });
    }
})();