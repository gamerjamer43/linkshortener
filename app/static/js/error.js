// set current timestamp
document.getElementById('timestamp').textContent = new Date().toLocaleString();

// try to get requested URL and params from the page
const currentUrl = window.location.href;
const urlDisplay = document.getElementById('requestedUrl');
const urlParams = new URLSearchParams(window.location.search);
const shortCode = urlParams.get('code');

// set content afterwards based on url and short
if (currentUrl) {
    urlDisplay.textContent = currentUrl;
}

if (shortCode) {
    urlDisplay.textContent = window.location.host + '/' + shortCode;
}