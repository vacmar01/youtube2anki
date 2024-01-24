function generateTxt() {
    let content = '';
    document.querySelectorAll('.qa-pair').forEach(pair => {
        let question = pair.querySelector('.question').textContent;
        let answer = pair.querySelector('.answer').textContent;
        content += `${question};${answer}\n`;
    });

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'youtube2anki.txt';
    a.click();
    URL.revokeObjectURL(url);
}