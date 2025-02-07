function ScriptProcessor() {
    const [inputText, setInputText] = React.useState('');
    const [outputText, setOutputText] = React.useState('');
    const [error, setError] = React.useState('');
    const fileInputRef = React.useRef();

    const transformDialogue = (dialogue) => {
        // Remove all apostrophes
        dialogue = dialogue.replace(/'/g, '');
        // Replace each word with its first letter, preserving punctuation
        return dialogue.replace(/\b\w+\b/g, match => match[0]);
    };

    const processScript = (text) => {
        const lines = text.split('\n');
        const transformedLines = lines.map(line => {
            // Check if the line is a dialogue line
            const match = line.match(/^([A-Z]+\s?[A-Z]*)\.(.+)/);
            if (match) {
                const [, character, dialogue] = match;
                // Transform the dialogue
                const transformedDialogue = transformDialogue(dialogue);
                return `${character}.${transformedDialogue}`;
            }
            return line;
        });
        return transformedLines.join('\n');
    };

    const handleFileSelect = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.txt')) {
            setError('Please select a .txt file');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            setInputText(e.target.result);
            setError('');
        };
        reader.onerror = () => {
            setError('Error reading file');
        };
        reader.readAsText(file);
    };

    const handleProcess = () => {
        if (!inputText.trim()) {
            setError('Please select a file or enter text first');
            return;
        }
        try {
            const result = processScript(inputText);
            setOutputText(result);
            setError('');
        } catch (err) {
            setError('Error processing text: ' + err.message);
        }
    };

    const handleDownload = () => {
        if (!outputText) {
            setError('No processed text to download');
            return;
        }

        const blob = new Blob([outputText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'transformed_script.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };

    const handleTextInput = (event) => {
        setInputText(event.target.value);
        setError('');
    };

    return (
        <div className="container">
            <h1>LHS Drama Script Processor</h1>
            
            <div className="controls">
                <button onClick={() => fileInputRef.current.click()}>
                    Select File
                </button>
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    accept=".txt"
                    style={{ display: 'none' }}
                />
                <button onClick={handleProcess} disabled={!inputText}>
                    Process Text
                </button>
                <button onClick={handleDownload} disabled={!outputText}>
                    Download Result
                </button>
            </div>

            {error && <div className="error">{error}</div>}

            <div className="text-areas">
                <div className="text-area-container">
                    <h3>Input Text</h3>
                    <textarea
                        value={inputText}
                        onChange={handleTextInput}
                        placeholder="Select a file or paste your script here..."
                    />
                </div>
                <div className="text-area-container">
                    <h3>Output Text</h3>
                    <textarea
                        value={outputText}
                        readOnly
                        placeholder="Processed text will appear here..."
                    />
                </div>
            </div>
        </div>
    );
}

ReactDOM.render(<ScriptProcessor />, document.getElementById('root'));
