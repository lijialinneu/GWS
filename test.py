def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'test/html')])
    return [b"Hello world"]
