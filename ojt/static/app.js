// FOSSology License Detection - Frontend Application

const API_BASE = 'http://localhost:5000/api';

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabName = btn.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.getElementById(`${tabName}-tab`).classList.add('active');
}

// Analyze single text
document.getElementById('analyze-btn').addEventListener('click', async () => {
    const text = document.getElementById('input-text').value.trim();
    if (!text) {
        showError('analyze-result', 'Please enter some text to analyze');
        return;
    }
    
    const resultDiv = document.getElementById('analyze-result');
    resultDiv.innerHTML = '<div class="loading">Analyzing...</div>';
    
    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const result = await response.json();
        displayAnalysisResult(resultDiv, result);
    } catch (error) {
        showError('analyze-result', `Error: ${error.message}`);
    }
});

function displayAnalysisResult(container, result) {
    const isAmbiguous = result.is_ambiguous;
    const confidence = result.confidence || 0;
    const licenseName = result.detected_license || 'Unknown';
    const spdxId = result.spdx_id || 'N/A';
    
    let confidenceClass = 'confidence-low';
    if (confidence >= 0.8) confidenceClass = 'confidence-high';
    else if (confidence >= 0.6) confidenceClass = 'confidence-medium';
    
    const ambiguousBadge = isAmbiguous 
        ? '<span class="ambiguous-badge">⚠️ Ambiguous</span>' 
        : '';
    
    let matchesHtml = '';
    if (result.matches && result.matches.length > 0) {
        matchesHtml = '<div class="matches-list"><strong>Top Matches:</strong>';
        result.matches.slice(0, 5).forEach(match => {
            matchesHtml += `
                <div class="match-item">
                    <span>${match.license_name}</span>
                    <span>${(match.combined_score * 100).toFixed(1)}%</span>
                </div>
            `;
        });
        matchesHtml += '</div>';
    }
    
    container.innerHTML = `
        <div class="result-item ${isAmbiguous ? 'ambiguous' : 'confident'}">
            <div class="result-header">
                <div>
                    <div class="license-name">${licenseName} ${ambiguousBadge}</div>
                    <div class="spdx-id">SPDX ID: ${spdxId}</div>
                </div>
                <div class="confidence-badge ${confidenceClass}">
                    ${(confidence * 100).toFixed(1)}% confidence
                </div>
            </div>
            ${matchesHtml}
        </div>
    `;
}

// Batch analysis
let batchResults = [];

document.getElementById('load-samples-btn').addEventListener('click', async () => {
    try {
        const response = await fetch('/data/sample_fragments.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const samples = await response.json();
        await analyzeBatch(samples);
    } catch (error) {
        showError('batch-results', `Error loading samples: ${error.message}`);
    }
});

document.getElementById('file-input').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = async (event) => {
        try {
            let data;
            if (file.name.endsWith('.json')) {
                data = JSON.parse(event.target.result);
            } else if (file.name.endsWith('.csv')) {
                data = parseCSV(event.target.result);
            }
            
            if (Array.isArray(data)) {
                await analyzeBatch(data);
            } else {
                showError('batch-results', 'File must contain an array of objects');
            }
        } catch (error) {
            showError('batch-results', `Error parsing file: ${error.message}`);
        }
    };
    reader.readAsText(file);
});

