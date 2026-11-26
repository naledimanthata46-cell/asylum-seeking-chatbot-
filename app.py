

from flask import Flask, render_template_string, request, jsonify
import re
import unicodedata

app = Flask(__name__)

# --------------------------------------------------
# RSA ASYLUM ASSISTANCE
# Free information chatbot - no API key required
# --------------------------------------------------

SOURCES = {
    "application": "https://help.unhcr.org/southafrica/topics/asylum/",
    "government": "https://www.gov.za/services/services-foreign-nationals/temporary-residence/asylum-seeker-and-refugee-permits",
    "rights": "https://help.unhcr.org/southafrica/get-help/documentation/asylum-seeker/",
    "renewal": "https://help.unhcr.org/southafrica/get-help/asylum/",
    "law": "https://www.dha.gov.za/images/REFUGEES_ACT_130_OF_1998.pdf",
    "legal": "https://help.unhcr.org/southafrica/",
    "offices": "https://help.unhcr.org/southafrica/topics/asylum/"
}

# Detailed information is maintained in one place.
# The language selector translates the interface and the
# core responses below. Detailed legal wording is kept
# in English where a reviewed translation is not available.

ANSWERS = {
    "en": {
        "greeting": "Hello! Welcome to RSA Asylum Assistance. I can help you understand the asylum process in South Africa, documents, rights, family dependants, renewals and legal support. What would you like to know?",
        "application": """HOW TO APPLY FOR ASYLUM IN SOUTH AFRICA

1. Approach a Refugee Reception Office (RRO) or another officially designated place.
2. Explain that you want to apply for asylum and follow the official registration procedure.
3. You will be asked for personal information and information about why you need protection.
4. Your photograph and fingerprints (biometrics) may be taken.
5. Declare your spouse and dependants, whether they are in South Africa or elsewhere.
6. You may be interviewed by a Refugee Status Determination Officer.
7. Ask for an interpreter if you cannot understand the language being used.
8. Keep copies of your application, permits, appointment notices and decisions.

The Department of Home Affairs manages the process. Apply as soon as possible after arriving. A Constitutional Court judgment in May 2026 confirmed that missing the five-day reporting period does not by itself remove a person's right to apply for asylum.

Your circumstances matter. Confirm the current procedure with Home Affairs or a qualified refugee-support organisation.""",
        "no_documents": """WHAT IF YOU DO NOT HAVE A PASSPORT OR IDENTITY DOCUMENTS?

Not having a passport or identity document does not automatically mean that you cannot apply for asylum.

The South African Government's information says people who have fled their country and do not have legal documents such as a passport or visa must apply at the nearest Refugee Reception Office.

Explain honestly which documents you do not have and why. Provide any available information that may help establish your identity and explain your circumstances.

Do not create, alter or submit false documents. Ask the Refugee Reception Office or a qualified refugee-support organisation what alternative steps apply to your situation.""",
        "documents": """DOCUMENT CHECKLIST

If available, prepare:
• Passport or other identity documents.
• Birth certificates for children.
• Marriage certificate or other information about a spouse, if applicable.
• Documents relating to dependants.
• Any available travel or entry documents.
• Documents or records that may help explain your reasons for seeking protection.
• Previous asylum documents, permits, appointment letters or Home Affairs correspondence, if applicable.
• Contact details and information about your current address.

Important:
This is a preparation checklist, not a rule that every document is compulsory. If you do not have a document, explain why. Ask Home Affairs or a qualified adviser what is required in your circumstances.""",
        "rights": """ASYLUM SEEKERS' RIGHTS AND RESPONSIBILITIES

According to UNHCR South Africa, asylum seekers have rights under the Constitution, except rights specifically reserved for South African citizens.

Rights and protections may include:
• The right to have an asylum application considered through the legal process.
• The right to an asylum-seeker document when the legal requirements are met.
• The right to seek renewal of the document while the claim is being processed.
• The right to request an interpreter when needed.
• Protection against unlawful treatment.

Responsibilities include:
• Follow South African law.
• Keep your asylum documentation safe.
• Attend appointments and follow instructions from Home Affairs.
• Renew your documentation when required.
• Keep your residential address updated with the relevant office.

The conditions printed on your own permit matter. Ask a qualified adviser if you are unsure about your rights in a particular situation.""",
        "family": """FAMILY MEMBERS AND DEPENDANTS

When applying for asylum, applicants must declare their spouses and dependants, whether they are in South Africa or elsewhere.

This may include:
• A husband or wife.
• Children.
• Other dependants, where relevant.

Family members may need to provide personal details and attend appointments for registration or biometrics.

Tell Home Affairs about your family circumstances truthfully. Ask a qualified refugee-law adviser how to add a family member if your circumstances change or a dependant was not included initially.""",
        "interview": """THE ASYLUM INTERVIEW

During the interview, an official may ask:
• Who you are and where you come from.
• Why you left your country.
• Why you fear returning.
• What happened to you or what you believe may happen if you return.
• Whether you have information or documents supporting your account.

Helpful reminders:
• Tell the truth.
• Explain events as clearly as you can.
• Do not invent information.
• Ask for an interpreter if you do not understand the language.
• Ask the official to explain a question if it is unclear.
• Keep copies of documents and written decisions.

This is general information. A legal adviser can help you prepare for your individual circumstances.""",
        "decision": """WHAT HAPPENS AFTER AN ASYLUM APPLICATION?

The Department of Home Affairs considers the application under the Refugees Act.

A decision may:
• Recognise the applicant as a refugee.
• Reject the application on one of the grounds provided for by law.

If the application is approved, the person may receive refugee status documentation under section 24.

If the application is rejected, read the written decision carefully. It should explain the outcome and relevant next steps.

Do not ignore a rejection or assume that you have unlimited time to respond. Appeal and review procedures have legal requirements and deadlines. Seek qualified legal assistance immediately.""",
        "renewal": """RENEWING ASYLUM DOCUMENTATION

Keep track of the expiry date and instructions on your own document.

UNHCR South Africa provides information about the Department of Home Affairs' online extension process for asylum-seeker and refugee documentation.

The process may require:
• Your permit number.
• A request for an extension.
• A copy of your current or expired document.
• Proof of your residential address or an accepted alternative.
• Separate requests for individual family members.

Requirements can change. Follow the latest instructions from Home Affairs and UNHCR. Be cautious of anyone demanding money for an official service that is supposed to be free.""",
        "appeal": """REJECTION, APPEALS AND LEGAL SUPPORT

If your asylum application is rejected:
1. Obtain and keep the written decision.
2. Read the reasons for rejection carefully.
3. Check which appeal or review procedure applies.
4. Check the deadline immediately.
5. Contact a qualified refugee-law organisation or legal practitioner as soon as possible.

Do not rely on this chatbot to calculate an appeal deadline. The correct procedure depends on the type of decision and your circumstances.

UNHCR South Africa provides information about legal assistance and refugee-support organisations.""",
        "offices": """REFUGEE RECEPTION OFFICES

UNHCR South Africa lists Refugee Reception Offices and provides information about the asylum process.

The offices listed in its asylum guidance include:
• Cape Town.
• Durban.
• Desmond Tutu Refugee Reception Office in Pretoria.
• Musina.
• Gqeberha.

Office arrangements and services can change. Check the latest information before travelling. Confirm which office can handle your application and whether an appointment or other arrangement is required.

Use the official UNHCR information link below rather than relying on an old address or phone number.""",
        "difference": """ASYLUM SEEKER VS REFUGEE

An asylum seeker is a person who has requested protection and whose application has not yet been finally decided.

A refugee is a person who has been recognised as meeting the legal definition of a refugee.

The Department of Home Affairs is responsible for determining refugee status in South Africa.""",
        "legal": """WHERE TO GET LEGAL HELP

For help with an individual asylum case, contact a qualified refugee-law practitioner or a recognised refugee-support organisation.

UNHCR South Africa provides information about organisations that may assist with:
• New asylum applications.
• Lost or expired documents.
• Rejected applications and appeals.
• Family-related matters.
• Children's cases.
• Questions about rights and documentation.

This chatbot provides general information. It is not a lawyer and cannot make decisions about an individual application.""",
        "privacy": """YOUR PRIVACY

For your safety, do not enter:
• Passport numbers.
• Permit numbers.
• Full home addresses.
• Passwords.
• Detailed personal accounts that could identify or endanger you.

This prototype does not need your personal case details to answer general questions. Avoid sharing sensitive information on public or shared devices.""",
        "fallback": "I don't have a verified answer for that exact question yet. You can ask me about applying for asylum, missing documents, the document checklist, rights, family dependants, interviews, decisions, renewals, appeals, Refugee Reception Offices or legal assistance."
    },

    "zu": {
        "greeting": "Sawubona! Siyakwamukela ku-RSA Asylum Assistance. Ngingakusiza ngolwazi mayelana nokufaka isicelo sokukhoseliswa eNingizimu Afrika, imibhalo, amalungelo, umndeni kanye nosizo lwezomthetho.",
        "application": "INDLELA YOKUFAKA ISICELO SOKUKHOSELISWA\n\n1. Yiya ehhovisi elisemthethweni labafuna ukukhoseliswa (Refugee Reception Office).\n2. Chaza ukuthi ufuna ukufaka isicelo sokukhoseliswa.\n3. Uzocelwa imininingwane yakho kanye nezizathu zokufuna ukuvikelwa.\n4. Kungathathwa isithombe neminwe yakho.\n5. Yisho umlingani wakho kanye nabantu abondliwa nguwe, noma ngabe bakuphi.\n6. Ungase uxoxisane nesikhulu esihlola izicelo.\n7. Cela umhumushi uma ungaluqondi ulimi olusetshenziswayo.\n8. Gcina amakhophi ayo yonke imibhalo nezaziso.\n\nImininingwane ingashintsha. Qinisekisa izinyathelo zakamuva kwa-Home Affairs noma enhlanganweni yosizo lwezomthetho.",
        "no_documents": "UMA UNGENAYO IPASIPOTI NOMA OMAZISI\n\nUkungabi nepasipoti noma umazisi akusho ngokuzenzakalela ukuthi awukwazi ukufaka isicelo sokukhoseliswa.\n\nUhulumeni waseNingizimu Afrika uthi abantu ababaleke emazweni abo futhi abangenawo amaphepha asemthethweni kufanele bafake isicelo ehhovisi eliseduze labafuna ukukhoseliswa.\n\nChaza ngokweqiniso ukuthi yimiphi imibhalo ongenayo nokuthi kungani. Cela iseluleko ngezinyathelo ezisebenza esimweni sakho. Ungalokothi usebenzise imibhalo engamanga.",
        "documents": "UHLU LOKULUNGISELELA IMIBHALO\n\nUma unayo, lungisa:\n• Ipasipoti noma eminye imibhalo kamazisi.\n• Izitifiketi zokuzalwa zezingane.\n• Isitifiketi somshado uma sikhona.\n• Imibhalo yabantu abondliwa nguwe.\n• Imibhalo yohambo noma yokungena ezweni.\n• Noma yiluphi ulwazi oluchaza izizathu zokufuna ukuvikelwa.\n• Imibhalo yakudala yakwa-Home Affairs.\n\nLolu uhlu lokulungiselela, akusho ukuthi yonke imibhalo iyimpoqo. Chaza uma ungenayo.",
        "rights": "AMALUNGELO KANYE NEZIBOPHO\n\nAbafuna ukukhoseliswa banamalungelo ngaphansi koMthethosisekelo waseNingizimu Afrika, ngaphandle kwamalungelo agcinelwe izakhamuzi kuphela.\n\nIzibopho zingafaka ukulandela imithetho, ukugcina imibhalo iphephile, ukuya kuma-aphoyintimenti, ukuvuselela imibhalo ngesikhathi kanye nokwazisa ihhovisi uma ikheli lishintsha.\n\nHlola imibandela esephepheni lakho futhi uthole usizo lwezomthetho uma ungaqiniseki.",
        "family": "UMNDENI NABANTU OBAONDLA\n\nUma ufaka isicelo, kufanele usho umlingani wakho kanye nabantu abondliwa nguwe, noma ngabe baseNingizimu Afrika noma bakwelinye izwe.\n\nLokhu kungafaka umyeni noma inkosikazi, izingane kanye nabanye abantu abondliwa nguwe. Buza umeluleki wezomthetho ukuthi ungamfaka kanjani umuntu omusha uma isimo somndeni sishintsha.",
        "fallback": "Anginayo impendulo eqinisekisiwe yalowo mbuzo okwamanje. Ungabuza ngokufaka isicelo, imibhalo, amalungelo, umndeni, ukuvuselela amaphepha, izikhalazo noma usizo lwezomthetho."
    },

    "xh": {
        "greeting": "Molo! Wamkelekile kwi-RSA Asylum Assistance. Ndingakunceda ngolwazi malunga nesicelo sokukhuselwa eMzantsi Afrika, amaxwebhu, amalungelo, usapho noncedo lwezomthetho.",
        "application": "INDLELA YOKUFAKA ISICELO SOKUKHUSELWA\n\n1. Yiya kwi-Refugee Reception Office okanye kwenye indawo egunyaziswe ngokusemthethweni.\n2. Chaza ukuba ufuna ukufaka isicelo sokukhuselwa.\n3. Uya kucelwa iinkcukacha zakho nezizathu zokufuna ukhuseleko.\n4. Iifoto neminwe yakho zinokuthathwa.\n5. Chaza iqabane lakho nabantu obaxhasayo, nokuba bakweliphi ilizwe.\n6. Ungadliwano-ndlebe negosa elihlola izicelo.\n7. Cela itoliki xa ungaluqondi ulwimi.\n8. Gcina iikopi zawo onke amaxwebhu nezaziso.\n\nQinisekisa iinkqubo zangoku kwi-Home Affairs okanye kumbutho woncedo lwezomthetho.",
        "no_documents": "UKUBA AWUNAYO IPASIPOTI OKANYE ISAZISI\n\nUkungabi nayo ipasipoti okanye isazisi akuthethi ngokuzenzekelayo ukuba awunakufaka isicelo sokukhuselwa.\n\nChaza ngokunyanisekileyo ukuba ngawaphi amaxwebhu ongenawo nokuba kutheni. Cela igosa okanye umbutho woncedo lwezomthetho akuchazele amanyathelo asebenzayo kwimeko yakho. Musa ukusebenzisa amaxwebhu obuxoki.",
        "documents": "ULUHLU LWAMAXWEBHU\n\nUkuba unawo, lungisa:\n• Ipasipoti okanye amanye amaxwebhu esazisi.\n• Izatifikethi zokuzalwa zabantwana.\n• Isatifikethi somtshato ukuba sikhona.\n• Amaxwebhu abantu obaxhasayo.\n• Amaxwebhu ohambo okanye okungena kweli lizwe.\n• Ulwazi olunokuchaza izizathu zokufuna ukhuseleko.\n• Amaxwebhu amadala e-Home Affairs.\n\nOlu luluhlu lokulungiselela, aluthethi ukuba onke amaxwebhu ayimfuneko. Chaza ukuba awunawo.",
        "rights": "AMALUNGELO NEEMFANELO\n\nAbantu abafuna ukukhuselwa banamalungelo phantsi koMgaqo-siseko waseMzantsi Afrika, ngaphandle kwamalungelo agcinelwe abemi kuphela.\n\nIimfanelo ziquka ukulandela imithetho, ukugcina amaxwebhu ekhuselekile, ukuya kwiintlanganiso ezimiselweyo, ukuhlaziya amaxwebhu ngexesha nokwazisa iofisi xa idilesi itshintsha.\n\nJonga imiqathango ekuxwebhu lwakho uze ufune uncedo lwezomthetho xa ungaqinisekanga.",
        "family": "USAPHO NABANTU OBAXHASAYO\n\nXa ufaka isicelo, chaza iqabane lakho nabo baxhomekeke kuwe, nokuba baseMzantsi Afrika okanye bakwelinye ilizwe.\n\nOku kunokuquka umyeni okanye inkosikazi, abantwana nabanye abantu obaxhasayo. Cela ingcebiso yezomthetho xa kufuneka wongeze ilungu losapho.",
        "fallback": "Andinayo impendulo eqinisekisiweyo yaloo mbuzo okwangoku. Ungabuza ngokufaka isicelo, amaxwebhu, amalungelo, usapho, ukuhlaziya amaxwebhu, izibheno okanye uncedo lwezomthetho."
    },

    "fr": {
        "greeting": "Bonjour ! Bienvenue sur RSA Asylum Assistance. Je peux vous aider à comprendre la procédure d'asile en Afrique du Sud, les documents, les droits, la famille et l'assistance juridique.",
        "application": "COMMENT DEMANDER L'ASILE EN AFRIQUE DU SUD\n\n1. Rendez-vous dans un Refugee Reception Office ou un autre lieu officiellement désigné.\n2. Expliquez que vous souhaitez demander l'asile.\n3. Vous devrez fournir vos informations personnelles et expliquer pourquoi vous demandez une protection.\n4. Vos empreintes digitales et une photographie peuvent être prises.\n5. Déclarez votre conjoint et les personnes à votre charge, où qu'elles se trouvent.\n6. Vous pouvez être convoqué à un entretien.\n7. Demandez un interprète si vous ne comprenez pas la langue utilisée.\n8. Conservez des copies de tous les documents et avis.\n\nVérifiez toujours la procédure actuelle auprès du ministère de l'Intérieur ou d'une organisation juridique qualifiée.",
        "no_documents": "SI VOUS N'AVEZ PAS DE PASSEPORT OU DE PIÈCE D'IDENTITÉ\n\nL'absence de passeport ou de pièce d'identité ne signifie pas automatiquement que vous ne pouvez pas demander l'asile.\n\nExpliquez honnêtement quels documents vous n'avez pas et pourquoi. Demandez aux agents ou à une organisation d'aide juridique quelles démarches s'appliquent à votre situation. N'utilisez jamais de faux documents.",
        "documents": "LISTE DES DOCUMENTS À PRÉPARER\n\nSi vous les avez, préparez :\n• Passeport ou autres pièces d'identité.\n• Actes de naissance des enfants.\n• Certificat de mariage, le cas échéant.\n• Documents concernant les personnes à charge.\n• Documents de voyage ou d'entrée.\n• Informations pouvant expliquer votre demande de protection.\n• Anciens documents ou courriers du ministère de l'Intérieur.\n\nCette liste sert à vous préparer. Tous ces documents ne sont pas nécessairement obligatoires. Expliquez si un document vous manque.",
        "rights": "DROITS ET RESPONSABILITÉS\n\nLes demandeurs d'asile bénéficient des droits constitutionnels en Afrique du Sud, à l'exception des droits réservés aux citoyens.\n\nLes responsabilités peuvent inclure le respect de la loi, la conservation des documents, la présence aux rendez-vous, le renouvellement des documents et la mise à jour de l'adresse auprès du bureau compétent.\n\nVérifiez les conditions inscrites sur votre propre document et demandez conseil si nécessaire.",
        "family": "FAMILLE ET PERSONNES À CHARGE\n\nLors de la demande, déclarez votre conjoint et les personnes à votre charge, qu'ils se trouvent en Afrique du Sud ou ailleurs.\n\nCela peut inclure un époux ou une épouse, des enfants et d'autres personnes à charge. Demandez conseil sur la procédure à suivre si votre situation familiale change.",
        "fallback": "Je ne dispose pas encore d'une réponse vérifiée à cette question précise. Vous pouvez poser une question sur la demande d'asile, les documents, les droits, la famille, le renouvellement, les recours ou l'aide juridique."
    },

    "sw": {
        "greeting": "Habari! Karibu kwenye RSA Asylum Assistance. Ninaweza kukusaidia kuelewa mchakato wa kuomba hifadhi Afrika Kusini, nyaraka, haki, familia na msaada wa kisheria.",
        "application": "JINSI YA KUOMBA HIFADHI AFRIKA KUSINI\n\n1. Nenda katika Refugee Reception Office au eneo jingine lililoidhinishwa rasmi.\n2. Eleza kwamba unataka kuomba hifadhi.\n3. Utaombwa kutoa taarifa zako na sababu za kuhitaji ulinzi.\n4. Picha na alama za vidole zinaweza kuchukuliwa.\n5. Taja mwenzi wako na wategemezi wako, popote walipo.\n6. Unaweza kuitwa kwa mahojiano.\n7. Omba mkalimani ikiwa huelewi lugha inayotumika.\n8. Hifadhi nakala za nyaraka na barua zote.\n\nThibitisha utaratibu wa sasa kwa Home Affairs au shirika la msaada wa kisheria.",
        "no_documents": "IKIWA HUNA PASIPOTI AU KITAMBULISHO\n\nKutokuwa na pasipoti au kitambulisho hakumaanishi moja kwa moja kwamba huwezi kuomba hifadhi.\n\nEleza kwa ukweli nyaraka ambazo huna na sababu zake. Uliza maafisa au shirika la msaada wa kisheria kuhusu hatua zinazohusika katika hali yako. Usitumie nyaraka za uongo.",
        "documents": "ORODHA YA NYARAKA ZA KUANDAA\n\nIkiwa unazo, andaa:\n• Pasipoti au nyaraka nyingine za utambulisho.\n• Vyeti vya kuzaliwa vya watoto.\n• Cheti cha ndoa ikiwa kinahusika.\n• Nyaraka za wategemezi.\n• Nyaraka za safari au kuingia nchini.\n• Taarifa zinazoweza kueleza sababu za kuomba ulinzi.\n• Nyaraka za zamani za Home Affairs.\n\nHii ni orodha ya maandalizi. Si lazima kila nyaraka iwe nayo kila mtu. Eleza ikiwa huna nyaraka fulani.",
        "rights": "HAKI NA WAJIBU\n\nWanaotafuta hifadhi wana haki chini ya Katiba ya Afrika Kusini, isipokuwa haki zilizotengwa kwa raia pekee.\n\nWajibu unaweza kujumuisha kufuata sheria, kutunza nyaraka, kuhudhuria miadi, kufanya upya nyaraka inapohitajika na kusasisha anwani yako kwa ofisi husika.\n\nAngalia masharti yaliyo kwenye hati yako na uombe ushauri ikiwa huna uhakika.",
        "family": "FAMILIA NA WATEGEMEZI\n\nUnapoomba hifadhi, taja mwenzi wako na watu wanaokutegemea, iwe wako Afrika Kusini au nchi nyingine.\n\nHii inaweza kujumuisha mume au mke, watoto na wategemezi wengine. Omba ushauri kuhusu kuongeza mwanafamilia ikiwa hali yako itabadilika.",
        "fallback": "Sina jibu lililothibitishwa kwa swali hilo kwa sasa. Unaweza kuuliza kuhusu maombi ya hifadhi, nyaraka, haki, familia, kufanya upya nyaraka, rufaa au msaada wa kisheria."
    },

    "af": {
        "greeting": "Hallo! Welkom by RSA Asylum Assistance. Ek kan jou help met inligting oor die asielproses in Suid-Afrika, dokumente, regte, gesinslede en regshulp.",
        "application": "HOE OM ASIEL IN SUID-AFRIKA AAN TE VRA\n\n1. Gaan na 'n Refugee Reception Office of 'n ander amptelik aangewese plek.\n2. Verduidelik dat jy om asiel wil aansoek doen.\n3. Jy sal persoonlike besonderhede en redes vir jou versoek om beskerming moet gee.\n4. Jou foto en vingerafdrukke kan geneem word.\n5. Verklaar jou gade en afhanklikes, waar hulle ook al is.\n6. Jy kan vir 'n onderhoud ontbied word.\n7. Vra vir 'n tolk as jy nie die taal verstaan nie.\n8. Hou afskrifte van alle dokumente en kennisgewings.\n\nBevestig die huidige prosedure by Home Affairs of 'n gekwalifiseerde regsorganisasie.",
        "no_documents": "AS JY NIE 'N PASPOORT OF IDENTITEITSDOKUMENT HET NIE\n\nDie gebrek aan 'n paspoort of identiteitsdokument beteken nie outomaties dat jy nie om asiel kan aansoek doen nie.\n\nVerduidelik eerlik watter dokumente jy nie het nie en waarom. Vra die amptenare of 'n regsorganisasie watter stappe op jou situasie van toepassing is. Moenie vals dokumente gebruik nie.",
        "documents": "DOKUMENTKONTROLELYS\n\nIndien beskikbaar, berei voor:\n• Paspoort of ander identiteitsdokumente.\n• Geboortesertifikate van kinders.\n• Huweliksertifikaat, indien van toepassing.\n• Dokumente van afhanklikes.\n• Reis- of toegangs dokumente.\n• Inligting wat jou redes vir beskerming kan verduidelik.\n• Vorige Home Affairs-dokumente.\n\nDit is 'n voorbereidingslys. Nie elke dokument is noodwendig verpligtend nie. Verduidelik indien jy 'n dokument nie het nie.",
        "rights": "REGTE EN VERANTWOORDELIKHEDE\n\nAsielsoekers het grondwetlike regte in Suid-Afrika, behalwe regte wat uitsluitlik vir burgers gereserveer is.\n\nVerantwoordelikhede kan insluit om die wet te gehoorsaam, dokumente veilig te hou, afsprake by te woon, dokumente betyds te hernu en jou adres by die toepaslike kantoor by te werk.\n\nKontroleer die voorwaardes op jou eie dokument en vra raad indien jy onseker is.",
        "family": "GESIN EN AFHANKLIKES\n\nWanneer jy aansoek doen, verklaar jou gade en afhanklikes, of hulle nou in Suid-Afrika of elders is.\n\nDit kan 'n man of vrou, kinders en ander afhanklikes insluit. Vra regsadvies oor hoe om 'n familielid by te voeg as jou omstandighede verander.",
        "fallback": "Ek het nog nie 'n geverifieerde antwoord op daardie spesifieke vraag nie. Jy kan vra oor aansoeke, dokumente, regte, gesin, hernuwing, appèlle of regshulp."
    },

    "st": {
        "greeting": "Dumela! Rea o amohela ho RSA Asylum Assistance. Nka o thusa ka tlhahisoleseding mabapi le kopo ya botshabelo Afrika Borwa, ditokomane, ditokelo, lelapa le thuso ya molao.",
        "application": "MOKHOA OA HO ETSA KOPO EA BOTSHABELO\n\n1. Eya Refugee Reception Office kapa sebakeng se seng se dumelletsweng ka molao.\n2. Hlalosa hore o batla ho etsa kopo ya botshabelo.\n3. O tla kopuwa dintlha tsa hao le mabaka a ho batla tshireletso.\n4. Senepe le dikgatiso tsa menwana di ka nkuwa.\n5. Bolela molekane wa hao le batho bao o ba hlokomelang, ho sa tsotellehe moo ba leng teng.\n6. O ka bitswa bakeng sa puisano.\n7. Kopa toloko haeba o sa utlwisise puo e sebediswang.\n8. Boloka dikopi tsa ditokomane tsohle le ditsebiso.\n\nNetefatsa mehato ya hajwale ho Home Affairs kapa mokgatlong wa thuso ya molao.",
        "no_documents": "HAEBA O SE NA PASEPORO KAPA TOKOMANE YA BOITSEBISO\n\nHo se be le pasepoto kapa tokomane ya boitsebiso ha ho bolele ka bohona hore o ke ke wa etsa kopo ya botshabelo.\n\nHlalosa ka nnete hore na ke ditokomane dife tseo o se nang tsona le lebaka. Kopa keletso ho balaodi kapa mokgatlong wa thuso ya molao. O se ke wa sebedisa ditokomane tsa bohata.",
        "documents": "LENANE LA DITOKOMANE\n\nHaeba o na le tsona, lokisetsa:\n• Pasepoto kapa ditokomane tse ding tsa boitsebiso.\n• Disetifikeiti tsa tswalo tsa bana.\n• Setifikeiti sa lenyalo haeba se le teng.\n• Ditokomane tsa batho bao o ba hlokomelang.\n• Ditokomane tsa leeto kapa tsa ho kena naheng.\n• Tlhahisoleseding e hlalosang mabaka a ho batla tshireletso.\n• Ditokomane tsa kgale tsa Home Affairs.\n\nLena ke lenane la boitokisetso, ha le bolele hore tokomane e nngwe le e nngwe e a hlokahala. Hlalosa haeba o se na tokomane.",
        "rights": "DITOKELO LE BOIKARABELO\n\nBatho ba batlang botshabelo ba na le ditokelo tlasa Molaotheo wa Afrika Borwa, ntle le ditokelo tse boloketsweng baahi feela.\n\nBoikarabelo bo ka kenyelletsa ho latela molao, ho boloka ditokomane di bolokehile, ho ya dikopanong, ho ntjhafatsa ditokomane ka nako le ho tsebisa ofisi ha aterese e fetoha.\n\nSheba maemo a ngotsweng tokomaneng ya hao mme o kope keletso haeba o sa tiiseha.",
        "family": "LELAPA LE BATHO BA ITHEKGETSENG KA WENA\n\nHa o etsa kopo, bolela molekane wa hao le batho ba ithekgileng ka wena, ebang ba Afrika Borwa kapa naheng e nngwe.\n\nSena se ka kenyelletsa monna kapa mosadi, bana le batho ba bang ba ithekgileng ka wena. Kopa keletso ya molao haeba o hloka ho eketsa setho sa lelapa.",
        "fallback": "Ha ke na karabo e netefaditsweng ya potso eo hona jwale. O ka botsa ka kopo ya botshabelo, ditokomane, ditokelo, lelapa, ho ntjhafatsa ditokomane, boipiletso kapa thuso ya molao."
    }
}

