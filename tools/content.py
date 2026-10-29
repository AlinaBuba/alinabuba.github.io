"""Page content (UA + EN). Each page function takes a Ctx (see build.py) and returns a dict:
title, desc, body (HTML), and optionally faq (list of (id, question, answer_html))."""

PRICE = 800
PACK_N = 4
PACK_DISCOUNT = 5
PACK_PRICE = round(PRICE * PACK_N * (100 - PACK_DISCOUNT) / 100)

TOPICS = ("emotions", "self-discovery", "neuropsychology", "children")


def home(c):
    t, u = c.t, c.u
    topics = {
        "emotions": (t("Емоційний стан", "Emotional wellbeing"), t("Тривожність, знижений настрій, виснаження, самокритика, труднощі з регуляцією емоцій.", "Anxiety, low mood, burnout, self-criticism, difficulty regulating emotions.")),
        "self-discovery": (t("Самопізнання", "Self-discovery"), t("Власні потреби й цінності, складні рішення, особистісні кризи, пошук орієнтирів.", "Your needs and values, difficult decisions, personal crises, finding direction.")),
        "neuropsychology": (t("Когнітивні функції", "Cognitive functions"), t("Концентрація, пам'ять, самоорганізація, планування. Нейропсихологічна оцінка.", "Concentration, memory, self-organisation, planning. Neuropsychological assessment.")),
        "children": (t("Діти та підлітки", "Children and teens"), t("Увага, пам'ять, навчання, саморегуляція, СДУГ. Нейропсихологічна діагностика.", "Attention, memory, learning, self-regulation, ADHD. Neuropsychological diagnostics.")),
    }
    cards = "".join(
        f'<a class="card link-card" href="{u("specializations")}#{k}"><h3>{n}</h3><p>{d}</p></a>'
        for k, (n, d) in topics.items()
    )
    familiar = [
        t("Ви прокидаєтесь із відчуттям, що вже втомилися, хоча день ще не почався.", "You wake up already tired, before the day has even begun."),
        t("Голова «крутить» одні й ті самі думки, а вночі вони голосніші.", "Your mind loops the same thoughts, and at night they get louder."),
        t("Складно зосередитися, а здається, що пам'ять підводить.", "It is hard to concentrate, and it feels like your memory lets you down."),
        t("Ви багато вмієте, але рідко дозволяєте собі зупинитися.", "You can do a lot, but rarely let yourself stop."),
        t("Складно сказати «ні» або попросити про допомогу.", "It is hard to say “no” or to ask for help."),
        t("Хвилює, як вчиться, зосереджується чи поводиться ваша дитина.", "You worry about how your child learns, focuses or behaves."),
    ]
    body = f"""
<section class="hero-sec"><div class="wrap hero">
<div class="hero-text">
<p class="eyebrow">{t("Психологиня · онлайн", "Psychologist · online")}</p>
<h1>{t("Жити спокійніше навіть тоді, коли довкола неспокійно", "Living more calmly, even when things around you are not calm")}</h1>
<p class="lead">{t("Я Аліна, клінічна психологиня та нейропсихологиня. Працюю онлайн із дорослими, підлітками й дітьми: допомагаю розібратися з емоційними труднощами, краще зрозуміти себе та підтримати когнітивні функції. Без поспіху й оцінок.", "I am Alina, a clinical psychologist and neuropsychologist. I work online with adults, teenagers and children: helping with emotional difficulties, understanding yourself better and supporting cognitive functions. No rush, no judgement.")}</p>
<p class="actions"><a class="btn" href="{u("contacts")}#book" data-track="cta_click" data-label="hero">{t("Записатися на ознайомчу розмову", "Book an intro call")}</a>
<a class="btn ghost" href="{u("about")}" data-track="cta_click" data-label="hero_about">{t("Дізнатися більше", "Learn more")}</a></p>
<ul class="chips"><li>{t("КПТ", "CBT")}</li><li>{t("Психодіагностика", "Psychodiagnostics")}</li><li>{t("Нейропсихологія", "Neuropsychology")}</li><li>{t("Онлайн", "Online")}</li><li>UA / EN</li></ul>
</div>
{c.photo("portrait", hero=True)}
</div></section>

<section class="alt"><div class="wrap narrow">
<h2>{t("Можливо, це знайоме", "Does this sound familiar?")}</h2>
<ul class="ticks">{"".join(f"<li>{x}</li>" for x in familiar)}</ul>
<p>{t("Якщо ви впізнали себе, це не означає, що з вами щось «не так». Це привід дати собі підтримку.", "If you recognise yourself, it does not mean something is “wrong” with you. It is a reason to give yourself support.")}</p>
</div></section>

<section><div class="wrap">
<h2>{t("З чим я працюю", "What I work with")}</h2>
<div class="grid">{cards}</div>
</div></section>

<section class="alt"><div class="wrap">
<h2>{t("Як ми працюватимемо", "How we will work")}</h2>
<ol class="steps">
<li><h3>{t("Ознайомча розмова", "Intro call")}</h3><p>{t("15 хвилин, безкоштовно. Ви розповідаєте, з чим прийшли, а я пояснюю, як я працюю. Це нічого не зобов'язує.", "15 minutes, free. You tell me what brings you here, and I explain how I work. No obligation.")}</p></li>
<li><h3>{t("Перша сесія", "First session")}</h3><p>{t("Уточнюємо запит, домовляємося про цілі й формат. Ви самі вирішуєте, про що говорити.", "We clarify your request and agree on goals and format. You decide what to talk about.")}</p></li>
<li><h3>{t("Регулярна робота", "Regular work")}</h3><p>{t("Зазвичай зустрічі раз на тиждень. Разом дивимось, що працює, і за потреби коригуємо план.", "Usually weekly meetings. Together we see what works and adjust the plan when needed.")}</p></li>
</ol>
</div></section>

<section><div class="wrap about-teaser">
{c.photo("about")}
<div>
<h2>{t("Кілька слів про мене", "A few words about me")}</h2>
<p>{t("Я клінічна психологиня та нейропсихологиня, магістр клінічної психології з основами психотерапії (Київський національний університет імені Тараса Шевченка). Спираюся на клінічну психологію, сучасні методи психодіагностики та принципи когнітивно-поведінкової терапії.", "I am a clinical psychologist and neuropsychologist with a master’s degree in clinical psychology with fundamentals of psychotherapy (Taras Shevchenko National University of Kyiv). I draw on clinical psychology, modern psychodiagnostic methods and the principles of cognitive-behavioural therapy.")}</p>
<p>{t("Для мене важливо створити простір, у якому можна відкрито говорити про свої переживання, не боячись осуду.", "It matters to me to create a space where you can speak openly about your experiences without fear of judgement.")}</p>
<p><a href="{u("about")}">{t("Освіта й підхід докладніше", "Education and approach in detail")}</a></p>
</div></div></section>

<section class="band"><div class="wrap">
<h2>{t("Готові зробити перший крок?", "Ready to take the first step?")}</h2>
<p>{t("Напишіть мені, і ми домовимося про безкоштовну розмову на 15 хвилин.", "Write to me and we will arrange a free 15-minute call.")}</p>
<p><a class="btn" href="{u("contacts")}#book" data-track="cta_click" data-label="band">{t("Записатися", "Book now")}</a></p>
</div></section>"""
    return dict(
        title=t("Аліна Буба, психологиня онлайн: КПТ, нейропсихологія, діти й дорослі", "Alina Buba, online psychologist: CBT, neuropsychology, children and adults"),
        desc=t("Аліна Буба: клінічна психологиня та нейропсихологиня. Онлайн для дорослих, підлітків і дітей: тривожність, виснаження, самооцінка, увага й пам'ять, СДУГ. Розмова 15 хв безкоштовно.", "Alina Buba: clinical psychologist and neuropsychologist. Online for adults, teens and children: anxiety, burnout, self-esteem, attention and memory, ADHD. Free 15-minute intro call."),
        body=body,
    )


