from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from email.parser import BytesParser
from email.policy import default
from html import unescape
import json, os, subprocess, tempfile, zipfile, io, re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
EXE = ROOT / ('similarity_engine.exe' if os.name == 'nt' else 'similarity_engine')
MAX_UPLOAD = 5 * 1024 * 1024
MAX_TEXT = 30000


def extract_document(filename, data):
    ext = Path(filename).suffix.lower()
    if ext == '.txt':
        return data.decode('utf-8-sig')
    if ext == '.docx':
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as doc:
                xml = doc.read('word/document.xml')
            root = ET.fromstring(xml)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            paragraphs = []
            for p in root.findall('.//w:p', ns):
                words = [t.text or '' for t in p.findall('.//w:t', ns)]
                paragraphs.append(''.join(words))
            return '\n'.join(paragraphs)
        except (KeyError, zipfile.BadZipFile, ET.ParseError):
            raise ValueError(f'{filename} is not a valid .docx document')
    if ext == '.pdf':
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            return '\n'.join(page.extract_text() or '' for page in reader.pages)
        except ImportError:
            raise ValueError('PDF support needs pypdf. Close the server and run: python -m pip install -r requirements.txt')
        except Exception as exc:
            raise ValueError(f'Could not read PDF: {exc}')
    raise ValueError('Supported formats are .txt, .docx and .pdf')


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'web'), **kwargs)

    def reply(self, code, obj):
        body = json.dumps(obj).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != '/compare':
            return self.reply(404, {'error': 'Unknown endpoint'})
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size <= 0 or size > 2 * MAX_UPLOAD + 10000:
                return self.reply(400, {'error': 'Each uploaded file must be 5 MB or smaller.'})
            raw = self.rfile.read(size)
            if self.headers.get_content_type() == 'multipart/form-data':
                message = BytesParser(policy=default).parsebytes(
                    b'Content-Type: ' + self.headers['Content-Type'].encode() + b'\r\nMIME-Version: 1.0\r\n\r\n' + raw
                )
                files = {}
                for part in message.iter_parts():
                    key = part.get_param('name', header='content-disposition')
                    if key in ('documentA', 'documentB'):
                        filename = part.get_filename() or 'document.txt'
                        data = part.get_payload(decode=True) or b''
                        if len(data) > MAX_UPLOAD:
                            return self.reply(400, {'error': 'Each uploaded file must be 5 MB or smaller.'})
                        files[key] = extract_document(filename, data)
                a, b = files.get('documentA', ''), files.get('documentB', '')
            else:
                payload = json.loads(raw)
                a, b = payload.get('documentA', ''), payload.get('documentB', '')
            if not isinstance(a, str) or not isinstance(b, str) or not a.strip() or not b.strip():
                return self.reply(400, {'error': 'Please choose both documents.'})
            if len(a) > MAX_TEXT or len(b) > MAX_TEXT:
                return self.reply(400, {'error': 'Each extracted document must be 30,000 characters or less.'})
            if not EXE.exists():
                return self.reply(500, {'error': 'C engine not compiled. Run the launcher.'})
            with tempfile.TemporaryDirectory() as td:
                pa, pb = Path(td) / 'a.txt', Path(td) / 'b.txt'
                pa.write_text(a, encoding='utf-8')
                pb.write_text(b, encoding='utf-8')
                result = subprocess.run([str(EXE), str(pa), str(pb)], capture_output=True, text=True, timeout=10)
                if result.returncode:
                    return self.reply(500, {'error': result.stderr or 'C engine error'})
                return self.reply(200, json.loads(result.stdout))
        except (ValueError, UnicodeDecodeError) as exc:
            return self.reply(400, {'error': str(exc)})
        except Exception as exc:
            return self.reply(400, {'error': str(exc)})


if __name__ == '__main__':
    print('Open http://127.0.0.1:8000 (Ctrl+C to stop)')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
