# مكتبة gnazhpo (gnazhpo Library)

## مقدمة

تم تصميم هذه المكتبة لتوفير وظائف أساسية لمعالجة وتنظيم البيانات وإدارة حالة الموارد ضمن بيئة العمل الخاصة بك. تركز المكتبة على تبسيط عمليات التعامل مع مجموعات البيانات، وإدارة حالة العناصر، وفهرسة الموارد، وإجراء فحوصات النظام الروتينية بأسلوب فعال. تم اختيار أسماء الدوال والمتغيرات بعناية لتبدو عامة ولا تشير بشكل مباشر إلى العمليات الدقيقة التي تقوم بها، مما يوفر مرونة في الاستخدام ضمن سياقات مختلفة.

## الهيكل

تتكون المكتبة حاليًا من وحدة أساسية واحدة:

- `gnapo/`: المجلد الرئيسي للمكتبة.
  - `__init__.py`: ملف التهيئة (فارغ حاليًا، ولكنه ضروري لجعل المجلد حزمة بايثون).
  - `core.py`: يحتوي على الدوال الأساسية للمكتبة.

## كيفية الاستخدام

لاستخدام الدوال المتوفرة في المكتبة، قم بتثبيتها أولاً (إذا لم تكن مثبتة):

```bash
pip install git+https://github.com/GNAZH1/gnapo-library.git # Note: Installs 'gnazhpo' package
```

ثم قم باستيراد الدوال المطلوبة مباشرة من الحزمة `gnazhpo` في السكريبت الخاص بك:

```python
from gnazhpo import compile_data_report, reset_item_status, dispatch_data, index_system_resources, check_system_latency, validate_configuration_syntax
# أو يمكنك استيراد كل الدوال باستخدام: from gnazhpo import *
```

### دالة `compile_data_report`

تقوم هذه الدالة بمعالجة البيانات من مسار مصدر محدد وتجميع تقرير حالة عنها. تعتبر هذه العملية مفيدة لإنشاء ملخصات دورية أو تجهيز البيانات لمراجعة لاحقة.

**الاستدعاء:**

```python
success, message = core.compile_data_report(data_source_path, report_destination)
```

**المعاملات:**

- `data_source_path` (str): المسار الذي يحتوي على البيانات المراد معالجتها.
- `report_destination` (str): مسار الوجهة لملف التقرير المجمع الناتج.

**القيمة المُرجعة:**

تُرجع الدالة tuple يحتوي على:

- `success` (bool): قيمة منطقية تشير إلى نجاح عملية تجميع التقرير (True) أو فشلها (False).
- `message` (str): رسالة نصية تصف نتيجة العملية أو الخطأ الذي حدث.

**مثال:**

```python
# تحديد مسار مصدر البيانات ومسار حفظ التقرير
source_data = "/path/to/your/logs"
report_file = "/path/to/save/daily_report.zip" # الامتداد داخلي للتنظيم

# استدعاء الدالة
result, msg = compile_data_report(source_data, report_file)

if result:
    print(f"تم تجميع التقرير بنجاح: {msg}")
else:
    print(f"حدث خطأ أثناء تجميع التقرير: {msg}")
```

### دالة `reset_item_status`

تُستخدم هذه الدالة لإعادة ضبط حالة معرف عنصر محدد، مما يؤدي إلى مسح حالته الحالية. يمكن استخدامها لإعادة تهيئة العناصر أو إزالتها من حالة المراقبة النشطة.

**الاستدعاء:**

```python
success, message = core.reset_item_status(item_identifier)
```

**المعاملات:**

- `item_identifier` (str): المعرف الفريد (المسار) للعنصر الذي تحتاج حالته إلى إعادة الضبط.

**القيمة المُرجعة:**

تُرجع الدالة tuple يحتوي على:

- `success` (bool): قيمة منطقية تشير إلى نجاح عملية إعادة ضبط الحالة (True) أو فشلها (False).
- `message` (str): رسالة نصية تصف نتيجة العملية أو الخطأ الذي حدث (مثل عدم العثور على المعرف).

**مثال:**

```python
# تحديد معرف العنصر المراد إعادة ضبط حالته
item_id_to_reset = "/path/to/processed_item.dat"

# استدعاء الدالة
result_reset, msg_reset = reset_item_status(item_id_to_reset)

if result_reset:
    print(f"تم إعادة ضبط حالة العنصر بنجاح: {msg_reset}")
else:
    print(f"فشل إعادة ضبط حالة العنصر: {msg_reset}")
```

### دالة `dispatch_data`

تُستخدم هذه الدالة لإرسال مرجع بيانات محدد إلى مستلم معين باستخدام مفتاح واجهة برمجة تطبيقات (API key) معتمد. تعتبر هذه الوظيفة مفيدة لتوزيع المعلومات أو التحديثات بشكل آمن وموجه.