LANGUAGE_NAMES = {
    "en": "English",
    "zu": "isiZulu",
    "xh": "isiXhosa",
    "st": "Sesotho",
    "af": "Afrikaans",
    "fr": "Français",
    "sw": "Kiswahili"
}

UI = {
    "en": {
        "subtitle": "Information and guidance for people seeking asylum in South Africa",
        "placeholder": "Type your question here...",
        "send": "Send",
        "welcome": "Ask a question to get started.",
        "notice": "This is an information tool, not a legal service. Always confirm important details with Home Affairs or a qualified legal-support organisation.",
        "sources": "Official information sources",
        "clear": "Clear conversation"
    },
    "zu": {
        "subtitle": "Ulwazi nesiqondiso sabantu abafuna ukukhoseliswa eNingizimu Afrika",
        "placeholder": "Bhala umbuzo wakho lapha...",
        "send": "Thumela",
        "welcome": "Buza umbuzo ukuze uqale.",
        "notice": "Leli ithuluzi lolwazi, akulona isevisi yezomthetho. Qinisekisa imininingwane ebalulekile kwa-Home Affairs noma enhlanganweni yosizo lwezomthetho.",
        "sources": "Imithombo yolwazi esemthethweni",
        "clear": "Sula ingxoxo"
    },
    "xh": {
        "subtitle": "Ulwazi nesikhokelo kubantu abafuna ukukhuselwa eMzantsi Afrika",
        "placeholder": "Bhala umbuzo wakho apha...",
        "send": "Thumela",
        "welcome": "Buza umbuzo ukuze uqalise.",
        "notice": "Esi sisixhobo solwazi, asiyonkonzo yezomthetho. Qinisekisa iinkcukacha ezibalulekileyo kwi-Home Affairs okanye kumbutho woncedo lwezomthetho.",
        "sources": "Imithombo yolwazi esemthethweni",
        "clear": "Cima incoko"
    },
    "st": {
        "subtitle": "Tlhahisoleseding le tataiso bakeng sa batho ba batlang botshabelo Afrika Borwa",
        "placeholder": "Ngola potso ya hao mona...",
        "send": "Romela",
        "welcome": "Botsa potso ho qala.",
        "notice": "Sena ke sesebediswa sa tlhahisoleseding, ha se tshebeletso ya molao. Netefatsa dintlha tsa bohlokwa ho Home Affairs kapa mokgatlong wa thuso ya molao.",
        "sources": "Mehlodi ya tlhahisoleseding ya semmuso",
        "clear": "Hlakola moqoqo"
    },
    "af": {
        "subtitle": "Inligting en leiding vir mense wat asiel in Suid-Afrika soek",
        "placeholder": "Tik jou vraag hier...",
        "send": "Stuur",
        "welcome": "Vra 'n vraag om te begin.",
        "notice": "Hierdie is 'n inligtingshulpmiddel, nie 'n regsdienste nie. Bevestig belangrike besonderhede by Home Affairs of 'n gekwalifiseerde regsorganisasie.",
        "sources": "Amptelike inligtingsbronne",
        "clear": "Vee gesprek uit"
    },
    "fr": {
        "subtitle": "Informations et conseils pour les personnes demandant l'asile en Afrique du Sud",
        "placeholder": "Écrivez votre question ici...",
        "send": "Envoyer",
        "welcome": "Posez une question pour commencer.",
        "notice": "Cet outil fournit des informations générales et ne remplace pas un service juridique. Vérifiez les informations importantes auprès des autorités ou d'une organisation qualifiée.",
        "sources": "Sources officielles",
        "clear": "Effacer la conversation"
    },
    "sw": {
        "subtitle": "Taarifa na mwongozo kwa watu wanaotafuta hifadhi Afrika Kusini",
        "placeholder": "Andika swali lako hapa...",
        "send": "Tuma",
        "welcome": "Uliza swali ili kuanza.",
        "notice": "Hiki ni chombo cha taarifa, si huduma ya kisheria. Thibitisha taarifa muhimu kwa Home Affairs au shirika la msaada wa kisheria.",
        "sources": "Vyanzo rasmi vya taarifa",
        "clear": "Futa mazungumzo"
    }
}

