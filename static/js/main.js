// ═══════════════════════════════════════
// HACKER PORTFOLIO — Full JavaScript
// ═══════════════════════════════════════

// ── Detect mobile ──
var isMobile = window.innerWidth < 768;
var prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ═══ BOOT SEQUENCE ═══
(function() {
    var bootEl = document.getElementById('boot');
    if (!bootEl) return;
    
    var bootText = document.getElementById('boot-text');
    var bootBar = document.getElementById('boot-bar-fill');
    var bootSkip = document.getElementById('boot-skip');
    var skipped = false;
    
    var lines = [
        {t: 'BIOS v2.4.1 — POST Check...', c: 'dim', d: 200},
        {t: '[OK] CPU: AMD EPYC 713 — 128 threads', c: 'ok', d: 150},
        {t: '[OK] Memory Test: 170GB — Passed', c: 'ok', d: 200},
        {t: '[OK] NVMe SSD: 476GB — Healthy', c: 'ok', d: 150},
        {t: 'Loading kernel v6.8.0-hacker...', c: 'dim', d: 300},
        {t: 'Mounting /dev/sda1...', c: 'dim', d: 200},
        {t: 'Starting network interfaces...', c: 'dim', d: 250},
        {t: '[OK] eth0: 921 Mbps UP', c: 'ok', d: 150},
        {t: 'Initializing Matrix Rain Engine...', c: 'dim', d: 200},
        {t: '[OK] Canvas renderer active', c: 'ok', d: 150},
        {t: 'Loading 3D subsystem...', c: 'dim', d: 200},
        {t: '[OK] WebGL context created', c: 'ok', d: 150},
        {t: 'Parsing GitHub API data...', c: 'dim', d: 250},
        {t: '[OK] 13 repositories loaded', c: 'ok', d: 150},
        {t: '[OK] 5 languages indexed', c: 'ok', d: 100},
        {t: 'Building contribution graph...', c: 'dim', d: 200},
        {t: 'Initializing interactive terminal...', c: 'dim', d: 200},
        {t: '[OK] Terminal ready — type "help" for commands', c: 'ok', d: 150},
        {t: 'Applying CRT shader effects...', c: 'dim', d: 200},
        {t: '[OK] Scanlines + vignette active', c: 'ok', d: 100},
        {t: '', c: 'dim', d: 100},
        {t: '>>> SYSTEM READY — Welcome, visitor <<<', c: 'bright', d: 400},
    ];
    
    var totalLines = lines.length;
    var currentLine = 0;
    
    function addBootLine(idx) {
        if (skipped || idx >= lines.length) {
            finishBoot();
            return;
        }
        var line = lines[idx];
        var el = document.createElement('div');
        el.className = 'bline ' + line.c;
        el.textContent = line.t;
        bootText.appendChild(el);
        bootText.scrollTop = bootText.scrollHeight;
        bootBar.style.width = ((idx + 1) / totalLines * 100) + '%';
        currentLine = idx + 1;
        setTimeout(function() { addBootLine(idx + 1); }, line.d);
    }
    
    function finishBoot() {
        bootBar.style.width = '100%';
        setTimeout(function() {
            bootEl.classList.add('hidden');
            setTimeout(function() {
                bootEl.style.display = 'none';
                startPortfolio();
            }, 800);
        }, 500);
    }
    
    if (bootSkip) {
        bootSkip.addEventListener('click', function() {
            skipped = true;
            finishBoot();
        });
    }
    
    if (prefersReduced) {
        finishBoot();
    } else {
        setTimeout(function() { addBootLine(0); }, 500);
    }
})();

// ═══ START PORTFOLIO (after boot) ═══
function startPortfolio() {
    var nav = document.querySelector('nav');
    if (nav) nav.classList.add('show');
    
    if (!prefersReduced) {
        startMatrix();
        startRunningTerminal();
        typeHeroName();
        startCursorTrail();
    } else {
        showHeroImmediate();
    }
    
    initSections();
    initCards();
    initAvatarParallax();
    initInteractiveTerminal();
    initKonamiCode();
}

