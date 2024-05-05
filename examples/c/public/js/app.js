// Initialize the chessboard
function initChessboard() {
    const chessboard = document.getElementById('chessboard');

    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            const square = document.createElement('div');
            square.classList.add('square');

            if ((i + j) % 2 === 0) {
                square.classList.add('square-white');
            } else {
                square.classList.add('square-black');
            }

            chessboard.appendChild(square);
        }
    }
}

// Initialize the game
function initGame() {
    initChessboard();
    // Add game logic here
}

// Start the game
initGame();