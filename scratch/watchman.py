import pywatchman

def run():
    client = pywatchman.client()
    sub_result = client.query('subscribe', '/tmp', 'testsub', {
        "expression": [
            "allof",
            ["type", "f"],
            ["suffix", 'js']
        ],
        "fields": ["name"]
    })
    print sub_result
    while True:
        try:
            print client.receive()
        except Exception, e:
            print 'Nothing yet'

if __name__ == "__main__":
    run()