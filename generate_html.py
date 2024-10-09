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


# Добавляем кнопки копирования с уникальными id под каждый блок кода
class CodeBlockWithCopyButtonPostprocessor(Postprocessor):
    def __init__(self, md):
        super().__init__(md)
        self.counter = 0  # Счётчик для уникальных id

    def run(self, text):
        # Находим все блоки кода и добавляем под ними кнопку с уникальным id
        def replace_block(match):
            self.counter += 1
            code_id = f"code-block-{self.counter}"
            return f'<div class="code-container"><pre class="highlight"><code class="language-python linenums" id="{code_id}"' + match.group(1) + \
                f'</code></pre><button class="copy-button" onclick="copyCode(\'{code_id}\')">Копировать код</button></div>'

        # Обновляем блоки кода, добавляем div с кнопкой
        return re.sub(r'<pre class="highlight"><code class="language-python linenums"(.*?)</code></pre>', replace_block, text, flags=re.DOTALL)


class CodeBlockWithCopyButtonExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(CodeBlockWithCopyButtonPostprocessor(md), 'add_copy_button', 15)


# Постпроцессор для добавления target="_blank" к ссылкам, игнорируя блоки кода
class LinkTargetBlankPostprocessor(Postprocessor):
    def run(self, text):
        # Избегаем обработки текста в блоках кода
        def replace_link(match):
            return f'<a href="{match.group(1)}" target="_blank">{match.group(1)}</a>'

        # Заменяем ссылки, игнорируя текст в блоках кода
        return re.sub(r'(?<!<code>)(http[s]?://[^\s<]+)(?!<\/code>)', replace_link, text)


class LinkTargetBlankExtension(markdown.extensions.Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(LinkTargetBlankPostprocessor(md), 'add_target_blank', 10)


def generate_html_with_code_and_toc(md_file_path, output_html_path):
    # Читаем содержимое Markdown файла
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    html = markdown.markdown(md_content,
                             extensions=[CustomTOCExtension(), WrapContentExtension(),
                                         CodeBlockWithCopyButtonExtension(), LinkTargetBlankExtension(),
                                         'fenced_code', 'codehilite', 'tables'],
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

    with open(output_html_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_output)

    print(f"HTML файл с оглавлением и кнопками копирования успешно сгенерирован: {output_html_path}")


if __name__ == '__main__':
    file = 'readme'
    generate_html_with_code_and_toc(file+'.md', file+'.html')

