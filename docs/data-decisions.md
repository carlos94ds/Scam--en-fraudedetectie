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
