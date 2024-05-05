document.addEventListener('DOMContentLoaded', function() {
    fetchTimes();
    setInterval(fetchTimes, 1000);
});

function fetchTimes() {
    fetch('/api/times')
        .then(response => response.json())
        .then(data => {
            displayClocks(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function displayClocks(times) {
    const clockContainer = document.getElementById('clock-container');
    clockContainer.innerHTML = '';

    times.forEach(time => {
        const clockDiv = document.createElement('div');
        clockDiv.classList.add('clock');

        const clockFace = document.createElement('div');
        clockFace.classList.add('clock-face');

        const hourHand = document.createElement('div');
        hourHand.classList.add('hand', 'hour-hand');
        const minuteHand = document.createElement('div');
        minuteHand.classList.add('hand', 'minute-hand');
        const secondHand = document.createElement('div');
        secondHand.classList.add('hand', 'second-hand');

        const timeInfo = document.createElement('div');
        timeInfo.classList.add('clock-info');
        timeInfo.textContent = `${time.country}: ${time.time}`;

        const currentTime = new Date(time.time);
        const hours = currentTime.getHours();
        const minutes = currentTime.getMinutes();
        const seconds = currentTime.getSeconds();

        const hoursDegrees = (hours / 12) * 360 + (minutes / 60) * 30 + 90;
        hourHand.style.transform = `rotate(${hoursDegrees}deg)`;

        const minutesDegrees = (minutes / 60) * 360 + (seconds / 60) * 6 + 90;
        minuteHand.style.transform = `rotate(${minutesDegrees}deg)`;

        const secondsDegrees = (seconds / 60) * 360 + 90;
        secondHand.style.transform = `rotate(${secondsDegrees}deg)`;

        clockFace.appendChild(hourHand);
        clockFace.appendChild(minuteHand);
        clockFace.appendChild(secondHand);

        clockDiv.appendChild(clockFace);
        clockDiv.appendChild(timeInfo);

        clockContainer.appendChild(clockDiv);
    });
}