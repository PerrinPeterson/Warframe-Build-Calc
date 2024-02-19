import random

class Gun():
    def __init__(self):
        self.name = ""
        self.imageName ="gunImages/" + self.name + ".png"
        self.critChance = 0.0
        self.critMultiplier = 1      
        self.statusChance = 0.0
        self.statusDuration = 0
        self.fireRate = 1
        self.magazine = 1
        self.reload = 1
        self.multishot = 1
        self.tags = ["rifle"]
        self.damageTypes = {
            "impact": 1,
            "puncture": 1,
            "slash": 1,
            "heat": 0,
            "cold": 0,
            "electricity": 0,
            "toxin": 0,
            "blast": 0,
            "corrosive": 0,
            "gas": 0,
            "magnetic": 0,
            "radiation": 0,
            "viral": 0
        }

    def GetStats(self):
        stats = ""
        stats += "Crit Chance: " + str(self.critChance * 100) + "%\n"
        stats += "Crit Multiplier: " + str(self.critMultiplier) + "x\n"
        stats += "Status Chance: " + str(self.statusChance * 100) + "%\n"
        stats += "Status Duration: " + str(self.statusDuration) + "s\n"
        stats += "Fire Rate: " + str(self.fireRate) + " rounds/s\n"
        stats += "Magazine: " + str(self.magazine) + " rounds\n"
        stats += "Reload: " + str(self.reload) + "s\n"
        stats += "Multishot: " + str(self.multishot) + "x\n"

        for key in self.damageTypes:
            if self.damageTypes[key] > 0:
                statName = key
                #capatalize the first letter, cause my OCD demands it
                statName = statName[0].upper() + statName[1:]
                stats += statName + ": " + str(self.damageTypes[key]) + " damage\n" 
        return stats

    def apply(self, modProfile):
        self.critChance *= modProfile.BonusCritChance + 1
        self.critMultiplier *= modProfile.BonusCritMultiplier + 1
        self.statusChance *= modProfile.BonusStatusChance + 1
        self.statusDuration *= modProfile.BonusStatusDuration + 1
        self.fireRate *= modProfile.BonusFireRate + 1
        self.magazine *= modProfile.BonusMagazine + 1
        self.reload *= modProfile.BonusReload + 1
        self.multishot *= modProfile.BonusMultishot + 1

        baseDamage = 0
        for key in self.damageTypes:
            baseDamage += self.damageTypes[key]
        
        
        if modProfile.BonusImpact > 0:
            self.damageTypes["impact"] = self.damageTypes["impact"] * (modProfile.BonusImpact + 1)
        if modProfile.BonusPuncture > 0:
            self.damageTypes["puncture"] = self.damageTypes["puncture"] * (modProfile.BonusPuncture + 1)
        if modProfile.BonusSlash > 0:
            self.damageTypes["slash"] = self.damageTypes["slash"] * (modProfile.BonusSlash + 1)
        if modProfile.BonusHeat > 0:
            self.damageTypes["heat"] = baseDamage * (modProfile.BonusHeat)
        if modProfile.BonusCold > 0:
            self.damageTypes["cold"] = baseDamage * (modProfile.BonusCold)
        if modProfile.BonusElectricity > 0:
            self.damageTypes["electricity"] = baseDamage * (modProfile.BonusElectricity)
        if modProfile.BonusToxin > 0:
            self.damageTypes["toxin"] = baseDamage * (modProfile.BonusToxin)
        if modProfile.BonusBlast > 0:
            self.damageTypes["blast"] = baseDamage * (modProfile.BonusBlast)
        if modProfile.BonusCorrosive > 0:
            self.damageTypes["corrosive"] = baseDamage * (modProfile.BonusCorrosive)
        if modProfile.BonusGas > 0:
            self.damageTypes["gas"] = baseDamage * (modProfile.BonusGas)
        if modProfile.BonusMagnetic > 0:
            self.damageTypes["magnetic"] = baseDamage * (modProfile.BonusMagnetic)
        if modProfile.BonusRadiation > 0:
            self.damageTypes["radiation"] = baseDamage * (modProfile.BonusRadiation)
        if modProfile.BonusViral > 0:
            self.damageTypes["viral"] = baseDamage * (modProfile.BonusViral)

        for key in self.damageTypes:
            self.damageTypes[key] = self.damageTypes[key] * (modProfile.BonusDamagePercent + 1) + modProfile.BonusDamageFlat
            if key == "impact" or key == "puncture" or key == "slash":
                self.damageTypes[key] = round(self.damageTypes[key], 2)
            else:
                self.damageTypes[key] = round(self.damageTypes[key])
    
    #REALLY conviluted way to adjust the damage types for the weapon, but it works
    def AdjustForDamageCombinations(self, mods):
        ComboDict = {}
        #getting all the damage types
        for mod in mods:
            if "BonusElectricity" in mod.modDict:
                if "BonusElectricity" not in ComboDict:
                    ComboDict["BonusElectricity"] = self.damageTypes["electricity"]
            if "BonusHeat" in mod.modDict:
                if "BonusHeat" not in ComboDict:
                    ComboDict["BonusHeat"] = self.damageTypes["heat"]
            if "BonusCold" in mod.modDict:
                if "BonusCold" not in ComboDict:
                    ComboDict["BonusCold"] = self.damageTypes["cold"]
            if "BonusToxin" in mod.modDict:
                if "BonusToxin" not in ComboDict:
                    ComboDict["BonusToxin"] = self.damageTypes["toxin"]
        
        #stacking them on existing damage combinations
        if self.damageTypes["blast"] > 0:
            if "BonusHeat" in ComboDict:
                self.damageTypes["blast"] += ComboDict["BonusHeat"]
                self.damageTypes["heat"] = 0
                ComboDict.pop("BonusHeat")
            if "BonusCold" in ComboDict:
                self.damageTypes["blast"] += ComboDict["BonusCold"]
                self.damageTypes["cold"] = 0
                ComboDict.pop("BonusCold")
        if self.damageTypes["corrosive"] > 0:
            if "BonusElectricity" in ComboDict:
                self.damageTypes["corrosive"] += ComboDict["BonusElectricity"]
                self.damageTypes["electricity"] = 0
                ComboDict.pop("BonusElectricity")
            if "BonusToxin" in ComboDict:
                self.damageTypes["corrosive"] += ComboDict["BonusToxin"]
                self.damageTypes["toxin"] = 0
                ComboDict.pop("BonusToxin")
        if self.damageTypes["gas"] > 0:
            if "BonusHeat" in ComboDict:
                self.damageTypes["gas"] += ComboDict["BonusHeat"]
                self.damageTypes["heat"] = 0
                ComboDict.pop("BonusHeat")
            if "BonusToxin" in ComboDict:
                self.damageTypes["gas"] += ComboDict["BonusToxin"]
                self.damageTypes["toxin"] = 0
                ComboDict.pop("BonusToxin")
        if self.damageTypes["magnetic"] > 0:
            if "BonusCold" in ComboDict:
                self.damageTypes["magnetic"] += ComboDict["BonusCold"]
                self.damageTypes["cold"] = 0
                ComboDict.pop("BonusCold")
            if "BonusElectricity" in ComboDict:
                self.damageTypes["magnetic"] += ComboDict["BonusElectricity"]
                self.damageTypes["electricity"] = 0
                ComboDict.pop("BonusElectricity")
        if self.damageTypes["radiation"] > 0:
            if "BonusHeat" in ComboDict:
                self.damageTypes["radiation"] += ComboDict["BonusHeat"]
                self.damageTypes["heat"] = 0
                ComboDict.pop("BonusHeat")
            if "BonusElectricity" in ComboDict:
                self.damageTypes["radiation"] += ComboDict["BonusElectricity"]
                self.damageTypes["electricity"] = 0
                ComboDict.pop("BonusElectricity")
        if self.damageTypes["viral"] > 0:
            if "BonusCold" in ComboDict:
                self.damageTypes["viral"] += ComboDict["BonusCold"]
                self.damageTypes["cold"] = 0
                ComboDict.pop("BonusCold")
            if "BonusToxin" in ComboDict:
                self.damageTypes["viral"] += ComboDict["BonusToxin"]
                self.damageTypes["toxin"] = 0
                ComboDict.pop("BonusToxin")

        #combining the remaining damage types, in order they were added to the build
        #ComboDict should only have 2 or 3 keys at this point
        while len(ComboDict) > 0:
            key = list(ComboDict.keys())[0]
            if len(ComboDict) == 1:
                if key == "BonusHeat":
                    self.damageTypes["heat"] = ComboDict["BonusHeat"]
                elif key == "BonusCold":
                    self.damageTypes["cold"] = ComboDict["BonusCold"]
                elif key == "BonusElectricity":
                    self.damageTypes["electricity"] = ComboDict["BonusElectricity"]
                elif key == "BonusToxin":
                    self.damageTypes["toxin"] = ComboDict["BonusToxin"]
                ComboDict.pop(key)
                continue
            
            if key == "BonusHeat":
                keyTwo = list(ComboDict.keys())[1]
                if keyTwo == "BonusCold":
                    self.damageTypes["blast"] = ComboDict["BonusHeat"] + ComboDict["BonusCold"]
                    self.damageTypes["heat"] = 0
                    self.damageTypes["cold"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusElectricity":
                    self.damageTypes["radiation"] = ComboDict["BonusHeat"] + ComboDict["BonusElectricity"]
                    self.damageTypes["heat"] = 0
                    self.damageTypes["electricity"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusToxin":
                    self.damageTypes["gas"] = ComboDict["BonusHeat"] + ComboDict["BonusToxin"]
                    self.damageTypes["heat"] = 0
                    self.damageTypes["toxin"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
            elif key == "BonusCold":
                keyTwo = list(ComboDict.keys())[1]
                if keyTwo == "BonusElectricity":
                    self.damageTypes["magnetic"] = ComboDict["BonusCold"] + ComboDict["BonusElectricity"]
                    self.damageTypes["cold"] = 0
                    self.damageTypes["electricity"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusToxin":
                    self.damageTypes["viral"] = ComboDict["BonusCold"] + ComboDict["BonusToxin"]
                    self.damageTypes["cold"] = 0
                    self.damageTypes["toxin"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusHeat":
                    self.damageTypes["blast"] = ComboDict["BonusCold"] + ComboDict["BonusHeat"]
                    self.damageTypes["cold"] = 0
                    self.damageTypes["heat"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
            elif key == "BonusElectricity":
                keyTwo = list(ComboDict.keys())[1]
                if keyTwo == "BonusToxin":
                    self.damageTypes["corrosive"] = ComboDict["BonusElectricity"] + ComboDict["BonusToxin"]
                    self.damageTypes["electricity"] = 0
                    self.damageTypes["toxin"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusHeat":
                    self.damageTypes["radiation"] = ComboDict["BonusElectricity"] + ComboDict["BonusHeat"]
                    self.damageTypes["electricity"] = 0
                    self.damageTypes["heat"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusCold":
                    self.damageTypes["magnetic"] = ComboDict["BonusElectricity"] + ComboDict["BonusCold"]
                    self.damageTypes["electricity"] = 0
                    self.damageTypes["cold"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
            elif key == "BonusToxin":
                keyTwo = list(ComboDict.keys())[1]
                if keyTwo == "BonusHeat":
                    self.damageTypes["gas"] = ComboDict["BonusToxin"] + ComboDict["BonusHeat"]
                    self.damageTypes["toxin"] = 0
                    self.damageTypes["heat"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusElectricity":
                    self.damageTypes["corrosive"] = ComboDict["BonusToxin"] + ComboDict["BonusElectricity"]
                    self.damageTypes["toxin"] = 0
                    self.damageTypes["electricity"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                elif keyTwo == "BonusCold":
                    self.damageTypes["viral"] = ComboDict["BonusToxin"] + ComboDict["BonusCold"]
                    self.damageTypes["toxin"] = 0
                    self.damageTypes["cold"] = 0
                    ComboDict.pop(key)
                    ComboDict.pop(keyTwo)
                    continue
                


def getWeaponList():
    return [Dera(), Amprex(), AKStiletto(), Regulators()]

class Dera(Gun):
    def __init__(self):
        self.name = "Dera"
        self.imageName = "gunImages/Dera.png"
        self.critChance = 0.08
        self.critMultiplier = 1.6      
        self.statusChance = 0.22
        self.statusDuration = 0
        self.fireRate = 11.25
        self.magazine = 45
        self.reload = 1.8
        self.multishot = 1
        self.tags = ["rifle"]
        self.damageTypes = {
            "impact": 6,
            "puncture": 22.5,
            "slash": 1.5,
            "heat": 0,
            "cold": 0,
            "electricity": 0,
            "toxin": 0,
            "blast": 0,
            "corrosive": 0,
            "gas": 0,
            "magnetic": 0,
            "radiation": 0,
            "viral": 0
        }     

class Amprex(Gun):
    def __init__(self):
        self.name = "Amprex"
        self.imageName = "gunImages/Amprex.png"
        self.critChance = 0.32
        self.critMultiplier = 2.2       #2.2
        self.statusChance = 0.22
        self.statusDuration = 0
        self.fireRate = 12
        self.magazine = 100
        self.reload = 2.6
        self.multishot = 1
        self.tags = ["rifle"]
        self.damageTypes = {
            "impact": 0,
            "puncture": 0,
            "slash": 0,
            "heat": 0,
            "cold": 0,
            "electricity": 22,
            "toxin": 0,
            "blast": 0,
            "corrosive": 0,
            "gas": 0,
            "magnetic": 0,
            "radiation": 0,
            "viral": 0
        }
    
    def apply(self, modProfile):
        self.critChance *= modProfile.BonusCritChance + 1
        self.critMultiplier *= modProfile.BonusCritMultiplier + 1
        self.statusChance *= modProfile.BonusStatusChance + 1
        self.statusDuration *= modProfile.BonusStatusDuration + 1
        self.fireRate *= modProfile.BonusFireRate + 1
        self.magazine *= modProfile.BonusMagazine + 1
        self.reload *= modProfile.BonusReload + 1
        self.multishot *= modProfile.BonusMultishot + 1

        baseDamage = 0
        for key in self.damageTypes:
            baseDamage += self.damageTypes[key]
        
        #This gun can't have puncture, slash, or impact damage
        if modProfile.BonusHeat > 0:
            self.damageTypes["heat"] = baseDamage * (modProfile.BonusHeat + 1)
        if modProfile.BonusCold > 0:
            self.damageTypes["cold"] = baseDamage * (modProfile.BonusCold + 1)
        if modProfile.BonusElectricity > 0:
            self.damageTypes["electricity"] = baseDamage * (modProfile.BonusElectricity + 1)
        if modProfile.BonusToxin > 0:
            self.damageTypes["toxin"] = baseDamage * (modProfile.BonusToxin + 1)


        for key in self.damageTypes:
            self.damageTypes[key] = self.damageTypes[key] * (modProfile.BonusDamagePercent + 1) + modProfile.BonusDamageFlat
            self.damageTypes[key] = round(self.damageTypes[key], 2)

class AKStiletto(Gun):
    def __init__(self):
        self.name = "Akstiletto"
        self.imageName = "gunImages/Akstiletto.png"
        self.critChance = 0.18
        self.critMultiplier = 1.8      
        self.statusChance = 0.18
        self.statusDuration = 0
        self.fireRate = 10
        self.magazine = 28
        self.reload = 1.1
        self.multishot = 1
        self.tags = ["pistol"]
        self.damageTypes = {
            "impact": 16.8,
            "puncture": 2.8,
            "slash": 8.4,
            "heat": 0,
            "cold": 0,
            "electricity": 0,
            "toxin": 0,
            "blast": 0,
            "corrosive": 0,
            "gas": 0,
            "magnetic": 0,
            "radiation": 0,
            "viral": 0
        }

class Regulators(Gun):
    def __init__(self):
        self.name = "Regulators"
        self.imageName = "gunImages/Regulators.png"
        self.critChance = 0.25
        self.critMultiplier = 3      
        self.statusChance = 0.10
        self.statusDuration = 0
        self.fireRate = 14.8
        self.magazine = 100
        self.reload = 1.8
        self.multishot = 1
        self.tags = ["pistol"]
        self.damageTypes = {
            "impact": 50,
            "puncture": 25,
            "slash": 25,
            "heat": 0,
            "cold": 0,
            "electricity": 0,
            "toxin": 0,
            "blast": 0,
            "corrosive": 0,
            "gas": 0,
            "magnetic": 0,
            "radiation": 0,
            "viral": 0
        }

class Boar(Gun):
    def __init__(self):
        self.name = "Boar"
        self.imageName = "gunImages/Boar.png"
        self.critChance = 0.1
        self.critMultiplier = 1.5      
        self.statusChance = 0.075
        self.statusDuration = 0
        self.fireRate = 4.17
        self.magazine = 20
        self.reload = 2.7
        self.multishot = 8
        self.tags = ["shotgun"]
        self.damageTypes = {
            "impact": 12.1,
            "puncture": 3.3,
            "slash": 6.6,
            "heat": 0,
            "cold": 0,
            "electricity": 0,
            "toxin": 0,
            "blast": 0,
            "corrosive": 0,
            "gas": 0,
            "magnetic": 0,
            "radiation": 0,
            "viral": 0
        }