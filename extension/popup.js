var ws_host = $("#ws_host")
chrome.storage.sync.get(['ws_host'], function(result){
    ws_host.val(result['ws_host']);
});
ws_host.on("change", function(){
    var host = $(this).val();
    console.log("Host " + host);
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {"ws_host": host});
    });
    chrome.storage.sync.set({'ws_host': host}, function(){
        console.log("Websocket Host Updated to " + host);
    });
});

