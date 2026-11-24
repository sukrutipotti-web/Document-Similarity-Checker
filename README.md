# Document Similarity & Plagiarism Checker — Phase 2

A local classroom prototype that compares **two user-provided text documents** using C, data structures and algorithms.

## Features
- Normalizes text to lowercase and treats punctuation/whitespace as word separators.
- Tokenizes text into word arrays.
- Calculates the Longest Common Subsequence (LCS) using Dynamic Programming.
- Calculates similarity using `(2 × LCS length / (word count A + word count B)) × 100`.
- Uses a hash table to index candidate three-word phrases and verifies candidate matches against the original tokens.
- Uses a linked list to collect unique matching phrase records.
- Displays similarity, LCS length, word counts and matching phrases in a browser interface.
- Uploads `.txt`, `.docx` and text-based `.pdf` files directly from the browser (up to 5 MB each).

**Important scope note:** the application compares only the two inputs. It does not search the internet or an external document database. Similarity is evidence of textual overlap, not proof of plagiarism.

## Technologies
- C: preprocessing, arrays, LCS/DP, hash table and linked-list phrase records.
- Python 3 standard library: local HTTP connector between browser and C engine.
- HTML, CSS and JavaScript: frontend.

One Python package, `pypdf`, is used to extract text from PDFs. DOCX extraction uses Python standard-library modules.

## Requirements
1. Python 3.
2. GCC compiler (MinGW-w64 GCC on Windows; GCC on Linux).
3. Modern web browser.

Check installation with `python --version` and `gcc --version` (on some systems use `python3`).

## Run on Windows
1. Install Python and GCC and add both to PATH.
2. Open Command Prompt in this project folder.
3. Run `run_windows.bat`.
4. Open `http://127.0.0.1:8000` in your browser.
5. Paste text into both boxes and click **Compare Documents**.
6. Stop the server by pressing `Ctrl+C` in the terminal.

Manual commands:
```bat
gcc -std=c11 -Wall -Wextra -O2 c_core\main.c -o similarity_engine.exe
python -m pip install -r requirements.txt
python server.py
```

## Run on Linux/macOS
Run these commands from the project folder:
```bash
chmod +x run_linux_mac.sh
./run_linux_mac.sh
```
Then open `http://127.0.0.1:8000`. Stop with `Ctrl+C`.

Manual commands:
```bash
gcc -std=c11 -Wall -Wextra -O2 c_core/main.c -o similarity_engine
python3 -m pip install -r requirements.txt
python3 server.py
```

## How it works
1. The browser uploads both selected files to the local Python connector.
2. Python extracts text from TXT, DOCX or text-based PDF files and writes it into temporary text files.
3. Python runs the compiled C engine.
4. C reads, normalizes and tokenizes the text.
5. LCS Dynamic Programming calculates ordered overlap.
6. A hash table indexes three-word phrases from Document A. Candidate phrases from Document B are checked against the original tokens.
7. Verified unique phrase matches are stored in a linked list.
8. C returns JSON and the browser displays the result.

## Folder structure
```text
phase2_document_similarity_checker/
├── c_core/main.c
├── web/index.html
├── web/style.css
├── web/app.js
├── server.py
├── samples/document_a.txt
├── samples/document_b.txt
├── tests/test_cases.md
├── run_windows.bat
├── run_linux_mac.sh
└── README.md
```

## Testing
Use the sample documents in `samples/` or follow `tests/test_cases.md`. Test identical, completely different, partially overlapping, case/punctuation and empty inputs.

## Limitations
- Two documents per comparison; supported inputs are TXT, DOCX and text-based PDF. Scanned/image-only PDFs need OCR and are not supported.
- Maximum upload size is 5 MB per file; extracted text is limited to 30,000 characters per document.
- Maximum 500 tokens per document in this prototype; the LCS DP table is sized accordingly.
- Matching phrase detection checks contiguous three-word sequences only.
- Paraphrasing and semantic similarity are not detected.
- Score depends on preprocessing and the selected formula.
- The local server is intended for a classroom demo, not public deployment.

## Team
- SUKRUTI P
- SHRINIDHI MADDALI
- V VINSHU

Course: Data Structures | Department: Information Science and Engineering | Academic Year: 2026–2027
