# Hurkos-OpenCache

A jelenlegi piacon számos olyan switch és router kapható, amely habár támogatja az Openflow protokoll valamely verzióját,
mégsincs benne minden, az OpenFlow ajánlás által definiált funkció implementálva.  Munkánk során számos olyan eszközzel 
találkozhatunk, melyek - az OpenCache rendszer műkédéséhez szükséges - csomag fejléc mezők módosítását nem támogatják. 

Az OpenCache rendszer megalkotásakor nem állt rendelkezésünkre, olyan eszköz amely tökéletes lett volna számunkra, 
mivel egyik rendelkezésünkre álló switch sem támogatta a beérkező csomagok header mezőinek módosítását. E kritérium miatt 
újra kellett tervezni az OpenCache rendszer működését! 

A rendszer lényege, hogy olyan hálózati eszközzel is tudjunk működtetni a cache-elést, amely nem támogat header módosítást.
A Létrehoztunk egy multifunkcionális szervert, mely a következő alkalmazásokat futtatja:

OFC - Open Floodlight Controller
OVS - Open vSwitch
OCC - OpenCache Controller
OCN - OpenCache Node
MongodDB

A nagy újdonság az eredeti OC rendszerhez képest az OVS beépítése a működésbe. Ez a komponens gondoskodik a csomagok fejléc
mezőinek módosításáról, így a konkrét fizikai OpenFlow eszköznek (esetünkben MikroTik CCR) a feladata, hogy minden módosítandó
csomagot továbbítson az OVS számára. Az OVS, a bejövő portján detektált csomagot, a megfelelő értékekkel módosítja, majd a kapott eredményt, visszaküldi a fizikai eszköznek. A kettő OpenFlow switch között kialakult hurok miatt neveztük el a rendszert “Hurkos” OpenCache-nek.
