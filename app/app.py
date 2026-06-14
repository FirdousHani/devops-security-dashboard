from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Security Dashboard</h1>
    <p>Status: Running</p>
    <p>Deployment: Automated via Jenkins + Docker</p>
    <p><a href="/dashboard">Open Full Dashboard →</a></p>
    '''

@app.route('/health')
def health():
    return {"status": "ok"}, 200

@app.route('/dashboard')
def dashboard():
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Security Dashboard</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --accent: #00ff9c;
    --accent2: #58a6ff;
    --text: #e6edf3;
    --muted: #8b949e;
    --danger: #f85149;
    --warn: #d29922;
    --success: #3fb950;
    --radius: 8px;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    min-height: 100vh;
  }

  header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 14px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .logo {
    font-size: 16px;
    font-weight: 600;
    color: var(--accent);
    letter-spacing: 0.5px;
  }

  .status-pill {
    background: rgba(63,185,80,0.12);
    color: var(--success);
    border: 1px solid rgba(63,185,80,0.3);
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
  }

  .tabs {
    display: flex;
    gap: 2px;
    padding: 16px 24px 0;
    border-bottom: 1px solid var(--border);
    background: var(--surface);
  }

  .tab-btn {
    background: none;
    border: none;
    color: var(--muted);
    padding: 8px 18px;
    cursor: pointer;
    border-radius: var(--radius) var(--radius) 0 0;
    font-size: 13px;
    font-weight: 500;
    border-bottom: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s;
  }

  .tab-btn.active {
    color: var(--accent);
    border-bottom-color: var(--accent);
    background: rgba(0,255,156,0.05);
  }

  .tab-btn:hover:not(.active) { color: var(--text); }

  main { padding: 24px; max-width: 960px; margin: 0 auto; }

  .panel { display: none; }
  .panel.active { display: block; }

  /* NOTES */
  .notes-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .note-composer {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px;
  }

  .note-composer textarea {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    padding: 10px;
    font-size: 13px;
    resize: vertical;
    min-height: 120px;
    font-family: inherit;
    outline: none;
  }

  .note-composer textarea:focus { border-color: var(--accent); }

  .tag-select {
    margin-top: 10px;
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }

  .tag-chip {
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 500;
    cursor: pointer;
    border: 1px solid transparent;
    opacity: 0.5;
    transition: opacity 0.15s;
  }

  .tag-chip.selected { opacity: 1; }
  .tag-chip[data-tag="recon"]    { background: rgba(88,166,255,0.15); color: var(--accent2); border-color: rgba(88,166,255,0.3); }
  .tag-chip[data-tag="exploit"]  { background: rgba(248,81,73,0.12);  color: var(--danger);  border-color: rgba(248,81,73,0.3); }
  .tag-chip[data-tag="defense"]  { background: rgba(63,185,80,0.12);  color: var(--success); border-color: rgba(63,185,80,0.3); }
  .tag-chip[data-tag="misc"]     { background: rgba(139,148,158,0.15);color: var(--muted);   border-color: rgba(139,148,158,0.3); }

  .btn {
    display: inline-block;
    margin-top: 10px;
    padding: 7px 18px;
    border-radius: var(--radius);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: opacity 0.15s;
  }

  .btn:hover { opacity: 0.85; }
  .btn-accent { background: var(--accent); color: #0d1117; }
  .btn-ghost  { background: transparent; border: 1px solid var(--border); color: var(--muted); }

  .notes-list { display: flex; flex-direction: column; gap: 10px; max-height: 460px; overflow-y: auto; }

  .note-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 12px 14px;
    position: relative;
    border-left: 3px solid var(--border);
  }

  .note-card[data-tag="recon"]   { border-left-color: var(--accent2); }
  .note-card[data-tag="exploit"] { border-left-color: var(--danger); }
  .note-card[data-tag="defense"] { border-left-color: var(--success); }
  .note-card[data-tag="misc"]    { border-left-color: var(--muted); }

  .note-card .note-text { font-size: 13px; white-space: pre-wrap; margin-bottom: 6px; }
  .note-card .note-meta { font-size: 11px; color: var(--muted); display: flex; justify-content: space-between; }

  .del-btn {
    background: none; border: none; color: var(--muted);
    cursor: pointer; font-size: 16px; position: absolute;
    top: 8px; right: 10px;
  }
  .del-btn:hover { color: var(--danger); }

  .empty-state { color: var(--muted); font-size: 13px; padding: 20px 0; }

  /* QUIZ */
  .quiz-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 20px; }
  .score-badge {
    background: rgba(0,255,156,0.1);
    border: 1px solid rgba(0,255,156,0.3);
    color: var(--accent);
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
  }

  .progress-bar {
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    margin-bottom: 24px;
    overflow: hidden;
  }
  .progress-fill {
    height: 100%;
    background: var(--accent);
    border-radius: 2px;
    transition: width 0.4s ease;
  }

  .question-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 16px;
  }

  .question-text {
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 16px;
    line-height: 1.5;
  }

  .category-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 10px;
  }

  .opt-btn {
    display: block;
    width: 100%;
    text-align: left;
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 10px 14px;
    border-radius: var(--radius);
    margin-bottom: 8px;
    cursor: pointer;
    font-size: 13px;
    transition: border-color 0.15s, background 0.15s;
  }

  .opt-btn:hover:not(:disabled) { border-color: var(--accent2); background: rgba(88,166,255,0.05); }
  .opt-btn.correct  { border-color: var(--success); background: rgba(63,185,80,0.1);  color: var(--success); }
  .opt-btn.wrong    { border-color: var(--danger);  background: rgba(248,81,73,0.08); color: var(--danger); }

  .explanation {
    margin-top: 12px;
    padding: 10px 14px;
    border-radius: var(--radius);
    background: rgba(0,255,156,0.05);
    border: 1px solid rgba(0,255,156,0.15);
    font-size: 12px;
    color: var(--muted);
    display: none;
  }

  .quiz-footer { display: flex; gap: 10px; margin-top: 8px; }

  .final-screen {
    text-align: center;
    padding: 40px 20px;
    display: none;
  }

  .final-score { font-size: 48px; font-weight: 700; color: var(--accent); }
  .final-label { font-size: 14px; color: var(--muted); margin-top: 4px; }
  .final-msg   { font-size: 15px; margin: 20px 0; }

  /* EVENTS */
  .event-list { display: flex; flex-direction: column; gap: 10px; }

  .event-item {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 14px 16px;
    display: flex;
    gap: 16px;
    align-items: flex-start;
  }

  .event-date {
    min-width: 44px;
    text-align: center;
    background: rgba(0,255,156,0.08);
    border-radius: 6px;
    padding: 6px;
  }

  .event-date .day  { font-size: 22px; font-weight: 700; color: var(--accent); line-height: 1; }
  .event-date .mon  { font-size: 10px; color: var(--muted); text-transform: uppercase; }

  .event-info h3 { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
  .event-info p  { font-size: 12px; color: var(--muted); }

  .event-tag {
    margin-left: auto;
    font-size: 10px;
    padding: 3px 8px;
    border-radius: 4px;
    white-space: nowrap;
    align-self: center;
  }

  .tag-live   { background: rgba(248,81,73,0.12);  color: var(--danger);  border: 1px solid rgba(248,81,73,0.3); }
  .tag-coming { background: rgba(88,166,255,0.12); color: var(--accent2); border: 1px solid rgba(88,166,255,0.3); }

  h2 { font-size: 16px; font-weight: 600; margin-bottom: 14px; color: var(--text); }

  .section-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    color: var(--muted);
    margin-bottom: 10px;
    font-weight: 600;
  }
</style>
</head>
<body>

<header>
  <div class="logo">⬡ SecDash</div>
  <span class="status-pill">● LIVE</span>
</header>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('notes', this)">📝 Notes</button>
  <button class="tab-btn" onclick="switchTab('quiz', this)">🎯 Quiz</button>
  <button class="tab-btn" onclick="switchTab('events', this)">📅 Events</button>
</div>

<main>

  <!-- NOTES PANEL -->
  <div id="panel-notes" class="panel active">
    <div class="notes-grid">
      <div>
        <div class="section-label">New note</div>
        <div class="note-composer">
          <textarea id="note-input" placeholder="Paste findings, commands, observations…" rows="6"></textarea>
          <div class="tag-select">
            <span class="tag-chip selected" data-tag="recon" onclick="selectTag(this)">Recon</span>
            <span class="tag-chip" data-tag="exploit" onclick="selectTag(this)">Exploit</span>
            <span class="tag-chip" data-tag="defense" onclick="selectTag(this)">Defense</span>
            <span class="tag-chip" data-tag="misc" onclick="selectTag(this)">Misc</span>
          </div>
          <button class="btn btn-accent" onclick="addNote()">Save note</button>
        </div>
      </div>
      <div>
        <div class="section-label">Saved notes</div>
        <div id="notes-list" class="notes-list">
          <p class="empty-state">No notes yet. Write one →</p>
        </div>
      </div>
    </div>
  </div>

  <!-- QUIZ PANEL -->
  <div id="panel-quiz" class="panel">
    <div class="quiz-header">
      <div>
        <div class="section-label">Security quiz</div>
        <h2 id="quiz-title">Web &amp; Network Security</h2>
      </div>
      <div class="score-badge" id="score-display">0 / 0</div>
    </div>
    <div class="progress-bar"><div class="progress-fill" id="progress-fill" style="width:0%"></div></div>

    <div id="quiz-body"></div>

    <div id="final-screen" class="final-screen">
      <div class="final-score" id="final-score-val">—</div>
      <div class="final-label">correct answers</div>
      <div class="final-msg" id="final-msg"></div>
      <button class="btn btn-accent" onclick="restartQuiz()">Restart quiz</button>
    </div>
  </div>

  <!-- EVENTS PANEL -->
  <div id="panel-events" class="panel">
    <div class="section-label">Upcoming — Bengaluru</div>
    <div class="event-list">

      <div class="event-item">
        <div class="event-date"><div class="day">27</div><div class="mon">Jun</div></div>
        <div class="event-info">
          <h3>null/OWASP Bangalore Combined Meetup</h3>
          <p>Live security talks · Web application security · Community CTF warm-up</p>
        </div>
        <span class="event-tag tag-coming">Registered ✓</span>
      </div>

      <div class="event-item">
        <div class="event-date"><div class="day">10</div><div class="mon">Jul</div></div>
        <div class="event-info">
          <h3>FutureGPT — AI Red Teaming</h3>
          <p>Adversarial AI · LLM security · Prompt injection techniques · Venue TBA</p>
        </div>
        <span class="event-tag tag-coming">Registered ✓</span>
      </div>

      <div class="event-item">
        <div class="event-date"><div class="day">—</div><div class="mon">TBA</div></div>
        <div class="event-info">
          <h3>SIEM Team Competition</h3>
          <p>Alarm Engine · Threat Engine · Correlation Engine · Real-time browser log analysis</p>
        </div>
        <span class="event-tag tag-live">In progress</span>
      </div>

    </div>
  </div>

</main>

<script>
// ─── TAB SWITCHING ────────────────────────────────────────────
function switchTab(name, btn) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('panel-' + name).classList.add('active');
  btn.classList.add('active');
}

// ─── NOTES ───────────────────────────────────────────────────
let notes = JSON.parse(localStorage.getItem('secdash_notes') || '[]');
let activeTag = 'recon';

function selectTag(chip) {
  document.querySelectorAll('.tag-chip').forEach(c => c.classList.remove('selected'));
  chip.classList.add('selected');
  activeTag = chip.dataset.tag;
}

function addNote() {
  const text = document.getElementById('note-input').value.trim();
  if (!text) return;
  const note = { id: Date.now(), text, tag: activeTag, ts: new Date().toLocaleString() };
  notes.unshift(note);
  localStorage.setItem('secdash_notes', JSON.stringify(notes));
  document.getElementById('note-input').value = '';
  renderNotes();
}

function deleteNote(id) {
  notes = notes.filter(n => n.id !== id);
  localStorage.setItem('secdash_notes', JSON.stringify(notes));
  renderNotes();
}

function renderNotes() {
  const el = document.getElementById('notes-list');
  if (notes.length === 0) {
    el.innerHTML = '<p class="empty-state">No notes yet. Write one →</p>';
    return;
  }
  el.innerHTML = notes.map(n => `
    <div class="note-card" data-tag="${n.tag}">
      <button class="del-btn" onclick="deleteNote(${n.id})">×</button>
      <div class="note-text">${escHtml(n.text)}</div>
      <div class="note-meta"><span class="tag-chip tag-chip-sm" data-tag="${n.tag}">${n.tag}</span><span>${n.ts}</span></div>
    </div>`).join('');
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

renderNotes();

// ─── QUIZ ─────────────────────────────────────────────────────
const questions = [
  {
    q: "Which OWASP Top 10 category covers insecure direct object references (IDOR)?",
    cat: "Web Security",
    opts: ["A01: Broken Access Control", "A03: Injection", "A05: Security Misconfiguration", "A07: Auth Failures"],
    ans: 0,
    exp: "IDOR is a Broken Access Control flaw — users can access resources they don't own by manipulating IDs."
  },
  {
    q: "What does the Isolation Forest algorithm detect in anomaly detection?",
    cat: "ML Security",
    opts: ["Clustered data points", "Points that are easy to isolate from the rest", "Gradient descent errors", "Overfitted training samples"],
    ans: 1,
    exp: "Isolation Forest isolates anomalies by randomly partitioning — outliers require fewer splits to isolate."
  },
  {
    q: "In MITRE ATT&CK, what tactic does 'Spearphishing Attachment' (T1566.001) fall under?",
    cat: "MITRE ATT&CK",
    opts: ["Execution", "Initial Access", "Persistence", "Collection"],
    ans: 1,
    exp: "Spearphishing Attachment is an Initial Access technique — the attacker is getting a foothold, not executing yet."
  },
  {
    q: "What HTTP security header prevents clickjacking attacks?",
    cat: "Web Security",
    opts: ["Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security", "X-XSS-Protection"],
    ans: 1,
    exp: "X-Frame-Options: DENY prevents your page from being embedded in iframes, blocking clickjacking."
  },
  {
    q: "A Burp Suite Intruder attack that cycles through a single wordlist on one position is called?",
    cat: "Tools",
    opts: ["Pitchfork", "Cluster Bomb", "Sniper", "Battering Ram"],
    ans: 2,
    exp: "Sniper = one payload set, one position at a time. Pitchfork = parallel lists. Cluster Bomb = all combos."
  },
  {
    q: "In a UNION-based SQL injection, what must match between your injected SELECT and the original query?",
    cat: "Web Security",
    opts: ["Table names", "WHERE clauses", "Number and type of columns", "Database version"],
    ans: 2,
    exp: "UNION requires the same number of columns with compatible data types in both SELECT statements."
  },
  {
    q: "What port does SSH run on by default?",
    cat: "Network",
    opts: ["21", "22", "23", "2222"],
    ans: 1,
    exp: "SSH = port 22. FTP = 21. Telnet = 23. (Though SSH is often moved to a non-default port for security.)"
  },
  {
    q: "Which Nmap flag performs a SYN scan (stealth scan) without completing the TCP handshake?",
    cat: "Tools",
    opts: ["-sU", "-sT", "-sS", "-sV"],
    ans: 2,
    exp: "-sS is the SYN scan — it sends SYN, gets SYN/ACK, but sends RST instead of completing the handshake."
  },
  {
    q: "What is the primary function of an MXDR (Managed Extended Detection & Response) platform?",
    cat: "Blue Team",
    opts: [
      "Patch management automation",
      "Cross-layer threat detection, correlation, and response across endpoints, network, and cloud",
      "Firewall rule configuration",
      "Vulnerability scanning only"
    ],
    ans: 1,
    exp: "MXDR extends EDR across multiple security layers with managed detection, correlation, and response — your SISA project!"
  },
  {
    q: "In Flask, which decorator registers a URL route to a function?",
    cat: "Dev / AppSec",
    opts: ["@app.url()", "@app.route()", "@app.endpoint()", "@app.view()"],
    ans: 1,
    exp: "@app.route('/path') maps a URL path to a Python function — standard Flask pattern you're using right now."
  }
];

let current = 0, score = 0, answered = false;

function renderQuestion() {
  const q = questions[current];
  const pct = (current / questions.length) * 100;
  document.getElementById('progress-fill').style.width = pct + '%';
  document.getElementById('score-display').textContent = score + ' / ' + current;

  const catColor = {
    'Web Security': '#58a6ff', 'ML Security': '#00ff9c',
    'MITRE ATT&CK': '#f85149', 'Tools': '#d29922',
    'Network': '#a371f7', 'Blue Team': '#3fb950', 'Dev / AppSec': '#58a6ff'
  }[q.cat] || '#8b949e';

  document.getElementById('quiz-body').innerHTML = `
    <div class="question-card">
      <div class="category-badge" style="background:${catColor}22;color:${catColor};border:1px solid ${catColor}44">${q.cat}</div>
      <div class="question-text">Q${current + 1} of ${questions.length} — ${escHtml(q.q)}</div>
      ${q.opts.map((o, i) => `
        <button class="opt-btn" id="opt-${i}" onclick="answer(${i})">${escHtml(o)}</button>
      `).join('')}
      <div class="explanation" id="explanation">${escHtml(q.exp)}</div>
    </div>
    <div class="quiz-footer" id="quiz-footer" style="display:none">
      <button class="btn btn-accent" onclick="nextQuestion()">${current < questions.length - 1 ? 'Next →' : 'See results'}</button>
    </div>`;
  answered = false;
}

function answer(idx) {
  if (answered) return;
  answered = true;
  const q = questions[current];
  document.querySelectorAll('.opt-btn').forEach((b, i) => {
    b.disabled = true;
    if (i === q.ans) b.classList.add('correct');
    else if (i === idx && idx !== q.ans) b.classList.add('wrong');
  });
  if (idx === q.ans) score++;
  document.getElementById('score-display').textContent = score + ' / ' + (current + 1);
  document.getElementById('explanation').style.display = 'block';
  document.getElementById('quiz-footer').style.display = 'flex';
}

function nextQuestion() {
  current++;
  if (current >= questions.length) { showFinal(); return; }
  renderQuestion();
}

function showFinal() {
  document.getElementById('quiz-body').style.display = 'none';
  document.getElementById('progress-fill').style.width = '100%';
  const pct = Math.round((score / questions.length) * 100);
  const msgs = [
    [90, "🔥 Strong. You've internalized this."],
    [70, "⚡ Solid — keep grinding the gaps."],
    [50, "🔨 Room to grow. Review the explanations."],
    [0,  "📚 Start with the basics — it stacks up."]
  ];
  const msg = msgs.find(([t]) => pct >= t)[1];
  document.getElementById('final-score-val').textContent = score + '/' + questions.length;
  document.getElementById('final-msg').textContent = msg;
  document.getElementById('final-screen').style.display = 'block';
}

function restartQuiz() {
  current = 0; score = 0; answered = false;
  document.getElementById('final-screen').style.display = 'none';
  document.getElementById('quiz-body').style.display = 'block';
  renderQuestion();
}

renderQuestion();
</script>

</body>
</html>'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
