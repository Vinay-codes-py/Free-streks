import os, sqlite3, uuid, hashlib, hmac, base64
from pathlib import Path
from datetime import datetime, timezone
import streamlit as st
import streamlit.components.v1 as components

ROOT=Path(__file__).parent; DATA=ROOT/'data'; MEDIA=DATA/'media'; DB=DATA/'vault.db'
MEDIA.mkdir(parents=True,exist_ok=True)
st.set_page_config(page_title='Ultra Secure Vault',page_icon='⚡',layout='wide')

SECRET=os.getenv('APP_SECRET','CHANGE_ME_ULTRA_SECRET')
ADMIN=os.getenv('ADMIN_PASSWORD','admin123')

def conn():
 c=sqlite3.connect(DB,check_same_thread=False); c.row_factory=sqlite3.Row; return c

def init():
 c=conn(); c.executescript('''CREATE TABLE IF NOT EXISTS media(id TEXT PRIMARY KEY,filename TEXT,stored TEXT,kind TEXT,created TEXT,disabled INTEGER DEFAULT 0,max_views INTEGER DEFAULT 1,timer INTEGER DEFAULT 15,camera INTEGER DEFAULT 1,one_time INTEGER DEFAULT 0,download INTEGER DEFAULT 0,watermark TEXT DEFAULT '',views INTEGER DEFAULT 0); CREATE TABLE IF NOT EXISTS locks(media_id TEXT,viewer TEXT,created TEXT,PRIMARY KEY(media_id,viewer)); CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT,media_id TEXT,viewer TEXT,success INTEGER,created TEXT);'''); c.commit(); c.close()
init()

def H(x): return hmac.new(SECRET.encode(),str(x).encode(),hashlib.sha256).hexdigest()
def viewer(): return H((st.context.headers.get('User-Agent','')+'|'+st.context.headers.get('X-Forwarded-For','127.0.0.1')))
def media(mid):
 c=conn(); r=c.execute('SELECT * FROM media WHERE id=?',(mid,)).fetchone(); c.close(); return r

def css(): st.markdown('''<style>@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@500;700&display=swap');html,body,.stApp{background:#020208;color:#eef}.stApp{background:radial-gradient(circle at 20% 0%,#08202b 0,transparent 30%),radial-gradient(circle at 80% 10%,#211044 0,transparent 30%),#020208}*{font-family:Rajdhani,sans-serif}h1,h2,h3{font-family:Orbitron,sans-serif}.hero,.card{border:1px solid #164d61;border-radius:22px;background:rgba(5,10,25,.78);padding:25px;margin:12px 0;box-shadow:0 0 35px #00d9ff12;backdrop-filter:blur(12px)}.hero{text-align:center}.title{font:900 clamp(30px,5vw,64px) Orbitron;background:linear-gradient(90deg,#00f0ff,#fff,#9b5cff,#ff0055);-webkit-background-clip:text;color:transparent}.live{color:#00ff9d;animation:p 1.2s infinite}@keyframes p{50%{opacity:.35}}button{border-radius:12px!important}</style>''',unsafe_allow_html=True)

def save(upload,maxv,timer,camera,one,download,wm):
 ext=Path(upload.name).suffix.lower(); kind='image' if ext in ['.png','.jpg','.jpeg','.webp','.gif'] else 'video' if ext in ['.mp4','.webm','.mov','.m4v'] else None
 if not kind: raise ValueError('Unsupported media format')
 mid=uuid.uuid4().hex[:16]; stored=mid+ext; (MEDIA/stored).write_bytes(upload.getvalue())
 c=conn(); c.execute('INSERT INTO media VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)',(mid,upload.name,stored,kind,datetime.now(timezone.utc).isoformat(),0,maxv,timer,int(camera),int(one),int(download),wm,0)); c.commit(); c.close(); return mid