// ═══ MATRIX RAIN ═══
function startMatrix() {
    var mc = document.getElementById('matrix');
    if (!mc) return;
    var ctx = mc.getContext('2d');
    function resize() { mc.width = innerWidth; mc.height = innerHeight; }
    resize();
    addEventListener('resize', resize);
    
    var chars = '\u30A2\u30A4\u30A6\u30A8\u30AA\u30AB\u30AD\u30AF\u30B1\u30B301{}[]<>=/\\|;:@#$%^&*';
    var fs = isMobile ? 16 : 13;
    var cols = Math.floor(innerWidth / fs);
    var drops = [];
    for (var i = 0; i < cols; i++) drops.push(Math.random() * -100);
    
    function draw() {
        ctx.fillStyle = 'rgba(0,0,0,0.06)';
        ctx.fillRect(0, 0, mc.width, mc.height);
        ctx.font = fs + 'px JetBrains Mono';
        for (var i = 0; i < drops.length; i++) {
            var ch = chars[Math.floor(Math.random() * chars.length)];
            if (Math.random() > 0.96) {
                ctx.fillStyle = '#ffffff';
                ctx.shadowColor = '#00ff41';
                ctx.shadowBlur = 15;
            } else {
                ctx.fillStyle = 'rgba(0,255,65,' + (0.3 + Math.random() * 0.4) + ')';
                ctx.shadowBlur = 0;
            }
            ctx.fillText(ch, i * fs, drops[i] * fs);
            ctx.shadowBlur = 0;
            if (drops[i] * fs > mc.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, isMobile ? 80 : 45);
}

// ═══ RUNNING TERMINAL BG ═══
function startRunningTerminal() {
    var box = document.getElementById('rterm');
    if (!box) return;
    
    var cmds = [
        {p:'~$',c:'nmap -sV 192.168.1.0/24',o:'Scanning 256 hosts...'},
        {p:'~$',c:'ssh deploy@server-prod',o:'Connection established.'},
        {p:'deploy@prod:~$',c:'docker compose up -d',o:'3 containers started'},
        {p:'~$',c:'git push origin main',o:'Enumerating objects: 47, done.'},
        {p:'~$',c:'python3 train.py --epochs 100',o:'Epoch 100/100 \u2014 loss: 0.0023'},
        {p:'~$',c:'kubectl get pods',o:'All pods running.'},
        {p:'~$',c:'cargo build --release',o:'Compiling... finished in 12.3s'},
        {p:'~$',c:'hermes chat -q "deploy to prod"',o:'Agent executing...'},
        {p:'~$',c:'solana program deploy myapp.so',o:'Deployed: 7xKX...9aBc'},
        {p:'~$',c:'npx hardhat verify 0x1234',o:'Contract verified \u2713'},
        {p:'~$',c:'htop',o:'CPU: 23%  Mem: 4.2/8GB'},
        {p:'~$',c:'forge test --gas-report',o:'32 tests passed, 0 failed'},
        {p:'~$',c:'python3 bot.py --mode arb',o:'3 opportunities found'},
        {p:'~$',c:'npm run deploy',o:'Deployed to Vercel.'},
        {p:'~$',c:'curl -s api.github.com/users/Fatkhl',o:'Fetching profile...'},
        {p:'~$',c:'docker ps --format "table"',o:'5 containers running'},
        {p:'~$',c:'go build -o server ./cmd/api',o:'Build successful'},
        {p:'~$',c:'cargo clippy -- -W clippy::all',o:'0 warnings, 0 errors'},
    ];
    var idx = 0;
    
    function spawn() {
        var e = cmds[idx % cmds.length];
        idx++;
        var el = document.createElement('div');
        el.className = 'tl';
        el.style.left = (3 + Math.random() * 85) + '%';
        el.style.top = '100%';
        var dur = 18 + Math.random() * 22;
        var delay = Math.random() * 2;
        el.style.animationDuration = dur + 's';
        el.style.animationDelay = delay + 's';
        el.style.fontSize = (9 + Math.random() * 3) + 'px';
        el.innerHTML = '<span class="p">' + e.p + '</span> <span class="c">' + e.c + '</span><br><span class="o">' + e.o + '</span>';
        box.appendChild(el);
        setTimeout(function() { el.remove(); }, (dur + delay) * 1000);
    }
    
    var interval = isMobile ? 4000 : 2200;
    setInterval(spawn, interval);
    for (var j = 0; j < (isMobile ? 4 : 10); j++) setTimeout(spawn, j * 350);
}

// ═══ TYPING ANIMATION ═══
function typeText(el, text, speed, cb) {
    if (!el || !text) { if (cb) cb(); return; }
    var i = 0;
    el.innerHTML = '<span class="typed-cursor"></span>';
    function type() {
        if (i < text.length) {
            el.innerHTML = text.substring(0, i + 1) + '<span class="typed-cursor"></span>';
            i++;
            setTimeout(type, speed + Math.random() * 40);
        } else {
            el.innerHTML = text + '<span class="typed-cursor"></span>';
            if (cb) setTimeout(cb, 300);
        }
    }
    type();
}

function typeHeroName() {
    var nameEl = document.querySelector('.hero-name');
    var handleEl = document.querySelector('.handle');
    var bioEl = document.querySelector('.hero-bio');
    
    if (!nameEl) return;
    
    var nameText = nameEl.getAttribute('data-text') || nameEl.textContent;
    var handleText = handleEl ? handleEl.getAttribute('data-handle') || '' : '';
    var bioText = bioEl ? bioEl.getAttribute('data-bio') || '' : '';
    
    typeText(nameEl, nameText, 60, function() {
        nameEl.classList.add('glitch-active');
        if (handleEl) {
            typeText(handleEl, handleText, 40, function() {
                if (bioEl) typeText(bioEl, bioText, 25);
            });
        }
    });
}

function showHeroImmediate() {
    var nameEl = document.querySelector('.hero-name');
    var handleEl = document.querySelector('.handle');
    var bioEl = document.querySelector('.hero-bio');
    if (nameEl) { nameEl.textContent = nameEl.getAttribute('data-text'); nameEl.classList.add('glitch-active'); }
    if (handleEl) handleEl.textContent = handleEl.getAttribute('data-handle');
    if (bioEl) bioEl.textContent = bioEl.getAttribute('data-bio');
}

// ═══ CURSOR TRAIL ═══
function startCursorTrail() {
    if (isMobile) return;
    var trail = [];
    var count = 12;
    for (var i = 0; i < count; i++) {
        var dot = document.createElement('div');
        dot.className = 'ctrail';
        dot.style.width = (8 - i * 0.4) + 'px';
        dot.style.height = (8 - i * 0.4) + 'px';
        document.body.appendChild(dot);
        trail.push({el: dot, x: 0, y: 0});
    }
    
    var mx = 0, my = 0;
    document.addEventListener('mousemove', function(e) { mx = e.clientX; my = e.clientY; });
    
    function animate() {
        var px = mx, py = my;
        for (var i = 0; i < trail.length; i++) {
            var t = trail[i];
            t.x += (px - t.x) * (0.35 - i * 0.015);
            t.y += (py - t.y) * (0.35 - i * 0.015);
            t.el.style.left = t.x + 'px';
            t.el.style.top = t.y + 'px';
            t.el.style.opacity = (1 - i / count) * 0.6;
            px = t.x; py = t.y;
        }
        requestAnimationFrame(animate);
    }
    animate();
}

// ═══ SCROLL SECTIONS ═══
function initSections() {
    var sections = document.querySelectorAll('.section');
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) {
            if (e.isIntersecting) {
                e.target.classList.add('vis');
                // Stagger children
                var items = e.target.querySelectorAll('.lang-i,.arow,.repo-card');
                items.forEach(function(item, idx) {
                    setTimeout(function() { item.classList.add('vis'); }, idx * 80);
                });
            }
        });
    }, { threshold: 0.1 });
    sections.forEach(function(s) { observer.observe(s); });
    
    // Nav active
    addEventListener('scroll', function() {
        var y = scrollY + 100;
        sections.forEach(function(s) {
            var top = s.offsetTop, h = s.offsetHeight, id = s.id;
            var link = document.querySelector('.nav-links a[href="#' + id + '"]');
            if (link) link.style.color = (y >= top && y < top + h) ? '#00ff41' : '';
        });
    });
}