def about(c):
    t, u = c.t, c.u
    edu = [
        ("2020 – 2022", t("Магістр клінічної психології з основами психотерапії", "Master’s degree in clinical psychology with fundamentals of psychotherapy"), t("Київський національний університет імені Тараса Шевченка", "Taras Shevchenko National University of Kyiv")),
    ]
    extra = [
        ("", t("Школа психолога-консультанта PsyStart", "PsyStart counsellor school"), t("Асоціація когнітивно-поведінкової психотерапії", "Association of Cognitive-Behavioural Psychotherapy")),
        ("", t("Школа психодіагностики", "School of Psychodiagnostics"), t("Психодіагностика в індивідуальному консультуванні та інструменти оцінювання особистості", "Psychodiagnostics in individual counselling and personality assessment tools")),
        ("2023", t("«Клінічна нейропсихологія та основи нейропсихологічної реабілітації»", "“Clinical Neuropsychology and Fundamentals of Neuropsychological Rehabilitation”"), ""),
        ("2024 – 2025", t("«Нейропсихологічна діагностика та корекція в дитячому віці», 120 годин", "“Neuropsychological Diagnostics and Correction in Childhood”, 120 hours"), ""),
        ("", t("Навчання з питань СДУГ, порушень поведінки та психологічного консультування підлітків", "Training on ADHD, behavioural difficulties and counselling teenagers"), ""),
    ]

    def li(items):
        out = ""
        for when, what, where in items:
            out += f'<li><span class="when">{when}</span><div><strong>{what}</strong>{f"<br><span class=muted>{where}</span>" if where else ""}</div></li>'
        return f'<ul class="timeline">{out}</ul>'

    body = f"""
<section class="page-head"><div class="wrap narrow"><h1>{t("Про мене", "About me")}</h1>
<p class="lead">{t("Мене звати Аліна, я психологиня, клінічна психологиня та нейропсихологиня.", "My name is Alina, I am a psychologist, clinical psychologist and neuropsychologist.")}</p></div></section>

<section><div class="wrap about-teaser">
{c.photo("about")}
<div>
<h2>{t("Хто я", "Who I am")}</h2>
<p>{t("Маю магістерський ступінь із клінічної психології з основами психотерапії, здобутий у Київському національному університеті імені Тараса Шевченка. Мій професійний інтерес: клінічна психологія, психодіагностика, нейропсихологія та когнітивно-поведінковий підхід.", "I hold a master’s degree in clinical psychology with fundamentals of psychotherapy from Taras Shevchenko National University of Kyiv. My professional interests are clinical psychology, psychodiagnostics, neuropsychology and the cognitive-behavioural approach.")}</p>
<p>{t("Я переконана, що розуміння власних емоцій, поведінки та особливостей мислення допомагає людині краще пізнати себе, знаходити внутрішні ресурси й поступово змінювати своє життя.", "I am convinced that understanding your own emotions, behaviour and ways of thinking helps you know yourself better, find inner resources and gradually change your life.")}</p>
<p>{t("Мови: українська та англійська. Окрім психології, я викладаю англійську мову, тому проводжу сесії й англійською, а ще вивчаю французьку.", "Languages: Ukrainian and English. Besides psychology, I teach English, so I hold sessions in English too, and I am also learning French.")}</p>
</div></div></section>

<section class="alt"><div class="wrap narrow">
<h2>{t("Мій підхід", "My approach")}</h2>
<p>{t("Наукова обґрунтованість, індивідуальність та повага до кожної людини. У роботі я спираюся на знання клінічної психології, сучасні методи психодіагностики та принципи когнітивно-поведінкової терапії.", "Scientific grounding, individuality and respect for every person. In my work I draw on clinical psychology, modern psychodiagnostic methods and the principles of cognitive-behavioural therapy.")}</p>
<p>{t("Мені важливо не лише вислухати людину, а й допомогти їй зрозуміти причини труднощів, побачити взаємозв'язки між думками, емоціями та поведінкою й знайти практичні способи покращити психологічний стан.", "It matters to me not only to listen, but to help you understand the causes of difficulties, see the links between thoughts, emotions and behaviour, and find practical ways to improve how you feel.")}</p>
<p>{t("Окреме місце в моїй роботі посідає нейропсихологія: дослідження взаємозв'язку між роботою мозку, пізнавальними процесами та поведінкою людини.", "Neuropsychology has a special place in my work: the study of how brain function, cognitive processes and behaviour are connected.")}</p>
<p>{t("Для мене важливо створити простір, у якому можна відкрито говорити про свої переживання, не боячись осуду.", "It matters to me to create a space where you can speak openly about your experiences without fear of judgement.")}</p>
</div></section>

<section><div class="wrap">
<h2>{t("Принципи", "Principles")}</h2>
<div class="grid">
<div class="card"><h3>{t("Наукова обґрунтованість", "Scientific grounding")}</h3><p>{t("Клінічна психологія, сучасна психодіагностика й когнітивно-поведінкова терапія. Без обіцянок чудес чи гарантованого результату.", "Clinical psychology, modern psychodiagnostics and cognitive-behavioural therapy. No promises of miracles or guaranteed results.")}</p></div>
<div class="card"><h3>{t("Індивідуальність", "Individuality")}</h3><p>{t("Ви самі обираєте темп і те, про що говорити. План роботи залежить від вашого запиту й особливостей.", "You choose the pace and what to talk about. The plan depends on your request and your individual features.")}</p></div>
<div class="card"><h3>{t("Повага", "Respect")}</h3><p>{t("Повага до вашого досвіду та меж, конфіденційність і простір без осуду.", "Respect for your experience and boundaries, confidentiality and a space without judgement.")}</p></div>
</div></div></section>

<section class="alt"><div class="wrap narrow">
<h2>{t("Освіта", "Education")}</h2>
{li(edu)}
<h2 class="mt">{t("Додаткова професійна підготовка", "Further professional training")}</h2>
{li(extra)}
<p>{t("Я постійно поглиблюю знання з клінічної психології, нейропсихології та психологічного консультування.", "I keep deepening my knowledge of clinical psychology, neuropsychology and psychological counselling.")}</p>
<p><em>{t("Моя мета: допомагати людям краще розуміти себе та свої психологічні особливості, спираючись на наукові знання, уважність і повагу до індивідуального досвіду кожного.", "My aim: to help people understand themselves and their psychological features better, relying on scientific knowledge, attentiveness and respect for each person’s individual experience.")}</em></p>
</div></section>

<section class="band"><div class="wrap">
<h2>{t("Познайомимось?", "Shall we meet?")}</h2>
<p>{t("Безкоштовна розмова на 15 хвилин допоможе зрозуміти, чи підходимо ми одне одному.", "A free 15-minute call will help us see whether we are a good fit.")}</p>
<p><a class="btn" href="{u("contacts")}#book" data-track="cta_click" data-label="band">{t("Записатися", "Book now")}</a></p>
</div></section>"""
    return dict(
        title=t("Про мене: Аліна Буба, клінічна психологиня та нейропсихологиня", "About: Alina Buba, clinical psychologist and neuropsychologist"),
        desc=t("Аліна Буба: магістр клінічної психології (КНУ імені Шевченка), нейропсихологія, психодіагностика, когнітивно-поведінковий підхід. Освіта й підготовка.", "Alina Buba: master’s in clinical psychology (Taras Shevchenko National University of Kyiv), neuropsychology, psychodiagnostics, cognitive-behavioural approach. Education and training."),
        body=body,
    )


