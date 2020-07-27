import os
import time
from flask import request, Flask, Response

app = Flask(__name__)
DELAY_TAG = 'delay-'
NUM_LINKS_TAG = 'num_links-'
NUM_DIGITS=3


@app.route('/', defaults={'path': '0'})
@app.route('/<path:path>')
def catch_all(path):
    if path == 'healthcheck':
        return 'OK', 200

    if not path.endswith('.tmp.xml') and not path.endswith('/'):
        return '''
            URL needs to end with /<br><br>
            Examples: <br>
            <table>
                <tr>
                    <td width=150>/1/</td><td>= default 10 datasets</td>
                </tr>
                <tr>
                    <td>/1/num_links-50/</td><td>= 50 datasets, up to maximum of 99</td>
                </tr>
                <tr>
                    <td>/1/num_links-50/delay-5/</td><td>= delay each request by 5 seconds, default is 1</td>
                </tr>
            </table>
        '''

    path_split = path.split('/')
    url_index = path_split[0] if '/' in path else path if len(path) else '0'

    if path.endswith('.tmp.xml'):
        filename_base = path_split[-1]
        filename_parts = filename_base.split('.')
        delay = 1

        if len(path_split) > 2 and path_split[2].startswith(DELAY_TAG):
            delay = int(path_split[2][len(DELAY_TAG):])

        filename = '.'.join([filename_parts[-4], filename_parts[-2], filename_parts[-1]])
        _id = filename_parts[-3].zfill(NUM_DIGITS)

        with open(filename, 'rb') as f:
            content = f.read().decode('utf-8')
            content = content.replace('{{url-index}}', url_index.zfill(NUM_DIGITS))
            content = content.replace('{{end-guid}}', _id)

            # delay to simulate slow servers
            if delay > 0:
                time.sleep(delay)

            resp = Response(content)
            resp.headers['Content-type'] = 'text/xml'

            if filename_parts[-3] == '10':
                return 'Error', 400
            else:
                return resp
    else:
        delay = 1
        num_links = 10
        if path_split[1].startswith(NUM_LINKS_TAG):
            num_links = int(path_split[1][len(NUM_LINKS_TAG):])

        num_links = num_links if num_links < 1000 else 999
        links = ''
        for index in range(1, 1 + num_links):
            links += f'<div><a href="test.{index}.tmp.xml">Harvest source {index}</a></div>'
        content = f'<html><body>{url_index}{links}</body></html>'

        return content


if __name__ == "__main__":
    app.run(debug='DEBUG' in os.environ, host='0.0.0.0', port=int(os.getenv("PORT", 8001)))
