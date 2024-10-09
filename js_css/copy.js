function copyCode(blockId) {
    const codeBlock = document.getElementById(blockId); // Получаем элемент с кодом по идентификатору
    const textArea = document.createElement('textarea'); // Создаем временный текстовый элемент
    textArea.value = codeBlock.innerText; // Сохраняем код в текстовом элементе
    document.body.appendChild(textArea); // Добавляем его в документ
    textArea.select(); // Выделяем текст
    document.execCommand('copy'); // Копируем текст
    document.body.removeChild(textArea); // Удаляем текстовый элемент

    alert('Код скопирован!'); // Сообщение для пользователя
}