def specializations(c):
    t, u = c.t, c.u

    def ul(items):
        return '<ul class="ticks">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"

    data = {
        "emotions": (
            t("Емоційний стан та психологічні труднощі", "Emotional state and psychological difficulties"),
            [t("Тривожність, надмірне хвилювання, постійне напруження", "Anxiety, excessive worry, constant tension"),
             t("Знижений настрій, апатія, втрата мотивації", "Low mood, apathy, loss of motivation"),
             t("Емоційне виснаження, стрес та труднощі адаптації", "Emotional exhaustion, stress and difficulty adapting"),
             t("Невпевненість у собі, низька самооцінка, самокритика", "Self-doubt, low self-esteem, self-criticism"),
             t("Труднощі з розумінням та регуляцією емоцій", "Difficulty understanding and regulating emotions")],
            t("Разом розбираємо, що стоїть за станом: помічаємо зв'язок між думками, емоціями й поведінкою та підбираємо практичні способи його покращити. За потреби використовуємо методи психодіагностики.", "Together we explore what is behind the state: we notice the link between thoughts, emotions and behaviour and choose practical ways to improve it. When needed, we use psychodiagnostic methods."),
        ),
        "self-discovery": (
            t("Самопізнання та особистісний розвиток", "Self-discovery and personal growth"),
            [t("Дослідження особистісних особливостей", "Exploring personality features"),
             t("Розуміння власних потреб, цінностей та поведінкових реакцій", "Understanding your needs, values and behavioural reactions"),
             t("Труднощі в прийнятті рішень", "Difficulty making decisions"),
             t("Особистісні кризи та пошук життєвих орієнтирів", "Personal crises and searching for direction")],
            t("Досліджуємо ваші особливості, потреби й цінності, розглядаємо варіанти рішень і шукаємо орієнтири в темпі, який комфортний вам.", "We explore your features, needs and values, look at options for decisions and search for direction at a pace that is comfortable for you."),
        ),
        "neuropsychology": (
            t("Когнітивні функції та нейропсихологія", "Cognitive functions and neuropsychology"),
            [t("Труднощі з концентрацією та підтриманням уваги", "Difficulty concentrating and sustaining attention"),
             t("Особливості пам'яті, мислення та пізнавальної діяльності", "Features of memory, thinking and cognitive activity"),
             t("Проблеми із самоорганізацією, плануванням і контролем поведінки", "Problems with self-organisation, planning and behavioural control"),
             t("Нейропсихологічна оцінка когнітивних функцій", "Neuropsychological assessment of cognitive functions")],
            t("Починаємо з розмови та, за потреби, нейропсихологічної оцінки когнітивних функцій. На її основі обговорюємо, що можна робити далі. Оцінка не замінює медичної діагностики.", "We start with a conversation and, when needed, a neuropsychological assessment of cognitive functions. Based on it we discuss what can be done next. The assessment does not replace a medical diagnosis."),
        ),
        "children": (
            t("Дитяча та підліткова психологія", "Child and adolescent psychology"),
            [t("Труднощі з увагою, пам'яттю та навчанням", "Difficulties with attention, memory and learning"),
             t("Особливості розвитку когнітивних функцій у дітей", "Features of cognitive development in children"),
             t("Труднощі із саморегуляцією та поведінкою", "Difficulties with self-regulation and behaviour"),
             t("Питання, пов'язані із синдромом дефіциту уваги та гіперактивності (СДУГ)", "Questions related to attention deficit hyperactivity disorder (ADHD)"),
             t("Нейропсихологічна діагностика та визначення напрямів корекційної роботи", "Neuropsychological diagnostics and choosing directions for corrective work")],
            t("Нейропсихологічна діагностика допомагає зрозуміти особливості розвитку дитини й визначити напрями корекційної роботи. Медичний діагноз, зокрема СДУГ, встановлює лікар, а не психолог.", "Neuropsychological diagnostics helps understand a child’s developmental features and choose directions for corrective work. A medical diagnosis, including ADHD, is made by a doctor, not a psychologist."),
        ),
    }
    sections = ""
    for i, (k, (n, items, how)) in enumerate(data.items()):
        sections += f"""<section id="{k}" class="{'alt' if i % 2 == 0 else ''}"><div class="wrap narrow">
<h2>{n}</h2>
<h3>{t("З чим звертаються", "Common requests")}</h3>{ul(items)}
<h3>{t("Як ми працюємо", "How we work")}</h3><p>{how}</p>
</div></section>"""
    body = f"""
<section class="page-head"><div class="wrap narrow"><h1>{t("Спеціалізації", "Specialisations")}</h1>
<p class="lead">{t("Теми, з якими до мене звертаються дорослі, підлітки та батьки дітей. Якщо вашого запиту тут немає, напишіть: разом з'ясуємо, чи можу я допомогти.", "Topics that adults, teenagers and parents of children bring to me. If your request is not here, write to me and we will see whether I can help.")}</p></div></section>
{sections}
<section><div class="wrap narrow">
<h2>{t("Що виходить за межі моєї роботи", "What is outside my work")}</h2>
<ul class="ticks"><li>{t("Гострі психіатричні стани (психози, виражена депресія з думками про самогубство).", "Acute psychiatric conditions (psychosis, severe depression with suicidal thoughts).")}</li>
<li>{t("Лікування залежностей.", "Treatment of addictions.")}</li>
<li>{t("Призначення чи скасування ліків. Це робить лише лікар-психіатр.", "Prescribing or stopping medication. Only a psychiatrist can do this.")}</li></ul>
<p>{t("У таких випадках я допоможу знайти відповідного фахівця.", "In such cases I will help you find the right specialist.")}</p>
<h2 class="mt">{t("Чи підходить мені терапія?", "Is therapy right for me?")}</h2>
<p>{t("Терапія підходить, якщо ви готові до регулярних зустрічей і невеликих завдань між ними, а також хочете краще розуміти себе. Не обов'язково мати «серйозну» причину: достатньо відчуття, що так, як є, вам складно.", "Therapy suits you if you are ready for regular meetings and small tasks between them, and want to understand yourself better. You do not need a “serious” reason: it is enough to feel that things are hard as they are.")}</p>
<p><a class="btn" href="{u("contacts")}#book" data-track="cta_click" data-label="specializations">{t("Обговорити свій запит", "Discuss your request")}</a></p>
</div></section>"""
    return dict(
        title=t("Спеціалізації: емоційний стан, нейропсихологія, діти й підлітки", "Specialisations: emotional wellbeing, neuropsychology, children and teens"),
        desc=t("З чим працює Аліна Буба: тривожність, виснаження, самооцінка, самопізнання, увага й пам'ять, нейропсихологічна діагностика, СДУГ, діти та підлітки.", "What Alina Buba works with: anxiety, burnout, self-esteem, self-discovery, attention and memory, neuropsychological diagnostics, ADHD, children and teens."),
        body=body,
    )