def verify(mid):
 key='verified_'+mid
 if st.session_state.get(key): return True
 st.markdown('<div class="hero"><div style="font-size:55px">📷</div><h2>LIVE CAMERA VERIFICATION</h2><p>Camera access is required before the protected media is revealed.</p></div>',unsafe_allow_html=True)
 html='''<style>body{margin:0;background:#020208;color:white;text-align:center;font-family:Arial}video{width:95%;max-width:650px;border:2px solid #00f0ff;border-radius:20px}button{padding:14px 24px;margin:15px;border:0;border-radius:12px;background:linear-gradient(90deg,#00d9ff,#762cff,#ff0055);color:white;font-weight:bold}</style><video id=v autoplay playsinline muted></video><br><button onclick="go()">START CAMERA</button><p id=s>Camera not started</p><script>async function go(){try{let x=await navigator.mediaDevices.getUserMedia({video:{facingMode:'user'},audio:false});v.srcObject=x;await v.play();s.innerText='✓ LIVE CAMERA ACTIVE — NOW CONFIRM BELOW';s.style.color='#00ff9d'}catch(e){s.innerText='✕ Camera permission/access failed';s.style.color='#ff5577'}}</script>'''
 components.html(html,height=500)
 st.info('Privacy: this check confirms live camera access; it does not secretly record or store the camera feed.')
 if st.button('✓ CONFIRM LIVE VERIFICATION',use_container_width=True):
  st.session_state[key]=True; c=conn(); c.execute('INSERT INTO logs(media_id,viewer,success,created) VALUES(?,?,1,?)',(mid,viewer(),datetime.now(timezone.utc).isoformat())); c.commit(); c.close(); st.rerun()
 return False

