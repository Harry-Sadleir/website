document.addEventListener('DOMContentLoaded', () => {
    const markdownInput = document.querySelector('textarea[name="markdown"]');
    const previewPane = document.getElementById('preview');
    const nameInput = document.getElementById('name-input');
    const emailInput = document.getElementById('email-input');
    const phoneInput = document.getElementById('phone-input');
    const postcodeInput = document.getElementById('postcode-input');
    const githubTextInput = document.getElementById('github-text-input');
    const githubUrlInput = document.getElementById('github-url-input');
    const portfolioTextInput = document.getElementById('portfolio-text-input');
    const portfolioUrlInput = document.getElementById('portfolio-url-input');

    const segmentIds = ['intro', '1', '2', '3', 'conclusion'];
    const segments = segmentIds.map(id => document.getElementById(`markdown-input-${id}`));

    const inputs = [
        nameInput, emailInput, phoneInput, postcodeInput,
        githubTextInput, githubUrlInput, portfolioTextInput, portfolioUrlInput,
        ...segments
    ];

    let timeout = null;

    const renderPreview = async (markdownText) => {
        try {
            const response = await fetch('/render-markdown-preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ markdown: markdownText }),
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            previewPane.innerHTML = data.html;
        } catch (error) {
            console.error('Error rendering Markdown preview:', error);
            previewPane.innerHTML = '<p style="color: red;">Error rendering preview.</p>';
        }
    };

    const updateContent = () => {
        const name = nameInput.value;
        const email = emailInput.value;
        const phone = phoneInput.value;
        const postcode = postcodeInput.value;
        const githubText = githubTextInput.value;
        const githubUrl = githubUrlInput.value;
        const portfolioText = portfolioTextInput.value;
        const portfolioUrl = portfolioUrlInput.value;

        const details = [
            email,
            githubText && githubUrl ? `[${githubText}](${githubUrl})` : '',
            portfolioText && portfolioUrl ? `[${portfolioText}](${portfolioUrl})` : '',
            phone,
            postcode
        ].filter(Boolean).join(' | ');

        const headerMarkdown = `# ${name}\n\n${details}\n\n---\n\n`;

        const body = segments.map(segment => segment.value).join('\n\n');
        const combinedMarkdown = headerMarkdown + body;
        
        markdownInput.value = combinedMarkdown;

        clearTimeout(timeout);
        timeout = setTimeout(() => {
            renderPreview(combinedMarkdown);
        }, 300);
    };

    if (previewPane && markdownInput && inputs.every(i => i)) {
        updateContent();

        inputs.forEach(element => {
            element.addEventListener('input', updateContent);
        });
    }
});