# Match specific topics before general topics.
# Word boundaries prevent "hi" matching inside "while".
INTENTS = [
    ("no_documents", [
        "no passport", "without a passport", "don't have a passport",
        "do not have a passport", "no documents", "without documents",
        "no identity document", "no id", "lost my passport",
        "lost my documents", "identity papers", "missing documents"
    ]),
    ("appeal", [
        "appeal", "appealing", "rejected", "rejection",
        "refused", "unfounded", "manifestly unfounded",
        "review my case", "challenge a decision"
    ]),
    ("renewal", [
        "renew", "renewal", "extend my permit", "extension",
        "expired permit", "expiry", "expires", "section 22 renewal",
        "online extension"
    ]),
    ("rights", [
        "rights", "right", "responsibilities", "responsibility",
        "while my application", "while waiting", "pending application",
        "can i work", "work permit", "school", "education",
        "healthcare", "arrest", "detained"
    ]),
    ("family", [
        "family", "dependant", "dependent", "spouse", "husband",
        "wife", "children", "child", "son", "daughter",
        "add my child", "family member"
    ]),
    ("documents", [
        "documents", "paperwork", "checklist", "what must i bring",
        "what should i bring", "supporting evidence", "birth certificate"
    ]),
    ("interview", [
        "interview", "interpreter", "translation", "fingerprints",
        "biometrics", "what will they ask", "what questions"
    ]),
    ("offices", [
        "office", "offices", "where do i apply", "where can i apply",
        "refugee reception", "rro", "location", "address", "pretoria",
        "durban", "cape town", "musina", "gqeberha"
    ]),
    ("decision", [
        "decision", "approved", "approval", "what happens next",
        "section 24", "refugee status", "after applying"
    ]),
    ("difference", [
        "difference between refugee and asylum seeker",
        "what is a refugee", "what is an asylum seeker"
    ]),
    ("legal", [
        "lawyer", "legal help", "legal assistance", "human rights organisation",
        "organisation", "help with my case", "who can help"
    ]),
    ("privacy", [
        "privacy", "personal information", "data protection",
        "is my information safe"
    ]),
    ("application", [
        "apply", "application", "asylum process", "how do i start",
        "how to apply", "want to seek asylum", "seeking asylum"
    ])
]