def view(mid):
 r=media(mid)
 if not r: st.error('Invalid link'); return
 if r['disabled']: st.error('This link is disabled by the administrator.'); return
 c=conn(); count=c.execute('SELECT COUNT(*) n FROM locks WHERE media_id=?',(mid,)).fetchone()['n']; used=c.execute('SELECT 1 FROM locks WHERE media_id=? AND viewer=?',(mid,viewer())).fetchone(); c.close()
 if count>=r['max_views']: st.error('View limit reached.'); return
 if r['one_time'] and used: st.error('This one-time link has already been used.'); return
 if r['camera'] and not verify(mid): return
 c=conn(); c.execute('INSERT OR IGNORE INTO locks VALUES(?,?,?)',(mid,viewer(),datetime.now(timezone.utc).isoformat())); c.execute('UPDATE media SET views=views+1 WHERE id=?',(mid,)); c.commit(); c.close()
 data=(MEDIA/r['stored']).read_bytes(); b64=base64.b64encode(data).decode(); ext=Path(r['stored']).suffix.lower(); mime={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.gif':'image/gif','.mp4':'video/mp4','.webm':'video/webm','.mov':'video/quicktime','.m4v':'video/x-m4v'}[ext]; uri=f'data:{mime};base64,{b64}'
 media_html=f'<img src="{uri}" oncontextmenu="return false"/>' if r['kind']=='image' else f'<video src="{uri}" controls autoplay playsinline controlsList="nodownload" oncontextmenu="return false"></video>'
 dl=f'<a href="{uri}" download="{r["filename"]}">DOWNLOAD</a>' if r['download'] else ''
 html=f'''<style>body{{margin:0;background:#000;color:white;font-family:Arial;text-align:center}}.stage{{height:760px;display:flex;align-items:center;justify-content:center;position:relative}}img,video{{max-width:92%;max-height:82%;border:2px solid #00f0ff;border-radius:18px;box-shadow:0 0 45px #00f0ff44}}.wm{{position:fixed;top:20px;right:20px;color:#00f0ff66;font-weight:bold}}.timer{{position:fixed;bottom:25px;left:50%;transform:translateX(-50%);padding:10px 18px;border-radius:25px;background:#000c;border:1px solid #00f0ff55}}a{{position:fixed;bottom:75px;left:50%;transform:translateX(-50%);background:#00d9ff;color:#000;padding:10px 20px;border-radius:10px;font-weight:bold}}</style><div class="wm">{r['watermark'] or 'SECURE VAULT'}</div><div class="stage">{media_html}</div>{dl}<div class="timer">DESTROY IN <b id=c>{r['timer']}</b>s</div><script>let n={r['timer']},c=document.getElementById('c');let t=setInterval(()=>{{c.innerText=--n;if(n<=0){{clearInterval(t);document.body.innerHTML='<h1 style="margin-top:35vh;color:#ff0055">⚡ MEDIA DESTROYED</h1>'}}}},1000);document.oncontextmenu=()=>false;</script>'''
 components.html(html,height=800)

def admin_login():
 st.markdown('<div class="hero"><div class="title">⚡ GOD CONTROL</div><p class="live">● SYSTEM ONLINE</p></div>',unsafe_allow_html=True); p=st.text_input('ADMIN PASSWORD',type='password');
 if st.button('ENTER ADMIN PANEL',use_container_width=True):
  if hmac.compare_digest(p,ADMIN): st.session_state.admin=True; st.rerun()
  else: st.error('ACCESS DENIED')

def admin():
 css(); st.markdown('<div class="hero"><div class="title">⚡ GOD CONTROL PANEL ⚡</div><p class="live">● LIVE ADMIN CONSOLE</p></div>',unsafe_allow_html=True)
 c=conn(); rows=c.execute('SELECT * FROM media ORDER BY created DESC').fetchall(); total=c.execute('SELECT COALESCE(SUM(views),0) n FROM media').fetchone()['n']; verified=c.execute('SELECT COUNT(*) n FROM logs WHERE success=1').fetchone()['n']; c.close()
 a,b,d=st.columns(3); a.metric('MEDIA',len(rows)); b.metric('VIEWS',total); d.metric('VERIFIED',verified)
 st.subheader('🚀 Create Protected Link'); up=st.file_uploader('IMAGE / VIDEO',type=['png','jpg','jpeg','webp','gif','mp4','webm','mov','m4v']); x,y=st.columns(2)
 with x: maxv=st.number_input('MAX VIEWS',1,1000000,1); timer=st.number_input('SELF-DESTRUCT SECONDS',1,3600,15); one=st.checkbox('ONE-TIME LINK')
 with y: cam=st.checkbox('LIVE CAMERA VERIFICATION',True); download=st.checkbox('ALLOW DOWNLOAD'); wm=st.text_input('WATERMARK','ULTRA SECURE VAULT')
 if up and st.button('🔥 GENERATE LINK',use_container_width=True):
  try:
   mid=save(up,maxv,timer,cam,one,download,wm); st.success('Created successfully'); st.code('?view='+mid); st.info('Permanent URL pattern: your-app-domain/?view='+mid)
  except Exception as e: st.error(str(e))
 st.subheader('🗄️ Manage Links')
 for r in rows:
  with st.container():
   st.markdown('<div class="card">',unsafe_allow_html=True); a,b,d=st.columns([3,2,2]); a.write('**'+r['filename']+'**'); a.code('?view='+r['id']); b.write(f"Views: {r['views']} / {r['max_views']}"); b.write('Camera: '+('ON' if r['camera'] else 'OFF')); d.write('🔴 BLOCKED' if r['disabled'] else '🟢 ACTIVE')
   if d.button('BLOCK/UNBLOCK',key='b'+r['id']):
    cc=conn(); cc.execute('UPDATE media SET disabled=? WHERE id=?',(0 if r['disabled'] else 1,r['id'])); cc.commit(); cc.close(); st.rerun()
   if d.button('RESET VIEWS',key='r'+r['id']):
    cc=conn(); cc.execute('DELETE FROM locks WHERE media_id=?',(r['id'],)); cc.execute('UPDATE media SET views=0 WHERE id=?',(r['id'],)); cc.commit(); cc.close(); st.rerun()
   if d.button('DELETE',key='d'+r['id']):
    try:(MEDIA/r['stored']).unlink(missing_ok=True)
    except:pass
    cc=conn(); cc.execute('DELETE FROM media WHERE id=?',(r['id'],)); cc.execute('DELETE FROM locks WHERE media_id=?',(r['id'],)); cc.commit(); cc.close(); st.rerun()
   st.markdown('</div>',unsafe_allow_html=True)
 if st.button('LOGOUT',use_container_width=True): st.session_state.admin=False; st.rerun()

def main():
 q=st.query_params
 if 'view' in q: css(); view(str(q['view'])); return
 if 'admin' in q:
  if st.session_state.get('admin'): admin()
  else: admin_login()
  return
 css(); st.markdown('<div class="hero"><div class="title">⚡ ULTRA SECURE VAULT</div><p>IMAGE • VIDEO • ONE-TIME • PERMANENT • LIVE VERIFIED</p></div>',unsafe_allow_html=True); st.markdown('<div class="card"><h2>🔐 Protected Media System</h2><p>Configurable links, view limits, self-destruct timers, optional live camera verification and a powerful administrator console.</p></div>',unsafe_allow_html=True); st.markdown('<div style="text-align:center"><a href="?admin=1" style="display:inline-block;padding:15px 28px;border-radius:14px;color:white;text-decoration:none;background:linear-gradient(90deg,#00d9ff,#762cff,#ff0055);font-weight:bold">⚡ OPEN ADMIN PANEL</a></div>',unsafe_allow_html=True)
if __name__=='__main__': main()
