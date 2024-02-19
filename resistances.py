
class ResistanceProfile:
    #{name : amount}
    def __init__(self, impact = 0, slash = 0, puncture = 0, cold = 0, electricity = 0, heat = 0, toxin = 0, blast = 0, corrosive = 0, gas = 0, magnetic = 0, radiation = 0, viral = 0, true = 0, appliesAsArmor = False, factionTag = "Grineer"):
        self.resistances = {"impact": impact, "slash": slash, "puncture": puncture, "cold": cold, "electricity": electricity, "heat": heat, "toxin": toxin, "blast": blast, "corrosive": corrosive, "gas": gas, "magnetic": magnetic, "radiation": radiation, "viral": viral, "true": true}
        self.appliesAsArmor = appliesAsArmor
        self.factionTag = factionTag

    def applyRes(self, damageDict):
        for damageType in damageDict:
            damageDict[damageType] = round(damageDict[damageType] + damageDict[damageType] * self.resistances[damageType], 2)
        return damageDict
    
    def applyAsArmor(self, damageDict, armorAmount):
        for damageType in damageDict:
            netArmor = armorAmount * (1 - self.resistances[damageType])
            damageReduction = netArmor / (netArmor + 300)
            damageDict[damageType] = max(round(damageDict[damageType] - (damageDict[damageType] * damageReduction), 2), 1)
        return damageDict

            

    
RESISTANCES = {
    "Grineer|Cloned Flesh": ResistanceProfile(impact= -0.25, slash=0.25, heat=0.25, gas=-0.25, viral=0.75),
    "Grineer|Ferrite Armor": ResistanceProfile(puncture=0.5, slash=-0.15, blast=-0.25, corrosive=0.75, appliesAsArmor=True),
    "Grineer|Alloy Armor": ResistanceProfile(puncture=0.15, slash=-0.5, cold=0.25, electricity=-0.5, magnetic=-0.5, radiation=0.75, appliesAsArmor=True),
    "Grineer|Machinery": ResistanceProfile(impact=0.25, electricity=0.50, toxin=-0.25, blast=0.75, viral=-0.25),

    "Corpus|Flesh": ResistanceProfile(impact=-0.25, slash=0.25, toxin=0.5, gas=-0.25, viral=0.5, factionTag="Corpus"),
    "Corpus|Shield": ResistanceProfile(impact=0.5, puncture=-0.2, cold=0.5, magnetic=0.75, radiation=-0.25, factionTag="Corpus"),
    "Corpus|Proto Shield": ResistanceProfile(impact=0.15, puncture=-0.5, heat=-0.5, corrosive=-0.5, magnetic=0.75, factionTag="Corpus"),
    "Corpus|Robotic": ResistanceProfile(puncture=0.25, slash=-0.25, electricity=0.5, toxin=-0.25, radiation=0.25, factionTag="Corpus"),
    "Corpus|Ferrite Armor": ResistanceProfile(puncture=0.5, slash=-0.15, blast=-0.25, corrosive=0.75, appliesAsArmor=True, factionTag="Corpus"),
    "Corpus|Alloy Armor": ResistanceProfile(puncture=0.15, slash=-0.5, cold=0.25, electricity=-0.5, magnetic=-0.5, radiation=0.75, appliesAsArmor=True, factionTag="Corpus"),

    "Infested|Infested": ResistanceProfile(slash=0.25, heat=0.25, gas=0.75, radiation=-0.5, viral=0.5, factionTag="Infested"),
    "Infested|Infested Flesh": ResistanceProfile(slash=0.5, cold=-0.5, heat=0.5, gas=0.5, factionTag="Infested"),
    "Infested|Fossilized": ResistanceProfile(slash=0.15, cold=-0.25, toxin=-0.5, blast=0.5, corrosive=0.75, radiation=-0.75, factionTag="Infested"),
    "Infested|Infested Sinew": ResistanceProfile(puncture=0.25, cold=0.25, blast=-0.5, radiation=0.5, appliesAsArmor=True, factionTag="Infested"),
}