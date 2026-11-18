# القواعد النهائية المقترحة لـ Firebase

الملف `firebase.database.rules.final.json` هو البديل الآمن للقواعد الحالية المفتوحة:

```json
{
  "rules": {
    ".read": false,
    ".write": false,
    "appData": {
      ".read": "auth != null",
      ".write": "auth != null && (auth.token.developer === true || auth.token.admin === true)"
    }
  }
}
```

## قبل التطبيق

القواعد الحالية للتطبيق تعتمد على تسجيل دخول مخصص داخل JavaScript، وليست Firebase Authentication. لذلك لا يوجد حاليًا `auth.uid` أو `auth.token.developer` داخل Firebase.

إذا طبقت القواعد النهائية الآن مباشرة، فسيتم منع النسخة الحالية من قراءة وكتابة `appData` حتى يتم تفعيل Firebase Authentication وترحيل الدخول إليها. هذا أفضل أمنيًا، لكنه سيوقف عمليات الطلبات القديمة مؤقتًا.

## طريقة التطبيق الصحيحة

1. من Firebase Console افتح Realtime Database ثم Rules.
2. احتفظ بنسخة من القواعد الحالية قبل التغيير.
3. فعّل Firebase Authentication.
4. أنشئ حسابات المستخدمين عبر Firebase Authentication.
5. امنح حساب المطور Custom Claim باسم `developer: true` من خادم موثوق أو Firebase Admin SDK، وليس من التطبيق.
6. الصق محتوى `firebase.database.rules.final.json` في صفحة Rules.
7. اختبر القراءة والكتابة من Rules Simulator قبل اعتماد القواعد.

## ملاحظة عن appData

بما أن التطبيق الحالي يكتب كامل `appData` دفعة واحدة، لا يمكن إعطاء الزبون أو التاجر صلاحية كتابة جزئية آمنة داخل هذا المسار. لذلك القواعد النهائية تجعل كتابة `appData` للمطور/المشرف فقط. الإطلاق الآمن الكامل يحتاج نقل البيانات إلى مسارات منفصلة مثل `orders/{orderId}` و`users/{uid}` مع Firebase Authentication.

أما `liveLocations/{orderId}` فأضيفت له حماية المشاركين: السائق صاحب الموقع، الزبون، التاجر المرتبط بالطلب، أو المطور فقط.
