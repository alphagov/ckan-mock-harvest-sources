import time
from flask import request, Flask, Response
import urllib.parse as urlparse
from urllib.parse import parse_qs

app = Flask(__name__)


@app.route('/', defaults={'path': '0'})
@app.route('/<path:path>')
def catch_all(path):
    if not path.endswith('.tmp.xml') and not path.endswith('/'):
        return '''
            URL needs to end with /<br><br>
            Examples: <br>
            <table>
                <tr>
                    <td width=150>/1/</td><td>= default 10 datasets</td>
                </tr>
                <tr>
                    <td>/1/?num_links=50</td><td>= 50 datasets, up to maximum of 99</td>
                </tr>
                <tr>
                    <td>/1/?delay=5</td><td>= delay each request by 5 seconds, default is 1</td>
                </tr>
            </table>
        '''

    parsed = urlparse.urlparse(request.url)
    query_string = parse_qs(parsed.query)
    path_split = path.split('/')
    url_index = path_split[0] if '/' in path else path if len(path) else '0'
    delay = int(query_string.get('delay')[0]) if 'delay' in query_string else 1

    if path.endswith('.tmp.xml'):
        filename_base = path_split[-1]
        filename_parts = filename_base.split('.')
        filename = '.'.join([filename_parts[0], filename_parts[-2], filename_parts[-1]])
        _id = filename_parts[1].zfill(2)

        with open(filename, 'rb') as f:
            content = f.read().decode('utf-8')
            content = content.replace('{{url-index}}', url_index.zfill(2))
            content = content.replace('{{end-guid}}', _id)

            # delay to simulate slow servers
            if delay > 0:
                time.sleep(delay)

            resp = Response(content)
            resp.headers['Content-type'] = 'text/xml'

            return resp
    else:
        num_links = int(query_string.get('num_links')[0]) if 'num_links' in query_string else 10
        num_links = num_links if num_links < 100 else 99
        links = ''
        for index in range(1, 1 + num_links):
            links += f'<div><a href="test.{index}.tmp.xml?delay={delay}">Harvest source {index}</a></div>'
        content = f'<html><body>{url_index}{links}</body></html>'

        return content


if __name__ == "__main__":
    app.run(debug=True, port=8001)
