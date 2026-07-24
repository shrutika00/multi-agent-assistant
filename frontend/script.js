// Backend URL configuration
const BACKEND_URL = 'http://127.0.0.1:8000';

// DOM Elements
const form = document.getElementById('workflow-form');
const textarea = document.getElementById('user-query');
const submitBtn = document.getElementById('submit-btn');
const btnSpinner = document.getElementById('btn-spinner');
const btnText = submitBtn.querySelector('.btn-text');
const backendStatus = document.getElementById('backend-status');
const statusDot = document.querySelector('.status-dot');

const resultCard = document.getElementById('result-card');
const finalAnswerContainer = document.getElementById('final-answer-container');

// Tabs DOM
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');

// Agent Node DOM mappings
const nodes = {
    coordinator: {
        el: document.getElementById('node-coordinator'),
        line: document.getElementById('line-1'),
        badge: document.getElementById('node-coordinator').querySelector('.node-status'),
        msg: document.getElementById('node-coordinator').querySelector('.node-msg'),
        time: null
    },
    research: {
        el: document.getElementById('node-research'),
        line: document.getElementById('line-2'),
        badge: document.getElementById('node-research').querySelector('.node-status'),
        msg: document.getElementById('node-research').querySelector('.node-msg'),
        time: document.getElementById('node-research').querySelector('.node-time')
    },
    factCheck: {
        el: document.getElementById('node-fact-check'),
        line: document.getElementById('line-3'),
        badge: document.getElementById('node-fact-check').querySelector('.node-status'),
        msg: document.getElementById('node-fact-check').querySelector('.node-msg'),
        time: document.getElementById('node-fact-check').querySelector('.node-time')
    },
    summary: {
        el: document.getElementById('node-summary'),
        line: document.getElementById('line-4'),
        badge: document.getElementById('node-summary').querySelector('.node-status'),
        msg: document.getElementById('node-summary').querySelector('.node-msg'),
        time: document.getElementById('node-summary').querySelector('.node-time')
    },
    qa: {
        el: document.getElementById('node-qa'),
        line: null,
        badge: document.getElementById('node-qa').querySelector('.node-status'),
        msg: document.getElementById('node-qa').querySelector('.node-msg'),
        time: document.getElementById('node-qa').querySelector('.node-time')
    }
};

// Timing Table DOM elements
const timingEls = {
    research: document.getElementById('time-research'),
    factCheck: document.getElementById('time-fact-check'),
    summary: document.getElementById('time-summary'),
    qa: document.getElementById('time-qa'),
    total: document.getElementById('time-total')
};

// Tab values DOM elements
const tabContents = {
    research: document.getElementById('content-research'),
    factCheck: document.getElementById('content-fact-check'),
    summary: document.getElementById('content-summary')
};

// Initialize: check backend health
async function checkHealth() {
    try {
        const response = await fetch(`${BACKEND_URL}/health`);
        const data = await response.json();
        if (data.status === 'healthy') {
            backendStatus.textContent = 'Online';
            statusDot.className = 'status-dot green';
            submitBtn.disabled = false;
        } else {
            throw new Error();
        }
    } catch (e) {
        backendStatus.textContent = 'Offline';
        statusDot.className = 'status-dot red';
        submitBtn.disabled = true;
    }
}

// Node State Helper
function setNodeState(nodeKey, state, message = '', time = '') {
    const node = nodes[nodeKey];
    if (!node) return;

    // Remove state classes
    node.el.classList.remove('running', 'completed', 'failed');
    node.badge.className = 'node-status';

    if (state === 'Running') {
        node.el.classList.add('running');
        node.badge.classList.add('badge-running');
        node.badge.textContent = 'Running';
    } else if (state === 'Completed') {
        node.el.classList.add('completed');
        node.badge.classList.add('badge-completed');
        node.badge.textContent = 'Completed';
        if (node.line) node.line.classList.add('completed');
    } else if (state === 'Failed') {
        node.el.classList.add('failed');
        node.badge.classList.add('badge-failed');
        node.badge.textContent = 'Failed';
    } else {
        node.badge.classList.add('badge-waiting');
        node.badge.textContent = 'Waiting';
        if (node.line) node.line.classList.remove('completed');
    }

    if (message) {
        node.msg.textContent = message;
    }
    if (node.time && time) {
        node.time.textContent = time;
    } else if (node.time) {
        node.time.textContent = '';
    }
}

