const express = require('express');
const app = express();
const path = require('path');

app.use(express.static(path.join(__dirname, 'public')));

app.get('/api/times', (req, res) => {
    const currentTime = new Date();
    const times = [
        { country: 'New York', time: currentTime.toLocaleString('en-US', { timeZone: 'America/New_York' }) },
        { country: 'London', time: currentTime.toLocaleString('en-US', { timeZone: 'Europe/London' }) },
        { country: 'Tokyo', time: currentTime.toLocaleString('en-US', { timeZone: 'Asia/Tokyo' }) },
        { country: 'Sydney', time: currentTime.toLocaleString('en-US', { timeZone: 'Australia/Sydney' }) },
        { country: 'San Francisco', time: currentTime.toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }) }
    ];
    res.json(times);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});