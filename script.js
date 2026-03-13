// Sudoku Game with Points and Lives System
// Author: Red Donaldson
// Date: March 13, 2026

class SudokuGame {
    constructor() {
        this.board = [];
        this.solution = [];
        this.initialBoard = [];
        this.lives = 3;
        this.maxLives = 3;
        this.score = 0;
        this.selectedCell = null;
        this.difficulty = 'medium';
        this.timerInterval = null;
        this.seconds = 0;
        this.gameOver = false;
        
        this.difficultySettings = {
            easy: { cellsToRemove: 30, lives: 3, pointsPerCell: 5 },
            medium: { cellsToRemove: 40, lives: 3, pointsPerCell: 10 },
            hard: { cellsToRemove: 50, lives: 5, pointsPerCell: 15 }
        };
        
        this.init();
    }
    
    init() {
        this.createBoard();
        this.setupEventListeners();
        this.newGame();
    }
    
    createBoard() {
        const boardElement = document.getElementById('sudoku-board');
        boardElement.innerHTML = '';
        
        for (let i = 0; i < 81; i++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.index = i;
            cell.addEventListener('click', () => this.selectCell(i));
            boardElement.appendChild(cell);
        }
    }
    
    setupEventListeners() {
        // Number buttons
        document.querySelectorAll('.number-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const number = parseInt(btn.dataset.number);
                this.placeNumber(number);
            });
        });
        
        // Control buttons
        document.getElementById('new-game-btn').addEventListener('click', () => this.newGame());
        document.getElementById('hint-btn').addEventListener('click', () => this.giveHint());
        document.getElementById('check-btn').addEventListener('click', () => this.checkSolution());
        
        // Difficulty selector
        document.getElementById('difficulty').addEventListener('change', (e) => {
            this.difficulty = e.target.value;
        });
        
        // Keyboard input
        document.addEventListener('keydown', (e) => {
            if (this.gameOver) return;
            
            if (e.key >= '1' && e.key <= '9') {
                this.placeNumber(parseInt(e.key));
            } else if (e.key === 'Backspace' || e.key === 'Delete' || e.key === '0') {
                this.placeNumber(0);
            }
        });
    }
    
    newGame() {
        this.gameOver = false;
        this.score = 0;
        this.seconds = 0;
        
        // Set lives based on difficulty
        this.maxLives = this.difficultySettings[this.difficulty].lives;
        this.lives = this.maxLives;
        
        // Generate a new puzzle
        this.solution = this.generateCompleteSudoku();
        this.board = JSON.parse(JSON.stringify(this.solution));
        this.removeNumbers();
        this.initialBoard = JSON.parse(JSON.stringify(this.board));
        
        this.updateDisplay();
        this.renderBoard();
        this.startTimer();
        this.showMessage('New game started! Good luck!', 'info');
    }
    
    generateCompleteSudoku() {
        const board = Array(9).fill(null).map(() => Array(9).fill(0));
        this.fillBoard(board);
        return board;
    }
    
    fillBoard(board, row = 0, col = 0) {
        if (row === 9) return true;
        if (col === 9) return this.fillBoard(board, row + 1, 0);
        
        const numbers = this.shuffleArray([1, 2, 3, 4, 5, 6, 7, 8, 9]);
        
        for (let num of numbers) {
            if (this.isValidPlacement(board, row, col, num)) {
                board[row][col] = num;
                if (this.fillBoard(board, row, col + 1)) return true;
                board[row][col] = 0;
            }
        }
        
        return false;
    }
    
    isValidPlacement(board, row, col, num) {
        // Check row
        for (let x = 0; x < 9; x++) {
            if (board[row][x] === num) return false;
        }
        
        // Check column
        for (let x = 0; x < 9; x++) {
            if (board[x][col] === num) return false;
        }
        
        // Check 3x3 box
        const boxRow = Math.floor(row / 3) * 3;
        const boxCol = Math.floor(col / 3) * 3;
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                if (board[boxRow + i][boxCol + j] === num) return false;
            }
        }
        
        return true;
    }
    
    removeNumbers() {
        const cellsToRemove = this.difficultySettings[this.difficulty].cellsToRemove;
        let removed = 0;
        
        while (removed < cellsToRemove) {
            const row = Math.floor(Math.random() * 9);
            const col = Math.floor(Math.random() * 9);
            
            if (this.board[row][col] !== 0) {
                this.board[row][col] = 0;
                removed++;
            }
        }
    }
    
    shuffleArray(array) {
        const arr = [...array];
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
        return arr;
    }
    
    selectCell(index) {
        if (this.gameOver) return;
        
        const row = Math.floor(index / 9);
        const col = index % 9;
        
        // Can't select pre-filled cells
        if (this.initialBoard[row][col] !== 0) return;
        
        this.selectedCell = index;
        this.renderBoard();
    }
    
    placeNumber(number) {
        if (this.gameOver || this.selectedCell === null) return;
        
        const row = Math.floor(this.selectedCell / 9);
        const col = this.selectedCell % 9;
        
        // Can't modify pre-filled cells
        if (this.initialBoard[row][col] !== 0) return;
        
        // Erase
        if (number === 0) {
            this.board[row][col] = 0;
            this.renderBoard();
            return;
        }
        
        // Check if the number is correct
        const isCorrect = this.solution[row][col] === number;
        
        if (isCorrect) {
            this.board[row][col] = number;
            const points = this.difficultySettings[this.difficulty].pointsPerCell;
            this.score += points;
            this.showMessage(`Correct! +${points} points`, 'success');
            
            // Check if puzzle is complete
            if (this.isPuzzleComplete()) {
                this.winGame();
            }
        } else {
            this.lives--;
            this.showMessage(`Wrong! -1 life`, 'error');
            
            // Flash incorrect
            const cells = document.querySelectorAll('.cell');
            cells[this.selectedCell].classList.add('incorrect');
            setTimeout(() => {
                cells[this.selectedCell].classList.remove('incorrect');
            }, 500);
            
            if (this.lives <= 0) {
                this.loseGame();
            }
        }
        
        this.updateDisplay();
        this.renderBoard();
    }
    
    renderBoard() {
        const cells = document.querySelectorAll('.cell');
        
        cells.forEach((cell, index) => {
            const row = Math.floor(index / 9);
            const col = index % 9;
            const value = this.board[row][col];
            
            cell.textContent = value === 0 ? '' : value;
            cell.classList.remove('selected', 'given', 'correct', 'incorrect');
            
            if (this.initialBoard[row][col] !== 0) {
                cell.classList.add('given');
            } else if (value !== 0 && value === this.solution[row][col]) {
                cell.classList.add('correct');
            }
            
            if (index === this.selectedCell) {
                cell.classList.add('selected');
            }
        });
    }
    
    isPuzzleComplete() {
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.board[i][j] !== this.solution[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }
    
    giveHint() {
        if (this.gameOver) return;
        
        // Cost 10 points
        if (this.score >= 10) {
            this.score -= 10;
            
            // Find an empty cell
            const emptyCells = [];
            for (let i = 0; i < 9; i++) {
                for (let j = 0; j < 9; j++) {
                    if (this.board[i][j] === 0) {
                        emptyCells.push({ row: i, col: j });
                    }
                }
            }
            
            if (emptyCells.length > 0) {
                const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
                this.board[randomCell.row][randomCell.col] = this.solution[randomCell.row][randomCell.col];
                this.showMessage('Hint given! -10 points', 'info');
                
                if (this.isPuzzleComplete()) {
                    this.winGame();
                }
                
                this.updateDisplay();
                this.renderBoard();
            }
        } else {
            this.showMessage('Not enough points for a hint! (Need 10 points)', 'error');
        }
    }
    
    checkSolution() {
        if (this.gameOver) return;
        
        let correctCount = 0;
        let totalFilled = 0;
        
        for (let i = 0; i < 9; i++) {
            for (let j = 0; j < 9; j++) {
                if (this.board[i][j] !== 0 && this.initialBoard[i][j] === 0) {
                    totalFilled++;
                    if (this.board[i][j] === this.solution[i][j]) {
                        correctCount++;
                    }
                }
            }
        }
        
        if (totalFilled === 0) {
            this.showMessage('Place some numbers first!', 'info');
        } else {
            const percentage = Math.round((correctCount / totalFilled) * 100);
            this.showMessage(`${correctCount}/${totalFilled} correct (${percentage}%)`, 'info');
        }
    }
    
    winGame() {
        this.gameOver = true;
        this.stopTimer();
        
        const timeBonus = Math.max(0, 500 - this.seconds);
        const livesBonus = this.lives * 50;
        const totalScore = this.score + timeBonus + livesBonus;
        
        this.showMessage(
            `🎉 You Win! Total Score: ${totalScore} (Base: ${this.score} + Time: ${timeBonus} + Lives: ${livesBonus})`,
            'success'
        );
    }
    
    loseGame() {
        this.gameOver = true;
        this.stopTimer();
        this.showMessage(`💀 Game Over! You ran out of lives. Final Score: ${this.score}`, 'error');
        
        // Show solution
        setTimeout(() => {
            this.board = JSON.parse(JSON.stringify(this.solution));
            this.renderBoard();
        }, 1500);
    }
    
    startTimer() {
        this.stopTimer();
        this.timerInterval = setInterval(() => {
            this.seconds++;
            this.updateTimer();
        }, 1000);
    }
    
    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }
    
    updateTimer() {
        const minutes = Math.floor(this.seconds / 60);
        const seconds = this.seconds % 60;
        document.getElementById('timer').textContent = 
            `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
    
    updateDisplay() {
        document.getElementById('lives').textContent = this.lives;
        document.getElementById('score').textContent = this.score;
    }
    
    showMessage(text, type) {
        const messageElement = document.getElementById('message');
        messageElement.textContent = text;
        messageElement.className = `message ${type}`;
        
        // Clear message after 3 seconds
        setTimeout(() => {
            messageElement.textContent = '';
            messageElement.className = 'message';
        }, 3000);
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SudokuGame();
});
