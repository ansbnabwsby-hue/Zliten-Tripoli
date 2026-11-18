from pathlib import Path
p=Path('/home/ubuntu/zlitenapp/index.html')
s=p.read_text()

s=s.replace('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">\n<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIINfQ3q4t8X2Jf5p5Xz1Jb1c7l5D8wZ5c=" crossorigin="">')
s=s.replace('<script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>', '<script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>\n<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2q5E0nN7S9qB4i1S1Z0w0M=" crossorigin=""></script>')

css='''\n.live-map-card { padding:14px; }\n.live-map { height:260px; width:100%; border-radius:16px; overflow:hidden; background:#0b1730; border:1px solid var(--border); }\n.live-map .leaflet-control-attribution { font-size:9px; }\n.live-location-status { display:flex;align-items:center;gap:8px;margin-bottom:10px;color:var(--text-muted);font-size:.8rem; }\n.live-dot { width:9px;height:9px;border-radius:50%;background:var(--success);box-shadow:0 0 0 4px rgba(46,204,113,.14); }\n.live-dot.waiting { background:var(--warning);box-shadow:0 0 0 4px rgba(243,156,18,.14); }\n.live-privacy { margin-top:9px;color:var(--text-muted);font-size:.72rem;line-height:1.6; }\n'''
if '.live-map-card' not in s:
    s=s.replace('</style>', css+'\n</style>',1)

s=s.replace("let isLightTheme = localStorage.getItem('z_theme') === 'light';", "let isLightTheme = localStorage.getItem('z_theme') === 'light';\nlet activeLocationWatchId = null, activeLocationOrderId = null, liveLocationRef = null, liveLocationListener = null;\nlet liveMap = null, liveMarker = null, liveMapOrderId = null;")

s=s.replace("function logout() {\n    localStorage.removeItem", "function logout() {\n    stopLiveLocationTracking(true);\n    localStorage.removeItem",1)

insert_before='// ==================== تتبع الطلب ===================='
tracking=r'''// ==================== التتبع الحي لموقع السائق ====================
function stopLiveLocationTracking(removeRemote) {
    if (activeLocationWatchId !== null && navigator.geolocation) {
        navigator.geolocation.clearWatch(activeLocationWatchId);
    }
    activeLocationWatchId = null;
    activeLocationOrderId = null;
    if (liveLocationRef && liveLocationListener) liveLocationRef.off('value', liveLocationListener);
    liveLocationRef = null;
    liveLocationListener = null;
    if (removeRemote && liveMapOrderId) database.ref('liveLocations/' + liveMapOrderId).remove().catch(function(){});
}

function formatLocationTime(value) {
    if (!value) return 'بانتظار موقع السائق';
    try { return 'آخر تحديث: ' + new Date(value).toLocaleTimeString('ar-LY'); } catch(e) { return 'تم تحديث الموقع'; }
}

function updateLiveMap(location) {
    if (!location || !location.lat || !location.lng) return;
    var point = [Number(location.lat), Number(location.lng)];
    if (liveMarker) liveMarker.setLatLng(point);
    else if (liveMap) liveMarker = L.marker(point).addTo(liveMap).bindPopup('موقع السائق');
    if (liveMap) {
        if (!liveMap._hasDriverLocation) { liveMap.setView(point, 16); liveMap._hasDriverLocation = true; }
        else liveMap.panTo(point, { animate:true, duration:.5 });
    }
    var status = document.getElementById('live-location-status');
    if (status) status.innerHTML = '<span class="live-dot"></span><span>السائق متصل • ' + formatLocationTime(location.updatedAt) + (location.accuracy ? ' • دقة ' + Math.round(location.accuracy) + 'م' : '') + '</span>';
}

function initLiveMap(orderId, isDriver) {
    var holder = document.getElementById('live-map-' + orderId);
    if (!holder || typeof L === 'undefined') return;
    if (liveMap) { liveMap.remove(); liveMap = null; liveMarker = null; }
    liveMapOrderId = orderId;
    liveMap = L.map(holder, { zoomControl:true, attributionControl:true }).setView([32.467, 14.568], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom:19, attribution:'© OpenStreetMap' }).addTo(liveMap);
    if (isDriver) {
        var status = document.getElementById('live-location-status');
        if (status) status.innerHTML = '<span class="live-dot waiting"></span><span>جاري طلب إذن الموقع من الهاتف...</span>';
    }
    setTimeout(function(){ if (liveMap) liveMap.invalidateSize(); }, 250);
}

function startDriverLocationSharing(orderId) {
    if (!navigator.geolocation) {
        var status = document.getElementById('live-location-status');
        if (status) status.innerHTML = '<span class="live-dot waiting"></span><span>الموقع غير مدعوم على هذا الجهاز</span>';
        return;
    }
    if (activeLocationOrderId === orderId && activeLocationWatchId !== null) return;
    stopLiveLocationTracking(false);
    activeLocationOrderId = orderId;
    activeLocationWatchId = navigator.geolocation.watchPosition(function(pos) {
        var payload = { lat: pos.coords.latitude, lng: pos.coords.longitude, accuracy: pos.coords.accuracy || null, updatedAt: Date.now(), driverId: currentUser.id, driverName: currentUser.name };
        database.ref('liveLocations/' + orderId).set(payload).catch(function(){ showToast('تعذر تحديث موقعك حالياً', 'error', 2500); });
        updateLiveMap(payload);
    }, function() {
        var status = document.getElementById('live-location-status');
        if (status) status.innerHTML = '<span class="live-dot waiting"></span><span>يرجى السماح للتطبيق بالوصول إلى موقعك</span>';
    }, { enableHighAccuracy:true, maximumAge:5000, timeout:15000 });
}

function subscribeToDriverLocation(orderId) {
    if (liveLocationRef && liveLocationListener) liveLocationRef.off('value', liveLocationListener);
    liveLocationRef = database.ref('liveLocations/' + orderId);
    liveLocationListener = function(snapshot) {
        var location = snapshot.val();
        updateLiveMap(location);
        var status = document.getElementById('live-location-status');
        if (!location && status) status.innerHTML = '<span class="live-dot waiting"></span><span>بانتظار مشاركة موقع السائق...</span>';
    };
    liveLocationRef.on('value', liveLocationListener);
}

'''
if 'function startDriverLocationSharing' not in s:
    s=s.replace(insert_before, tracking+insert_before,1)