// ═══ 3D CARD TILT ═══
function initCards() {
    if (isMobile) return;
    document.querySelectorAll('.repo-card').forEach(function(card) {
        card.addEventListener('mousemove', function(e) {
            var r = card.getBoundingClientRect();
            var x = e.clientX - r.left, y = e.clientY - r.top;
            var rx = ((y - r.height/2) / (r.height/2)) * -8;
            var ry = ((x - r.width/2) / (r.width/2)) * 8;
            card.style.setProperty('--rx', rx + 'deg');
            card.style.setProperty('--ry', ry + 'deg');
            card.style.setProperty('--mx', (x / r.width * 100) + '%');
            card.style.setProperty('--my', (y / r.height * 100) + '%');
            card.classList.add('tilted');
        });
        card.addEventListener('mouseleave', function() {
            card.style.setProperty('--rx', '0deg');
            card.style.setProperty('--ry', '0deg');
            card.classList.remove('tilted');
        });
    });
}

// ═══ 3D AVATAR PARALLAX ═══
function initAvatarParallax() {
    if (isMobile) return;
    var av = document.querySelector('.avatar-3d');
    if (!av) return;
    document.addEventListener('mousemove', function(e) {
        var rx = ((e.clientY - innerHeight/2) / (innerHeight/2)) * -6;
        var ry = ((e.clientX - innerWidth/2) / (innerWidth/2)) * 10;
        av.style.transform = 'rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
    });
    
    var ht = document.querySelector('.hero-text');
    if (ht) {
        document.addEventListener('mousemove', function(e) {
            var mx = ((e.clientX - innerWidth/2) / (innerWidth/2)) * 3;
            var my = ((e.clientY - innerHeight/2) / (innerHeight/2)) * 2;
            ht.style.transform = 'translateX(' + mx + 'px) translateY(' + my + 'px) translateZ(10px)';
        });
    }
}

