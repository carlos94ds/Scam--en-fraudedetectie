# Data-beslissingen

## URLSimilarityIndex uitgesloten (19 september 2026)

Tijdens de EDA bleek `URLSimilarityIndex` een correlatie van 0,86 met het
label te hebben, veel hoger dan alle andere URL-only kenmerken. Verder
onderzoek liet zien dat deze kolom bij vrijwel alle legitieme URL's exact
dezelfde waarde (100,0) heeft, en bij nagenoeg geen enkele phishing-URL.
De kolom herhaalt daarmee in de praktijk het label, in plaats van dat het
een onafhankelijk voorspellend kenmerk is (datalekkage).

Daarnaast is deze waarde berekend door de makers van de dataset met hun
eigen gelijkenis-algoritme ten opzichte van bekende legitieme URL's. Die
berekening kunnen wij niet reproduceren voor een nieuwe URL die een
gebruiker in de applicatie invoert.

Besluit: `URLSimilarityIndex` wordt uitgesloten van de features waarop het
model traint.

## Kritische kanttekening bij het baseline-resultaat (19 september 2026)

Het baseline Logistic Regression-model (URL-only features) haalt 99,68%
accuracy, stabiel over 5-voudige cross-validation (std 0,0001) en niet
verklaard door duplicaten (slechts 1,0% van de dataset).

Dit resultaat is zo hoog en zo stabiel dat het vermoedelijk niet alleen
komt door hoe goed phishing-URL's te herkennen zijn, maar ook door hoe de
PhiUSIIL-dataset is samengesteld: phishing-URL's zijn verzameld via
threat-intelligence-feeds, legitieme URL's via een aparte, eigen curated
lijst. Twee verschillende verzamelmethodes kunnen stilistische verschillen
opleveren (bijvoorbeeld in lengte of tekenverdeling) die losstaan van of
een URL daadwerkelijk frauduleus is. Het model kan dus deels leren welke
bron een URL heeft, in plaats van puur wat phishing kenmerkt.

Consequentie: dit resultaat is een geldige baseline binnen deze dataset,
maar mag niet zonder kanttekening gepresenteerd worden als "hoe goed het
model phishing in de praktijk herkent". Bij een eventuele latere test op
URL's uit een andere bron (bijvoorbeeld handmatig verzamelde voorbeelden)
verwachten we een lagere score, en dat is dan een eerlijker beeld van de
werkelijke prestatie.
