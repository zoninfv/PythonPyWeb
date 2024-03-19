function clearForm() {
    const createPostForm = document.getElementById("post-form");
    const previewImage = document.getElementById("preview_image");
    const pubDateElement = document.querySelector('.form-group[data-pub-date]');
    const publishNowButton = document.querySelector('.button-group button:nth-child(1)');
    const publishLaterButton = document.querySelector('.button-group button:nth-child(2)');

    createPostForm.reset();
    previewImage.src = ""; // Установите путь изображения
    previewImage.style.display = "none"; // Скрыть элемент img
    pubDateElement.style.display = 'none';
    publishNowButton.style.display = 'block';
    publishLaterButton.style.display = 'none';
};


function hideForm() {
    const createPostForm = document.getElementById("post-form");
    createPostForm.style.display = 'none';
}

function showForm() {
    const createPostForm = document.getElementById("post-form");
    createPostForm.style.display = 'block';
}

 // Функция для получения значения куки по имени
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
function setStatus(status) {
        document.getElementById("status").value = status;
    }




const infoModal = document.getElementById('infoModal');
const modalTitle = infoModal.querySelector('.modal-title');
const modalBody = infoModal.querySelector('.modal-body');
const closeButton = infoModal.querySelector('.close');

// Показываем модальное окно при успешном создании поста
function showModal(title, message) {
    modalTitle.textContent = title;
    modalBody.textContent = message;
    infoModal.style.display = 'block'; // Показываем модальное окно
}

closeButton.addEventListener('click', function() {
    infoModal.style.display = 'none'; // Скрываем модальное окно
});


document.addEventListener("DOMContentLoaded", function() {
    const selectElement = document.getElementById("id_select");
    const pubDateElement = document.querySelector('.form-group[data-pub-date]');
    const publishNowButton = document.querySelector('.button-group button:nth-child(1)');
    const publishLaterButton = document.querySelector('.button-group button:nth-child(2)');

    selectElement.addEventListener('change', function() {
        const selectedValue = this.value;

        if (selectedValue === '1') {  // Опубликовать сейчас
            pubDateElement.style.display = 'none';
            publishNowButton.style.display = 'block';
            publishLaterButton.style.display = 'none';
        } else if (selectedValue === '2') {  // Опубликовать позже
            pubDateElement.style.display = 'block';
            publishNowButton.style.display = 'none';
            publishLaterButton.style.display = 'block';
        }
    });
});





// Отправка POST, PUT метода
document.addEventListener("DOMContentLoaded", function () {
    //const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let form = document.getElementById('post-form')
    let publishButton = form.querySelector('.button-group button.published');
    let publishLaterButton = form.querySelector('.button-group button.scheduled');
    let saveDraftButton = form.querySelector('.button-group button.draft');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        publishButton.disabled = true;
        publishLaterButton.disabled = true;
        saveDraftButton.disabled = true;

        // Создайте новый объект FormData внутри функции обработчика
        let formData = new FormData(form);
        console.log(formData);

        let csrfToken = formData.get('csrfmiddlewaretoken');

        let requestOptions = {
            method: form.dataset.method.toUpperCase(),  // Преобразовываем в верхний регистр
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        };

        fetch(form.action, requestOptions)
        .then(response => {
            if (!response.ok) {
                throw new Error('Произошла ошибка при отправке запроса.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            publishButton.disabled = false;
            publishLaterButton.disabled = false;
            saveDraftButton.disabled = false;
            if (requestOptions['method'] === "POST") {
                showModal('Успех!','Пост успешно создан!');
            } else {
                showModal('Успех!','Пост успешно обновлен!');
            }
            clearForm();
            hideForm();
        })
        .catch(error => {
            publishButton.disabled = false;
            publishLaterButton.disabled = false;
            saveDraftButton.disabled = false;
            if (error.message === 'Произошла ошибка при отправке запроса.') {
                showModal('Ошибка!', 'Произошла ошибка при отправке запроса.');
            } else {
                console.error('Error:', error);
                showModal('Ошибка!', 'Проверьте доступ до ресурса '+ form.action);
            }
        });
    });
});




    // Действия при нажатии на кнопку "Новый пост"
document.addEventListener("DOMContentLoaded", function() {
  const createPostButton = document.getElementById("create-post-button");
  const createPostForm = document.getElementById("post-form");

  createPostButton.addEventListener("click", function() {
      // Сбросьте значения всех полей формы
      clearForm();
      createPostForm.dataset.method = 'post';
      createPostForm.action = `/entry/`;
      showForm();

  });
});





// Отображение превью картинки
document.addEventListener("DOMContentLoaded", function() {
    const imageInput = document.getElementById("id_image");
    const imagePreview = document.getElementById("preview_image");

    // Добавьте обработчик события для изменения значения input
    imageInput.addEventListener("change", function() {
        // Отображение превью изображения
        displayImagePreview(this);
    });

    function displayImagePreview(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function(e) {
                // Устанавливаем атрибут src для элемента img
                imagePreview.src = e.target.result;
                // Отображаем элемент img
                imagePreview.style.display = "block";
            };

            // Читаем файл в формате base64
            reader.readAsDataURL(input.files[0]);
        }
    }
});




    // Получение данных поста по нажатии на значек карандаша
