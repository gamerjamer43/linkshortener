// index.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('shorten-form');
  const resultDiv = document.getElementById('result');
  const resultText = document.getElementById('resultText');
  const copyBtn = document.getElementById('copyBtn');
  const visitBtn = document.getElementById('visitBtn');

  // keep result structure and buttons intact, update values instead of replacing HTML
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('link').value.trim();
    const ending = document.getElementById('ending').value.trim();
    const duration = document.getElementById('duration').value;

    // show in-progress state
    resultText.textContent = 'Shortening…';
    resultDiv.style.display = 'block';
    visitBtn.href = '#';
    visitBtn.setAttribute('aria-disabled', 'true');

    // then actually post, catch errors safely
    try {
      const res = await fetch('/shorten', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, ending, duration })
      });
    
      // WOOHOO! WE DID IT!
      const data = await res.json();
      if (res.ok && data.shortened_url) {
        // set text and buttons
        resultText.textContent = data.shortened_url;
        resultDiv.setAttribute('data-short', data.shortened_url);
        visitBtn.href = data.shortened_url;
        visitBtn.removeAttribute('aria-disabled');
      } 
      
      else {
        resultText.textContent = `Error: ${data.error || 'Unknown error'}`;
        visitBtn.href = '#';
        visitBtn.setAttribute('aria-disabled', 'true');
      }
    } 
    
    catch (err) {
      resultText.textContent = 'Error: Failed to shorten URL';
      visitBtn.href = '#';
      visitBtn.setAttribute('aria-disabled', 'true');
    }
  });

  // copy button
  if (copyBtn) {
    copyBtn.addEventListener('click', async () => {
      const short = resultDiv.getAttribute('data-short') || resultText.textContent;
      if (!short) return;

      try {
        await navigator.clipboard.writeText(short);
        copyBtn.textContent = 'Copied!';
        setTimeout(() => copyBtn.textContent = 'Copy', 1400);
      } 
      
      catch (e) {
        copyBtn.textContent = 'Copy failed';
        setTimeout(() => copyBtn.textContent = 'Copy', 1400);
      }
    });
  }
});