def services(c):
    t, u, ph = c.t, c.u, c.ph
    body = f"""
<section class="page-head"><div class="wrap narrow"><h1>{t("Послуги й формат", "Services and format")}</h1>
<p class="lead">{t("Усе заздалегідь і прозоро: що, скільки коштує й на яких умовах.", "Everything clear in advance: what, how much and on what terms.")}</p></div></section>

<section><div class="wrap">
<div class="grid">
<div class="card"><h3>{t("Ознайомча розмова", "Intro call")}</h3><p class="price">{t("Безкоштовно", "Free")}</p><p class="muted">{t("15 хвилин", "15 minutes")}</p><p>{t("Знайомимося, обговорюємо ваш запит і те, як я працюю.", "We meet, discuss your request and how I work.")}</p></div>
<div class="card"><h3>{t("Індивідуальна сесія", "Individual session")}</h3><p class="price">{PRICE} {t("грн", "UAH")}</p><p class="muted">{t("50 хвилин", "50 minutes")}</p><p>{t("Онлайн-консультація у форматі відеозв'язку.", "Online video consultation.")}</p></div>
<div class="card"><h3>{t(f"Пакет із {PACK_N} сесій", f"Package of {PACK_N} sessions")}</h3><p class="price">{PACK_PRICE} {t("грн", "UAH")}</p><p class="muted">{t(f"знижка {PACK_DISCOUNT}%", f"{PACK_DISCOUNT}% discount")}</p><p>{t("Для тих, хто готовий до регулярної роботи. Сесії по 50 хвилин.", "For those ready for regular work. 50-minute sessions.")}</p></div>
</div></div></section>

<section class="alt"><div class="wrap narrow">
<h2>{t("Формат", "Format")}</h2>
<ul class="ticks">
<li>{t("Лише онлайн, відеозв'язок: Zoom або Google Meet. За домовленістю можна й у Viber чи WhatsApp.", "Online only, by video: Zoom or Google Meet. Viber or WhatsApp video is possible by arrangement.")}</li>
<li>{t("Зазвичай зустрічі раз на тиждень, час узгоджуємо заздалегідь.", "Usually weekly meetings, time agreed in advance.")}</li>
<li>{t("Мови: українська та англійська.", "Languages: Ukrainian and English.")}</li>
<li>{t("Працюю з дорослими, підлітками й дітьми. Вартість і тривалість нейропсихологічної діагностики обговорюємо на ознайомчій розмові.", "I work with adults, teenagers and children. We discuss the cost and duration of neuropsychological diagnostics during the intro call.")}</li>
</ul>
<h2 class="mt">{t("Умови", "Terms")}</h2>
<ul class="ticks">
<li>{t("Скасувати або перенести сесію можна не пізніше ніж за 24 години.", "A session can be cancelled or rescheduled at least 24 hours in advance.")}</li>
<li>{t("Для підтвердження сесії потрібна передоплата. Спосіб оплати узгоджуємо під час запису.", "A prepayment is required to confirm a session. We agree on the payment method when booking.")}</li>
</ul>
</div></section>

<section><div class="wrap narrow">
<h2>{t("Як записатися", "How to book")}</h2>
<ol class="steps">
<li><h3>{t("Напишіть мені", "Write to me")}</h3><p>{t("У Direct в Instagram: посилання на сторінці «Контакти».", "In an Instagram direct message: see the Contacts page.")}</p></li>
<li><h3>{t("Оберемо час", "We pick a time")}</h3><p>{t("Я працюю з понеділка по суботу, з 9:00 до 21:00.", "I work Monday to Saturday, 9:00 to 21:00.")}</p></li>
<li><h3>{t("Зустрінемось онлайн", "We meet online")}</h3><p>{t("Надішлю посилання на зустріч напередодні.", "I will send the meeting link the day before.")}</p></li>
</ol>
<p><a class="btn" href="{u("contacts")}#book" data-track="cta_click" data-label="services">{t("Записатися", "Book now")}</a></p>
</div></section>"""
    return dict(
        title=t("Послуги й ціни: онлайн-консультація психологині", "Services and prices: online psychologist sessions"),
        desc=t(f"Безкоштовна розмова 15 хв, сесія 50 хв ({PRICE} грн), пакет із {PACK_N} сесій. Онлайн, умови скасування, як записатися.", f"Free 15-minute call, 50-minute session ({PRICE} UAH), package of {PACK_N} sessions. Online, cancellation terms, how to book."),
        body=body,
    )


