// ASCII Art Generator in the browser: the real Python package runs inside Pyodide.
// Flow: load Pyodide -> install Pillow and pyfiglet -> unpack ascii_art_generator.zip
// -> call web_bridge.run_command(text) -> turn the ANSI colours in its output into HTML.
"use strict";

const EXAMPLES = {
  "Shapes": ["draw a heart size 4 color red", "draw a star 8 color yellow", "make a flower 8 color rainbow",
             "make a butterfly 8 color magenta", "draw a pentagon 8 color cyan", "make an oval 30x8 color green"],
  "Text": ["write HELLO", "write HELLO with font block", "write ASCII with font slant color cyan",
           "make a banner with text WELCOME"],
  "Styles": ["make a rectangle 12x5 color cyan style dotted", "draw a circle with radius 6 style empty color blue",
             "draw a heart size 3 border rounded color red", "draw a heart size 4 color rainbow"],
  "Random": ["make an emoji", "draw a sad emoji", "draw a big cat color yellow", "make a spiral 20"],
  "Combine": ["make a circle with radius 5 color blue and a rectangle 10x5 color red",
              "teach ecstatic as happy", "draw an ecstatic heart"],
};

const $ = (selector) => document.querySelector(selector);
const els = {
  form: $("#command-form"), input: $("#command"), run: $("#run"), status: $("#status"),
  output: $("#output"), chips: $("#chips"), copyText: $("#copy-text"), copyImage: $("#copy-image"), copyLink: $("#copy-link"),
  imageForm: $("#image-form"), imageFile: $("#image-file"), imageWidth: $("#image-width"),
  imageColor: $("#image-color"), imageRun: $("#image-run"),
};

let runCommand = null;      // set once Python is ready
let pyodide = null;
let lastText = "";          // plain text of the last result, for "Copy text"
let lastRaw = "";           // the same result with its ANSI colours, for "Copy as image"
const commandHistory = [];     // not `history`: that name is window.history
let historyPos = 0;

// --- ANSI -> HTML --------------------------------------------------------
const PALETTE = [
  "#545d68", "#ff7b72", "#56d364", "#e3b341", "#79c0ff", "#d2a8ff", "#56d4dd", "#e6edf3",   // 0-7 (black lifted so it shows)
  "#8b949e", "#ffa198", "#7ee787", "#f2cc60", "#a5d6ff", "#e2c5ff", "#76e3ea", "#ffffff",   // 8-15 bright
];

