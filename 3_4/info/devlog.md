## Izstrādes sesija – [16.05.2025.]
- Pabeidzu implementāciju abos ietvaros, kā arī notestēju galvenās funkcijas.
- Sakomplektēju un lokāli instalēju pēdējās iterācijas, bet saskaros ar problēmām ElectronJS projektā.

Grūtības:
- Neradās kļūdas sakomplektējot ElectronJS projektu, bet bija nepieciešams terminālis ar Admin privilēģiju, lai pabeigtu sakomplektēšanas procesu, jo tā laikā tika radīti symlinki.
- Instalējot ElectronJS versiju radās kļūdas, kas bija saistīta ar importiem. Kļūda noveda uz to, ka lietojumprogrammas galvenā loga instance netika izveidota, bet lietojumprogrammas paliek ieslēgta. Mēģinot atinstalēt bojāto versiju uzlec paziņojums, ka ir jārestartē dators -  iemesls šim ir tas, ka tiek mēģināts atinstalēt ieslēgtu lietojumprogrammu. Attiecīgi lietojumprogrammu jāizslēdz ar Task manager.

**Sastaptās grūtības / izaicinājumi:**  
- ElectronJs kļūda produkcijas vidē. Problēma bija electron-dl implementācija.

**Piezīmes / pārdomas:**
- N/A

## Izstrādes sesija – [15.05.2025.]

**Izstrādes sesijas ilgums:**  
- 8h

**Veiktie uzdevumi:**  
- Implementēju interneta savienojuma noteikšanas funkciju abos ietvaros, kas līdz šim tika izlaists, jo nebiju izvēlējies, cik funkcionāla būs ideja – izvēlos implementēt vienkārši un uzdevumam pietiekami adekvātu risinājumu.
- Implementēju rudimentāru paziņojumu sistēmu abos ietvaros, ar kuru palīdzību varēšu paziņot lietotājam, kad būs konstatēta kļūda. Paziņojums šajā gadījumā būs OS dialog logs.
- Veicu nelielas izmaiņas frontend kodā abos ietvaros.

**Sastaptās grūtības / izaicinājumi:**  
- N/A

**Piezīmes / pārdomas:**
- N/A

## Izstrādes sesija – [13.05.2025.]

**Izstrādes sesijas ilgums:**  
- 6h

**Veiktie uzdevumi:**  
- Pabeidzu ElectronJS projektu, un salaboju vieglākās kļūdas, kuras bija iespējams identificēt lietojumprogrammas darbības laikā.
- Normalizēju frontend kodu, lai tas būtu praktiskā ziņā vienāds abos projektos.

**Sastaptās grūtības / izaicinājumi:**  
- N/A

**Piezīmes / pārdomas:**
- Pirms sāku implementēju abos projektos, nebiju iedomājies, ka frontend kods, ieskaitot tā funkcionālās daļas, ir praktiskā ziņā pārizmantojamas abos ietvaros, kas varbūt liecina par Tauri iedvesmošanos no ElectronJS izstrādes ietvara pieejas. 

## Izstrādes sesija – [12.05.2025.]

**Izstrādes sesijas ilgums:**  
- 12h

**Veiktie uzdevumi:**  
- Implementēju pop up logus ElectronJS projektā. Nācās izdomāt no Tauri projekta atšķirīgu pieeju, kur tiek instancēti jauni lietojumprogrammas logi, un ar programmatisku pieeju, lietotājs tiek pārvirzīts uz noteiktu route, kas atbilst izvēlētajam pop up skata. Šķiet līdzīga pieeja tiek izmantota Tauri projektā, bet tā ir apslēpta Tauri API implementācijā. 
- Turpinu atjaunināt implementācijas iterācijas Blender versiju un projekta failu moduļiem.