def faq(c):
    t, u = c.t, c.u
    items = [
        ("first-session", t("Як проходить перша сесія?", "What happens in the first session?"),
         t("<p>Ми знайомимося, я розпитую про ваш запит і життєвий контекст, пояснюю, як проходить робота, і ми домовляємося про цілі. Ви самі вирішуєте, скільки розповідати. Після сесії ви можете вирішити, чи хочете продовжувати.</p>", "<p>We get to know each other, I ask about your request and life context, explain how the work goes and we agree on goals. You decide how much to share. After the session you can decide whether to continue.</p>")),
        ("confidentiality", t("Чи конфіденційні сесії?", "Are sessions confidential?"),
         t("<p>Так. Я не розкриваю інформацію про вас третім особам. Винятки передбачені законом, наприклад, пряма загроза життю й здоров'ю вашому чи інших людей. Про це я розповім заздалегідь.</p>", "<p>Yes. I do not disclose information about you to third parties. Exceptions are provided by law, for example a direct threat to your life or health or that of others. I will explain this beforehand.</p>")),
        ("how-many", t("Скільки сесій потрібно?", "How many sessions will I need?"),
         t("<p>Це залежить від запиту. Часто помітні зміни з'являються за кілька тижнів регулярної роботи, але гарантувати терміни чи результат неможливо. Ми будемо регулярно разом дивитися, чи допомагає робота.</p>", "<p>It depends on the request. Often noticeable changes appear within a few weeks of regular work, but timelines and results cannot be guaranteed. We will regularly review together whether the work helps.</p>")),
        ("online", t("Чи ефективна онлайн-терапія?", "Is online therapy effective?"),
         t("<p>Дослідження показують, що для багатьох запитів онлайн-формат працює так само добре, як очний. Потрібні лише стабільний інтернет і місце, де вас ніхто не почує.</p>", "<p>Research shows that for many requests the online format works as well as in-person. You only need a stable internet connection and a place where no one can overhear you.</p>")),
        ("psychologist-psychiatrist", t("Чим психолог відрізняється від психіатра?", "How is a psychologist different from a psychiatrist?"),
         t("<p>Психіатр лікар: ставить медичні діагнози й може призначати ліки. Психолог працює з розмовою, навичками й підтримкою та не призначає ліків. Якщо потрібна допомога психіатра, я підкажу про це.</p>", "<p>A psychiatrist is a medical doctor: makes medical diagnoses and can prescribe medication. A psychologist works through conversation, skills and support, and does not prescribe medication. If you need a psychiatrist, I will tell you.</p>")),
        ("cancellation", t("Що, якщо я не зможу прийти?", "What if I cannot attend?"),
         t("<p>Попередьте мене щонайменше за 24 години: сесію можна перенести без втрат. Пізніше скасування сесія вважається проведеною.</p>", "<p>Let me know at least 24 hours ahead and the session can be rescheduled at no cost. Later cancellations count as a held session.</p>")),
        ("cbt", t("Що таке КПТ і що означає нейропсихологічний погляд?", "What is CBT and what does a neuropsychological perspective mean?"),
         t("<p>КПТ (когнітивно-поведінкова терапія) допомагає помічати, як думки впливають на емоції й вчинки, і поступово змінювати те, що заважає. Нейропсихологічний погляд означає, що я також звертаю увагу на сон, стрес, навантаження й концентрацію.</p>", "<p>CBT (cognitive-behavioural therapy) helps you notice how thoughts affect emotions and actions, and gradually change what gets in the way. A neuropsychological perspective means I also look at sleep, stress, workload and concentration.</p>")),
    ]
    det = "".join(
        f'<details id="{i}"><summary>{q}</summary><div class="ans">{a}</div></details>' for i, q, a in items
    )
    body = f"""
<section class="page-head"><div class="wrap narrow"><h1>{t("Часті запитання", "FAQ")}</h1></div></section>
<section><div class="wrap narrow faq">{det}
<p class="mt">{t("Не знайшли відповідь?", "Did not find an answer?")} <a href="{u("contacts")}">{t("Напишіть мені", "Write to me")}</a>.</p></div></section>"""
    return dict(
        title=t("Часті запитання про консультації психолога", "Frequently asked questions about psychologist sessions"),
        desc=t("Як проходить перша сесія, конфіденційність, кількість сесій, онлайн-формат, різниця між психологом і психіатром, скасування, що таке КПТ.", "How the first session goes, confidentiality, number of sessions, online format, psychologist vs psychiatrist, cancellation, what CBT is."),
        body=body, faq=items,
    )


