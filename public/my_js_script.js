document.addEventListener('DOMContentLoaded', () => {
    const buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = `
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
        justify-content: center;
        width: 100%;
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
    `;

    const buttonStyles = `
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        color: white;
        font-weight: 500;
        transition: background-color 0.2s;
    `;

    const buttons = [
        {
            text: 'Find text info',
            color: '#3b82f6',
            hoverColor: '#2563eb',
            appendText: '. Use tool to find text info.'
        },
        {
            text: 'Find images',
            color: '#22c55e',
            hoverColor: '#16a34a',
            appendText: '. Use tool to find images.'
        },
        {
            text: 'Find videos',
            color: '#a855f7',
            hoverColor: '#9333ea',
            appendText: '. Use tool to find videos.'
        }
    ];

    buttons.forEach(btn => {
        const button = document.createElement('button');
        button.textContent = btn.text;
        button.style.cssText = buttonStyles + `background-color: ${btn.color};`;
        button.tabIndex = -1;

        button.addEventListener('mouseover', () => {
            button.style.backgroundColor = btn.hoverColor;
        });
        button.addEventListener('mouseout', () => {
            button.style.backgroundColor = btn.color;
        });

        button.addEventListener('click', () => {
            const textarea = document.querySelector('#chat-input');
            if (textarea) {
                console.log("IN TEXT");

                // Save the current caret position before appending text
                const endPos = textarea.textContent.length;
                const endendPos = endPos + btn.appendText.length

                textarea.setRangeText(btn.appendText, endPos, endendPos, 'select');

                console.log(textarea.value);  // Log the value, not textContent

                // Move the cursor to the end of the appended text
                textarea.selectionStart = textarea.selectionEnd = endendPos;

                // Trigger the input event to notify the framework (e.g., React)
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });

        // Prevent the button from being focused when pressing Enter
        button.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent the Enter key from triggering a click
            }
        });

        buttonContainer.appendChild(button);
    });

    document.body.appendChild(buttonContainer);
});