// Reset all nodes to waiting state
function resetAllNodes() {
    setNodeState('coordinator', 'Waiting', 'Ready to receive query.');
    setNodeState('research', 'Waiting', 'Waiting for coordinator dispatch.');
    setNodeState('factCheck', 'Waiting', 'Waiting for research notes.');
    setNodeState('summary', 'Waiting', 'Waiting for verified facts.');
    setNodeState('qa', 'Waiting', 'Waiting for summary draft.');
    
    // Reset timings in UI
    Object.values(timingEls).forEach(el => el.textContent = '-');
    resultCard.classList.add('hidden');
    finalAnswerContainer.textContent = '';
}

// Tab Switching logic
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');
        
        tabBtns.forEach(b => b.classList.remove('active'));
        tabPanes.forEach(p => p.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(targetTab).classList.add('active');
    });
});

// Submit Form Action
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = textarea.value.trim();
    if (!query) return;

    // Reset UI and show loading
    resetAllNodes();
    submitBtn.disabled = true;
    btnSpinner.style.display = 'inline-block';
    btnText.textContent = 'Processing...';

    // Phase 1: Coordinator starting
    setNodeState('coordinator', 'Running', 'Initiating workflow...');

    try {
        const response = await fetch(`${BACKEND_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: query })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred during execution.');
        }

        // Helper delay for UI playback
        const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        // Step 1: Coordinator Completed, Research Running
        setNodeState('coordinator', 'Completed', 'Workflow orchestrated. Dispatching to Research Agent.');
        setNodeState('research', 'Running', 'Analyzing query and compiling research notes...');
        await delay(1000);

        // Step 2: Research Completed, Fact Checker Running
        setNodeState('research', 'Completed', 'Research notes compiled.', data.execution_time.research);
        setNodeState('factCheck', 'Running', 'Reviewing research notes for inaccuracies and contradictions...');
        await delay(1000);

        // Step 3: Fact Checker Completed, Summary Running
        setNodeState('factCheck', 'Completed', 'Fact check notes compiled.', data.execution_time.fact_check);
        setNodeState('summary', 'Running', 'Synthesizing research notes and verified notes into a draft...');
        await delay(1000);

        // Step 4: Summary Completed, QA Running
        setNodeState('summary', 'Completed', 'Summary draft finalized.', data.execution_time.summary);
        setNodeState('qa', 'Running', 'Verifying completeness and polishing final response...');
        await delay(1000);

        // Step 5: QA Completed
        setNodeState('qa', 'Completed', 'Polished final answer produced.', data.execution_time.quality_assurance);

        // Display results
        finalAnswerContainer.textContent = data.final_answer;
        
        // Populate timings
        timingEls.research.textContent = data.execution_time.research;
        timingEls.factCheck.textContent = data.execution_time.fact_check;
        timingEls.summary.textContent = data.execution_time.summary;
        timingEls.qa.textContent = data.execution_time.quality_assurance;
        timingEls.total.textContent = data.execution_time.total;

        // Populate tabs content
        tabContents.research.textContent = data.research;
        tabContents.factCheck.textContent = data.fact_check;
        tabContents.summary.textContent = data.summary;

        // Show results block
        resultCard.classList.remove('hidden');
        resultCard.scrollIntoView({ behavior: 'smooth' });

    } catch (err) {
        // Set running node to Failed state
        if (nodes.research.el.classList.contains('running')) {
            setNodeState('research', 'Failed', err.message);
        } else if (nodes.factCheck.el.classList.contains('running')) {
            setNodeState('factCheck', 'Failed', err.message);
        } else if (nodes.summary.el.classList.contains('running')) {
            setNodeState('summary', 'Failed', err.message);
        } else if (nodes.qa.el.classList.contains('running')) {
            setNodeState('qa', 'Failed', err.message);
        } else {
            setNodeState('coordinator', 'Failed', err.message);
        }
        console.error(err);
    } finally {
        submitBtn.disabled = false;
        btnSpinner.style.display = 'none';
        btnText.textContent = 'Execute Workflow';
    }
});

// Run healthcheck on startup
checkHealth();
// Periodically check health every 15 seconds
setInterval(checkHealth, 15000);