def contacts(c):
    t, ph = c.t, c.ph
    ch = c.contacts
    rows = ""
    for key, label in (("instagram", "Instagram"), ("telegram", "Telegram"), ("viber", "Viber"), ("facebook", "Facebook"), ("linkedin", "LinkedIn")):
        if key in ch:
            handle = ch[key].rstrip("/").split("/")[-1]
            rows += f'<li><strong>{label}</strong> <a href="{ch[key]}" target="_blank" rel="noopener" data-track="contact_click" data-label="{key}">@{handle}</a></li>' if key == "instagram" else f'<li><strong>{label}</strong> <a href="{ch[key]}" target="_blank" rel="noopener" data-track="contact_click" data-label="{key}">{ch[key]}</a></li>'
    for key, label in (("email", t("Пошта", "Email")), ("phone", t("Телефон", "Phone"))):
        if key in ch:
            href = f"mailto:{ch[key]}" if key == "email" else f"tel:{ch[key]}"
            rows += f'<li><strong>{label}</strong> <a href="{href}" data-track="contact_click" data-label="{key}">{ch[key]}</a></li>'
    ig = ch.get("instagram")
    book = (f'<a class="btn" href="{ig}" target="_blank" rel="noopener" data-track="contact_click" data-label="instagram_book">{t("Написати в Instagram", "Message on Instagram")}</a>'
            if ig else ph(t("Кнопка запису", "Booking button")))
    body = f"""
<section class="page-head"><div class="wrap narrow"><h1>{t("Контакти", "Contacts")}</h1></div></section>
<section id="book"><div class="wrap narrow">
<h2>{t("Записатися на розмову", "Book a call")}</h2>
<p>{t("Напишіть мені, і ми домовимося про безкоштовну ознайомчу розмову на 15 хвилин.", "Write to me and we will arrange a free 15-minute intro call.")}</p>
<p>{book}</p>
<h2 class="mt">{t("Усі канали", "All channels")}</h2>
<ul class="ticks plain">{rows}</ul>
<h2 class="mt">{t("Години роботи", "Working hours")}</h2>
<p>{c.hours}</p>
<p class="muted">{t("Часовий пояс: Київ.", "Time zone: Kyiv.")}</p>
</div></section>
<section class="alt"><div class="wrap narrow">
<h2>{t("Якщо потрібна термінова допомога", "If you need urgent help")}</h2>
<p>{t("Я не надаю екстреної допомоги й не відповідаю миттєво. Якщо вам або комусь поруч загрожує небезпека, зателефонуйте:", "I do not provide emergency care and do not reply instantly. If you or someone near you is in danger, call:")}</p>
<ul class="ticks"><li><strong>112</strong>: {t("єдиний номер екстрених служб", "the emergency services number")}</li>
<li><strong>Lifeline Ukraine 7333</strong>: {t("лінія емоційної підтримки", "emotional support line")}</li></ul>
</div></section>"""
    return dict(
        title=t("Контакти й запис до психологині Аліни Бубі", "Contacts and booking with psychologist Alina Buba"),
        desc=t("Як зв'язатися з психологинею Аліною Бубою та записатися на безкоштовну розмову: канали, години роботи, термінова допомога.", "How to contact psychologist Alina and book a free intro call: channels, working hours, urgent help."),
        body=body,
    )


