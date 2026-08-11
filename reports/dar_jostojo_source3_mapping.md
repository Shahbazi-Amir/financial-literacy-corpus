# Dar Jostojo — Final-C vs 41-part site source

## Scope
- Final-C files: **29** → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30]
- 41-part source files actually present: **33** → [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 17, 18, 20, 21, 22, 23, 25, 26, 27, 28, 30, 31, 32, 33, 35, 37, 38, 40, 41]
- Missing numbers in the 41-part source: **[11, 13, 19, 24, 29, 34, 36, 39]**
- Missing numbers in Final-C: **[21]**
- Final-C and source files were read-only during this audit. Only this report was generated.

## Method
- Persian/Arabic character forms and punctuation were normalized for comparison.
- Similarity uses TF-IDF over words + adjacent word pairs, plus exact 3-word phrase overlap.
- `S→F coverage` = fraction of the site-piece 3-word phrases found in that Final-C file.
- `F→S coverage` = fraction of the Final-C 3-word phrases found in that one site-piece.
- The mapping is evidence for segmentation/overlap, not a license to modify either source.

## 41-part source → best Final-C match

| Site file | words | best Final-C | score | S→F | F→S | 2nd best | excerpt |
|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 507 | — | 0.084 | 0.6% | 0.2% | 30 (0.070) | متن بازبینی‌شده — session-01 سلام، ارادت‌مندم. خیلی خوشحالم که در خدمتتان هستم. ببینید، این کیف پول من است و توانایی‌ها، قابلیت‌ها و زمانم را تبدیل به پول می‌کنم و وارد این کیف می‌ |
| 2 | 181 | — | 0.047 | 0.0% | 0.0% | 29 (0.044) | متن بازبینی‌شده — session-02 من یک مهمان امروزم؛ آره، یک مهمان امروز. این «امروز» خیلی به دلم نشسته، چون وقتی در فضای آنچه از آکادمی هوش مالی و آموزش‌هایش فراگرفتم در حال شنا کردن  |
| 3 | 248 | — | 0.034 | 0.0% | 0.0% | 22 (0.033) | متن بازبینی‌شده — session-03 خدمتتان عرض کنم که دوره کم ندیده‌ام و کتاب کم نخوانده‌ام، اما واقعاً می‌توانم بگویم این دوره جزو باکیفیت‌ترین، منظم‌ترین و شسته‌رفته‌ترین دوره‌هایی بود |
| 4 | 150 | — | 0.057 | 0.7% | 0.1% | 30 (0.044) | متن بازبینی‌شده — session-04 تحصیلاتم، از دیپلم تا کارشناسی ارشد، در آمریکا بوده و من اصلاً در ایران درس نخوانده‌ام. با دیدن جزئیات دوره خیلی خوشحال شدم؛ از نظر کیفیت، نظم و برنامه |
| 5 | 485 | — | 0.069 | 0.4% | 0.1% | 30 (0.058) | متن بازبینی‌شده — session-05 سلام. خیلی ممنونم که همراه من هستید. می‌خواستم درباره دوره آموزشی سواد مالی برای بزرگسالان توضیحاتی بدهم. ببینید، وقتی به مدرسه می‌رفتیم، معلم سر کلاس  |
| 6 | 626 | — | 0.102 | 0.3% | 0.1% | 30 (0.072) | متن بازبینی‌شده — session-06 سلام. خیلی خوشحالم که خدمتتان هستم. می‌خواستم شعری از خیام برایتان بخوانم که خیلی جالب است: «تا چند حدیث پنج و چار ای ساقی؟ |
| 7 | 313 | — | 0.078 | 0.3% | 0.1% | 30 (0.060) | متن بازبینی‌شده — session-07 سلام. می‌خواستم کمی درباره این دوره آموزشی به شما بگویم. شرکت در دوره آموزشی سواد مالی برای بزرگسالان هیچ پیش‌نیازی ندارد؛ یعنی لازم نیست از قبل فرمول  |
| 8 | 202 | — | 0.023 | 0.0% | 0.0% | 1 (0.023) | متن بازبینی‌شده — session-08 سلام. حتماً اصطلاحی را شنیده‌اید که مثلاً به طرف می‌گوییم: «چه کار می‌کنی؟ مگر پی بدبختی می‌گردی؟» این تعبیر در فرهنگ ما هست؛ وقتی می‌پرسیم «چه کار می‌ |
| 9 | 495 | — | 0.154 | 0.7% | 0.2% | 30 (0.108) | متن بازبینی‌شده — session-09 سلام دوستان. می‌خواهم مطلبی را با شما در میان بگذارم و آن اینکه این دوره برای شماست؛ دقیقاً برای شما، تا آن را در زندگی به کار بگیرید و از نتایجش بهره‌ |
| 10 | 422 | — | 0.052 | 0.0% | 0.0% | 26 (0.043) | متن بازبینی‌شده — session-10 سلام. این دوره یک مقدمه بسیار مهم دارد. کسانی که می‌خواهند در این دوره شرکت کنند، حتماً باید این مقدمه را داشته باشند یا آن را در خودشان ایجاد کنند. دو |
| 12 | 1552 | 2 | 0.367 | 7.5% | 6.5% | 9 (0.090) | متن بازبینی‌شده — session-12 سلام. وضع مالی‌تان خوب است؟ فکر می‌کنم جواب بیشتر افراد «نه» باشد. از خیلی‌ها پرسیدم وضع مالی‌شان خوب است یا نه و بیشترشان، حتی آن‌هایی که خدا را شکر ک |
| 14 | 1175 | 4 | 0.352 | 7.8% | 7.2% | 3 (0.103) | متن بازبینی‌شده — session-14 سلام. امروز اولین جلسه «خرج و پس‌انداز» را خواهیم داشت و خواهید دید آموزش‌های سواد مالی چقدر ساده، کاربردی و فوق‌العاده کمک‌کننده در مدیریت زندگی‌اند.  |
| 15 | 1364 | 5 | 0.297 | 5.3% | 4.2% | 3 (0.081) | متن بازبینی‌شده — session-15 سلام. یکی از موضوعات جذاب آموزش سواد مالی، خریدکردن است؛ فوق‌العاده لذت‌بخش و البته آموزشی. وقتی کالا یا خدمتی می‌خواهیم—مثلاً کتاب، مبل، یخچال یا فرش، |
| 16 | 863 | 6 | 0.366 | 7.6% | 6.8% | 22 (0.157) | متن بازبینی‌شده — session-16 سلام. قرار شد هزینه‌ها را بنویسیم و چند راهکار هم گفتیم تا هزینه‌ها را به‌شکلی طبیعی کاهش بدهیم؛ مثل نوشتن هزینه‌ها، قضاوت درباره آن‌ها، نگهداری اسناد  |
| 17 | 910 | 7 | 0.406 | 5.9% | 5.0% | 6 (0.079) | متن بازبینی‌شده — session-17 سلام. تا اینجا بیست درصد بودجه‌مان تکمیل شد؛ چیز ترسناکی نیست. هرکدام از دسته‌بندی‌هایی که انجام داده بودیم، یک ردیف بودجه است و اکنون سه ردیف بودجه‌ما |
| 18 | 1074 | 8 | 0.478 | 7.7% | 5.7% | 13 (0.149) | متن بازبینی‌شده — session-18 سلام. خیلی خوشحالم که تا اینجا دوره را ادامه دادید. امروز می‌خواهیم درباره بانک صحبت کنیم؛ «بانک و ما اَدراکَ ما البنك»؛ بانک چیست و تو چه می‌دانی که ب |
| 20 | 898 | 10 | 0.265 | 3.4% | 2.4% | 11 (0.141) | متن بازبینی‌شده — session-20 سلام. داریم درباره یکی از مهم‌ترین مفاهیم سواد مالی، یعنی اعتبار، بدهی و قرض صحبت می‌کنیم. قبلاً گفتیم اصل بر قرض‌نگرفتن است. حالا می‌خواهم بگویم اگر م |
| 21 | 491 | 11 | 0.321 | 6.7% | 5.9% | 10 (0.112) | متن بازبینی‌شده — session-21 سلام. امروز یکی از جلسه‌های خوشحال‌کننده درباره قرض است. پیش‌تر خیلی درباره قرض بد گفتیم و تأکید کردیم اصل بر این است که قرض نگیرید، مگر اینکه مجبور با |
| 22 | 918 | 12 | 0.306 | 3.7% | 3.0% | 10 (0.093) | متن بازبینی‌شده — session-22 سلام. امروز می‌خواهیم درباره کارت‌های اعتباری صحبت کنیم. اعتبار ما چقدر است و چقدر می‌ارزیم؟ ممکن است خیلی‌ها به ما بگویند: «تو برای ما خیلی می‌ارزی؛ م |
| 23 | 749 | 13 | 0.263 | 3.4% | 2.2% | 8 (0.174) | متن بازبینی‌شده — session-23 سلام. این جلسه پایانی مدیریت اعتبار و بدهی است و می‌خواهیم درباره بانک صحبت کنیم. پیش‌تر درباره بانک، حساب‌های مختلف و تجهیز منابع گفتیم؛ یعنی بانک پول |
| 25 | 937 | 15 | 0.277 | 3.6% | 2.6% | 14 (0.120) | متن بازبینی‌شده — session-25 سلام. ممکن است شغلی داشته باشم که ماهانه به من حقوق می‌دهد، اما از آن ناراضی باشم. این موضوع پیچیده است و نگرانی درباره کار نیز بسیار رایج است. بسیاری  |
| 26 | 1573 | — | 0.113 | 0.0% | 0.0% | 14 (0.093) | متن بازبینی‌شده — session-26 سومین مبحث از مباحث شش‌گانه سواد مالی به کار و درآمد اختصاص دارد. کار و درآمد آن‌قدر درهم‌تنیده‌اند که برای بسیاری، کار هدفی جز درآمد ندارد. ریشه واژه  |
| 27 | 623 | 16 | 0.311 | 4.6% | 4.4% | 17 (0.112) | متن بازبینی‌شده — session-27 سلام. ممکن است بگوییم: «من شغل دارم و از شغلم هم راضی‌ام؛ پس دیگر سواد مالی به کارم نمی‌آید.» اما سواد مالی به نکته مهمی اشاره می‌کند: خیلی خوب است که  |
| 28 | 1186 | 17 | 0.315 | 5.2% | 4.1% | 16 (0.093) | متن بازبینی‌شده — session-28 سلام. امروز می‌خواهیم درباره یکی از مهم‌ترین موضوعات در کاریابی و درآمد صحبت کنیم: سبک‌های مختلف شغلی. همه ما شغلی داریم، اما آن را در سبک‌های متفاوتی  |
| 30 | 645 | 19 | 0.403 | 10.6% | 10.2% | 20 (0.146) | متن بازبینی‌شده — session-30 سلام. سرمایه‌گذاری قواعدی دارد. در واقع، پیش از اینکه وارد گزینه‌های سرمایه‌گذاری شویم باید بدانیم چگونه سرمایه‌گذاری کنیم. بگذارید سؤالی از شما بپرسم: |
| 31 | 1068 | 20 | 0.340 | 5.8% | 3.5% | 22 (0.181) | متن بازبینی‌شده — session-31 سلام. در موضوع جذاب سرمایه‌گذاری هستیم؛ سرمایه‌گذاری آن‌قدر جذاب است که معمولاً بدون شناخت، هول‌هولکی داخل دیگ آن می‌افتیم، حسابی می‌سوزیم و نقره‌داغ م |
| 32 | 1029 | 22 | 0.189 | 0.5% | 0.4% | 20 (0.156) | متن بازبینی‌شده — session-32 سلام. درباره گزینه‌های سرمایه‌گذاری صحبت کردیم و هرکس ممکن است براساس ویژگی‌ها و موقعیت خودش یکی از آن‌ها را انتخاب کند. آیا سواد مالی درباره یکی از گز |
| 33 | 940 | 22 | 0.482 | 7.8% | 6.4% | 20 (0.157) | متن بازبینی‌شده — session-33 سلام. بازار سرمایه برای همه هست، اما این به آن معنا نیست که همه باید مستقیم وارد بازار سرمایه شوند، کد معاملاتی یا کد بورسی بگیرند و از طریق کارگزاری م |
| 35 | 1010 | 24 | 0.501 | 3.7% | 2.7% | 23 (0.117) | متن بازبینی‌شده — session-35 سلام. درباره مدیریت ریسک و بیمه صحبت می‌کردیم. گفتیم وقتی با ریسک مواجه می‌شویم، ممکن است به نتیجه مورد انتظار نرسیم یا از نتیجه مطلوب منحرف شویم. در ح |
| 37 | 1603 | 26 | 0.290 | 4.2% | 3.0% | 25 (0.082) | متن بازبینی‌شده — session-37 سلام. درباره تصمیم‌گیری مالی صحبت می‌کردیم و سه شاخص را گفتیم: آیا دارایی درآمدزاست یا هزینه‌زاست؟ آیا به نیاز پاسخ می‌دهد یا خواسته؟ و هزینه فرصت آن چ |
| 38 | 1282 | 27 | 0.377 | 8.3% | 8.3% | 29 (0.093) | متن بازبینی‌شده — session-38 سلام. درباره تصمیم‌گیری مالی صحبت می‌کردیم. تا اینجا گفتیم یک فرد چگونه تصمیم می‌گیرد و ما چطور می‌توانیم به یک تصمیم رضایت‌بخش برسیم؛ اما تصمیم‌های ما |
| 40 | 1512 | 29 | 0.483 | 17.2% | 17.6% | 30 (0.132) | متن بازبینی‌شده — session-40 سلام. امروز می‌خواهم درباره سواد مالی در جهان صحبت کنم. سواد مالی موضوعی ذوقی نیست که مثلاً ما مدتی به آن فکر کرده و حالا خلقش کرده باشیم؛ سابقه‌ای دیر |
| 41 | 548 | 30 | 0.384 | 12.9% | 13.0% | 29 (0.156) | متن بازبینی‌شده — session-41 سلام. یکی از موضوعات مهم در آموزش سواد مالی، سنجش سواد مالی است. اینکه سنجش چیست را می‌توانیم با هم بررسی کنیم. یک نوع سنجش به دوره آموزشی مربوط است؛ م |

