import language


while True:
    text = input('>> ')
    result, error = language.run(text)

    if error: print(error.return_error())
    else: print(result)
