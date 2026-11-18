# نشر زلطن تريبول

المستودع: https://github.com/ansbnabwsby-hue/Zliten-Tripoli

## النشر التلقائي

كل Push إلى فرع `main` يشغل GitHub Actions ويبني ملفات الويب وPWA ثم ينشرها إلى Firebase Hosting.

أضف في GitHub Repository → Settings → Secrets and variables → Actions → New repository secret السر التالي:

- الاسم: `FIREBASE_SERVICE_ACCOUNT_ZLITEN_TRIPOL`
- القيمة: JSON لحساب خدمة Firebase يملك صلاحية Firebase Hosting Admin في مشروع `zliten-tripol`.

لا تضع هذا JSON داخل الكود أو داخل APK.

## النطاق

بعد أول نشر افتح Firebase Console → Hosting → Add custom domain. أضف النطاق المطلوب، ثم انسخ سجلات DNS التي تعرضها Firebase إلى مزود النطاق. لا يمكن إكمال التحقق من النطاق دون التحكم في DNS.

سيكون نطاق Firebase الافتراضي عادةً:

- `https://zliten-tripol.web.app`
- `https://zliten-tripol.firebaseapp.com`

بعد استخدام نطاق مخصص، أضفه أيضًا في Firebase Console → Authentication → Settings → Authorized domains حتى يعمل تسجيل الدخول منه.

## PWA

يتم نشر `manifest.webmanifest` و`sw.js` والأيقونات المحلية. التطبيق يدعم التثبيت على الهاتف، التخزين المؤقت للواجهة، والعمل جزئيًا دون اتصال. بيانات Firebase نفسها تحتاج اتصالًا بالإنترنت.
