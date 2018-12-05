from yattag import Doc

def generate_html():
    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('body'):
            with tag('p', id = 'main'):
                text('some text')
            with tag('a', href='/my-url'):
                text('some link')
    result = doc.getvalue()
    print(result)
    with open('test.html', 'wb') as my_file:
        my_file.writelines(result)
        my_file.close()