async function analyzeBatch(samples) {
    const resultsDiv = document.getElementById('batch-results');
    resultsDiv.innerHTML = '<div class="loading">Analyzing batch...</div>';
    
    try {
        const fragments = samples.map(s => ({
            id: s.id || Math.random(),
            text: s.text || s
        }));
        
        const response = await fetch(`${API_BASE}/batch-analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fragments })
        });
        
        const data = await response.json();
        batchResults = data.results || [];
        displayBatchResults(batchResults);
    } catch (error) {
        showError('batch-results', `Error: ${error.message}`);
    }
}

function displayBatchResults(results) {
    const resultsDiv = document.getElementById('batch-results');
    
    if (results.length === 0) {
        resultsDiv.innerHTML = '<div class="error">No results to display</div>';
        return;
    }
    
    resultsDiv.innerHTML = results.map((result, idx) => {
        const isAmbiguous = result.is_ambiguous;
        const confidence = result.confidence || 0;
        const licenseName = result.detected_license || 'Unknown';
        
        let confidenceClass = 'confidence-low';
        if (confidence >= 0.8) confidenceClass = 'confidence-high';
        else if (confidence >= 0.6) confidenceClass = 'confidence-medium';
        
        const ambiguousBadge = isAmbiguous 
            ? '<span class="ambiguous-badge">⚠️ Ambiguous</span>' 
            : '';
        
        return `
            <div class="result-item ${isAmbiguous ? 'ambiguous' : 'confident'}">
                <div class="result-header">
                    <div>
                        <div class="license-name">#${idx + 1}: ${licenseName} ${ambiguousBadge}</div>
                        <div class="spdx-id">SPDX: ${result.spdx_id || 'N/A'}</div>
                    </div>
                    <div class="confidence-badge ${confidenceClass}">
                        ${(confidence * 100).toFixed(1)}%
                    </div>
                </div>
                <div class="triage-text">${(result.original_text || '').substring(0, 200)}...</div>
            </div>
        `;
    }).join('');
}

// Export functions
document.getElementById('export-json-btn').addEventListener('click', () => {
    if (batchResults.length === 0) {
        alert('No results to export. Please run batch analysis first.');
        return;
    }
    exportData('json');
});

document.getElementById('export-csv-btn').addEventListener('click', () => {
    if (batchResults.length === 0) {
        alert('No results to export. Please run batch analysis first.');
        return;
    }
    exportData('csv');
});

document.getElementById('export-spdx-btn').addEventListener('click', () => {
    if (batchResults.length === 0) {
        alert('No results to export. Please run batch analysis first.');
        return;
    }
    exportData('spdx');
});

async function exportData(format) {
    try {
        const response = await fetch(`${API_BASE}/export`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ results: batchResults, format })
        });
        
        const data = await response.json();
        
        // Download file
        const blob = new Blob([data.data], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `license-report.${format}`;
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        alert(`Export error: ${error.message}`);
    }
}

// Triage view
let triageItems = [];

function loadTriageView() {
    // Filter ambiguous results for triage
    const ambiguousResults = batchResults.filter(r => r.is_ambiguous);
    triageItems = ambiguousResults;
    displayTriageItems();
}

function displayTriageItems() {
    const triageDiv = document.getElementById('triage-list');
    
    if (triageItems.length === 0) {
        triageDiv.innerHTML = '<div class="info-text">No ambiguous items to review. Run batch analysis first.</div>';
        return;
    }
    
    triageDiv.innerHTML = triageItems.map((item, idx) => {
        return `
            <div class="triage-item ambiguous">
                <div class="result-header">
                    <div>
                        <div class="license-name">${item.detected_license || 'Unknown'}</div>
                        <div class="spdx-id">SPDX: ${item.spdx_id || 'N/A'} | Confidence: ${(item.confidence * 100).toFixed(1)}%</div>
                    </div>
                </div>
                <div class="triage-text">${item.original_text || ''}</div>
                <div class="triage-actions">
                    <button class="btn btn-success" onclick="triageDecision(${idx}, 'accept')">✓ Accept</button>
                    <button class="btn btn-danger" onclick="triageDecision(${idx}, 'reject')">✗ Reject</button>
                </div>
            </div>
        `;
    }).join('');
}

window.triageDecision = async function(idx, decision) {
    const item = triageItems[idx];
    
    try {
        await fetch(`${API_BASE}/triage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id: item.id,
                decision,
                detected_license: item.detected_license,
                confidence: item.confidence,
                timestamp: new Date().toISOString()
            })
        });
        
        // Remove from triage list
        triageItems.splice(idx, 1);
        displayTriageItems();
        
        if (triageItems.length === 0) {
            showSuccess('triage-list', 'All items have been reviewed!');
        }
    } catch (error) {
        alert(`Error recording decision: ${error.message}`);
    }
};

// Evaluation
document.getElementById('evaluate-btn').addEventListener('click', async () => {
    try {
        const response = await fetch('/data/sample_fragments.json');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const samples = await response.json();
        
        const evalDiv = document.getElementById('evaluation-results');
        evalDiv.innerHTML = '<div class="loading">Evaluating...</div>';
        
        const evalResponse = await fetch(`${API_BASE}/evaluate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ samples })
        });
        
        const metrics = await evalResponse.json();
        displayMetrics(metrics);
    } catch (error) {
        showError('evaluation-results', `Error: ${error.message}`);
    }
});

function displayMetrics(metrics) {
    const metricsDiv = document.getElementById('evaluation-results');
    
    metricsDiv.innerHTML = `
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Accuracy</div>
                <div class="metric-value">${(metrics.accuracy * 100).toFixed(1)}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Precision</div>
                <div class="metric-value">${(metrics.precision * 100).toFixed(1)}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Recall</div>
                <div class="metric-value">${(metrics.recall * 100).toFixed(1)}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">F1 Score</div>
                <div class="metric-value">${(metrics.f1_score * 100).toFixed(1)}%</div>
            </div>
        </div>
        <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <strong>Details:</strong><br>
            Total Samples: ${metrics.total_samples}<br>
            Correct: ${metrics.correct}<br>
            True Positives: ${metrics.true_positives}<br>
            False Positives: ${metrics.false_positives}<br>
            False Negatives: ${metrics.false_negatives}
        </div>
    `;
}

// Utility functions
function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="error">${message}</div>`;
}

function showSuccess(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<div class="success">${message}</div>`;
}

function parseCSV(csvText) {
    const lines = csvText.split('\n');
    const headers = lines[0].split(',').map(h => h.trim());
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim()) {
            const values = lines[i].split(',').map(v => v.trim());
            const obj = {};
            headers.forEach((header, idx) => {
                obj[header] = values[idx] || '';
            });
            data.push(obj);
        }
    }
    
    return data;
}

// Auto-load triage when switching to triage tab
document.querySelector('[data-tab="triage"]').addEventListener('click', () => {
    setTimeout(loadTriageView, 100);
});

