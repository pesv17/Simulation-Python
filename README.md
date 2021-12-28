# Simulation-Python
There's three files. One with the actual code (Simsims.py) one with a json "converter" (jsonprogram.py) and one json file (simsims.json) that stores what jsonprogram created.
There's two predetermined scenarios in jsonprogram.py, these can be changed accordingly. The idea is to use these scenarios to run the simulation within Simsims.py and then the outcome will be stored in simsims.json.

# Description (Swedish):

# Bakgrund
För att studera flöden vill vi göra en simulering av en liten miniatyrvärld. Världen består av arbetare som jobbar, äter, sover och förökar sig. De bor i en värld av fabriker, åkrar, restauranger och hus.

I simuleringen används en modifierad version av s.k. petrinät. Utan att fördjupa oss i dessa nät kan man nämna att petrinät är ett grafiskt och matematiskt modelleringsverktyg utvecklat av Carl Petri 1962. Näten består av platser (places),  övergångar (transitions) samt inkanaler och utkanaler (arcs) som förbinder platser och övergångar. På dessa nät flödar resurser (tokens). I platserna lagras eventuella resurser i väntan på att de behövs i en övergång. Övergångar hämtar en eller flera resurser på inkanaler från en eller flera platser. Dessa resurser behandlas sedan på ett bestämt sätt av övergången. Antingen förbrukas eller skickas resurser vidare eller så kan nya resurser skapas. De resurser som blir resultatet i en övergång skickas via utkanaler till en eller flera platser. En övergång kan enbart hämta och behandla resurser om samtliga resurser den kräver finns tillgängliga via övergångens inkanaler. 

I bilderna nedan visas två exempel där petrinät styr trafikljus. Respektive lampa lyser när det finns en resurs i motsvarande plats. I det vänstra exemplet lyser alltså trafikljuset rött. Den övergång som kan agera är rg som alltså kan ta den enda resursen från platsen red och skicka den vidare till platsen green. I det högra exemplet styrs nu två trafikljus där de inte ska kunna bli gröna samtidigt. I detta fall lyser båda ljusen röda. Övergången yr1 har precis tagit en resurs från yellow1 och lagt var sin resurs i red1 och x1. Den enda övergång som kan agera nu är rg2. Övergången rg2 kan ta resurser från x1 och red2 och lägga en resurs i green2.


I näten gäller alltså följande egenskaper:

Det är övergångarna som styr simuleringen så tillvida att det är dem som kollar och förändrar tillståndet hos de andra komponenterna (platser och resurser).  Resurser och platser har alltså ingen egen vilja utan resurser förbrukas från platser i den ordning som resurser efterfrågas av övergångar.
Varje övergång arbetar autonomt, dvs den känner inte till något om världen förutom den information den kan få från kopplade platser via inkanaler.
En övergång kan enbart utföra sin uppgift om den får tillgång till samtliga resurser som krävs, annars hoppar den över en omgång och testar igen senare. En övergång måste alltså ha möjlighet att fråga en plats om tillgängliga resurser innan den hämtar resurser.
SimSims-världen
Resurser
Resurser flödar på nätet. Nya resurser kan skapas och försvinner ur näten i noderna.

Arbetarna är navet i simuleringen. De är dessa som producerar och förbrukar varor och mat, bor i husen och förökar sig. Livet tar dock på en arbetare som när hen skapats har 100% i livskraft men dör (tas bort från simuleringen) när hen kommer ned till 0%.


Mat produceras i åkernoder och äts av arbetare. Mat kan ha olika kvalitet.


Produkter produceras i fabriksnoder och förbrukas av arbetare.


# Platser (Places)
I platser väntar resurser i väntan på att de efterfrågas i någon övergång. Till platserna kan ett obegränsat antal inkanaler och utkanaler kopplas. Respektive behållare kan enbart lagra resurser av en i förväg bestämd typ.

# Vägar (Roads) kallas de noder där arbetare väntar. Att vara ute på vägarna gillar inte arbetare då där bildas köer. Ju längre kön är desto mer känner de hur livskraften rinner ur dem.

Kommentar: För att förenkla kan man tänka sig att en arbetare förlorar livskraft i och med att denne läggs till i platsen, ju fler som redan finns på vägen (platsen) desto mer minskar arbetarens livskraft. Om arbetaren då dör läggs den inte till i kön. Vägen ska alltså fungera som en kö för arbetarna (FIFO - först in, först ut).


# Lador (Barns) lagrar mat. Mat förbrukas i form av en kö (FIFO - först in, först ut).



# Lager (Storage) lagrar produkter. Produkter förbrukas i form av en stack (LIFO - sist in, först ut ut).

# Övergångar (Transitions)
Övergångar har ett fixt antal inkanaler. Via inkanalerna bevakar övergångar de platser som inkanalerna är kopplade till. När platserna har de resurser som krävs hämtas de via inkanalen. Väl inne i övergången sker den process som respektive övergång är konstruerad för. När övergången är klar skickar den eventuella resurser via kopplade utkanaler till en eller flera platser.

Fabriker producerar produkter av en arbetare. Det tar längre tid för en arbetare med låg livskraft att färdigställa en produkt än för en arbetare med god livskraft. Livet i fabriken är inte heller en dans på rosor utan skadligt och medan arbetaren befinner sig i fabriken minskas dennes livskraft vilket också kan variera mellan olika fabriker. Rätt vad det är kan också olyckor ske där den arme arbetaren dödas. Input till en fabrik är en arbetare och output är en produkt och en arbetare (om denne överlevt).


Åkrar producerar den mat som arbetarna behöver. Arbetet på åkern tar inte på livskraften men är inte riskfritt. Olyckor kan ske som förbrukar livskraft. Input till en åker är en arbetare och output är en enhet mat och en arbetare (om denne överlevt).


Matsalar används för att ge arbetarna mat efter hårt arbete. De känner hur livskraften återställs en smula medan de smaskar på en bit mat. Kvaliteten på maten kan skilja något vilket gör att livskraften inte återställs lika mycket vid varje besök i en matsal. Är kvaliteten riktigt dålig finns i stället risk för matförgiftning vilket istället minskar livskraften. Input till en matsal är en arbetare och en enhet mat och output är en arbetare (om denne överlevt).



Hus. Hem ljuva hem. Hemma i husen tar man igen sig och har skoj mellan lakanen. Är en arbetare ensam i huset tar denne enbart igen sig och vilar en stund medan dennes livskraft ökar en smula. Kommer det in två arbetare samtidigt finns det däremot ingen tid till vila och livskraften ökar inte, däremot finns det chans till att de tu blir tre. Vid varje besök av en eller två arbetare förbrukas en produkt. Input till ett hus är en eller två arbetare samt en produkt och output är en till tre arbetare. Observera att en arbetare inte har tid att vänta på ytterligare arbetare utan båda måste i så fall komma in i huset samtidigt som produkten.


# Simulering
Man barjar med att bygga upp ett simuleringsnät där platser och övergångar kopplas samman med kanaler. Flera olika komponenter av samma sort kan (ska) användas till att bygga stora nät. Resurser kan initialt enbart läggas i platserna. Efter att ett nät är uppbyggt kan simuleringen börja och den fortsätter så länge som det finns arbetare kvar i nätet. Nedan visas ett exempel där det finns ett lager, två vägar, två lador, två fabriker, två fält, tre matsalar, och fyra hus.