# Add live map card before chat card.
old="""        (order.deliveryProof ? '<div style=\"margin-top:10px;\"><b>📸 إثبات التسليم:</b><br><img src=\"' + order.deliveryProof + '\" style=\"max-width:100%;border-radius:12px;margin-top:8px;\"></div>' : '') +
        '</div>' +
        '<div class=\"card\">' +"""
new="""        (order.deliveryProof ? '<div style=\"margin-top:10px;\"><b>📸 إثبات التسليم:</b><br><img src=\"' + order.deliveryProof + '\" style=\"max-width:100%;border-radius:12px;margin-top:8px;\"></div>' : '') +
        '</div>' +
        (driver && !step4 ? '<div class=\"card live-map-card\"><h4 style=\"margin-bottom:8px;\">📍 موقع السائق مباشرة</h4><div id=\"live-location-status\" class=\"live-location-status\"><span class=\"live-dot waiting\"></span><span>جاري الاتصال بموقع السائق...</span></div><div id=\"live-map-' + order.id + '\" class=\"live-map\"></div><div class=\"live-privacy\">يتم تحديث الموقع أثناء التوصيل فقط، ويتوقف تلقائياً بعد إتمام الطلب.</div></div>' : '') +
        '<div class=\"card\">' +"""
if old not in s: raise SystemExit('tracking card anchor not found')
s=s.replace(old,new,1)

# Add initialization before existing chat scroll timeout.
old2="""    setTimeout(function() { let box = document.getElementById('track-chat-box'); if(box) box.scrollTop = box.scrollHeight; }, 100);
}"""
new2="""    if (driver && !step4) {
        setTimeout(function() {
            initLiveMap(orderId, isDriver);
            if (isDriver) startDriverLocationSharing(orderId); else subscribeToDriverLocation(orderId);
        }, 120);
    } else {
        if (liveLocationRef && liveLocationListener) liveLocationRef.off('value', liveLocationListener);
    }
    setTimeout(function() { let box = document.getElementById('track-chat-box'); if(box) box.scrollTop = box.scrollHeight; }, 100);
}"""
if old2 not in s: raise SystemExit('tracking tail anchor not found')
s=s.replace(old2,new2,1)

# Stop sharing and remove live record on delivery.
s=s.replace("order.status = 'تم التسليم ✅';\n        order.deliveryProof", "order.status = 'تم التسليم ✅';\n        stopLiveLocationTracking(true);\n        database.ref('liveLocations/' + oid).remove().catch(function(){});\n        order.deliveryProof",1)

p.write_text(s)
print('live tracking added')