GREETINGS = {
    "hello", "hi", "hey", "good morning", "good afternoon",
    "good evening", "sawubona", "molo", "dumela", "habari"
}


def normalise(text):
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s]", " ", text).strip()


def find_intent(question):
    cleaned = normalise(question)

    if cleaned in GREETINGS:
        return "greeting"

    # Match exact phrases or complete words, not accidental substrings.
    for intent, phrases in INTENTS:
        for phrase in phrases:
            phrase_clean = normalise(phrase)
            if re.search(r"(?<!\w)" + re.escape(phrase_clean) + r"(?!\w)", cleaned):
                return intent

    # Follow-up questions with a clear topic.
    if any(word in cleaned.split() for word in ["more", "explain", "details", "continue"]):
        return "application"

    return "fallback"


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    language = str(data.get("language", "en"))

    if language not in LANGUAGE_NAMES:
        language = "en"

    if not question:
        return jsonify({"answer": "Please enter a question.", "sources": []})

    if len(question) > 1500:
        return jsonify({
            "answer": "Please shorten your question to 1,500 characters or fewer.",
            "sources": []
        })

    intent = find_intent(question)
    answer = ANSWERS.get(language, ANSWERS["en"]).get(intent)

    # Some less common topics are available in English until
    # their translations can be properly reviewed.
    if not answer:
        answer = ANSWERS["en"].get(intent, ANSWERS["en"]["fallback"])
        if language != "en":
            answer += "\n\n(Additional detailed information is currently provided in English to avoid unreliable legal translations.)"

    source_map = {
        "application": ["application", "government", "law"],
        "no_documents": ["government", "application"],
        "documents": ["application", "law"],
        "rights": ["rights", "law"],
        "family": ["application", "law"],
        "interview": ["application", "law"],
        "decision": ["application", "law"],
        "renewal": ["renewal", "government"],
        "appeal": ["legal", "law"],
        "offices": ["application"],
        "difference": ["application", "government"],
        "legal": ["legal"],
        "privacy": ["law"]
    }

    sources = [
        {"name": key.replace("_", " ").title(), "url": SOURCES[key]}
        for key in source_map.get(intent, [])
    ]

    return jsonify({
        "answer": answer,
        "sources": sources,
        "topic": intent
    })


PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="RSA Asylum Assistance provides general information about the asylum process in South Africa.">
<title>RSA Asylum Assistance</title>

<style>
:root {
    --green: #176b52;
    --dark: #173b35;
    --light: #f3f7f5;
    --white: #ffffff;
    --border: #dce7e1;
    --muted: #62736d;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: var(--light);
    color: var(--dark);
    line-height: 1.6;
}

header {
    background: var(--white);
    border-bottom: 1px solid var(--border);
    padding: 16px 6%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    flex-wrap: wrap;
}

.brand {
    font-size: 19px;
    font-weight: bold;
    color: var(--green);
}

.language-area {
    display: flex;
    align-items: center;
    gap: 8px;
}

select, button, input {
    font: inherit;
}

select {
    padding: 9px 12px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: white;
    color: var(--dark);
}

.hero {
    background: linear-gradient(130deg, #176b52, #214b43);
    color: white;
    padding: 55px 8%;
    text-align: center;
}

.hero h1 {
    font-size: clamp(27px, 5vw, 42px);
    margin: 0 0 10px;
}

.hero p {
    max-width: 700px;
    margin: auto;
    opacity: .94;
}

main {
    max-width: 1050px;
    margin: 30px auto;
    padding: 0 18px;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px;
    margin-bottom: 28px;
}

.info-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
}