## Final-C → site pieces grouped by content

| Final-C | words | mapped site pieces | site words total | site/final size | combined exact 3-gram coverage of Final-C | interpretation |
|---:|---:|---|---:|---:|---:|---|
| 1 | 1999 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 2 | 1806 | 12 | 1552 | 0.86× | 6.5% | Likely one site clip corresponds mainly to this lesson. |
| 3 | 900 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 4 | 1263 | 14 | 1175 | 0.93× | 7.2% | Likely one site clip corresponds mainly to this lesson. |
| 5 | 1703 | 15 | 1364 | 0.80× | 4.2% | Likely one site clip corresponds mainly to this lesson. |
| 6 | 959 | 16 | 863 | 0.90× | 6.8% | Likely one site clip corresponds mainly to this lesson. |
| 7 | 1079 | 17 | 910 | 0.84× | 5.0% | Likely one site clip corresponds mainly to this lesson. |
| 8 | 1462 | 18 | 1074 | 0.73× | 5.7% | Likely one site clip corresponds mainly to this lesson. Final-C is materially larger; site version looks partial/compressed. |
| 9 | 1560 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 10 | 1281 | 20 | 898 | 0.70× | 2.4% | Likely one site clip corresponds mainly to this lesson. Final-C is materially larger; site version looks partial/compressed. |
| 11 | 555 | 21 | 491 | 0.88× | 5.9% | Likely one site clip corresponds mainly to this lesson. |
| 12 | 1126 | 22 | 918 | 0.82× | 3.0% | Likely one site clip corresponds mainly to this lesson. |
| 13 | 1140 | 23 | 749 | 0.66× | 2.2% | Likely one site clip corresponds mainly to this lesson. Final-C is materially larger; site version looks partial/compressed. |
| 14 | 866 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 15 | 1300 | 25 | 937 | 0.72× | 2.6% | Likely one site clip corresponds mainly to this lesson. Final-C is materially larger; site version looks partial/compressed. |
| 16 | 650 | 27 | 623 | 0.96× | 4.4% | Likely one site clip corresponds mainly to this lesson. |
| 17 | 1527 | 28 | 1186 | 0.78× | 4.1% | Likely one site clip corresponds mainly to this lesson. |
| 18 | 1483 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 19 | 642 | 30 | 645 | 1.00× | 10.2% | Likely one site clip corresponds mainly to this lesson. |
| 20 | 1804 | 31 | 1068 | 0.59× | 3.5% | Likely one site clip corresponds mainly to this lesson. Final-C is materially larger; site version looks partial/compressed. |
| 22 | 1189 | 32, 33 | 1969 | 1.66× | 6.4% | Likely split into multiple site clips. Site text is materially larger by token count; inspect for extra material. |
| 23 | 792 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 24 | 1428 | 35 | 1010 | 0.71× | 2.7% | Likely one site clip corresponds mainly to this lesson. Final-C is materially larger; site version looks partial/compressed. |
| 25 | 1539 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 26 | 2224 | 37 | 1603 | 0.72× | 3.0% | Likely one site clip corresponds mainly to this lesson. Final-C is materially larger; site version looks partial/compressed. |
| 27 | 1288 | 38 | 1282 | 1.00× | 8.3% | Likely one site clip corresponds mainly to this lesson. |
| 28 | 1400 | — | 0 | 0.00× | 0.0% | No confident site-piece mapped; check missing download / numbering / unique material. |
| 29 | 1467 | 40 | 1512 | 1.03× | 17.6% | Likely one site clip corresponds mainly to this lesson. |
| 30 | 546 | 41 | 548 | 1.00× | 13.0% | Likely one site clip corresponds mainly to this lesson. |