document.addEventListener("DOMContentLoaded", function() {
    const postForm = document.getElementById('post-form');
    const editPostLinks = document.querySelectorAll('.edit-post');

    editPostLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const entryId = this.getAttribute('data-entry-id');
            fetch(`/entry/${entryId}`)
                .then(response => response.json())
                .then(data => fillUpdateForm(data))
                .catch(error => console.error('Error:', error));
        });
    });

    function fillUpdateForm(data) {
        clearForm();
        const blogSelect = document.getElementById('id_blog');

        // Ищем опцию с нужным текстом
        let desiredOption = Array.from(blogSelect.options).find(option => option.text === data.blog_name);

        // Устанавливаем найденный <option> как выбранный
        if (desiredOption) {
            desiredOption.selected = true;
        }

        document.querySelector('#post-form #id_headline').value = data.headline;
        document.querySelector('#post-form #id_summary').value = data.summary;
        tinymce.get('id_content').setContent(data.body_text);

        document.getElementById('id_image').value = '';
        const previewImage = document.getElementById("preview_image");

        // Если есть путь к изображению в JSON, отобразите его в элементе img
        if (data.image) {
            previewImage.src = data.image; // Установите путь изображения
            previewImage.style.display = "block"; // Покажите элемент img
        }

        // Получение элемента select
        const selectAuthor = document.getElementById('id_authors');
        // Перебираем авторов в JSON
        data.authors.forEach(author => {
            // Ищем опцию с нужным именем автора
            let desiredOption = Array.from(selectAuthor.options).find(option => option.text === author.name);

            // Если найдено совпадение, устанавливаем эту опцию выбранной
            if (desiredOption) {
                desiredOption.selected = true;
            }
        });

        // Получение элемента select
        const selectTag = document.getElementById('id_tags');
        data.tags.forEach(tag => {
            let desiredOption = Array.from(selectTag.options).find(option => option.text === tag.name);

            // Если найдено совпадение, устанавливаем эту опцию выбранной
            if (desiredOption) {
                desiredOption.selected = true;
            }
        });

        postForm.action = `/entry/${data.entry_id}/`;
        postForm.dataset.method = "put";
        showForm();

    };
});




// Удаление строки с постом из интерфейса
function deleteRow(currentEntryId) {
    const postToDelete = document.querySelector(`tr[data-entry-id="${currentEntryId}"]`);
    if (postToDelete) {
        const table = postToDelete.closest('table'); // Находим таблицу, в которой была удалена строка
        postToDelete.remove();
       // Обновляем порядковые номера только в этой таблице
        const rowsToUpdate = table.querySelectorAll('tbody tr');
        rowsToUpdate.forEach((row, index) => {
            row.querySelector('td:first-child').textContent = index + 1;
});
} else {
    console.error('Error: Элемент поста не найден.');
};
};

    // обработчик удаления поста
document.addEventListener("DOMContentLoaded", function() {
    const deletePostLinks = document.querySelectorAll('.delete-post');
    const confirmationModal = document.getElementById('confirmationModal');
    const confirmDeleteButton = document.getElementById('confirmDelete');
    const cancelDeleteButton = document.getElementById('cancelDelete');

    let currentEntryId; // Хранит id текущего поста

    // Добавляем обработчики событий для каждой ссылки на удаление
    deletePostLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            currentEntryId = this.getAttribute('data-entry-id');
            confirmationModal.style.display = 'flex'; // Показываем модальное окно
        });
    });

    const csrftoken = getCookie('csrftoken');

    // Обработчик события для кнопки подтверждения удаления
    confirmDeleteButton.addEventListener('click', function() {
        // Отправка запроса на удаление
        console.log("Удаление", currentEntryId)
    fetch(`/entry/${currentEntryId}`, {
    method: 'DELETE',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
    }
    }).then(response => {
        if (response.ok) {
            // Если удаление прошло успешно, закрываем модальное окно
            confirmationModal.style.display = 'none';
            deleteRow(currentEntryId); // Удаление строки с постом из интерфейса
        } else {
            console.error('Error:', response.statusText);
        }
    })
    .catch(error => console.error('Error:', error));
    });

    // Обработчик события для кнопки отмены удаления
    cancelDeleteButton.addEventListener('click', function() {
        // Закрываем модальное окно
        confirmationModal.style.display = 'none';
    });
});





    // Поиск автора в форме
document.addEventListener("DOMContentLoaded", function() {
    // Получаем элементы
    var authorSelect = document.getElementById("id_authors");
    var authorSearchInput = document.getElementById("authorSearch");

    // Копируем все опции для последующей фильтрации
    var allOptions = Array.from(authorSelect.options);

    // Сохраняем исходные выбранные опции
    var selectedOptions = Array.from(authorSelect.selectedOptions);

    // Обработчик события ввода в поле поиска
    authorSearchInput.addEventListener("input", function() {
        var searchTerm = authorSearchInput.value.toLowerCase();

        // Фильтруем опции в соответствии с введенным текстом
        var filteredOptions = allOptions.filter(function(option) {
            return option.text.toLowerCase().includes(searchTerm);
        });

        // Очищаем список
        authorSelect.innerHTML = '';

        // Добавляем отфильтрованные опции обратно в список
        filteredOptions.forEach(function(option) {
            authorSelect.appendChild(option.cloneNode(true));
        });

        // Восстанавливаем ранее выбранные опции
        selectedOptions.forEach(function(selectedOption) {
            var restoredOption = authorSelect.querySelector('option[value="' + selectedOption.value + '"]');
            if (restoredOption) {
                restoredOption.selected = true;
            }
        });
    });
});
