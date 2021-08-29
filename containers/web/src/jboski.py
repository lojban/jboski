import re
from subprocess import *

from flask import Flask, request, redirect, url_for, jsonify, render_template 

app = Flask(__name__)

import logging
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

# Grab the HTML output from jbofihe and muck with it
#
# Note that jbofihe's output is not nested in any way unless you ask
# for a full parse tree, and that is *very* hard to parse, so we're
# limited in the cool stuff we can do (i.e. we can't make nested
# boxes like vlasisku).
#
# The actual substitutions we do here came from the original jboski
# https://lojban.org/jboski/index.php.txt by Raphaël Poss <r.poss@online.fr>
def parse(text):
    
    p = Popen("jbofihe -H", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
    p.stdin.write(text.encode())
    p.stdin.close()
    child_stdout = p.stdout.read()
    child_stderr = p.stderr.read()
    
    if len(child_stderr) > 0:
        return False, '<pre class="translationerror">' + child_stderr.decode() + '</pre>'
    
    content = child_stdout.decode()
    content = re.sub(r'^.*<BODY>\s*\n', '', content, flags=re.DOTALL)
    content = re.sub(r'</BODY>\s*$', '', content, flags=re.DOTALL)
    content = content.replace('<SUB><FONT SIZE="-3">', '<sub class="parenmark">')
    content = content.replace('</FONT></SUB>', '</sub>')
    content = content.replace('<U><FONT SIZE=-1>', '<em class="sumtiplace">')
    content = content.replace('</FONT></U>', '</em>')
    content = content.replace('<I>', '<em class="translation">')
    content = content.replace('</I>', '</em>')
    content = content.replace('<B>', '<strong class="lojban">')
    content = content.replace('</B>', '</strong>')
    content = content.replace('&gt;&gt;', '&raquo;')
    content = content.replace('&lt;&lt;', '&laquo;')
    content = content.replace('<P>', '<br />')
    
    return True, content

@app.route('/')
def index():
    text = request.args.get('text', "coi pilno mi'e jboski")
    grammatical = False
    parsed = ''
    try:
        grammatical, parsed = parse(text)
    except Exception as e:
        import traceback
        return "<pre>Exception thrown: " + "\n".join(traceback.format_exception(None, e, e.__traceback__)) + "</pre>"

    if 'json' in request.args:
        return jsonify(html=parsed, grammatical=grammatical)

    return render_template('index.html', parsed=parsed, grammatical=grammatical)

if __name__ == '__main__':
    app.run(debug=True)
