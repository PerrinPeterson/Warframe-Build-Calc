import random

class Gun():
    def __init__(self):
        self.name = ""
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
            self.damageTypes["heat"] = baseDamage * (modProfile.BonusHeat + 1)
        if modProfile.BonusCold > 0:
            self.damageTypes["cold"] = baseDamage * (modProfile.BonusCold + 1)
        if modProfile.BonusElectricity > 0:
            self.damageTypes["electricity"] = baseDamage * (modProfile.BonusElectricity + 1)
        if modProfile.BonusToxin > 0:
            self.damageTypes["toxin"] = baseDamage * (modProfile.BonusToxin + 1)
        if modProfile.BonusBlast > 0:
            self.damageTypes["blast"] = baseDamage * (modProfile.BonusBlast + 1)
        if modProfile.BonusCorrosive > 0:
            self.damageTypes["corrosive"] = baseDamage * (modProfile.BonusCorrosive + 1)
        if modProfile.BonusGas > 0:
            self.damageTypes["gas"] = baseDamage * (modProfile.BonusGas + 1)
        if modProfile.BonusMagnetic > 0:
            self.damageTypes["magnetic"] = baseDamage * (modProfile.BonusMagnetic + 1)
        if modProfile.BonusRadiation > 0:
            self.damageTypes["radiation"] = baseDamage * (modProfile.BonusRadiation + 1)
        if modProfile.BonusViral > 0:
            self.damageTypes["viral"] = baseDamage * (modProfile.BonusViral + 1)

        for key in self.damageTypes:
            self.damageTypes[key] = self.damageTypes[key] * (modProfile.BonusDamagePercent + 1) + modProfile.BonusDamageFlat
            self.damageTypes[key] = round(self.damageTypes[key], 2)
    def AdjustForDamageCombinations(self):
        def AdjustForBlast():
            if self.damageTypes["heat"] > 0 and self.damageTypes["cold"] > 0:
                self.damageTypes["blast"] = self.damageTypes["heat"] + self.damageTypes["cold"]
                self.damageTypes["heat"] = 0
                self.damageTypes["cold"] = 0
        def AdjustForCorrosive():
            if self.damageTypes["electricity"] > 0 and self.damageTypes["toxin"] > 0:
                self.damageTypes["corrosive"] = self.damageTypes["electricity"] + self.damageTypes["toxin"]
                self.damageTypes["electricity"] = 0
                self.damageTypes["toxin"] = 0
        def AdjustForGas():
            if self.damageTypes["heat"] > 0 and self.damageTypes["toxin"] > 0:
                self.damageTypes["gas"] = self.damageTypes["heat"] + self.damageTypes["toxin"]
                self.damageTypes["heat"] = 0
                self.damageTypes["toxin"] = 0
        def AdjustForMagnetic():
            if self.damageTypes["cold"] > 0 and self.damageTypes["electricity"] > 0:
                self.damageTypes["magnetic"] = self.damageTypes["cold"] + self.damageTypes["electricity"]
                self.damageTypes["cold"] = 0
                self.damageTypes["electricity"] = 0
        def AdjustForRadiation():
            if self.damageTypes["heat"] > 0 and self.damageTypes["electricity"] > 0:
                self.damageTypes["radiation"] = self.damageTypes["heat"] + self.damageTypes["electricity"]
                self.damageTypes["heat"] = 0
                self.damageTypes["electricity"] = 0
        def AdjustForViral():
            if self.damageTypes["cold"] > 0 and self.damageTypes["toxin"] > 0:
                self.damageTypes["viral"] = self.damageTypes["cold"] + self.damageTypes["toxin"]
                self.damageTypes["cold"] = 0
                self.damageTypes["toxin"] = 0

        AdjustmentFuncs = [AdjustForBlast, AdjustForCorrosive, AdjustForGas, AdjustForMagnetic, AdjustForRadiation, AdjustForViral]
        while len(AdjustmentFuncs) > 0:
            chosenFunc = random.choice(AdjustmentFuncs)
            chosenFunc()
            AdjustmentFuncs.remove(chosenFunc)

class Dera(Gun):
    def __init__(self):
        self.name = "Dera"
        self.critChance = 0.08
        self.critMultiplier = 1.6      
        self.statusChance = 0.22
        self.statusDuration = 0
        self.fireRate = 11.25
        self.magazine = 45
        self.reload = 1.8
        self.multishot = 1
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
        self.critChance = 0.32
        self.critMultiplier = 2.2       #2.2
        self.statusChance = 0.22
        self.statusDuration = 0
        self.fireRate = 12
        self.magazine = 100
        self.reload = 2.6
        self.multishot = 1
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