## Unassigned / likely non-core or unmatched site files
- [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 26]

- **Site 1** — best weak match Final-C 1 (score 0.084); متن بازبینی‌شده — session-01 سلام، ارادت‌مندم. خیلی خوشحالم که در خدمتتان هستم. ببینید، این کیف پول من است و توانایی‌ها، قابلیت‌ها و زمانم را تبدیل به پول می‌کنم و وارد این کیف می‌
- **Site 2** — best weak match Final-C 1 (score 0.047); متن بازبینی‌شده — session-02 من یک مهمان امروزم؛ آره، یک مهمان امروز. این «امروز» خیلی به دلم نشسته، چون وقتی در فضای آنچه از آکادمی هوش مالی و آموزش‌هایش فراگرفتم در حال شنا کردن 
- **Site 3** — best weak match Final-C 4 (score 0.034); متن بازبینی‌شده — session-03 خدمتتان عرض کنم که دوره کم ندیده‌ام و کتاب کم نخوانده‌ام، اما واقعاً می‌توانم بگویم این دوره جزو باکیفیت‌ترین، منظم‌ترین و شسته‌رفته‌ترین دوره‌هایی بود
- **Site 4** — best weak match Final-C 29 (score 0.057); متن بازبینی‌شده — session-04 تحصیلاتم، از دیپلم تا کارشناسی ارشد، در آمریکا بوده و من اصلاً در ایران درس نخوانده‌ام. با دیدن جزئیات دوره خیلی خوشحال شدم؛ از نظر کیفیت، نظم و برنامه
- **Site 5** — best weak match Final-C 29 (score 0.069); متن بازبینی‌شده — session-05 سلام. خیلی ممنونم که همراه من هستید. می‌خواستم درباره دوره آموزشی سواد مالی برای بزرگسالان توضیحاتی بدهم. ببینید، وقتی به مدرسه می‌رفتیم، معلم سر کلاس 
- **Site 6** — best weak match Final-C 29 (score 0.102); متن بازبینی‌شده — session-06 سلام. خیلی خوشحالم که خدمتتان هستم. می‌خواستم شعری از خیام برایتان بخوانم که خیلی جالب است: «تا چند حدیث پنج و چار ای ساقی؟
- **Site 7** — best weak match Final-C 2 (score 0.078); متن بازبینی‌شده — session-07 سلام. می‌خواستم کمی درباره این دوره آموزشی به شما بگویم. شرکت در دوره آموزشی سواد مالی برای بزرگسالان هیچ پیش‌نیازی ندارد؛ یعنی لازم نیست از قبل فرمول 
- **Site 8** — best weak match Final-C 9 (score 0.023); متن بازبینی‌شده — session-08 سلام. حتماً اصطلاحی را شنیده‌اید که مثلاً به طرف می‌گوییم: «چه کار می‌کنی؟ مگر پی بدبختی می‌گردی؟» این تعبیر در فرهنگ ما هست؛ وقتی می‌پرسیم «چه کار می‌
- **Site 9** — best weak match Final-C 29 (score 0.154); متن بازبینی‌شده — session-09 سلام دوستان. می‌خواهم مطلبی را با شما در میان بگذارم و آن اینکه این دوره برای شماست؛ دقیقاً برای شما، تا آن را در زندگی به کار بگیرید و از نتایجش بهره‌
- **Site 10** — best weak match Final-C 1 (score 0.052); متن بازبینی‌شده — session-10 سلام. این دوره یک مقدمه بسیار مهم دارد. کسانی که می‌خواهند در این دوره شرکت کنند، حتماً باید این مقدمه را داشته باشند یا آن را در خودشان ایجاد کنند. دو
- **Site 26** — best weak match Final-C 15 (score 0.113); متن بازبینی‌شده — session-26 سومین مبحث از مباحث شش‌گانه سواد مالی به کار و درآمد اختصاص دارد. کار و درآمد آن‌قدر درهم‌تنیده‌اند که برای بسیاری، کار هدفی جز درآمد ندارد. ریشه واژه 

