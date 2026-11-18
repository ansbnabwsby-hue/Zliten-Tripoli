from pathlib import Path
p = Path('/home/ubuntu/zlitenapp/index.html')
s = p.read_text()

css = r'''
/* ===== تحسينات المرحلة الأولى: الدخول والتوصيل ===== */
.auth-modern { margin-top:24px; padding:0; overflow:hidden; border:1px solid rgba(0,212,255,.28); background:linear-gradient(160deg,rgba(17,25,54,.98),rgba(6,8,24,.98)); }
.auth-hero { padding:28px 22px 24px; text-align:center; background:radial-gradient(circle at 50% 0%,rgba(0,212,255,.24),transparent 62%),linear-gradient(135deg,#101d4a,#071126); }
.auth-logo-modern { width:82px;height:82px;border-radius:27px;margin:0 auto 15px;display:flex;align-items:center;justify-content:center;font-size:2.7rem;background:var(--gradient-1);box-shadow:0 12px 30px rgba(0,212,255,.3); }
.auth-hero h2 { font-size:1.75rem; margin-bottom:5px; color:#fff; }
.auth-hero p { color:#b6c7df; font-size:.88rem; }
.auth-form { padding:20px 20px 22px; }
.auth-label { display:flex;align-items:center;gap:7px;color:#a9b8d1;font-size:.8rem;margin-top:9px; }
.auth-input-wrap { position:relative; }
.auth-input-wrap i { position:absolute;right:16px;top:50%;transform:translateY(-50%);color:var(--primary); }
.auth-input-wrap input { padding-right:45px; }
.auth-type-title { color:#a9b8d1;font-size:.8rem;margin-top:12px; }
.auth-types { display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:8px 0 15px; }
.auth-type { padding:11px 5px;border:1px solid var(--border);border-radius:13px;text-align:center;color:var(--text-muted);cursor:pointer;font-size:.75rem;transition:.2s; }
.auth-type.active { border-color:var(--primary);background:rgba(0,212,255,.12);color:var(--primary);box-shadow:0 0 0 2px rgba(0,212,255,.08); }
.auth-type i { display:block;font-size:1.25rem;margin-bottom:4px; }
.auth-hint { text-align:center;color:var(--text-muted);font-size:.74rem;margin-top:12px;line-height:1.7; }
.delivery-head { display:flex;justify-content:space-between;align-items:center;gap:10px;margin-bottom:14px; }
.delivery-head h3 { margin:0; }
.driver-online { display:flex;align-items:center;gap:7px;padding:7px 10px;border-radius:20px;background:rgba(46,204,113,.12);color:var(--success);font-size:.75rem; }
.driver-online.off { background:rgba(139,155,180,.12);color:var(--text-muted); }
.delivery-section-title { display:flex;align-items:center;justify-content:space-between;margin:22px 0 10px; }
.delivery-section-title h4 { margin:0; }
.delivery-order-card { border-right:3px solid var(--primary); }
.delivery-order-card.available { border-right-color:var(--warning); }
.delivery-meta { display:flex;flex-wrap:wrap;gap:7px;margin:10px 0;color:var(--text-muted);font-size:.78rem; }
.delivery-meta span { background:rgba(255,255,255,.05);padding:5px 8px;border-radius:8px; }
.delivery-actions { display:flex;gap:8px;flex-wrap:wrap;margin-top:12px; }
.delivery-actions .btn { flex:1;min-width:110px; }
.cash-card { background:linear-gradient(135deg,#067fa1,#07527f); }
@media(max-width:400px){.auth-types{gap:5px}.auth-type{font-size:.68rem}.delivery-actions .btn{min-width:0;padding:9px 10px}}
'''
marker = '  </style>'
if '/* ===== تحسينات المرحلة الأولى' not in s:
    s = s.replace(marker, css + '\n' + marker, 1)

