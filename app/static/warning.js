let countdown = 5;
const proceedBtn = document.getElementById('proceedBtn');
const countdownDiv = document.getElementById('countdown');

proceedBtn.style.opacity = '0.5';
proceedBtn.style.pointerEvents = 'none';

// timer function, put that shit on 1s interval
const timer = setInterval(() => {
    // set text for the countdown and count it down
    countdownDiv.textContent = `If you really want to... continue in ${countdown} seconds. BE CAREFUL!`;
    countdown--;
    
    // when countdown done
    if (countdown < 0) {
        // clear and hide it
        clearInterval(timer);

        proceedBtn.style.opacity = '1';
        proceedBtn.style.pointerEvents = 'auto';
        proceedBtn.style.boxShadow = '0 0 10px rgba(76, 175, 80, 0.5)';
        countdownDiv.textContent = '';
    }
}, 1000);

// placeholder for click tracking
proceedBtn.addEventListener('click', function() {
    console.log('user proceeded to external link:', '{{ target_url }}');
});