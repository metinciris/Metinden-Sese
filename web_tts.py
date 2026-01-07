import os
import re
import uuid
import subprocess
from datetime import datetime
from pathlib import Path

import numpy as np
import soundfile as sf

from flask import Flask, request, send_from_directory, jsonify, render_template_string

BASE = Path(__file__).parent.resolve()

MODEL_PATH = BASE / "tr_TR-dfki-medium.onnx"

OUT_DIR = BASE / "outputs"
OUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8"/>
<title>Lokal TTS (Piper)</title>
<style>
body{font-family:system-ui;max-width:900px;margin:30px auto;padding:0 16px}
textarea{width:100%;height:220px;font-size:16px;padding:12px}
.row{display:flex;gap:12px;flex-wrap:wrap;margin:12px 0}
label{user-select:none}
button{padding:10px 14px;font-size:16px}
.box{background:#f6f6f6;padding:12px;border-radius:10px}
audio{width:100%}
</style>
</head>
<body>

<h2>Lokal TTS (Piper)</h2>

<textarea id="text">Merhaba. Bu ses Piper ile yerel üretiliyor.</textarea>

<div class="row">
<input id="name" placeholder="dosya adı (opsiyonel)">
<label><input id="ts" type="checkbox" checked> zaman damgası</label>
</div>

<div class="row">
<label><input id="fast" type="checkbox"> hızlı</label>
<label><input id="slow" type="checkbox"> yavaş</label>
<label><input id="calm" type="checkbox"> sakin</label>
<label><input id="lively" type="checkbox"> canlı</label>
<label><input id="quiet" type="checkbox"> sesi azalt</label>
</div>

<div class="row">
<button onclick="go(false)">Üret + Çal</button>
<button onclick="go(true)">Üret + İndir</button>
</div>

<div class="box" id="status">Hazır</div>
<audio id="player" controls style="display:none"></audio>

<script>
async function go(download){
  const body={
    text: text.value,
    name: name.value,
    timestamp: ts.checked,
    download,
    opts:{
      fast:fast.checked,
      slow:slow.checked,
      calm:calm.checked,
      lively:lively.checked,
      quiet:quiet.checked
    }
  };

  status.innerText="Üretiliyor...";
  player.style.display="none";

  const r=await fetch("/tts",{method:"POST",headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  if(!r.ok){status.innerText="Hata";return;}

  if(download){
    const b=await r.blob();
    const a=document.createElement("a");
    a.href=URL.createObjectURL(b);
    a.download="ses.wav";
    a.click();
    return;
  }

  const j=await r.json();
  player.src=j.url+"?v="+Date.now();
  player.style.display="block";
  player.play();
  status.innerText="Çalıyor";
}
</script>

</body>
</html>
"""

def safe_filename(name):
    name = re.sub(r"[^\w\-ğüşöçıİĞÜŞÖÇı]+", "_", name or "", flags=re.UNICODE)
    return name.strip("_")[:80]

def out_name(base, ts):
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base}_{t}.wav" if base else f"tts_{t}.wav"

def reduce_volume(path, factor=0.7):
    data, sr = sf.read(path, dtype="float32")
    data *= factor
    sf.write(path, data, sr)

def piper(text, out, ls, ns, nws):
    subprocess.run([
        os.sys.executable, "-m", "piper",
        "-m", str(MODEL_PATH),
        "-f", str(out),
        "--length_scale", str(ls),
        "--noise_scale", str(ns),
        "--noise_w_scale", str(nws),
        "--", text
    ], check=True)

@app.get("/")
def index():
    return render_template_string(HTML)

@app.post("/tts")
def tts():
    d = request.json
    text = d["text"].strip()
    if not text:
        return "Boş", 400

    name = safe_filename(d.get("name", ""))
    fname = out_name(name, d.get("timestamp", True))
    out = OUT_DIR / fname

    o = d.get("opts", {})
    ls = 0.85 if o.get("fast") else 1.25 if o.get("slow") else 1.0
    ns, nws = (0.6, 0.7) if o.get("calm") else (0.85, 0.9) if o.get("lively") else (0.67, 0.8)

    piper(text, out, ls, ns, nws)

    if o.get("quiet"):
        reduce_volume(out)

    if d.get("download"):
        return send_from_directory(OUT_DIR, out.name, as_attachment=True)

    return jsonify({"url": f"/audio/{out.name}"})

@app.get("/audio/<f>")
def audio(f):
    return send_from_directory(OUT_DIR, f)
    
if __name__=="__main__":
    app.run("127.0.0.1",5000)