start = s.index('function renderAuth() {')
end = s.index('\nfunction handleAuth() {', start)
new_auth = r'''function renderAuth() {
    document.getElementById('app-content').innerHTML =
        '<div class="animate-fade">' +
        '<div class="card auth-modern">' +
        '<div class="auth-hero"><div class="auth-logo-modern">⚡</div>' +
        '<h2>زلطن تريبول</h2><p>سوقك المحلي في مكان واحد</p></div>' +
        '<div class="auth-form">' +
        '<div class="auth-label"><i class="fas fa-user"></i> الاسم الكامل</div>' +
        '<div class="auth-input-wrap"><i class="fas fa-user"></i><input id="auth-name" placeholder="اكتب اسمك هنا" autocomplete="name"></div>' +
        '<div class="auth-label"><i class="fas fa-lock"></i> كلمة المرور</div>' +
        '<div class="auth-input-wrap"><i class="fas fa-lock"></i><input id="auth-pass" type="password" placeholder="4 أحرف على الأقل" autocomplete="current-password"></div>' +
        '<div class="auth-label"><i class="fas fa-phone"></i> رقم الهاتف <small>(اختياري)</small></div>' +
        '<div class="auth-input-wrap"><i class="fas fa-phone"></i><input id="auth-phone" inputmode="tel" placeholder="09xxxxxxxx"></div>' +
        '<div class="auth-type-title">كيف ستستخدم التطبيق؟</div>' +
        '<div class="auth-types">' +
        '<div class="auth-type active" data-auth-type="customer" onclick="selectAuthType(this,\'customer\')"><i class="fas fa-user"></i>زبون</div>' +
        '<div class="auth-type" data-auth-type="store_owner" onclick="selectAuthType(this,\'store_owner\')"><i class="fas fa-store"></i>تاجر</div>' +
        '<div class="auth-type" data-auth-type="driver" onclick="selectAuthType(this,\'driver\')"><i class="fas fa-motorcycle"></i>سائق</div>' +
        '</div><input type="hidden" id="auth-type" value="customer">' +
        '<button class="btn btn-primary btn-lg" onclick="handleAuth()"><i class="fas fa-arrow-left"></i> دخول أو إنشاء حساب</button>' +
        '<button class="btn btn-ghost btn-sm" style="margin-top:10px" onclick="showPolicy()"><i class="fas fa-shield-alt"></i> سياسة الاستخدام والخصوصية</button>' +
        '<div class="auth-hint">بتسجيل الدخول أنت توافق على شروط استخدام زلطن تريبول<br>📍 زلطن - ليبيا</div>' +
        '</div></div></div>';
}

function selectAuthType(el, type) {
    document.querySelectorAll('.auth-type').forEach(function(x){ x.classList.remove('active'); });
    el.classList.add('active');
    var input = document.getElementById('auth-type'); if (input) input.value = type;
}
'''
s = s[:start] + new_auth + s[end:]

# Improve driver render with a modern wrapper while retaining all original actions.
s = s.replace("'<div class=\"wallet-card\"><div class=\"wallet-label\">💰 الكاش المجمع</div><div class=\"wallet-balance\">' + (currentUser.cashCollected || 0) + ' د.ل</div></div>'", "'<div class=\"wallet-card cash-card\"><div class=\"wallet-label\">💰 الكاش المجمع</div><div class=\"wallet-balance\">' + (currentUser.cashCollected || 0) + ' د.ل</div><div style=\"font-size:.75rem;opacity:.85\">المبلغ الذي تم تحصيله من الطلبات المسلّمة</div></div>'")
s = s.replace("'<div class=\"animate-fade\">' +\n        '<div class=\"wallet-card cash-card\"", "'<div class=\"animate-fade\">' +\n        '<div class=\"delivery-head\"><h3>🛵 مركز التوصيل</h3><span class=\"driver-online\"><i class=\"fas fa-circle\" style=\"font-size:.55rem\"></i> متاح لاستلام الطلبات</span></div>' +\n        '<div class=\"wallet-card cash-card\"")
s = s.replace("'<div class=\"card\">' +\n                '<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;\">' +\n                '<b>' + o.userName", "'<div class=\"card delivery-order-card\">' +\n                '<div style=\"display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;\">' +\n                '<b>' + o.userName", 1)
# Add delivery meta line after location for first task block only.
s = s.replace("'<div style=\"color:var(--text-muted);font-size:0.85rem;\">📞 ' + o.phone + '</div>' +", "'<div class=\"delivery-meta\"><span>📞 ' + o.phone + '</span><span>💰 ' + (o.total || 0) + ' د.ل</span><span>📦 ' + o.items.length + ' منتجات</span></div>' +", 1)
# Available card styling (second occurrence in available map)
s = s.replace("return '<div class=\"card\">' +\n                '<div style=\"display:flex;justify-content:space-between;align-items:center;\">'", "return '<div class=\"card delivery-order-card available\">' +\n                '<div style=\"display:flex;justify-content:space-between;align-items:center;\">", 1)
# Make delivery controls grouped visually.
s = s.replace("'<div style=\"display:flex;gap:8px;margin-top:10px;flex-wrap:wrap;\">' +", "'<div class=\"delivery-actions\">' +", 1)

p.write_text(s)
print('phase1 patched', len(s), 'bytes')
