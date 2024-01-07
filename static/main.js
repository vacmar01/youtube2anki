const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        questionAnswers: [],
        url: '',
        loading: false,
        loadingSeconds: 0,
        intervalId: null,
        finished: false,
        error: ''
    },
    methods: {
        // call localhost:5000/anki to get all qas using async await
        async getQAs() {
            this.startLoading();
            this.error = '';
            const response = await fetch('/api/anki?id=' + this.youtubeId);
            const json = await response.json();
            if (response.status === 500) {
                this.error = 'There was an error processing your request. Please make sure you enter a valid YouTube URL.';
                this.loading = false;
                this.finished = false;
                return;
            }
            this.questionAnswers = json;
            this.stopLoading();
        },
        generateCSV() {
            // generate csv file from questionAnswers
            // https://stackoverflow.com/questions/14964035/how-to-export-javascript-array-info-to-csv-on-client-side
            var csv = '';
            this.questionAnswers.forEach(function (row) {
                csv += row.question;
                csv += ';';
                csv += row.answer;
                csv += "\n";
            });

            var hiddenElement = document.createElement('a');
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
            hiddenElement.target = '_blank';
            hiddenElement.download = 'anki.txt';
            hiddenElement.click();
        },
        startLoading() {
            this.loading = true;
            this.finished = false;
            this.loadingSeconds = 0;
            this.intervalId = setInterval(() => {
                this.loadingSeconds++;
            }, 1000);
        },
        stopLoading() {
            this.loading = false;
            this.finished = true;
            clearInterval(this.intervalId);
            this.loadingSeconds = 0;
        },

    },
    computed: {
        youtubeId() {
            if (this.url.includes('youtu.be')) {
                return this.url.split('/').pop().split('?')[0];
            }

            const url = new URL(this.url);
            return url.searchParams.get('v');
        },
    }
})