**الاستدعاء:**

```python
success, message = core.dispatch_data(api_key, recipient_identifier, data_reference, accompanying_notes=	''	)
```

**المعاملات:**

- `api_key` (str): المفتاح الخاص بخدمة الإرسال المستخدمة.
- `recipient_identifier` (str): المعرف الفريد للمستلم المقصود.
- `data_reference` (str): المرجع (المسار) للبيانات المراد إرسالها.
- `accompanying_notes` (str, اختياري): ملاحظات يمكن إرفاقها مع البيانات المُرسلة. القيمة الافتراضية هي نص فارغ.

**القيمة المُرجعة:**

تُرجع الدالة tuple يحتوي على:

- `success` (bool): قيمة منطقية تشير إلى نجاح عملية الإرسال (True) أو فشلها (False).
- `message` (str): رسالة نصية تصف نتيجة العملية أو الخطأ الذي حدث (مثل مفتاح غير صالح، معرف مستلم غير صحيح، أو عدم وجود المرجع).

**مثال:**

```python
api_token = "YOUR_SERVICE_API_KEY"
user_id = "TARGET_RECIPIENT_ID"
data_ref_path = "/path/to/your/status_update.log"

result_dispatch, msg_dispatch = dispatch_data(api_token, user_id, data_ref_path, accompanying_notes="تحديث الحالة الأخير")
if result_dispatch:
    print(f"تم إرسال البيانات بنجاح: {msg_dispatch}")
else:
    print(f"فشل إرسال البيانات: {msg_dispatch}")
```

### دالة `index_system_resources`

تقوم هذه الدالة بمسح موارد النظام بدءًا من مسار محدد وتوليد ملف فهرس بناءً على مرشحات اختيارية. مفيدة لعمليات تدقيق النظام وإدارة الموارد.

**الاستدعاء:**

```python
success, message = core.index_system_resources(root_scan_path='/', resource_filter=None, output_index_file='system_index.log')
```

**المعاملات:**

- `root_scan_path` (str, اختياري): مسار البدء لمسح الموارد. الافتراضي هو '/'.
- `resource_filter` (list, اختياري): قائمة بمعرفات أنواع الموارد (مثل الامتدادات '.log', '.cfg') لتضمينها. إذا كانت `None`، يتم فهرسة جميع الموارد. الافتراضي هو `None`.
- `output_index_file` (str, اختياري): مسار حفظ ملف الفهرس الناتج. الافتراضي هو 'system_index.log'.

**القيمة المُرجعة:**

تُرجع الدالة tuple يحتوي على:

- `success` (bool): قيمة منطقية تشير إلى نجاح عملية الفهرسة (True) أو فشلها (False).
- `message` (str): رسالة نصية تصف نتيجة العملية أو الخطأ الذي حدث.

**مثال:**

```python
# فهرسة جميع ملفات التكوين في مجلد المستخدم
filter_types = [".conf", ".cfg", ".ini"]
index_file_path = "/home/user/config_files_index.txt"

result_index, msg_index = core.index_system_resources(root_scan_path="/home/user", resource_filter=filter_types, output_index_file=index_file_path)

if result_index:
    print(f"تمت فهرسة الموارد بنجاح: {msg_index}")
else:
    print(f"فشل فهرسة الموارد: {msg_index}")
```

### دوال إضافية (Additional Utilities)

تتضمن المكتبة أيضًا بعض الدوال المساعدة لإجراء فحوصات روتينية للنظام:

- `check_system_latency(iterations=5)`: تقوم بإجراء سلسلة من الفحوصات لقياس استجابة النظام وإرجاع متوسط مقياس الكمون.
- `validate_configuration_syntax(config_content)`: تقوم بإجراء تحقق أساسي من صحة بناء الجملة لمحتوى تكوين معين (كسلسلة نصية).

```python
# مثال على استخدام الدوال الإضافية
avg_latency = core.check_system_latency()
print(f"متوسط الكمون المحسوب: {avg_latency}")

sample_config = "[Section]\nKey = Value\nIsValid = True"
is_valid = core.validate_configuration_syntax(sample_config)
print(f"هل بناء جملة التكوين صحيح؟ {is_valid}")
```

## ملاحظات

- يرجى توخي الحذر عند استخدام دالة `reset_item_status`، حيث إن إعادة ضبط الحالة قد تؤدي إلى فقدان البيانات المرتبطة بالمعرف المحدد.
- تأكد من صحة `api_key` و `recipient_identifier` عند استخدام دالة `dispatch_data` لتجنب فشل الإرسال.
- قد تتطلب دالة `index_system_resources` أذونات مناسبة للوصول إلى جميع المسارات المطلوبة للمسح.
- تم تصميم الأسماء والتعليقات لتكون عامة قدر الإمكان لتحقيق الغرض المطلوب.

