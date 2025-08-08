document.getElementById('shorten-form').addEventListener('submit', async function(e) {
    // prevent default submission
    e.preventDefault();
    
    // get everything special we need
    const url = document.getElementById('link').value;
    const ending = document.getElementById('ending').value;
    const resultDiv = document.getElementById('result');
    
    // initial styling
    resultDiv.innerHTML = `<p style="color: #ff9800;">Shortening...</p>`;
    resultDiv.style.display = 'block';
    
    try {
        // get response frm the api
        const response = await fetch('/shorten', {
            // headers
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },

            // jsonify that shit
            body: JSON.stringify({
                url: url,
                ending: ending
            })
        });
        
        const data = await response.json();
        
        // if we get a url
        if (response.ok) {
            resultDiv.innerHTML = `<p><a href="${data.shortened_url}" target="_blank" style="color: #007BFF;">${data.shortened_url}</a></p>`;
        } 
        
        // otherwise if error
        else {
            resultDiv.innerHTML = `<p style="color: #ff6b6b;">Error: ${data.error}</p>`;
        }

    
    } 
    
    // double layered
    catch (error) {
        resultDiv.innerHTML = `<p style="color: #ff6b6b;">Error: Failed to shorten URL</p>`;
    }
});