// ═══ INTERACTIVE TERMINAL ═══
function initInteractiveTerminal() {
    var term = document.getElementById('iterm');
    var toggle = document.getElementById('iterm-toggle');
    var body = document.getElementById('iterm-body');
    var input = document.getElementById('iterm-input');
    var dotsR = document.querySelector('#iterm-dots .r');
    var dotsY = document.querySelector('#iterm-dots .y');
    var isOpen = false;
    
    if (!term || !toggle || !input) return;
    
    toggle.addEventListener('click', function() {
        isOpen = !isOpen;
        term.classList.toggle('open', isOpen);
        toggle.classList.toggle('hidden', isOpen);
        if (isOpen) input.focus();
    });
    
    if (dotsR) dotsR.addEventListener('click', function() {
        isOpen = false;
        term.classList.remove('open');
        toggle.classList.remove('hidden');
    });
    
    if (dotsY) dotsY.addEventListener('click', function() {
        // Minimize (just close)
        isOpen = false;
        term.classList.remove('open');
        toggle.classList.remove('hidden');
    });
    
    function addOutput(text, cls) {
        var el = document.createElement('div');
        el.className = 'it-output' + (cls ? ' ' + cls : '');
        el.innerHTML = text;
        body.appendChild(el);
        body.scrollTop = body.scrollHeight;
    }
    
    var name = document.querySelector('.hero-name');
    var nameStr = name ? (name.getAttribute('data-text') || 'Developer') : 'Developer';
    
    var commands = {
        help: function() {
            addOutput('<br><span class="cyan">Available commands:</span><br>' +
                '  <span class="ok">help</span>      — Show this message<br>' +
                '  <span class="ok">about</span>     — About me<br>' +
                '  <span class="ok">skills</span>    — Tech stack<br>' +
                '  <span class="ok">projects</span>  — Featured projects<br>' +
                '  <span class="ok">contact</span>   — Get in touch<br>' +
                '  <span class="ok">whoami</span>    — Who am I?<br>' +
                '  <span class="ok">date</span>      — Current date/time<br>' +
                '  <span class="ok">clear</span>     — Clear terminal<br>' +
                '  <span class="ok">matrix</span>    — ???<br>' +
                '  <span class="ok">sudo</span>      — Try it ;)<br>');
        },
        about: function() {
            addOutput('<br><span class="cyan">About ' + nameStr + ':</span><br>' +
                '  Web3 Developer &amp; AI Engineer<br>' +
                '  Building the future of blockchain automation<br>' +
                '  and AI-powered tools.<br><br>' +
                '  <span class="dim">GitHub: github.com/Fatkhl</span><br>');
        },
        skills: function() {
            var el = document.querySelectorAll('.lang-i .lang-n');
            var skills = [];
            el.forEach(function(e) { skills.push(e.textContent); });
            addOutput('<br><span class="cyan">Tech Stack:</span><br>  ' +
                skills.join(' \u2022 ') + '<br>');
        },
        projects: function() {
            var cards = document.querySelectorAll('.repo-name');
            var names = [];
            cards.forEach(function(e) { names.push(e.textContent); });
            addOutput('<br><span class="cyan">Top Projects:</span><br>  ' +
                names.slice(0, 6).join('<br>  ') + '<br><br>' +
                '  <span class="dim">Scroll down for more...</span><br>');
        },
        contact: function() {
            addOutput('<br><span class="cyan">Get in touch:</span><br>' +
                '  GitHub: <span class="ok">github.com/Fatkhl</span><br>' +
                '  Just reach out on GitHub! <span class="dim">\u2764</span><br>');
        },
        whoami: function() {
            addOutput('<br><span class="ok">visitor</span>@<span class="cyan">fatkhl-portfolio</span><br>');
        },
        date: function() {
            addOutput('<br>' + new Date().toString() + '<br>');
        },
        clear: function() {
            body.innerHTML = '';
        },
        matrix: function() {
            triggerKonami();
        },
        sudo: function() {
            addOutput('<br><span style="color:#ff1744">Nice try! But you don\'t have root access here ;)</span><br>' +
                '  <span class="dim">This incident will be reported.</span><br>');
        }
    };
    
    input.addEventListener('keydown', function(e) {
        if (e.key !== 'Enter') return;
        var val = input.value.trim().toLowerCase();
        if (!val) return;
        
        // Show the typed command
        addOutput('<span class="cyan">visitor@fatkhl:~$</span> ' + val);
        input.value = '';
        
        if (commands[val]) {
            commands[val]();
        } else {
            addOutput('<span class="dim">bash: ' + val + ': command not found. Type "help" for available commands.</span><br>');
        }
    });
}

// ═══ KONAMI CODE EASTER EGG ═══
function initKonamiCode() {
    var code = [38,38,40,40,37,39,37,39,66,65]; // ↑↑↓↓←→←→BA
    var pos = 0;
    
    document.addEventListener('keydown', function(e) {
        if (e.keyCode === code[pos]) {
            pos++;
            if (pos === code.length) {
                triggerKonami();
                pos = 0;
            }
        } else {
            pos = 0;
        }
    });
}

function triggerKonami() {
    var overlay = document.getElementById('matrix-mode');
    if (!overlay) return;
    overlay.classList.add('active');
    
    // Boost matrix rain
    var mc = document.getElementById('matrix');
    if (mc) mc.style.opacity = '0.4';
    
    setTimeout(function() {
        overlay.classList.remove('active');
        if (mc) mc.style.opacity = '';
    }, 5000);
}
