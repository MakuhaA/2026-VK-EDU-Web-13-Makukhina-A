const root = document.documentElement;

window.addEventListener("pointermove", (e) => {
  root.style.setProperty("--x", e.clientX);
  root.style.setProperty("--y", e.clientY);

  const xp = e.clientX / window.innerWidth - 0.5;
  const yp = e.clientY / window.innerHeight - 0.5;
  root.style.setProperty("--xp", xp);
  root.style.setProperty("--yp", yp);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

const likeAnswerButtons = document.querySelectorAll('.ajax-like-answer-btn');

for (const item of likeAnswerButtons) {
    item.addEventListener('click', (e) => {
        e.preventDefault();

        const counter = item.querySelector('.reaction__count');

        counter.innerText = Number(counter.innerText) + 1;

        const answerId = item.dataset.answerId;

        const request = new Request(
            `/ajax/like/answer/${answerId}/`,
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin'
            }
        );

        fetch(request).then(function(response) {
            response.json().then((data) => {
                counter.innerText = data.count;

                if (data.liked) {
                    item.classList.add('liked');
                } else {
                    item.classList.remove('liked');
                }
            });
        });
    })
}

const likeQuestionButtons = document.querySelectorAll('.ajax-like-question-btn');

for (const item of likeQuestionButtons) {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const counter = item.querySelector('.reaction__count');
        counter.innerText = Number(counter.innerText) + 1;

        const questionId = item.dataset.questionId;

        const request = new Request(
            `/ajax/like/question/${questionId}/`, // Проверьте URL в urls.py
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin'
            }
        );

        fetch(request).then(function(response) {
            response.json().then((data) => {
                counter.innerText = data.count;
                if (data.liked) {
                    item.classList.add('liked');
                } else {
                    item.classList.remove('liked');
                }
            });
        });
    })
}

const correctCheckboxes = document.querySelectorAll('.correct-answer-checkbox');

for (const checkbox of correctCheckboxes) {
    checkbox.addEventListener('change', function() {
        const currentCheckbox = this;

        const questionId = currentCheckbox.dataset.questionId;
        const answerId = currentCheckbox.dataset.answerId;

        const request = new Request(
            `/ajax/mark-correct/${questionId}/${answerId}/`,
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin'
            }
        );

        fetch(request).then(function(response) {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.error || 'Ошибка сервера');
                });
            }
            return response.json();
        })
        .then((data) => {
            if (data.success) {
                document.querySelectorAll('.correct-answer-checkbox').forEach(cb => {
                    if (cb !== currentCheckbox) {
                        cb.checked = false;
                    }
                });
            }
        })
        .catch((error) => {
            alert(error.message);
            currentCheckbox.checked = false;
        });
    });
}