.info-card h3 {
    margin: 0 0 6px;
    color: var(--green);
    font-size: 16px;
}

.info-card p {
    margin: 0;
    color: var(--muted);
    font-size: 14px;
}

.chat {
    background: white;
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 5px 20px rgba(20, 55, 40, .05);
}

.chat-heading {
    padding: 18px 20px;
    background: #e8f2ed;
    font-weight: bold;
    color: var(--dark);
}

.messages {
    padding: 18px;
    min-height: 260px;
    max-height: 500px;
    overflow-y: auto;
}

.message {
    padding: 13px 15px;
    margin: 12px 0;
    border-radius: 12px;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

.user {
    background: #e1f1e9;
    margin-left: 12%;
}

.bot {
    background: #f1f4f2;
    margin-right: 8%;
}

.message strong {
    display: block;
    margin-bottom: 5px;
}

.sources {
    margin-top: 12px;
    font-size: 13px;
}

.sources a {
    display: inline-block;
    margin: 4px 8px 4px 0;
    color: var(--green);
    text-decoration: underline;
}

.chat-form {
    display: flex;
    gap: 10px;
    padding: 15px;
    border-top: 1px solid var(--border);
}

.chat-form input {
    flex: 1;
    min-width: 0;
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 12px;
    outline-color: var(--green);
}

.send-button {
    background: var(--green);
    color: white;
    border: 0;
    border-radius: 9px;
    padding: 11px 20px;
    cursor: pointer;
}

.send-button:hover { background: #10533f; }

.tools {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    padding: 0 15px 15px;
    flex-wrap: wrap;
}

.secondary-button {
    border: 1px solid var(--border);
    background: white;
    color: var(--dark);
    border-radius: 8px;
    padding: 8px 12px;
    cursor: pointer;
}

.notice {
    background: #fff8e8;
    border: 1px solid #f0dfb7;
    border-radius: 10px;
    padding: 15px;
    margin: 20px 0;
    font-size: 13px;
    color: #66552c;
}

.official-links {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin-top: 20px;
}

.official-links a {
    display: block;
    margin: 8px 0;
    color: var(--green);
}

footer {
    text-align: center;
    color: var(--muted);
    font-size: 13px;
    padding: 25px 15px;
}

@media(max-width: 600px) {
    header { padding: 14px 5%; }
    .hero { padding: 40px 6%; }
    .chat-form { flex-direction: column; }
    .send-button { width: 100%; }
    .user { margin-left: 5%; }
    .bot { margin-right: 3%; }
}
</style>
</head>

<body>

<header>
    <div class="brand">RSA Asylum Assistance</div>
    <div class="language-area">
        <label for="language" id="language-label">Language:</label>
        <select id="language" onchange="changeLanguage()">
            <option value="en">English</option>
            <option value="zu">isiZulu</option>
            <option value="xh">isiXhosa</option>
            <option value="st">Sesotho</option>
            <option value="af">Afrikaans</option>
            <option value="fr">Français</option>
            <option value="sw">Kiswahili</option>
        </select>
    </div>
</header>

<section class="hero">
    <h1>RSA Asylum Assistance</h1>
    <p id="subtitle">Information and guidance for people seeking asylum in South Africa</p>
</section>

<main>

    <section class="info-grid">
        <div class="info-card">
            <h3>Application Process</h3>
            <p>Understand the general steps involved in applying for asylum.</p>
        </div>
        <div class="info-card">
            <h3>Documents</h3>
            <p>Learn what documents may be useful and what to do if you have none.</p>
        </div>
        <div class="info-card">
            <h3>Rights and Responsibilities</h3>
            <p>Find general information about asylum-seeker rights and responsibilities.</p>
        </div>
        <div class="info-card">
            <h3>Family Support</h3>
            <p>Learn about declaring spouses and dependants.</p>
        </div>
    </section>

    <section class="chat">
        <div class="chat-heading">RSA Assistance Guide</div>

        <div class="messages" id="messages" aria-live="polite">
            <div class="message bot" id="welcome-message">
                <strong>RSA Assistance Guide</strong>
                Ask a question to get started.
            </div>
        </div>

        <form class="chat-form" id="chat-form">
            <input
                type="text"
                id="user-message"
                placeholder="Type your question here..."
                maxlength="1500"
                autocomplete="off"
                required
            >
            <button class="send-button" type="submit" id="send-button">Send</button>
        </form>

        <div class="tools">
            <button class="secondary-button" type="button" onclick="clearConversation()" id="clear-button">
                Clear conversation
            </button>
            <span id="status" aria-live="polite"></span>
        </div>
    </section>

    <div class="notice" id="notice">
        This is an information tool, not a legal service. Always confirm important details with Home Affairs or a qualified legal-support organisation.
    </div>

    <section class="official-links">
        <h3 id="sources-heading">Official information sources</h3>
        <a href="https://www.gov.za/services/services-foreign-nationals/temporary-residence/asylum-seeker-and-refugee-permits" target="_blank" rel="noopener noreferrer">
            South African Government – Asylum-seeker and refugee permits
        </a>
        <a href="https://help.unhcr.org/southafrica/topics/asylum/" target="_blank" rel="noopener noreferrer">
            UNHCR South Africa – Asylum and refugee status
        </a>
        <a href="https://help.unhcr.org/southafrica/get-help/documentation/asylum-seeker/" target="_blank" rel="noopener noreferrer">
            UNHCR – Asylum-seeker rights and responsibilities
        </a>
        <a href="https://help.unhcr.org/southafrica/" target="_blank" rel="noopener noreferrer">
            UNHCR South Africa – Help and support
        </a>
    </section>

</main>

<footer>
    RSA Asylum Assistance | General information prototype
</footer>

<script>
const uiTranslations = {
    en: {
        subtitle: "Information and guidance for people seeking asylum in South Africa",
        placeholder: "Type your question here...",
        send: "Send",
        welcome: "Ask a question to get started.",
        notice: "This is an information tool, not a legal service. Always confirm important details with Home Affairs or a qualified legal-support organisation.",
        sources: "Official information sources",
        clear: "Clear conversation"
    },
    zu: {
        subtitle: "Ulwazi nesiqondiso sabantu abafuna ukukhoseliswa eNingizimu Afrika",
        placeholder: "Bhala umbuzo wakho lapha...",
        send: "Thumela",
        welcome: "Buza umbuzo ukuze uqale.",
        notice: "Leli ithuluzi lolwazi, akulona isevisi yezomthetho. Qinisekisa imininingwane ebalulekile kwa-Home Affairs noma enhlanganweni yosizo lwezomthetho.",
        sources: "Imithombo yolwazi esemthethweni",
        clear: "Sula ingxoxo"
    },
    xh: {
        subtitle: "Ulwazi nesikhokelo kubantu abafuna ukukhuselwa eMzantsi Afrika",
        placeholder: "Bhala umbuzo wakho apha...",
        send: "Thumela",
        welcome: "Buza umbuzo ukuze uqalise.",
        notice: "Esi sisixhobo solwazi, asiyonkonzo yezomthetho. Qinisekisa iinkcukacha ezibalulekileyo kwi-Home Affairs okanye kumbutho woncedo lwezomthetho.",
        sources: "Imithombo yolwazi esemthethweni",
        clear: "Cima incoko"
    },
    st: {
        subtitle: "Tlhahisoleseding le tataiso bakeng sa batho ba batlang botshabelo Afrika Borwa",
        placeholder: "Ngola potso ya hao mona...",
        send: "Romela",
        welcome: "Botsa potso ho qala.",
        notice: "Sena ke sesebediswa sa tlhahisoleseding, ha se tshebeletso ya molao. Netefatsa dintlha tsa bohlokwa ho Home Affairs kapa mokgatlong wa thuso ya molao.",
        sources: "Mehlodi ya semmuso",
        clear: "Hlakola moqoqo"
    },
    af: {
        subtitle: "Inligting en leiding vir mense wat asiel in Suid-Afrika soek",
        placeholder: "Tik jou vraag hier...",
        send: "Stuur",
        welcome: "Vra 'n vraag om te begin.",
        notice: "Hierdie is 'n inligtingshulpmiddel, nie 'n regsdienste nie. Bevestig belangrike besonderhede by Home Affairs of 'n gekwalifiseerde regsorganisasie.",
        sources: "Amptelike inligtingsbronne",
        clear: "Vee gesprek uit"
    },
    fr: {
        subtitle: "Informations et conseils pour les personnes demandant l'asile en Afrique du Sud",
        placeholder: "Écrivez votre question ici...",
        send: "Envoyer",
        welcome: "Posez une question pour commencer.",
        notice: "Cet outil fournit des informations générales et ne remplace pas un service juridique. Vérifiez les informations importantes auprès des autorités ou d'une organisation qualifiée.",
        sources: "Sources officielles",
        clear: "Effacer la conversation"
    },
    sw: {
        subtitle: "Taarifa na mwongozo kwa watu wanaotafuta hifadhi Afrika Kusini",
        placeholder: "Andika swali lako hapa...",
        send: "Tuma",
        welcome: "Uliza swali ili kuanza.",
        notice: "Hiki ni chombo cha taarifa, si huduma ya kisheria. Thibitisha taarifa muhimu kwa Home Affairs au shirika la msaada wa kisheria.",
        sources: "Vyanzo rasmi vya taarifa",
        clear: "Futa mazungumzo"
    }
};

function changeLanguage() {
    const lang = document.getElementById("language").value;
    const t = uiTranslations[lang] || uiTranslations.en;

    document.getElementById("subtitle").textContent = t.subtitle;
    document.getElementById("user-message").placeholder = t.placeholder;
    document.getElementById("send-button").textContent = t.send;
    document.getElementById("notice").textContent = t.notice;
    document.getElementById("sources-heading").textContent = t.sources;
    document.getElementById("clear-button").textContent = t.clear;

    const welcome = document.getElementById("welcome-message");
    if (welcome) {
        welcome.textContent = "";
        const heading = document.createElement("strong");
        heading.textContent = "RSA Assistance Guide";
        welcome.appendChild(heading);
        welcome.appendChild(document.createTextNode(t.welcome));
    }
}

function addMessage(type, heading, message, sources = []) {
    const messages = document.getElementById("messages");
    const bubble = document.createElement("div");
    bubble.className = "message " + type;

    const title = document.createElement("strong");
    title.textContent = heading;
    bubble.appendChild(title);

    bubble.appendChild(document.createTextNode(message));

    if (sources.length > 0) {
        const sourceArea = document.createElement("div");
        sourceArea.className = "sources";

        const sourceTitle = document.createElement("strong");
        sourceTitle.textContent = "Read more:";
        sourceArea.appendChild(sourceTitle);

        sources.forEach(source => {
            const link = document.createElement("a");
            link.href = source.url;
            link.textContent = source.name;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            sourceArea.appendChild(link);
        });

        bubble.appendChild(sourceArea);
    }

    messages.appendChild(bubble);
    messages.scrollTop = messages.scrollHeight;
}

async function sendMessage(event) {
    event.preventDefault();

    const input = document.getElementById("user-message");
    const status = document.getElementById("status");
    const question = input.value.trim();

    if (!question) return;

    const language = document.getElementById("language").value;

    addMessage("user", "You", question);
    input.value = "";
    status.textContent = "Finding information...";

    const sendButton = document.getElementById("send-button");
    sendButton.disabled = true;

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                question: question,
                language: language
            })
        });

        if (!response.ok) {
            throw new Error("The server returned an error.");
        }

        const data = await response.json();

        addMessage(
            "bot",
            "RSA Assistance Guide",
            data.answer,
            data.sources || []
        );

        status.textContent = "";
    } catch (error) {
        addMessage(
            "bot",
            "RSA Assistance Guide",
            "Sorry, I could not retrieve an answer. Please check your connection and try again."
        );
        status.textContent = "Connection problem";
    } finally {
        sendButton.disabled = false;
        input.focus();
    }
}

function clearConversation() {
    const messages = document.getElementById("messages");
    const lang = document.getElementById("language").value;
    const t = uiTranslations[lang] || uiTranslations.en;

    messages.innerHTML = "";

    const welcome = document.createElement("div");
    welcome.className = "message bot";
    welcome.id = "welcome-message";

    const heading = document.createElement("strong");
    heading.textContent = "RSA Assistance Guide";

    welcome.appendChild(heading);
    welcome.appendChild(document.createTextNode(t.welcome));
    messages.appendChild(welcome);
}

document.getElementById("chat-form").addEventListener("submit", sendMessage);
</script>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