## Potentially important cases to inspect manually

- Site **12** ↔ Final-C **2**: topical match but low exact phrase containment (score 0.367, S→F 7.5%).
- Site **14** ↔ Final-C **4**: topical match but low exact phrase containment (score 0.352, S→F 7.8%).
- Site **15** ↔ Final-C **5**: topical match but low exact phrase containment (score 0.297, S→F 5.3%).
- Site **16** ↔ Final-C **6**: topical match but low exact phrase containment (score 0.366, S→F 7.6%).
- Site **17** ↔ Final-C **7**: topical match but low exact phrase containment (score 0.406, S→F 5.9%).
- Site **18** ↔ Final-C **8**: topical match but low exact phrase containment (score 0.478, S→F 7.7%).
- Site **20** ↔ Final-C **10**: topical match but low exact phrase containment (score 0.265, S→F 3.4%).
- Site **21** ↔ Final-C **11**: topical match but low exact phrase containment (score 0.321, S→F 6.7%).
- Site **22** ↔ Final-C **12**: topical match but low exact phrase containment (score 0.306, S→F 3.7%).
- Site **23** ↔ Final-C **13**: topical match but low exact phrase containment (score 0.263, S→F 3.4%).
- Site **25** ↔ Final-C **15**: topical match but low exact phrase containment (score 0.277, S→F 3.6%).
- Site **27** ↔ Final-C **16**: topical match but low exact phrase containment (score 0.311, S→F 4.6%).
- Site **28** ↔ Final-C **17**: topical match but low exact phrase containment (score 0.315, S→F 5.2%).
- Site **31** ↔ Final-C **20**: topical match but low exact phrase containment (score 0.340, S→F 5.8%).
- Site **32** ↔ Final-C **22**: topical match but low exact phrase containment (score 0.189, S→F 0.5%).
- Site **33** ↔ Final-C **22**: topical match but low exact phrase containment (score 0.482, S→F 7.8%).
- Site **35** ↔ Final-C **24**: topical match but low exact phrase containment (score 0.501, S→F 3.7%).
- Site **37** ↔ Final-C **26**: topical match but low exact phrase containment (score 0.290, S→F 4.2%).
- Final-C **22** ↔ site **[32, 33]**: combined site text 1.66× the Final-C token count; possible extra material or duplicated site framing.

