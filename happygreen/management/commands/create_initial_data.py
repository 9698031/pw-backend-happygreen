import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from happygreen.models import (
    Badge, RecognizedObject, Product, Quiz, QuizQuestion, QuizOption, Challenge
)
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Crea dati iniziali per testare l\'applicazione HappyGreen'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creazione dati iniziali...')

        # Creazione badge
        self.create_badges()

        # Creazione oggetti riconosciuti
        self.create_recognized_objects()

        # Creazione prodotti
        self.create_products()

        # Creazione quiz
        self.create_quizzes()

        # Creazione sfide
        self.create_challenges()

        self.stdout.write(self.style.SUCCESS('Dati iniziali creati con successo!'))

    def create_badges(self):
        badges = [
            {
                'name': 'Eco-Detective',
                'description': 'Hai identificato correttamente 10 oggetti riciclabili.',
                'points_required': 50
            },
            {
                'name': 'Green Guardian',
                'description': 'Hai completato 5 sfide ecologiche.',
                'points_required': 100
            },
            {
                'name': 'Recycle Master',
                'description': 'Hai scansionato 20 oggetti e li hai classificati correttamente.',
                'points_required': 200
            },
            {
                'name': 'Quiz Champion',
                'description': 'Hai risposto correttamente a 50 domande sui quiz di sostenibilità.',
                'points_required': 150
            },
            {
                'name': 'Eco-Influencer',
                'description': 'Hai condiviso 10 post con il tuo gruppo.',
                'points_required': 75
            },
            {
                'name': 'Planet Protector',
                'description': 'Hai guadagnato 500 punti totali nella app.',
                'points_required': 500
            },
        ]

        created_count = 0
        for badge_data in badges:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults={
                    'description': badge_data['description'],
                    'points_required': badge_data['points_required'],
                    # Per un'app reale, sarebbe necessario creare icone reali
                    'icon': None
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'- Creati {created_count} nuovi badge')

    def create_recognized_objects(self):
        objects = [
            {
                'name': 'Bottiglia di Plastica',
                'description': 'Bottiglia d\'acqua in plastica PET',
                'category': 'plastica',
                'eco_impact': 'Una bottiglia di plastica può impiegare fino a 450 anni per decomporsi in natura.',
                'recycling_info': 'Riciclabile nella raccolta differenziata della plastica. Schiacciala per risparmiare spazio.',
                'sustainability_score': 3
            },
            {
                'name': 'Lattina di Alluminio',
                'description': 'Lattina per bevande in alluminio',
                'category': 'metallo',
                'eco_impact': 'L\'estrazione di alluminio richiede molta energia, ma l\'alluminio riciclato usa il 95% di energia in meno.',
                'recycling_info': 'Riciclabile all\'infinito senza perdere qualità. Va nella raccolta differenziata dei metalli.',
                'sustainability_score': 7
            },
            {
                'name': 'Giornale',
                'description': 'Quotidiano a stampa',
                'category': 'carta',
                'eco_impact': 'Per produrre carta vengono abbattuti alberi, ma la carta è biodegradabile in 2-5 mesi.',
                'recycling_info': 'Riciclabile nella raccolta differenziata della carta. Rimuovi eventuali parti plastificate.',
                'sustainability_score': 6
            },
            {
                'name': 'Bottiglia di Vetro',
                'description': 'Bottiglia in vetro per bevande',
                'category': 'vetro',
                'eco_impact': 'Il vetro è fatto di materiali naturali e può essere riciclato infinite volte senza perdere qualità.',
                'recycling_info': 'Va nella raccolta differenziata del vetro. Rimuovi tappi in metallo o plastica.',
                'sustainability_score': 8
            },
            {
                'name': 'Sacchetto di Plastica',
                'description': 'Sacchetto di plastica monouso',
                'category': 'plastica',
                'eco_impact': 'I sacchetti di plastica impiegano fino a 1000 anni per decomporsi e causano gravi danni alla fauna marina.',
                'recycling_info': 'Quando pulito, va nella raccolta differenziata della plastica. Meglio usare borse riutilizzabili.',
                'sustainability_score': 1
            },
            {
                'name': 'Batteria',
                'description': 'Batteria alcalina o ricaricabile',
                'category': 'rifiuti pericolosi',
                'eco_impact': 'Le batterie contengono metalli pesanti e sostanze chimiche dannose per l\'ambiente.',
                'recycling_info': 'Non gettare mai nella spazzatura normale. Portare ai punti di raccolta appositi o in isola ecologica.',
                'sustainability_score': 2
            },
            {
                'name': 'Tetrapak',
                'description': 'Contenitore per alimenti in cartone poliaccoppiato',
                'category': 'carta',
                'eco_impact': 'Composto da carta, plastica e alluminio, il tetrapak è più difficile da riciclare rispetto alla carta pura.',
                'recycling_info': 'In molti comuni va nella raccolta carta. Verifica le regole locali di smaltimento.',
                'sustainability_score': 5
            },
            {
                'name': 'Smartphone',
                'description': 'Telefono cellulare intelligente',
                'category': 'elettronica',
                'eco_impact': 'Contiene metalli rari e componenti che richiedono estrazione mineraria dannosa per l\'ambiente.',
                'recycling_info': 'Mai gettare nei rifiuti normali. Portare ai centri di raccolta RAEE o restituire al rivenditore quando si acquista uno nuovo.',
                'sustainability_score': 3
            },
            {
                'name': 'Foglia',
                'description': 'Foglia di albero deciduo',
                'category': 'organico',
                'eco_impact': 'Le foglie sono completamente biodegradabili e naturali, parte del ciclo ecologico.',
                'recycling_info': 'Può essere compostata o gettata nell\'umido. In natura si decompone in pochi mesi.',
                'sustainability_score': 10
            },
            {
                'name': 'Bicchiere di Carta',
                'description': 'Bicchiere monouso in carta',
                'category': 'carta',
                'eco_impact': 'Sebbene sia di carta, spesso contiene un rivestimento plastico che ne complica il riciclo.',
                'recycling_info': 'Verifica le regole locali. In alcuni comuni va nell\'indifferenziato a causa del rivestimento.',
                'sustainability_score': 4
            },
        ]

        created_count = 0
        for obj_data in objects:
            obj, created = RecognizedObject.objects.get_or_create(
                name=obj_data['name'],
                defaults={
                    'description': obj_data['description'],
                    'category': obj_data['category'],
                    'eco_impact': obj_data['eco_impact'],
                    'recycling_info': obj_data['recycling_info'],
                    'sustainability_score': obj_data['sustainability_score'],
                    'image': None  # Per un'app reale, bisognerebbe creare immagini reali
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'- Creati {created_count} nuovi oggetti riconoscibili')

    def create_products(self):
        products = [
            {
                'barcode': '8001097047991',
                'name': 'Acqua Naturale Bio',
                'description': 'Bottiglia d\'acqua naturale in vetro da 1 litro',
                'manufacturer': 'EcoWater',
                'eco_friendly': True,
                'recyclable': True,
                'sustainability_score': 8,
                'eco_info': 'Bottiglia in vetro completamente riciclabile. L\'azienda usa energia rinnovabile per la produzione.',
                'alternatives': 'Considera l\'uso di una borraccia riutilizzabile o filtri per l\'acqua del rubinetto.'
            },
            {
                'barcode': '5449000000996',
                'name': 'Cola Regular',
                'description': 'Bevanda gassata in bottiglia di plastica da 1,5 litri',
                'manufacturer': 'MegaSoft Drinks',
                'eco_friendly': False,
                'recyclable': True,
                'sustainability_score': 4,
                'eco_info': 'Bottiglia in plastica PET riciclabile, ma la produzione e il trasporto hanno un impatto ambientale significativo.',
                'alternatives': 'Preferisci bevande in lattina di alluminio o in vetro, che hanno un impatto minore.'
            },
            {
                'barcode': '3017624010701',
                'name': 'Crema Spalmabile al Cacao',
                'description': 'Crema spalmabile al cacao e nocciole in barattolo di vetro',
                'manufacturer': 'SweetLife',
                'eco_friendly': False,
                'recyclable': True,
                'sustainability_score': 5,
                'eco_info': 'Barattolo in vetro riciclabile, ma contiene olio di palma che contribuisce alla deforestazione.',
                'alternatives': 'Cerca prodotti con olio di palma sostenibile certificato o alternative senza olio di palma.'
            },
            {
                'barcode': '7290011989909',
                'name': 'Fazzoletti di Carta Ecologici',
                'description': 'Confezione di fazzoletti di carta da 10 pacchetti',
                'manufacturer': 'GreenPaper',
                'eco_friendly': True,
                'recyclable': True,
                'sustainability_score': 7,
                'eco_info': 'Prodotti con carta riciclata e imballaggio ridotto. L\'azienda pianta un albero per ogni tonnellata di carta utilizzata.',
                'alternatives': 'Considera l\'uso di fazzoletti in stoffa lavabili per ridurre ulteriormente i rifiuti.'
            },
            {
                'barcode': '8424358088320',
                'name': 'Detersivo Concentrato',
                'description': 'Detersivo per lavatrice concentrato in bottiglia',
                'manufacturer': 'CleanEco',
                'eco_friendly': True,
                'recyclable': True,
                'sustainability_score': 8,
                'eco_info': 'Formula biodegradabile con tensioattivi di origine vegetale. La bottiglia è fatta con plastica riciclata.',
                'alternatives': 'Prova detersivi solidi o in polvere che richiedono meno imballaggio.'
            },
            {
                'barcode': '3017620422003',
                'name': 'Biscotti al Cioccolato',
                'description': 'Confezione di biscotti al cioccolato',
                'manufacturer': 'BiscuitCo',
                'eco_friendly': False,
                'recyclable': False,
                'sustainability_score': 3,
                'eco_info': 'Imballaggio non riciclabile con pellicola metallizzata. Contiene ingredienti non sostenibili.',
                'alternatives': 'Scegli biscotti con imballaggio in carta o cartone riciclabile, o prova a farli in casa.'
            },
            {
                'barcode': '8718309289881',
                'name': 'Dentifricio Naturale',
                'description': 'Dentifricio con ingredienti naturali in tubetto',
                'manufacturer': 'NatureDent',
                'eco_friendly': True,
                'recyclable': False,
                'sustainability_score': 6,
                'eco_info': 'Ingredienti naturali e biodegradabili, ma il tubetto è difficile da riciclare.',
                'alternatives': 'Prova dentifricio in compresse o in barattolo di vetro.'
            },
            {
                'barcode': '4902430698146',
                'name': 'Shampoo Convenzionale',
                'description': 'Shampoo per capelli in flacone di plastica',
                'manufacturer': 'HairCare',
                'eco_friendly': False,
                'recyclable': True,
                'sustainability_score': 4,
                'eco_info': 'Contiene microplastiche e sostanze chimiche potenzialmente dannose per l\'ambiente acquatico.',
                'alternatives': 'Prova shampoo solido, che non richiede flacone di plastica, o marche eco-certificate.'
            },
            {
                'barcode': '8437004478443',
                'name': 'Caffè Biologico Equosolidale',
                'description': 'Caffè biologico in confezione compostabile',
                'manufacturer': 'FairBeans',
                'eco_friendly': True,
                'recyclable': True,
                'sustainability_score': 9,
                'eco_info': 'Coltivato biologicamente, commercio equo, confezione compostabile. L\'azienda supporta progetti sociali nelle comunità produttrici.',
                'alternatives': 'Questo è già un\'ottima scelta sostenibile!'
            },
            {
                'barcode': '4006381333931',
                'name': 'Batterie Usa e Getta',
                'description': 'Confezione di batterie alcaline AA',
                'manufacturer': 'PowerMax',
                'eco_friendly': False,
                'recyclable': False,
                'sustainability_score': 1,
                'eco_info': 'Le batterie usa e getta contengono metalli pesanti e sostanze tossiche. Richiedono smaltimento speciale.',
                'alternatives': 'Usa batterie ricaricabili, che possono essere riutilizzate centinaia di volte.'
            },
        ]

        created_count = 0
        for product_data in products:
            product, created = Product.objects.get_or_create(
                barcode=product_data['barcode'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'manufacturer': product_data['manufacturer'],
                    'eco_friendly': product_data['eco_friendly'],
                    'recyclable': product_data['recyclable'],
                    'sustainability_score': product_data['sustainability_score'],
                    'eco_info': product_data['eco_info'],
                    'alternatives': product_data['alternatives'],
                    'image': None  # Per un'app reale, bisognerebbe creare immagini reali
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'- Creati {created_count} nuovi prodotti')

    def create_quizzes(self):
        quizzes = [
            {
                'title': 'Riciclaggio 101',
                'description': 'Verifica le tue conoscenze sulle basi del riciclaggio e della raccolta differenziata',
                'points': 20,
                'questions': [
                    {
                        'question': 'In quale contenitore dovrebbero essere gettate le bottiglie di vetro?',
                        'options': [
                            {'text': 'Contenitore del vetro', 'is_correct': True},
                            {'text': 'Contenitore della plastica', 'is_correct': False},
                            {'text': 'Rifiuti indifferenziati', 'is_correct': False},
                            {'text': 'Contenitore della carta', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Quale di questi oggetti NON può essere riciclato nella plastica?',
                        'options': [
                            {'text': 'Bottiglia di acqua', 'is_correct': False},
                            {'text': 'Piatti di plastica puliti', 'is_correct': False},
                            {'text': 'Giocattoli di plastica', 'is_correct': True},
                            {'text': 'Flacone di detersivo', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Cosa significa l\'acronimo RAEE?',
                        'options': [
                            {'text': 'Rifiuti Alimentari ed Elettrodomestici', 'is_correct': False},
                            {'text': 'Riciclaggio Automatico Energia Elettrica', 'is_correct': False},
                            {'text': 'Rifiuti di Apparecchiature Elettriche ed Elettroniche', 'is_correct': True},
                            {'text': 'Raccolta Avanzata Elementi Ecologici', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Qual è il simbolo del riciclaggio?',
                        'options': [
                            {'text': 'Un cerchio', 'is_correct': False},
                            {'text': 'Un triangolo di frecce', 'is_correct': True},
                            {'text': 'Una stella', 'is_correct': False},
                            {'text': 'Un quadrato', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Cosa deve essere fatto prima di riciclare i contenitori alimentari?',
                        'options': [
                            {'text': 'Devono essere sterilizzati', 'is_correct': False},
                            {'text': 'Devono essere puliti dai residui di cibo', 'is_correct': True},
                            {'text': 'Devono essere schiacciati completamente', 'is_correct': False},
                            {'text': 'Devono essere separati in componenti', 'is_correct': False},
                        ]
                    },
                ]
            },
            {
                'title': 'Sostenibilità Ambientale',
                'description': 'Quanto ne sai sulle pratiche sostenibili e sull\'impatto ambientale delle nostre azioni?',
                'points': 25,
                'questions': [
                    {
                        'question': 'Quale delle seguenti azioni riduce maggiormente l\'impronta di carbonio?',
                        'options': [
                            {'text': 'Usare lampadine a LED', 'is_correct': False},
                            {'text': 'Ridurre il consumo di carne', 'is_correct': True},
                            {'text': 'Fare docce brevi', 'is_correct': False},
                            {'text': 'Usare sacchetti riutilizzabili', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Cosa significa "a km zero"?',
                        'options': [
                            {'text': 'Prodotti senza emissioni di CO2', 'is_correct': False},
                            {'text': 'Prodotti coltivati o realizzati localmente', 'is_correct': True},
                            {'text': 'Prodotti gratuiti', 'is_correct': False},
                            {'text': 'Prodotti che non richiedono energia', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Quale di questi mezzi di trasporto è più ecologico per una persona?',
                        'options': [
                            {'text': 'Auto a benzina', 'is_correct': False},
                            {'text': 'Auto elettrica', 'is_correct': False},
                            {'text': 'Bicicletta', 'is_correct': True},
                            {'text': 'Motocicletta', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Quanto tempo impiega una bottiglia di plastica a decomporsi in natura?',
                        'options': [
                            {'text': 'Circa 10 anni', 'is_correct': False},
                            {'text': 'Circa 50 anni', 'is_correct': False},
                            {'text': 'Circa 450 anni', 'is_correct': True},
                            {'text': 'Circa 1000 anni', 'is_correct': False},
                        ]
                    },
                    {
                        'question': 'Qual è lo scopo principale delle energie rinnovabili?',
                        'options': [
                            {'text': 'Ridurre il costo dell\'energia', 'is_correct': False},
                            {'text': 'Produrre energia senza esaurire risorse naturali', 'is_correct': True},
                            {'text': 'Creare più posti di lavoro', 'is_correct': False},
                            {'text': 'Aumentare la produzione di energia', 'is_correct': False},
                        ]
                    },
                ]
            },
        ]

        created_quizzes = 0
        created_questions = 0
        created_options = 0

        for quiz_data in quizzes:
            quiz, created = Quiz.objects.get_or_create(
                title=quiz_data['title'],
                defaults={
                    'description': quiz_data['description'],
                    'points': quiz_data['points']
                }
            )
            if created:
                created_quizzes += 1

            for question_data in quiz_data['questions']:
                question, q_created = QuizQuestion.objects.get_or_create(
                    quiz=quiz,
                    question=question_data['question']
                )
                if q_created:
                    created_questions += 1

                for option_data in question_data['options']:
                    option, o_created = QuizOption.objects.get_or_create(
                        question=question,
                        text=option_data['text'],
                        defaults={
                            'is_correct': option_data['is_correct']
                        }
                    )
                    if o_created:
                        created_options += 1

        self.stdout.write(
            f'- Creati {created_quizzes} nuovi quiz con {created_questions} domande e {created_options} opzioni')

    def create_challenges(self):
        now = timezone.now()

        challenges = [
            {
                'title': 'Settimana Senza Plastica',
                'description': 'Evita di utilizzare prodotti in plastica monouso per una settimana. Scansiona almeno 5 alternative ecologiche che hai utilizzato.',
                'points': 50,
                'start_date': now - timedelta(days=5),
                'end_date': now + timedelta(days=25)
            },
            {
                'title': 'Caccia al Rifiuto',
                'description': 'Trova e raccogli rifiuti abbandonati in un parco o in spiaggia. Scatta foto prima e dopo la tua raccolta.',
                'points': 75,
                'start_date': now - timedelta(days=10),
                'end_date': now + timedelta(days=20)
            },
            {
                'title': 'Pianta un Albero',
                'description': 'Partecipa all\'iniziativa di piantare alberi nella tua città. Registrati come volontario e condividi la tua esperienza.',
                'points': 100,
                'start_date': now + timedelta(days=15),
                'end_date': now + timedelta(days=45)
            },
            {
                'title': 'Mobilità Sostenibile',
                'description': 'Usa solo mezzi di trasporto sostenibili (bici, piedi, mezzi pubblici) per una settimana. Traccia i tuoi spostamenti.',
                'points': 60,
                'start_date': now - timedelta(days=2),
                'end_date': now + timedelta(days=12)
            },
            {
                'title': 'Cucina a Impatto Zero',
                'description': 'Prepara 5 pasti utilizzando solo ingredienti locali e di stagione, evitando imballaggi superflui.',
                'points': 40,
                'start_date': now,
                'end_date': now + timedelta(days=30)
            },
        ]

        created_count = 0
        for challenge_data in challenges:
            challenge, created = Challenge.objects.get_or_create(
                title=challenge_data['title'],
                defaults={
                    'description': challenge_data['description'],
                    'points': challenge_data['points'],
                    'start_date': challenge_data['start_date'],
                    'end_date': challenge_data['end_date']
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'- Create {created_count} nuove sfide')