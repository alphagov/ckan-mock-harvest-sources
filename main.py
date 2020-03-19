import time
from flask import Flask, Response

app = Flask(__name__)


@app.route('/', defaults={'path': '0'})
@app.route('/<path:path>')
def catch_all(path):
    url_index = path.split('/')[0] if '/' in path else path if len(path) else '0'

    if path.endswith('.tmp.xml'):
        filename_base = path.split('/')[-1]
        filename_parts = filename_base.split('.')
        filename = '.'.join([filename_parts[0], filename_parts[-2], filename_parts[-1]])
        _id = filename_parts[1].zfill(2)

        # print(_id)
        with open(filename, 'rb') as f:
            content = f.read().decode('utf-8')
            content = content.replace('{{url-index}}', url_index.zfill(2))
            content = content.replace('{{end-guid}}', _id)

            # delay to simulate slow servers
            time.sleep(9)

            resp = Response(content)
            resp.headers['Content-type'] = 'text/xml'

            return resp
    else:
        content = '<html><body>{url_index}{links}</body></html>'
        links = ''
        for i in range(1, 11):
            links += '<div><a href="/{url_index}/test.{index}.tmp.xml">Harvest source {index}</a></div>'.format(
                url_index=url_index, index=i)
        content = content.format(url_index=url_index, links=links)

        return content


if __name__ == "__main__":
    app.run(debug=True, port=8001)