function color256(n) {
  if (n < 16) return PALETTE[n];
  if (n < 232) {
    n -= 16;
    const level = (v) => (v ? 55 + v * 40 : 0);
    return `rgb(${level(Math.floor(n / 36))},${level(Math.floor(n / 6) % 6)},${level(n % 6)})`;
  }
  const grey = 8 + (n - 232) * 10;
  return `rgb(${grey},${grey},${grey})`;
}

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// Calls emit(chunk, state) for every run of text that shares one colour and weight.
function walkAnsi(text, emit) {
  text = text.replace(/\x1b\[[0-9;?]*[A-Za-ln-z]/g, "");          // cursor moves etc.: not needed here
  const state = { fg: null, bold: false, underline: false };
  let last = 0;

  const applyCodes = (codes) => {
    for (let i = 0; i < codes.length; i++) {
      const c = codes[i];
      if (c === 0) { state.fg = null; state.bold = false; state.underline = false; }
      else if (c === 1) state.bold = true;
      else if (c === 22) state.bold = false;
      else if (c === 4) state.underline = true;
      else if (c === 24) state.underline = false;
      else if (c >= 30 && c <= 37) state.fg = PALETTE[c - 30];
      else if (c >= 90 && c <= 97) state.fg = PALETTE[c - 90 + 8];
      else if (c === 39) state.fg = null;
      else if (c === 38 && codes[i + 1] === 5) { state.fg = color256(codes[i + 2] ?? 0); i += 2; }
      else if (c === 38 && codes[i + 1] === 2) {
        state.fg = `rgb(${codes[i + 2] ?? 0},${codes[i + 3] ?? 0},${codes[i + 4] ?? 0})`; i += 4;
      }
    }
  };

  const pattern = /\x1b\[([0-9;]*)m/g;
  let match;
  while ((match = pattern.exec(text)) !== null) {
    if (match.index > last) emit(text.slice(last, match.index), state);
    applyCodes(match[1] === "" ? [0] : match[1].split(";").map(Number));
    last = pattern.lastIndex;
  }
  if (last < text.length) emit(text.slice(last), state);
}

function ansiToHtml(text) {
  let html = "";
  walkAnsi(text, (chunk, state) => {
    const style = [];
    if (state.fg) style.push(`color:${state.fg}`);
    if (state.bold) style.push("font-weight:700");
    if (state.underline) style.push("text-decoration:underline");
    html += style.length ? `<span style="${style.join(";")}">${escapeHtml(chunk)}</span>` : escapeHtml(chunk);
  });
  return html;
}

const stripAnsi = (text) => text.replace(/\x1b\[[0-9;?]*[A-Za-z]/g, "");

// The drawing as plain text: no colour codes, no trailing spaces, no blank lines at either end.
function plainText(text) {
  const lines = stripAnsi(text).split("\n").map((line) => line.replace(/\s+$/, ""));
  while (lines.length && !lines[0]) lines.shift();
  while (lines.length && !lines[lines.length - 1]) lines.pop();
  return lines.join("\n");
}

// --- drawing -> PNG ------------------------------------------------------
// Pasted as text, a drawing loses its colours in a chat app and wraps on a phone. A picture does neither.
const IMAGE_MAX_SIDE = 4096;      // longest side in pixels; larger canvases fail in some browsers

// The drawing as rows of coloured cells, trimmed the same way as plainText().
function colourCells(text) {
  const rows = [[]];
  walkAnsi(text, (chunk, state) => {
    for (const ch of chunk) {
      if (ch === "\n") rows.push([]);
      else rows[rows.length - 1].push({ ch, fg: state.fg, bold: state.bold });
    }
  });
  for (const row of rows) {
    while (row.length && /\s/.test(row[row.length - 1].ch)) row.pop();
  }
  while (rows.length && !rows[0].length) rows.shift();
  while (rows.length && !rows[rows.length - 1].length) rows.pop();
  return rows;
}

// Paints the drawing with the result panel's own font and colours; null when there is nothing to paint.
function drawingCanvas(text) {
  const rows = colourCells(text);
  if (!rows.length) return null;
  const style = getComputedStyle(els.output);
  const size = parseFloat(style.fontSize);
  const font = (bold) => `${bold ? 700 : 400} ${size}px ${style.fontFamily}`;
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");
  ctx.font = font(false);
  const cellW = ctx.measureText("M").width;
  const cellH = parseFloat(style.lineHeight) || size * 1.15;
  const pad = size;
  const width = Math.max(...rows.map((row) => row.length)) * cellW + 2 * pad;
  const height = rows.length * cellH + 2 * pad;
  const scale = Math.min(2, IMAGE_MAX_SIDE / Math.max(width, height));      // 2x keeps it sharp when zoomed

  canvas.width = Math.ceil(width * scale);
  canvas.height = Math.ceil(height * scale);
  ctx.scale(scale, scale);
  ctx.fillStyle = getComputedStyle(els.output.parentElement).backgroundColor;
  ctx.fillRect(0, 0, width, height);
  ctx.textBaseline = "middle";
  rows.forEach((row, y) => {
    // one character per cell, so a glyph from a fallback font cannot shift the rest of the line
    row.forEach((cell, x) => {
      ctx.font = font(cell.bold);
      ctx.fillStyle = cell.fg ?? style.color;
      ctx.fillText(cell.ch, pad + x * cellW, pad + (y + 0.5) * cellH);
    });
  });
  return canvas;
}

const canvasBlob = (canvas) => new Promise((resolve, reject) => {
  canvas.toBlob((blob) => (blob ? resolve(blob) : reject(new Error("could not encode the image"))), "image/png");
});

function download(blob, name) {
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 1000);
}

// --- UI helpers ----------------------------------------------------------
function setStatus(message, isError = false) {
  els.status.textContent = message;
  els.status.classList.toggle("error", isError);
}

function setReady(ready) {
  for (const el of [els.input, els.run, els.copyText, els.copyImage, els.copyLink, els.imageFile, els.imageRun]) {
    el.disabled = !ready;
  }
  document.querySelectorAll(".chip").forEach((chip) => { chip.disabled = !ready; });
}

function show(raw) {
  const text = raw.replace(/^\n+/, "");
  lastText = plainText(text);
  lastRaw = text;
  els.output.innerHTML = ansiToHtml(text);
  els.output.scrollTop = 0;
  document.body.dataset.rendered = String(lastText.length);    // handy for automated checks
}

function execute(command, { remember = true } = {}) {
  command = command.trim();
  if (!command || !runCommand) return;
  els.input.value = command;
  setStatus("Running...");
  // let the browser paint "Running..." before the (synchronous) Python call
  setTimeout(() => {
    const started = performance.now();
    try {
      show(runCommand(command));
      setStatus(`Done in ${Math.round(performance.now() - started)} ms.`);
    } catch (error) {
      show(`Error: ${error}`);
      setStatus("That command failed.", true);
    }
    if (remember && commandHistory[commandHistory.length - 1] !== command) commandHistory.push(command);
    if (commandHistory.length > 200) commandHistory.shift();
    historyPos = commandHistory.length;
    const url = new URL(location.href);
    url.searchParams.set("cmd", command);
    replaceUrl(url);
  }, 20);
}

function replaceUrl(url) {
  try { window.history.replaceState(null, "", url); } catch (_) { /* file:// and sandboxes */ }
}

function buildChips() {
  for (const [group, commands] of Object.entries(EXAMPLES)) {
    const wrap = document.createElement("div");
    wrap.className = "group";
    const title = document.createElement("h3");
    title.textContent = group;
    wrap.append(title);
    for (const command of commands) {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "chip";
      chip.textContent = command;
      chip.disabled = true;
      chip.addEventListener("click", () => execute(command));
      wrap.append(chip);
    }
    els.chips.append(wrap);
  }
  document.querySelectorAll(".inline-example").forEach((button) => {
    button.addEventListener("click", () => { els.input.value = button.dataset.cmd; execute(button.dataset.cmd); });
  });
}

// --- boot ----------------------------------------------------------------
async function boot() {
  if (typeof loadPyodide !== "function") {
    throw new Error("Could not load Pyodide (are you offline?).");
  }
  setStatus("Starting Python...");
  pyodide = await loadPyodide();

  setStatus("Loading Pillow and pyfiglet...");
  await pyodide.loadPackage(["micropip", "pillow"]);
  try {
    await pyodide.pyimport("micropip").install("pyfiglet");
  } catch (error) {
    // The generator falls back to its built-in fonts without pyfiglet.
    console.warn("pyfiglet unavailable, using built-in fonts:", error);
  }

  setStatus("Loading the generator...");
  const response = await fetch("ascii_art_generator.zip");
  if (!response.ok) throw new Error("Could not download ascii_art_generator.zip");
  pyodide.unpackArchive(await response.arrayBuffer(), "zip");
  pyodide.runPython("import os; os.environ['COLUMNS'] = '100'");
  const bridge = pyodide.pyimport("ascii_art_generator.web_bridge");
  runCommand = (command) => bridge.run_command(command);

  setReady(true);
  setStatus("Ready.");
  document.body.dataset.ready = "true";

  const initial = new URL(location.href).searchParams.get("cmd");
  if (initial) execute(initial, { remember: false });
  else els.input.focus();
}

// --- events --------------------------------------------------------------
els.form.addEventListener("submit", (event) => { event.preventDefault(); execute(els.input.value); });

els.input.addEventListener("keydown", (event) => {
  if (event.key === "ArrowUp" && commandHistory.length) {
    event.preventDefault();
    historyPos = Math.max(0, historyPos - 1);
    els.input.value = commandHistory[historyPos] ?? "";
  } else if (event.key === "ArrowDown" && commandHistory.length) {
    event.preventDefault();
    historyPos = Math.min(commandHistory.length, historyPos + 1);
    els.input.value = commandHistory[historyPos] ?? "";
  }
});

// navigator.clipboard only exists in a secure context (https or localhost). Opening the page over
// plain http, for example from a phone on the local network, needs the older execCommand route.
function legacyCopy(text) {
  const area = document.createElement("textarea");
  area.value = text;
  area.setAttribute("readonly", "");
  area.style.cssText = "position:fixed;top:0;left:0;opacity:0";
  document.body.appendChild(area);
  area.select();
  area.setSelectionRange(0, text.length);
  try {
    return document.execCommand("copy");
  } finally {
    area.remove();
  }
}

// Shows a short message on the button, then puts its label back.
function flash(button, message) {
  const label = button.dataset.label ?? (button.dataset.label = button.textContent);
  button.textContent = message;
  setTimeout(() => { button.textContent = label; }, 1400);
}

async function copy(text, button, done) {
  try {
    if (navigator.clipboard) await navigator.clipboard.writeText(text);
    else if (!legacyCopy(text)) throw new Error("copy command refused");
    flash(button, done);
  } catch (_) {
    flash(button, "Copy failed");
  }
}
els.copyText.addEventListener("click", () => copy(lastText, els.copyText, "Copied"));
els.copyImage.addEventListener("click", async () => {
  const canvas = drawingCanvas(lastRaw);
  if (!canvas) { setStatus("Nothing to copy yet. Run a command first.", true); return; }
  const blob = canvasBlob(canvas);
  try {
    // The promise goes in as it is: Safari only allows the write while the click is being handled.
    await navigator.clipboard.write([new ClipboardItem({ "image/png": blob })]);
    flash(els.copyImage, "Copied");
    setStatus("Copied as an image. Paste it into the chat.");
  } catch (_) {
    // No image clipboard here (an older browser, or a page opened over plain http): save the file.
    try {
      download(await blob, "ascii-art.png");
      flash(els.copyImage, "Downloaded");
      setStatus("This browser cannot copy images, so the picture was downloaded as ascii-art.png.");
    } catch (error) {
      flash(els.copyImage, "Copy failed");
      setStatus(`Could not make the image: ${error.message || error}`, true);
    }
  }
});
els.copyLink.addEventListener("click", () => copy(location.href, els.copyLink, "Copied"));

els.imageForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = els.imageFile.files[0];
  if (!file) { setStatus("Choose an image first.", true); return; }
  setStatus("Converting...");
  const bytes = new Uint8Array(await file.arrayBuffer());
  const path = "/tmp/upload" + (file.name.match(/\.[A-Za-z0-9]+$/)?.[0] ?? "");
  pyodide.FS.writeFile(path, bytes);
  const width = Math.min(200, Math.max(10, parseInt(els.imageWidth.value, 10) || 80));
  execute(`convert image ${path} width ${width}${els.imageColor.checked ? " color" : ""}`, { remember: false });
});

buildChips();
setReady(false);
boot().catch((error) => {
  console.error(error);
  setStatus(String(error.message || error), true);
});
