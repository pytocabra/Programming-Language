import language


while True:
    text = input('>> ')
    result, error = language.run('file1', text)

    if error: print(error.return_error())
    else: print(result)