def privacy(c):
    t, ph = c.t, c.ph
    owner = t("Власниця сайту: Аліна Буба (фізична особа)", "Site owner: Alina Buba (individual)")
    ig = c.contacts.get("instagram")
    contact = f'<a href="{ig}" target="_blank" rel="noopener">Instagram</a>' if ig else ""
    body = f"""
<section class="page-head"><div class="wrap narrow"><h1>{t("Політика конфіденційності й cookie", "Privacy and cookie policy")}</h1>
</div></section>
<section><div class="wrap narrow prose">
<h2>{t("Хто володіє сайтом", "Who owns the site")}</h2>
<p>{owner}. {t("Контакт з питань даних (Direct в Instagram):", "Contact for data questions:")} {contact}.</p>
<h2>{t("Які дані ми збираємо", "What data we collect")}</h2>
<p>{t("На сайті немає форм, реєстрації чи коментарів, тому ми не збираємо ваші імена, телефони чи листи через сайт. Коли ви пишете мені в месенджері чи соцмережі, діють правила цієї платформи.", "The site has no forms, registration or comments, so we do not collect your names, phone numbers or messages through the site. When you write to me in a messenger or social network, that platform’s rules apply.")}</p>
<h2>Google Analytics 4 {t("і cookie", "and cookies")}</h2>
<p>{t("За вашої згоди ми використовуємо Google Analytics 4, щоб розуміти, які сторінки читають. Він ставить cookie <code>_ga</code> і <code>_ga_*</code> та збирає знеособлену статистику: переглянуті сторінки, тип пристрою, приблизну країну. Ми не використовуємо рекламні функції, Google Signals і персоналізацію.", "With your consent we use Google Analytics 4 to understand which pages are read. It sets the cookies <code>_ga</code> and <code>_ga_*</code> and collects anonymised statistics: pages viewed, device type, approximate country. We do not use advertising features, Google Signals or personalisation.")}</p>
<p>{t("До вашого вибору скрипт Google Analytics не завантажується. Працює Google Consent Mode v2: усі типи зберігання за замовчуванням вимкнені.", "Until you choose, the Google Analytics script is not loaded. Google Consent Mode v2 is used: all storage types are denied by default.")}</p>
<h2>{t("Як відкликати згоду", "How to withdraw consent")}</h2>
<p>{t("Натисніть кнопку нижче або «Налаштування cookie» у футері. Після відмови ми видаляємо cookie <code>_ga*</code>.", "Press the button below or “Cookie settings” in the footer. After you decline, we delete the <code>_ga*</code> cookies.")}</p>
<p><button class="btn ghost" type="button" data-cookie-settings>{t("Налаштування cookie", "Cookie settings")}</button></p>
<h2>{t("Хто обробляє дані", "Who processes data")}</h2>
<p>{t("Google Ireland Limited (для користувачів у ЄЕЗ і Великій Британії) та Google LLC (США). Дані можуть передаватися за межі вашої країни на основі стандартних договірних положень.", "Google Ireland Limited (for users in the EEA and UK) and Google LLC (USA). Data may be transferred outside your country under standard contractual clauses.")}</p>
<h2>{t("Ваші права", "Your rights")}</h2>
<p>{t("Згідно із Законом України «Про захист персональних даних» і GDPR ви маєте право на доступ, виправлення, видалення даних, обмеження обробки та відкликання згоди. Напишіть нам за контактами вище.", "Under the Ukrainian Law on Personal Data Protection and the GDPR you have the right to access, rectify and erase data, restrict processing and withdraw consent. Write to us using the contacts above.")}</p>
<p class="muted">{t("Останнє оновлення:", "Last updated:")} {c.today}</p>
</div></section>"""
    return dict(
        title=t("Політика конфіденційності й cookie", "Privacy and cookie policy"),
        desc=t("Які дані збирає сайт, як працює Google Analytics 4 і згода на cookie, як відкликати згоду та які у вас права.", "What data the site collects, how Google Analytics 4 and cookie consent work, how to withdraw consent and your rights."),
        body=body,
    )


PAGES = {
    "home": home,
    "about": about,
    "specializations": specializations,
    "services": services,
    "faq": faq,
    "contacts": contacts,
    "privacy": privacy,
}