## Top-3 matches for every site file (debug/audit)

- Site **1**: F1 score=0.084 cos=0.106 S→F=0.6%, F30 score=0.070 cos=0.089 S→F=0.4%, F29 score=0.065 cos=0.082 S→F=0.6%
- Site **2**: F1 score=0.047 cos=0.060 S→F=0.0%, F29 score=0.044 cos=0.056 S→F=1.1%, F9 score=0.035 cos=0.045 S→F=0.0%
- Site **3**: F4 score=0.034 cos=0.044 S→F=0.0%, F22 score=0.033 cos=0.043 S→F=0.0%, F20 score=0.032 cos=0.040 S→F=0.0%
- Site **4**: F29 score=0.057 cos=0.073 S→F=0.7%, F30 score=0.044 cos=0.054 S→F=1.4%, F1 score=0.036 cos=0.046 S→F=0.7%
- Site **5**: F29 score=0.069 cos=0.088 S→F=0.4%, F30 score=0.058 cos=0.073 S→F=0.6%, F1 score=0.056 cos=0.072 S→F=0.2%
- Site **6**: F29 score=0.102 cos=0.130 S→F=0.3%, F30 score=0.072 cos=0.091 S→F=0.5%, F28 score=0.070 cos=0.089 S→F=0.3%
- Site **7**: F2 score=0.078 cos=0.100 S→F=0.3%, F30 score=0.060 cos=0.076 S→F=0.7%, F1 score=0.054 cos=0.069 S→F=0.3%
- Site **8**: F9 score=0.023 cos=0.030 S→F=0.0%, F1 score=0.023 cos=0.029 S→F=0.5%, F6 score=0.022 cos=0.029 S→F=0.0%
- Site **9**: F29 score=0.154 cos=0.196 S→F=0.7%, F30 score=0.108 cos=0.137 S→F=0.4%, F28 score=0.076 cos=0.096 S→F=0.9%
- Site **10**: F1 score=0.052 cos=0.067 S→F=0.0%, F26 score=0.043 cos=0.056 S→F=0.0%, F2 score=0.039 cos=0.050 S→F=0.0%
- Site **12**: F2 score=0.367 cos=0.451 S→F=7.5%, F9 score=0.090 cos=0.115 S→F=0.1%, F3 score=0.087 cos=0.111 S→F=0.1%
- Site **14**: F4 score=0.352 cos=0.430 S→F=7.8%, F3 score=0.103 cos=0.132 S→F=0.0%, F5 score=0.073 cos=0.093 S→F=0.1%
- Site **15**: F5 score=0.297 cos=0.367 S→F=5.3%, F3 score=0.081 cos=0.103 S→F=0.1%, F4 score=0.072 cos=0.093 S→F=0.0%
- Site **16**: F6 score=0.366 cos=0.449 S→F=7.6%, F22 score=0.157 cos=0.202 S→F=0.0%, F20 score=0.090 cos=0.116 S→F=0.0%
- Site **17**: F7 score=0.406 cos=0.505 S→F=5.9%, F6 score=0.079 cos=0.101 S→F=0.3%, F4 score=0.068 cos=0.087 S→F=0.0%
- Site **18**: F8 score=0.478 cos=0.595 S→F=7.7%, F13 score=0.149 cos=0.190 S→F=0.5%, F20 score=0.101 cos=0.128 S→F=0.5%
- Site **20**: F10 score=0.265 cos=0.332 S→F=3.4%, F11 score=0.141 cos=0.179 S→F=0.6%, F8 score=0.093 cos=0.119 S→F=0.0%
- Site **21**: F11 score=0.321 cos=0.394 S→F=6.7%, F10 score=0.112 cos=0.143 S→F=0.6%, F9 score=0.077 cos=0.099 S→F=0.2%
- Site **22**: F12 score=0.306 cos=0.383 S→F=3.7%, F10 score=0.093 cos=0.119 S→F=0.0%, F8 score=0.090 cos=0.115 S→F=0.0%
- Site **23**: F13 score=0.263 cos=0.329 S→F=3.4%, F8 score=0.174 cos=0.222 S→F=0.4%, F10 score=0.085 cos=0.109 S→F=0.1%
- Site **25**: F15 score=0.277 cos=0.347 S→F=3.6%, F14 score=0.120 cos=0.153 S→F=0.1%, F17 score=0.096 cos=0.124 S→F=0.0%
- Site **26**: F15 score=0.113 cos=0.144 S→F=0.0%, F14 score=0.093 cos=0.120 S→F=0.0%, F16 score=0.081 cos=0.103 S→F=0.0%
- Site **27**: F16 score=0.311 cos=0.386 S→F=4.6%, F17 score=0.112 cos=0.144 S→F=0.0%, F15 score=0.073 cos=0.093 S→F=0.0%
- Site **28**: F17 score=0.315 cos=0.390 S→F=5.2%, F16 score=0.093 cos=0.119 S→F=0.0%, F15 score=0.070 cos=0.090 S→F=0.0%
- Site **30**: F19 score=0.403 cos=0.487 S→F=10.6%, F20 score=0.146 cos=0.185 S→F=0.9%, F18 score=0.135 cos=0.171 S→F=1.2%
- Site **31**: F20 score=0.340 cos=0.424 S→F=5.8%, F22 score=0.181 cos=0.230 S→F=0.7%, F18 score=0.161 cos=0.204 S→F=0.7%
- Site **32**: F22 score=0.189 cos=0.240 S→F=0.5%, F20 score=0.156 cos=0.199 S→F=0.7%, F29 score=0.114 cos=0.146 S→F=0.2%
- Site **33**: F22 score=0.482 cos=0.599 S→F=7.8%, F20 score=0.157 cos=0.199 S→F=0.8%, F6 score=0.133 cos=0.171 S→F=0.0%
- Site **35**: F24 score=0.501 cos=0.634 S→F=3.7%, F23 score=0.117 cos=0.151 S→F=0.0%, F20 score=0.052 cos=0.067 S→F=0.1%
- Site **37**: F26 score=0.290 cos=0.361 S→F=4.2%, F25 score=0.082 cos=0.105 S→F=0.1%, F20 score=0.063 cos=0.081 S→F=0.0%
- Site **38**: F27 score=0.377 cos=0.460 S→F=8.3%, F29 score=0.093 cos=0.118 S→F=0.4%, F2 score=0.082 cos=0.105 S→F=0.1%
- Site **40**: F29 score=0.483 cos=0.570 S→F=17.2%, F30 score=0.132 cos=0.169 S→F=0.1%, F28 score=0.128 cos=0.163 S→F=0.4%
- Site **41**: F30 score=0.384 cos=0.456 S→F=12.9%, F29 score=0.156 cos=0.199 S→F=0.6%, F1 score=0.079 cos=0.100 S→F=0.6%
