// following code is lowkey vibe coded
// I don't have a clue how to make this especially in js
// documentation is human made

const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    // Basic documentation database for Hades
    const hadesDocs = {
        'print': '### `print`\nPrints to terminal.'           ,
        'type' : '### `type`\nReturns the type of the object.',
        'len'  : '### `len`\nReturns the length of a string or list'
    };

    // Register the hover provider for the 'hades' language
    const hoverProvider = vscode.languages.registerHoverProvider('hades', {
        provideHover(document, position, token) {
            // Get the word currently under the mouse cursor
            const range = document.getWordRangeAtPosition(position);
            const word = document.getText(range);

            // Check if we have documentation for this specific word
            if (hadesDocs[word]) {
                return new vscode.Hover(new vscode.MarkdownString(hadesDocs[word]));
            }

            // Return undefined if we don't have a hover card for this word
            return undefined;
        }
    });

    context.subscriptions.push(hoverProvider);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};