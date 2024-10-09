import re
import markdown
from markdown.extensions.toc import TocExtension
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from xml.etree.ElementTree import Element


# Создаем расширение для обертки контента в <div class="content">
class WrapContentExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        # Добавляем Treeprocessor для обертки основного контента
        md.treeprocessors.register(WrapContentTreeprocessor(md), 'wrap_content', 15)


class WrapContentTreeprocessor(Treeprocessor):
    def run(self, root):
        # Создаем <div class="content"> и перемещаем в него все содержимое
        content_div = Element('div', {'class': 'content'})
        while len(root) > 1:
            content_div.append(root[1])  # Перемещаем все элементы кроме первого (оглавление)
            root.remove(root[1])
        root.append(content_div)  # Добавляем <div class="content"> в root


# Обработка postprocessor для замены div class toc на div class sidebar
class CustomTOCPostprocessor(Postprocessor):
    def run(self, text):
        # Заменяем <div class="toc"> на <div class="sidebar">
        return text.replace('<div class="toc">', '<div class="sidebar">')


# Кастомное расширение для замены class toc на sidebar
class CustomTOCExtension(TocExtension):
    def extendMarkdown(self, md):
        # Расширяем стандартное расширение TOC
        super().extendMarkdown(md)
        # Добавляем Postprocessor для изменения div class="toc" на div class="sidebar"
        md.postprocessors.register(CustomTOCPostprocessor(md), 'toc_sidebar', 10)


def generate_html_with_code_and_toc(md_file_path, output_html_path):
    # Читаем содержимое Markdown файла
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        markdown_content = md_file.read()

    # Создаем заголовки и оглавление
    toc = []
    html_content = []
    code_block_counter = 0  # Для уникальных ID кодовых блоков

    # Обрабатываем каждую строку и ищем заголовки или блоки кода
    inside_code_block = False
    current_code_block = []

    for line in markdown_content.splitlines():
        if line.startswith("```python"):
            # Начало блока Python кода
            inside_code_block = True
            code_block_counter += 1
            current_code_block = []
        elif line.startswith("```") and inside_code_block:
            # Конец блока кода
            inside_code_block = False
            code_html = ''.join(current_code_block)
            html_content.append(f"""
            <div class="code-container">
                <pre><code class="language-python" id="code-block-{code_block_counter}">{code_html}</code></pre>
                <button class="copy-button" onclick="copyCode('code-block-{code_block_counter}')">Копировать код</button>
            </div>
            """)
        # elif inside_code_block:
        #     # Добавляем строки кода в блок кода, избегая обработки Markdown синтаксиса
        #     current_code_block.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + '\n')
        else:
            # Ищем заголовки уровней 1, 2 и 3
            h1_match = re.match(r'^\# (.+)', line)
            h2_match = re.match(r'^\#\# (.+)', line)
            h3_match = re.match(r'^\#\#\# (.+)', line)

            if h1_match:
                header = h1_match.group(1)
                anchor = re.sub(r'\s+', '-', header.lower())
                toc.append(f'<li><a href="#{anchor}">{header}</a></li>')
                html_content.append(f'<h1 id="{anchor}">{header}</h1>')
            elif h2_match:
                header = h2_match.group(1)
                anchor = re.sub(r'\s+', '-', header.lower())
                toc.append(f'<li style="margin-left: 20px;"><a href="#{anchor}">{header}</a></li>')
                html_content.append(f'<h2 id="{anchor}">{header}</h2>')
            elif h3_match:
                header = h3_match.group(1)
                anchor = re.sub(r'\s+', '-', header.lower())
                toc.append(f'<li style="margin-left: 40px;"><a href="#{anchor}">{header}</a></li>')
                html_content.append(f'<h3 id="{anchor}">{header}</h3>')
            else:
                # Если это не заголовок и не блок кода, просто добавляем строку в HTML-контент
                html_content.append(line)

    # Преобразуем оставшийся Markdown контент в HTML
    html_body = markdown.markdown('\n'.join(html_content))

    # Генерация финального HTML-документа
    html_output = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Оглавление</title>
    
        <link rel="stylesheet" href="/js_css/main.css">
        <link rel="stylesheet" href="/js_css/default.min.css">
        <!-- Подключаем js -->
        <script src="/js_css/copy.js"></script>
        <script src="/js_css/highlight.min.js"></script>
        <script>hljs.highlightAll();</script>
    </head>
    <body>
        <div class="sidebar">
            <h2>Оглавление</h2>
            <ul>
                {''.join(toc)}
            </ul>
        </div>
        <div class="content">
            {html_body}
        </div>
    </body>
    </html>
    """

    # Записываем HTML-контент в выходной файл
    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_output)

    print(f"HTML файл с оглавлением и кнопками копирования успешно сгенерирован: {output_html_path}")


if __name__ == '__main__':
    file = 'readme'
    # generate_html_with_code_and_toc(file+'.md', file+'.html')
    with open(file + '.md', 'r', encoding='utf-8') as f:
        md_content = f.read()

    html = markdown.markdown(md_content,
                             extensions=[CustomTOCExtension(), WrapContentExtension(), 'fenced_code', 'codehilite', 'tables'],
                             extension_configs={'codehilite': {'linenums': True, 'css_class': 'highlight'},
                                                'toc_sidebar': {
                                                    'title': 'Оглавление',
                                                    'anchorlink': True,
                                                    'permalink': True,
                                                    'toc_depth': '1-3'
                                                }})

    html_output = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Оглавление</title>

            <link rel="stylesheet" href="/js_css/main.css">
            <link rel="stylesheet" href="/js_css/default.min.css">
            <!-- Подключаем js -->
            <script src="/js_css/copy.js"></script>
            <script src="/js_css/highlight.min.js"></script>
            <script>hljs.highlightAll();</script>
        </head>
        <body>
            {html}
        </body>
        </html>
    """

    with open(file + '.html', 'w', encoding='utf-8') as output_file:
        output_file.write(html_output)
