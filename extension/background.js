chrome.runtime.onInstalled.addListener(function() {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
      chrome.declarativeContent.onPageChanged.addRules([{
        conditions: [new chrome.declarativeContent.PageStateMatcher({
          pageUrl: {hostEquals: 'meet.google.com', schemes: ['https']},
        })],
        actions: [new chrome.declarativeContent.ShowPageAction()]
      }]);
    });
});