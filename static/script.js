const factText = document.getElementById('fact-text');
const container = document.getElementById('fact-container');
const shareBtn = document.getElementById('share-btn');
const mesh = document.getElementById('mesh-gradient');
const loader = document.getElementById('loader-overlay');

const themes = {
    nasa: { aura: 'rgba(138, 43, 226, 0.15)', text: '#dcd0ff' },
    wiki: { aura: 'rgba(0, 255, 127, 0.12)', text: '#baffda' },
    numbers: { aura: 'rgba(0, 191, 255, 0.12)', text: '#bae1ff' },
    sponsor: { aura: 'rgba(255, 215, 0, 0.15)', text: '#fff3b0' },
    default: { aura: 'rgba(255, 255, 255, 0.05)', text: '#ffffff' }
};

async function getDiscovery() {
    loader.classList.add('active');
    container.classList.add('hidden');
    shareBtn.classList.remove('visible');

    try {
        const response = await fetch('/get-discovery');
        const data = await response.json();

        setTimeout(() => {
            const theme = themes[data.type] || themes.default;
            factText.innerText = data.content;
            factText.style.color = theme.text;
            mesh.style.background = `radial-gradient(circle at 50% 50%, ${theme.aura} 0%, transparent 80%)`;
            loader.classList.remove('active');
            container.classList.remove('hidden');
            shareBtn.classList.add('visible');
            
            if(data.is_sponsored) shareBtn.innerText = "Visit Sponsor";
            else shareBtn.innerText = "Capture Discovery";
        }, 600);
    } catch (e) {
        factText.innerText = "The void is silent. Check your connection.";
        loader.classList.remove('active');
        container.classList.remove('hidden');
    }
}

shareBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const text = `"${factText.innerText}" — via Trivially Relevant.`;
    if (navigator.share) {
        navigator.share({ title: 'Trivially Relevant', text: text, url: window.location.href });
    } else {
        navigator.clipboard.writeText(text);
        const oldText = shareBtn.innerText;
        shareBtn.innerText = "Copied to Clipboard";
        setTimeout(() => shareBtn.innerText = oldText, 2000);
    }
});

document.body.addEventListener('click', (e) => {
    if (!e.target.closest('#share-btn') && !e.target.closest('#ethicalads-container')) {
        getDiscovery();
    }
});

window.onload = getDiscovery;