**Sastaptās grūtības / izaicinājumi:**  
- Grūtības izveidot veidu, kā instancēt pop up logus. Nācās izmantot šādi aprakstītu pieeju, kas strādāt, bet šķiet ir lēnāka nekā Tauri projektā, proti, ir iespējams redzēt sākuma skatu pirms lietotājs tiek pārvirzīts uz pop up skatu (https://stackoverflow.com/questions/65938717/how-to-create-child-window-in-electron-react-application).

**Piezīmes / pārdomas:**
- N/A

## Izstrādes sesija – [11.05.2025.]

**Izstrādes sesijas ilgums:**  
- 4h

**Veiktie uzdevumi:**  
- Laboju kļūdas saistībā ar datu ievadi datubāzē ElectronJS projektā. Nācās implementēt būla vērtību kartēšanu no integer vērtībām, kādas tās ir datubāzes tabulās, uz būla vērtībām JavaScript kodā. Pārbaudīju vai līdzīga problēma nav Tauri projektā (nav).

**Sastaptās grūtības / izaicinājumi:**  
- N/A

**Piezīmes / pārdomas:**
- N/A

## Izstrādes sesija – [08.05.2025.]

**Izstrādes sesijas ilgums:**  
- 8h

**Veiktie uzdevumi:**  
- Pabeidzu blender repo path implementāciju ElectronJS projektā. 
- Pabeidzu Blender versijas moduļa funkcijas ElectronJS projektā, lai gan nāksies vēlāk to pielabot, kad tiks salīdzināts kods ar Tauri projektu.

**Sastaptās grūtības / izaicinājumi:**  
- Grūti noķert kļūdas ar JavaScript - jālieto papildus linter faili, lai atrastu dažādas sinstakses kļūdas. Nezinu, vai tā ir mana vaina un izmantotās izstrādes vides nepilnība, bet tas nav tik nozīmīgi eksperimenta ietvaros.
- Piemēram, ir grūti identificējamas problēmas kā await atslēgvārda neeksistēšana async funkcijas izsaukuma sākumā. Attiecīgi var sastapt ļoti sliktas kļūdas, kuras, bez šī iepriekšējā fakta pārbaudes, var sākt jaukt galvu par funkciju validitāti.

**Piezīmes / pārdomas:**
- N/A

## Izstrādes sesija – [07.05.2025.]

**Izstrādes sesijas ilgums:**  
- 4h

**Veiktie uzdevumi:**  
- Implementēju komandrindas parametrus un blender repo paths ElectronJS projektā, vadoties no esošās implementācijas Tauri projektā.

**Sastaptās grūtības / izaicinājumi:**  
- N/A

**Piezīmes / pārdomas:**
- N/A

## Izstrādes sesija – [06.05.2025.]

**Izstrādes sesijas ilgums:**  
- 4h

**Veiktie uzdevumi:**  
- Implementēju Tauri līdzīgu datubāzes repozitorijas slāni ElectronJS projektam. 
- Implementēju Python skriptu tabulu un tās funkcionalitāti, lai pārbaudītu datubāzes integrāciju.

**Sastaptās grūtības / izaicinājumi:**  
- Db migrāciju nācās implementēt tieši kodā, kur nu Tauri projekta bija iespējams nodalīt migrāciju .sql kodu atsevišķos failos, kurus pārvaldība sqlx.
- Sastapu ļoti daudz kļūdas saistībā ar ESM un commonjs import stila veidu. Turpmāk izmantošu ESM, bet līdz galam nesapratu, kādēļ eksistē šāda problēma JavaScript projektiem? 
- Sarežģījumi piedabūt, lai preload.js pareizi strādātu, un lai būtu iespējams testēt funkciju kodu.
- Grūtības inicializēt ElectronJS projekta datubāzi iepriekš minēto problēmu dēļ.

**Piezīmes / pārdomas:**
- ElectronJS izmantotais better-sqlite3 ir praktiski ekvivalents sqlx Tauri projektā, bet neeksistē sqlx-cli līdzīgs rīks, tādēļ lielu daļu no datubāzes implementācijas ir jārada manuāli.

## Izstrādes sesija – [05.05.2025.]

**Izstrādes sesijas ilgums:**  
- 5h (“pabeidzu” Tauri projektu. Nāksies vēlāk implementēt kļūdu un informācijas paziņojumu dialog logu implementāciju).
- 7h sāku ElectronJS projekta izstrādi.

**Veiktie uzdevumi:**  
- Pabeidzu Tauri projektu, bet to nāksies vēlāk papildināt dažādos veidos, attiecīgi skatoties uz atziņām, kuras radīsies izstrādājot ElectronJS projektu.
- Uzlaboju frontend kodu, lai to būtu iespējams vieglāk pārizmantot ElectronJS projektā.
- Implementēju pēdējās Python skripta un komandrindas parametru funkcijas Tauri projektā.

**Sastaptās grūtības / izaicinājumi:**  
- Grūtības izsekot un izķert kļūdas Tauri projekta implementācijā. Nāksies vēlāk to pārskatīt, to salīdzinot ar ElectronJS implementāciju.

**Piezīmes / pārdomas:**  
- N/A

## Izstrādes sesija – [04.05.2025.]

**Izstrādes sesijas ilgums:**  
- 10h

**Veiktie uzdevumi:**  
- Strādāju pie .blend failu atvēršanas funkcijas papildināšanas.
- Implementēju Blender versiju saglabāšanu, kas noris ārpus Blender versiju lejupielādes.
- Implementēju pēdējās atlikušās funkcionalitātes komandrindas parametriem un Python skriptiem.
- Uzlaboju pop up logu implementāciju Tauri projektā. To ir iespējams pārizmantot dažādu pop up logu implementēšanai.

**Sastaptās grūtības / izaicinājumi:**  
- N/A

**Piezīmes / pārdomas:**  
- N/A

## Izstrādes sesija – [03.05.2025.]

**Izstrādes sesijas ilgums:**  
- 10h

**Veiktie uzdevumi:**  
- Turpināju Projekta failu moduļa implementāciju, sekojot specifikācijā noteiktajām funkcijām.
- Pabeidzu pirmo iterāciju .blend faila atvēršanas funkcijai. Iesāku Python script un komandrindas parametru loģikas izstrādi.

**Sastaptās grūtības / izaicinājumi:**  
- Šī ir smaga komponente, kur tiek lietotas daudzas daļas no sistēmas, pareizāk sakot, no datubāzes tabulām. To sakot, šāda koda implementācija tomēr būs noderīga koda ABC analīzē.

**Piezīmes / pārdomas:**  
- N/A

## Izstrādes sesija – [02.05.2025.]

**Izstrādes sesijas ilgums:**  
- 9h

**Veiktie uzdevumi:**  
- Implementēju Blender versiju moduļa funkcijas, to skait lejupielādēto Blender versiju lejupielādēto versiju arhīvfaila atvēršanu, attiecīgi arī datu reģistrēšanu datubāzē.
- Iesāku Projektu failu moduļa implementāciju Tauri projektā. 

**Sastaptās grūtības / izaicinājumi:**  
- N/A

**Piezīmes / pārdomas:**  
- Skatoties uz to, ka pašlaik koncentrējos uz Tauri implementāciju, var rasties tas, ka ElectronJS implementāciju stipri ietekmēs Tauri implementācija. Savā ziņā, tas nav slikti, bet ir svarīgi to atzīmēt.

## Izstrādes sesija – [01.05.2025.]

**Izstrādes sesijas ilgums:**  
- 11h

**Veiktie uzdevumi:**  
- Implementēju Blender daily builds versiju API izsaukšanas metodi, kura ir spējīga izfiltrēt versijas starp Windows, macOS un Linux sistēmām.
- Implementēju (Upload)[https://v2.tauri.app/plugin/upload/] plugin Tauri projektā - analizējot kodu visticamāk izvēlēšos izlaist šo daļu koda abos projektos, jo tas ir sadalīts ir pamatīgi sadalīts starp backend un frontend kodu, tādēļ būtu grūti to pilnvērtīgi izanalizēt.
- Implementēju dialog logu izštancēšanu noteiktām Rust funkcijām, kur tas ir nepieciešams.
- Sāku implementēt Settings skatu, kur parādīsies Blender instalācijas lokācijas, komandrindas parametru un Python skriptu saraksti.
- Implementēju Blender versijas lejupielādi ar popup loga izštancēšanu.

**Sastaptās grūtības / izaicinājumi:**  
- Grūtības implementēt rudimentāru download progress indikatoru ReactJS frontend komponentē - atlika lietot DOM manipulāciju. 

**Piezīmes / pārdomas:**  
- Ir iespējams lietot Tauri state pārvaldnieku (līdzīgi kā Zustand vai Redux state manager ReactJS frontendā) funkciju lai implementētu dependency injection, un saglabātu vienu db pool visām metodēm.

## Izstrādes sesija – [27.04.2025.]

**Izstrādes sesijas ilgums:**  
- 13h 

**Veiktie uzdevumi:**  
- Uzstādīju sqlx datubāzi ar sākotnējām tabulām Tauri projektā. 
- Izveidoju un sadalīju datubāzes loģiku datubāzes repozitorijas slāņos. 

**Sastaptās grūtības / izaicinājumi:**  
- Ir sqlx-cli rīks, ar kuru var izveidot, piemēram, datubāzes migrāciju, bet nav iespējams tām ģenerēt atbilstošu Rust koda struct implementācijas. To kods ir jāraksta pašam, attiecīgi kā modeļus, kurus ir iespējams sarealizēt uz datubāzes tabulas ierakstiem.
- Nāksies vēlāk uzlabot koda implementāciju, jo nav līdz galam skaidrs, vai esošā implementācija ir pietiekami laba/idiomātiska.

**Piezīmes / pārdomas:**  
- sqlx liekas pilnīgi pietiekams dotajam projektam, bet būtu vēlme dažādiem life quality uzlabojumiem, kā struct ģenerēšana SQL definētā tabulām vai vice versa. Citādāk var rasties kļūdas, rakstot šādu kodu manuāli.

## Izstrādes sesija – [22.04.2025.]

**Izstrādes sesijas ilgums:**  
- 4h

**Veiktie uzdevumi:**  
- Izkārtoju Tauri projekta kodu failus sekojot specifikācijā noteikto moduļu struktūrai. 
- Sāku uzstādīt sqlite datubāzi un tās repozitorijas slāni Tauri projektā.

**Sastaptās grūtības / izaicinājumi:**  
- Grūtītas uzstādīt debuggeri.
- SQL plugins tiek izmantots tikai FE, ne backend. Backendam jāimplementē no jauna ar sqlx.
- Grūtības pareizi uzstādīt 

**Piezīmes / pārdomas:**  
- Izvēlējos eksperimentā apskatītās lietojumprogrammas implementāciju Tauri izstrādes ietvarā, jo:
  - Bija iepriekšēja un plaša pieredze lietojot Tauri;
  - Vēlējos cik vien ātri pārbaudīt specifikācijā noteikto funkciju implementācijas iespējas.
- Attiecīgi lietojumprogrammas sākotnējā izstrāde galvenokārt koncentrējās uz Tauri izstrādes ietvaru.

## Izstrādes sesija – [20.04.2025.]

**Izstrādes sesijas ilgums:**  
- 1h

**Veiktie uzdevumi:**  
- Izstrādāju sākuma frontend ReactJS komponentes, kuras tiks izmantotas gan Tauri, gan ElectronJS ietvaru lietojumprogrammu versiju izstrādē.
- Ievietoju sākotnējo ReactJS FE kodu abu ietvaru projektos.

**Sastaptās grūtības / izaicinājumi:**  
- N/A

**Piezīmes / pārdomas:**  
- Pateicoties ReactJS dēļ, nebija praktiski nekāds atšķirības šī ReactJS ātrai integrācijai.  

## Izstrādes sesija – [19.04.2025.]

**Izstrādes sesijas ilgums:**  
- 1h

**Veiktie uzdevumi:**  
- Inicializēju projektu Tauri un ElectronJs ietvaros ar ReactJS frontend lietojot šo dokumentāciju: 
    - https://tauri.app/start/,
    - https://electron-vite.org/guide/
- Sāku iepazīties ar specifikāciju, un kā to būs visvieglāk implementēt dotajos izstrādes ietvaros - dažādas funkcionālitātes, kā arhīvfailu manipulācijai, būs jāizmanto trešo pušu bibliotēkas.
- Priekš Blender versiju lejupielādes Tauri izstrādes ietvarā būs iespējams izmantot (upload plugin)[https://v2.tauri.app/plugin/upload/]. ElectronJS neeksitēja šads API, tādēļ tika izvēlēts lietot trešo pušu bibliotēku (electron-dl)[https://www.npmjs.com/package/electron-dl].

**Sastaptās grūtības / izaicinājumi:**  
- Grūtības izvēlēties ElectronJS projekta izveidotāju. Eksistēja 2 varianti, kas izmanto Vite, un abi izskatījās pietiekami piemēroti eksperimenta vajadzībām. 

**Piezīmes / pārdomas:**  
- Kā jau zināms, uzsākt Tauri projektu, kur ir iesākta frontend komponente ar kādu frontend izstrādes ietvaru, nodrošina pati Tauri organizācija, bet ElectronJs gadījumā ir jāmeklē trešo pušu rīki. Grūti saprast, kādēļ tik plaši izmantotam rīkam šāda iespēja vēl nav oficiāli integrēta vai, ja ir, uzreiz reklamēta oficiālajā mājaslapā?  
