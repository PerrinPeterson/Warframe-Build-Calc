import random
import math
import threading
from tqdm import tqdm
import copy

class ModProfile():
    def __init__(self):
        self.BonusDamageFlat = 0
        self.BonusDamagePercent = 0
        self.BonusCritChance = 0
        self.BonusCritMultiplier = 0
        self.BonusStatusChance = 0
        self.BonusStatusDuration = 0
        self.BonusFireRate = 0
        self.BonusMagazine = 0
        self.BonusReload = 0
        self.BonusMultishot = 0
        self.BonusImpact = 0
        self.BonusPuncture = 0
        self.BonusSlash = 0
        self.BonusHeat = 0
        self.BonusCold = 0
        self.BonusElectricity = 0
        self.BonusToxin = 0
        self.BonusBlast = 0
        self.BonusCorrosive = 0
        self.BonusGas = 0
        self.BonusMagnetic = 0
        self.BonusRadiation = 0
        self.BonusViral = 0

        self.mods = []

    def AdjustForDamageCombinations(self):
        def AdjustForBlast():
            if self.BonusHeat > 0 and self.BonusCold > 0:
                self.BonusBlast = self.BonusHeat + self.BonusCold
                self.BonusHeat = 0
                self.BonusCold = 0
        def AdjustForCorrosive():
            if self.BonusElectricity > 0 and self.BonusToxin > 0:
                self.BonusCorrosive = self.BonusElectricity + self.BonusToxin
                self.BonusElectricity = 0
                self.BonusToxin = 0
        def AdjustForGas():
            if self.BonusHeat > 0 and self.BonusToxin > 0:
                self.BonusGas = self.BonusHeat + self.BonusToxin
                self.BonusHeat = 0
                self.BonusToxin = 0
        def AdjustForMagnetic():
            if self.BonusCold > 0 and self.BonusElectricity > 0:
                self.BonusMagnetic = self.BonusCold + self.BonusElectricity
                self.BonusCold = 0
                self.BonusElectricity = 0
        def AdjustForRadiation():
            if self.BonusHeat > 0 and self.BonusElectricity > 0:
                self.BonusRadiation = self.BonusHeat + self.BonusElectricity
                self.BonusHeat = 0
                self.BonusElectricity = 0
        def AdjustForViral():
            if self.BonusCold > 0 and self.BonusToxin > 0:
                self.BonusViral = self.BonusCold + self.BonusToxin
                self.BonusCold = 0
                self.BonusToxin = 0

        AdjustmentFuncs = [AdjustForBlast, AdjustForCorrosive, AdjustForGas, AdjustForMagnetic, AdjustForRadiation, AdjustForViral]
        while len(AdjustmentFuncs) > 0:
            chosenFunc = random.choice(AdjustmentFuncs)
            chosenFunc()
            AdjustmentFuncs.remove(chosenFunc)

class Mod():
    def __init__(self, name, modDict, cost, nameForConflicts = "", conflicts = [], canBeDuplicated = False, tags = ["rifle"]):
        self.name = name
        self.modDict = modDict
        self.cost = cost
        self.nameForConflicts = nameForConflicts
        self.conflicts = conflicts
        self.canBeDuplicated = canBeDuplicated
        self.tags = tags

    def apply(self, modProfile):
        modProfile.mods.append(self.name)
        for key in self.modDict:
            if key == "BonusDamageFlat":
                modProfile.BonusDamageFlat += self.modDict[key]
            elif key == "BonusDamagePercent":
                modProfile.BonusDamagePercent += self.modDict[key]
            elif key == "BonusCritChance":
                modProfile.BonusCritChance += self.modDict[key]
            elif key == "BonusCritMultiplier":
                modProfile.BonusCritMultiplier += self.modDict[key]
            elif key == "BonusStatusChance":         
                modProfile.BonusStatusChance += self.modDict[key]
            elif key == "BonusStatusDuration":
                modProfile.BonusStatusDuration += self.modDict[key]
            elif key == "BonusFireRate":
                modProfile.BonusFireRate += self.modDict[key]
            elif key == "BonusMagazine":
                modProfile.BonusMagazine += self.modDict[key]
            elif key == "BonusReload":
                modProfile.BonusReload += self.modDict[key]
            elif key == "BonusMultishot":
                modProfile.BonusMultishot += self.modDict[key]
            elif key == "BonusImpact":
                modProfile.BonusImpact += self.modDict[key]
            elif key == "BonusPuncture":
                modProfile.BonusPuncture += self.modDict[key]
            elif key == "BonusSlash":
                modProfile.BonusSlash += self.modDict[key]
            elif key == "BonusHeat":
                modProfile.BonusHeat += self.modDict[key]
            elif key == "BonusCold":
                modProfile.BonusCold += self.modDict[key]
            elif key == "BonusElectricity":
                modProfile.BonusElectricity += self.modDict[key]
            elif key == "BonusToxin":
                modProfile.BonusToxin += self.modDict[key]
            elif key == "BonusBlast":
                modProfile.BonusBlast += self.modDict[key]
            elif key == "BonusCorrosive":
                modProfile.BonusCorrosive += self.modDict[key]
            elif key == "BonusGas":
                modProfile.BonusGas += self.modDict[key]
            elif key == "BonusMagnetic":
                modProfile.BonusMagnetic += self.modDict[key]
            elif key == "BonusRadiation":
                modProfile.BonusRadiation += self.modDict[key]
            elif key == "BonusViral":
                modProfile.BonusViral += self.modDict[key]



    NUM_LOOPS = 10000000
    NUM_MODS_IN_BUILD = 6
    MAX_COST = 120

    MODS = [
        Mod("Serration", {"BonusDamagePercent": 0.15}, 4, "Serration"),
        Mod("Serration1", {"BonusDamagePercent": 0.3}, 5, "Serration"),
        Mod("Serration2", {"BonusDamagePercent": 0.45}, 6, "Serration"),
        Mod("Serration3", {"BonusDamagePercent": 0.6}, 7, "Serration"),
        Mod("Serration4", {"BonusDamagePercent": 0.75}, 8, "Serration"),
        Mod("Serration5", {"BonusDamagePercent": 0.9}, 9, "Serration"),
        Mod("Serration6", {"BonusDamagePercent": 1.05}, 10, "Serration"),
        Mod("Serration7", {"BonusDamagePercent": 1.2}, 11, "Serration"),
        Mod("Serration8", {"BonusDamagePercent": 1.35}, 12, "Serration"),
        Mod("Serration9", {"BonusDamagePercent": 1.5}, 13, "Serration"),
        Mod("Serration10", {"BonusDamagePercent": 1.65}, 14, "Serration"),

        Mod("CriticalDelay", {"BonusCritChance": 0.333, "BonusFireRate": -0.033}, 4, "CriticalDelay"),
        Mod("CriticalDelay1", {"BonusCritChance": 0.667, "BonusFireRate": -0.067}, 5, "CriticalDelay"),
        Mod("CriticalDelay2", {"BonusCritChance": 1, "BonusFireRate": -0.1}, 6, "CriticalDelay"),
        Mod("CriticalDelay3", {"BonusCritChance": 1.333, "BonusFireRate": -0.133}, 7, "CriticalDelay"),
        Mod("CriticalDelay4", {"BonusCritChance": 1.667, "BonusFireRate": -0.167}, 8, "CriticalDelay"),
        Mod("CriticalDelay5", {"BonusCritChance": 2, "BonusFireRate": -0.2}, 9, "CriticalDelay"),

        Mod("FastHands", {"BonusReload": -0.05}, 2, "FastHands"),
        Mod("FastHands1", {"BonusReload": -0.1}, 3, "FastHands"),
        Mod("FastHands2", {"BonusReload": -0.15}, 4, "FastHands"),
        Mod("FastHands3", {"BonusReload": -0.2}, 5, "FastHands"),
        Mod("FastHands4", {"BonusReload": -0.25}, 6, "FastHands"),
        Mod("FastHands5", {"BonusReload": -0.3}, 7, "FastHands"),

        Mod("Hellfire", {"BonusHeat": 0.15}, 6, "Hellfire"),
        Mod("Hellfire1", {"BonusHeat": 0.3}, 7, "Hellfire"),
        Mod("Hellfire2", {"BonusHeat": 0.45}, 8, "Hellfire"),
        Mod("Hellfire3", {"BonusHeat": 0.6}, 9, "Hellfire"),
        Mod("Hellfire4", {"BonusHeat": 0.75}, 10, "Hellfire"),
        Mod("Hellfire5", {"BonusHeat": 0.9}, 11, "Hellfire"),

        Mod("InfectedClip", {"BonusToxin": 0.15}, 6, "InfectedClip"),
        Mod("InfectedClip1", {"BonusToxin": 0.3}, 7, "InfectedClip"),
        Mod("InfectedClip2", {"BonusToxin": 0.45}, 8, "InfectedClip"),
        Mod("InfectedClip3", {"BonusToxin": 0.6}, 9, "InfectedClip"),
        Mod("InfectedClip4", {"BonusToxin": 0.75}, 10, "InfectedClip"),
        Mod("InfectedClip5", {"BonusToxin": 0.9}, 11, "InfectedClip"),

        Mod("MagazineWarp", {"BonusMagazine": 0.05}, 4, "MagazineWarp"),
        Mod("MagazineWarp1", {"BonusMagazine": 0.1}, 5, "MagazineWarp"),
        Mod("MagazineWarp2", {"BonusMagazine": 0.15}, 6, "MagazineWarp"),
        Mod("MagazineWarp3", {"BonusMagazine": 0.2}, 7, "MagazineWarp"),
        Mod("MagazineWarp4", {"BonusMagazine": 0.25}, 8, "MagazineWarp"),
        Mod("MagazineWarp5", {"BonusMagazine": 0.3}, 9, "MagazineWarp"),

        Mod("Stormbringer", {"BonusElectricity": 0.15}, 6, "Stormbringer"),
        Mod("Stormbringer1", {"BonusElectricity": 0.3}, 7, "Stormbringer"),
        Mod("Stormbringer2", {"BonusElectricity": 0.45}, 8, "Stormbringer"),
        Mod("Stormbringer3", {"BonusElectricity": 0.6}, 9, "Stormbringer"),
        Mod("Stormbringer4", {"BonusElectricity": 0.75}, 10, "Stormbringer"),
        Mod("Stormbringer5", {"BonusElectricity": 0.9}, 11, "Stormbringer"),

        Mod("CryoRounds", {"BonusCold": 0.15}, 6, "CryoRounds"),
        Mod("CryoRounds1", {"BonusCold": 0.3}, 7, "CryoRounds"),
        Mod("CryoRounds2", {"BonusCold": 0.45}, 8, "CryoRounds"),
        Mod("CryoRounds3", {"BonusCold": 0.6}, 9, "CryoRounds"),
        Mod("CryoRounds4", {"BonusCold": 0.75}, 10, "CryoRounds"),
        Mod("CryoRounds5", {"BonusCold": 0.9}, 11, "CryoRounds"),

        Mod("TaintedMag", {"BonusReload": -0.03, "BonusMagazine": 0.06}, 4, "TaintedMag"),
        Mod("TaintedMag1", {"BonusReload": -0.06, "BonusMagazine": 0.12}, 5, "TaintedMag"),
        Mod("TaintedMag2", {"BonusReload": -0.09, "BonusMagazine": 0.18}, 6, "TaintedMag"),
        Mod("TaintedMag3", {"BonusReload": -0.12, "BonusMagazine": 0.24}, 7, "TaintedMag"),
        Mod("TaintedMag4", {"BonusReload": -0.15, "BonusMagazine": 0.3}, 8, "TaintedMag"),
        Mod("TaintedMag5", {"BonusReload": -0.18, "BonusMagazine": 0.36}, 9, "TaintedMag"),
        Mod("TaintedMag6", {"BonusReload": -0.21, "BonusMagazine": 0.42}, 10, "TaintedMag"),
        Mod("TaintedMag7", {"BonusReload": -0.24, "BonusMagazine": 0.48}, 11, "TaintedMag"),
        Mod("TaintedMag8", {"BonusReload": -0.27, "BonusMagazine": 0.54}, 12, "TaintedMag"),
        Mod("TaintedMag9", {"BonusReload": -0.3, "BonusMagazine": 0.6}, 13, "TaintedMag"),
        Mod("TaintedMag10", {"BonusReload": -0.33, "BonusMagazine": 0.66}, 14, "TaintedMag"),

        Mod("PrimedCryoRounds", {"BonusCold": 0.15}, 6, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds1", {"BonusCold": 0.3}, 7, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds2", {"BonusCold": 0.45}, 8, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds3", {"BonusCold": 0.6}, 9, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds4", {"BonusCold": 0.75}, 10, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds5", {"BonusCold": 0.9}, 11, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds6", {"BonusCold": 1.05}, 12, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds7", {"BonusCold": 1.2}, 13, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds8", {"BonusCold": 1.35}, 14, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds9", {"BonusCold": 1.5}, 15, "PrimedCryoRounds"),
        Mod("PrimedCryoRounds10", {"BonusCold": 1.65}, 16, "PrimedCryoRounds"),

        Mod("RifleAmplitude", {"BonusStatusChance": 0.15}, 4, "RifleAmplitude"),
        Mod("RifleAmplitude1", {"BonusStatusChance": 0.3}, 5, "RifleAmplitude"),
        Mod("RifleAmplitude2", {"BonusStatusChance": 0.45}, 6, "RifleAmplitude"),
        Mod("RifleAmplitude3", {"BonusStatusChance": 0.6}, 7, "RifleAmplitude"),
        Mod("RifleAmplitude4", {"BonusStatusChance": 0.75}, 8, "RifleAmplitude"),
        Mod("RifleAmplitude5", {"BonusStatusChance": 0.9}, 9, "RifleAmplitude"),

        Mod("HeavyCaliber", {"BonusDamagePercent": 0.15}, 6, "HeavyCaliber"),
        Mod("HeavyCaliber1", {"BonusDamagePercent": 0.3}, 7, "HeavyCaliber"),
        Mod("HeavyCaliber2", {"BonusDamagePercent": 0.45}, 8, "HeavyCaliber"),
        Mod("HeavyCaliber3", {"BonusDamagePercent": 0.6}, 9, "HeavyCaliber"),
        Mod("HeavyCaliber4", {"BonusDamagePercent": 0.75}, 10, "HeavyCaliber"),
        Mod("HeavyCaliber5", {"BonusDamagePercent": 0.9}, 11, "HeavyCaliber"),
        Mod("HeavyCaliber6", {"BonusDamagePercent": 1.05}, 12, "HeavyCaliber"),
        Mod("HeavyCaliber7", {"BonusDamagePercent": 1.2}, 13, "HeavyCaliber"),
        Mod("HeavyCaliber8", {"BonusDamagePercent": 1.35}, 14, "HeavyCaliber"),
        Mod("HeavyCaliber9", {"BonusDamagePercent": 1.5}, 15, "HeavyCaliber"),
        Mod("HeavyCaliber10", {"BonusDamagePercent": 1.65}, 16, "HeavyCaliber"),

        Mod("MalignantForce", {"BonusToxin": 0.15, "BonusStatusChance": 0.15}, 4, "MalignantForce"),
        Mod("MalignantForce1", {"BonusToxin": 0.3, "BonusStatusChance": 0.3}, 5, "MalignantForce"),
        Mod("MalignantForce2", {"BonusToxin": 0.45, "BonusStatusChance": 0.45}, 6, "MalignantForce"),
        Mod("MalignantForce3", {"BonusToxin": 0.6, "BonusStatusChance": 0.6}, 7, "MalignantForce"),

        Mod("PointStrike", {"BonusCritChance": 0.25}, 4, "PointStrike"),
        Mod("PointStrike1", {"BonusCritChance": 0.5}, 5, "PointStrike"),
        Mod("PointStrike2", {"BonusCritChance": 0.75}, 6, "PointStrike"),
        Mod("PointStrike3", {"BonusCritChance": 1}, 7, "PointStrike"),
        Mod("PointStrike4", {"BonusCritChance": 1.25}, 8, "PointStrike"),
        Mod("PointStrike5", {"BonusCritChance": 1.5}, 9, "PointStrike"),

        Mod("SpeedTrigger", {"BonusFireRate": 0.10}, 4, "SpeedTrigger"),
        Mod("SpeedTrigger1", {"BonusFireRate": 0.20}, 5, "SpeedTrigger"),
        Mod("SpeedTrigger2", {"BonusFireRate": 0.30}, 6, "SpeedTrigger"),
        Mod("SpeedTrigger3", {"BonusFireRate": 0.40}, 7, "SpeedTrigger"),
        Mod("SpeedTrigger4", {"BonusFireRate": 0.50}, 8, "SpeedTrigger"),
        Mod("SpeedTrigger5", {"BonusFireRate": 0.60}, 9, "SpeedTrigger"),

        Mod("SplitChamber", {"BonusMultishot": 0.15}, 10, "SplitChamber"),
        Mod("SplitChamber1", {"BonusMultishot": 0.3}, 11, "SplitChamber"),
        Mod("SplitChamber2", {"BonusMultishot": 0.45}, 12, "SplitChamber"),
        Mod("SplitChamber3", {"BonusMultishot": 0.6}, 13, "SplitChamber"),
        Mod("SplitChamber4", {"BonusMultishot": 0.75}, 14, "SplitChamber"),
        Mod("SplitChamber5", {"BonusMultishot": 0.9}, 15, "SplitChamber"),

        Mod("VitalSense", {"BonusCritMultiplier": 0.20}, 4, "VitalSense"),
        Mod("VitalSense1", {"BonusCritMultiplier": 0.40}, 5, "VitalSense"),
        Mod("VitalSense2", {"BonusCritMultiplier": 0.60}, 6, "VitalSense"),
        Mod("VitalSense3", {"BonusCritMultiplier": 0.80}, 7, "VitalSense"),
        Mod("VitalSense4", {"BonusCritMultiplier": 1.00}, 8, "VitalSense"),
        Mod("VitalSense5", {"BonusCritMultiplier": 1.20}, 9, "VitalSense"),

        Mod("Wildfire", {"BonusHeat": 0.15, "BonusMagazine": 0.05}, 6, "Wildfire"),
        Mod("Wildfire1", {"BonusHeat": 0.3, "BonusMagazine": 0.1}, 7, "Wildfire"),
        Mod("Wildfire2", {"BonusHeat": 0.45, "BonusMagazine": 0.15}, 8, "Wildfire"),
        Mod("Wildfire3", {"BonusHeat": 0.6, "BonusMagazine": 0.2}, 9, "Wildfire"),
    ]

    #modprofile.mods : dps
    Top10 = {}
    NUM_CHANGING_BUILDS = 10
    NUM_CHANGES_PER_ROTATION = 3
    builds = []

    for i in tqdm(range(NUM_LOOPS)):
        #randomly select mods
        if builds == []:
            for j in range(NUM_CHANGING_BUILDS):
                build = []
                cost = 0
                for k in range(NUM_MODS_IN_BUILD):
                    mod = random.choice(MODS)
                    if mod.conflicts != []:
                        for conflict in mod.conflicts:
                            if conflict in [mod.nameForConflicts for mod in build]:
                                continue
                    if cost + mod.cost > MAX_COST:
                        continue
                    build.append(mod)
                    cost += mod.cost
                builds.append(build)
        else:
            for build in builds:
                numModsToChange = random.randint(1, NUM_CHANGES_PER_ROTATION)
                for j in range(numModsToChange):
                    choice = random.randint(0, 2)
                    if choice == 0: #change a mod
                        index = random.randint(0, len(build) - 1)
                        MAX_ATTEMPTS = 100
                        removed = build.pop(index)
                        currentModNames = [mod.nameForConflicts for mod in build]
                        currentCost = sum([mod.cost for mod in build])
                        for k in range(MAX_ATTEMPTS):
                            mod = random.choice(MODS)
                            if mod.nameForConflicts in currentModNames:
                                continue
                            if mod.conflicts != []:
                                for conflict in mod.conflicts:
                                    if conflict in currentModNames:
                                        continue
                            if currentCost + mod.cost > MAX_COST:
                                continue
                            build.append(mod)
                            cost += mod.cost
                            break
                        else:
                            #failed to find a mod for the build, so we'll assume we've got the max cost
                            build.append(removed)
                            continue
                    elif choice == 1: # add a mod
                        if len(build) == NUM_MODS_IN_BUILD:
                            continue
                        MAX_ATTEMPTS = 100
                        currentModNames = [mod.nameForConflicts for mod in build]
                        currentCost = sum([mod.cost for mod in build])
                        for k in range(MAX_ATTEMPTS):
                            mod = random.choice(MODS)
                            if mod.nameForConflicts in currentModNames:
                                continue
                            if mod.conflicts != []:
                                for conflict in mod.conflicts:
                                    if conflict in currentModNames:
                                        continue
                            if currentCost + mod.cost > MAX_COST:
                                continue
                            build.append(mod)
                            cost += mod.cost
                            break
                        else:
                            #failed to find a mod for the build, so we'll assume we've got the max cost
                            continue
                    elif choice == 2: # remove a mod
                        if len(build) == 1:
                            continue
                        index = random.randint(0, len(build) - 1)
                        build.pop(index)
                        continue


        def TestBuild(build, damages, ModLists):
            #apply mods
            modProfile = ModProfile()
            for mod in build:
                mod.apply(modProfile)

            #use the mod profile to mod the weapon
            amprex = Amprex()
            amprex.apply(modProfile)

            #calculate damage over a minute
            damage = 0
            magazine = amprex.magazine
            for i in range(math.floor(amprex.fireRate * 60)):
                if magazine == 0:
                    magazine = amprex.magazine
                    #convert time to reload, into shots fired
                    missedShots = math.ceil(amprex.reload * amprex.fireRate)
                    i += missedShots
                    continue
                hits = 0
                multishot = amprex.multishot
                while multishot >= 1:
                    hits += 1
                    multishot -= 1
                if random.random() < multishot:
                    hits += 1

                for j in range(hits):
                    criticalHits = 0
                    critChance = amprex.critChance
                    while critChance >= 1:
                        criticalHits += 1
                        critChance -= 1
                    if random.random() < critChance:
                        criticalHits += 1
                    
                    critMulti = amprex.critMultiplier
                    if criticalHits > 0:
                        critMulti *= criticalHits
                    else:
                        critMulti = 1

                    totalDamage = 0
                    for key in amprex.damageTypes:
                        totalDamage += amprex.damageTypes[key]
                    
                    totalDamage *= critMulti
                    damage += totalDamage

                magazine -= 1

            damage /= 60 #damage per second
            damage = round(damage, 2)
            damages.append(damage)
            ModLists.append(build)

        NUM_THREADS = 5
        damages = []
        modLists = []
        for i in range(NUM_THREADS):
            thread = threading.Thread(target=TestBuild, args=(builds[i], damages, modLists))
            thread.start()

        for i in range(NUM_THREADS):
            thread.join()
        
        for i in range(NUM_THREADS):
            thread = threading.Thread(target=TestBuild, args=(builds[i+5], damages, modLists))
            thread.start()

        for i in range(NUM_THREADS):
            thread.join()

        #add the build to the top 10
        for i in range(len(damages)):
            damage = damages[i]
            build = modLists[i] 
            if len(Top10) < 10:
                Top10[damage] = build
            else:
                if damage > min(Top10):
                    Top10.pop(min(Top10))
                    Top10[damage] = build

            

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))

    #print the top 10
    i = 1
    for key in Top10:
        print("-----------------" + str(i) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        
#TODO: Change 1 and 2 to pure incremental, the rest are incremental with saved builds
def sequencialTest():
    #Test Single Slot
    from mods import MODS
    from resistances import RESISTANCES
    import guns
    RES = [RESISTANCES["Infested|Fossilized"], RESISTANCES["Infested|Infested Flesh"], RESISTANCES["Infested|Infested"], RESISTANCES["Infested|Infested Sinew"], RESISTANCES["Grineer|Ferrite Armor"]]
    #RES = [RESISTANCES["Grineer|Ferrite Armor"], RESISTANCES["Grineer|Cloned Flesh"], RESISTANCES["Grineer|Alloy Armor"], RESISTANCES["Grineer|Machinery"]]
    #RES = [RESISTANCES["Corpus|Flesh"], RESISTANCES["Corpus|Robotic"], RESISTANCES["Corpus|Shield"], RESISTANCES["Corpus|Proto Shield"], RESISTANCES["Corpus|Alloy Armor"], RESISTANCES["Corpus|Ferrite Armor"]]
    #RES = [RESISTANCES["Corpus|Proto Shield"]]
    MAX_THREADS = 25
    SAVED_BUILDS = 120
    MAX_COST = 31 #TODO: Change this to be an actual mod cost
    USING_FORMA = False
    TARGET_ARMOR = 1000
    WEAPON_CLASS = guns.Regulators
    MINUTES = 1
    Top10 = {}
    SavedBuilds = {}
    #Returns True if there is a conflict
    def CheckForConflicts(mod, build):
        weapon = WEAPON_CLASS()
        weaponTags = weapon.tags
        modNames = [mod.nameForConflicts for mod in build]
        modTags = [mod.tags for mod in build]
        if mod.tags != []:
            for tag in mod.tags:
                if tag not in weaponTags:
                    return True
        if mod.nameForConflicts in modNames and not mod.canBeDuplicated:
            return True
        
        if mod.conflicts != []:
            for conflict in mod.conflicts:
                if conflict in modNames:
                    return True
        cost = math.ceil(mod.cost / 2)
        for mod in build:
            cost += math.ceil(mod.cost / 2)
        if cost > MAX_COST:
            return True
        return False

    def TestBuild(build, damages, ModLists):
        #apply mods
        modProfile = ModProfile()
        for mod in build:
            mod.apply(modProfile)
        modProfile.AdjustForDamageCombinations()
        #use the mod profile to mod the weapon
        weapon = WEAPON_CLASS()
        weapon.apply(modProfile)
        weapon.AdjustForDamageCombinations()

        #calculate damage over a minute
        damage = 0
        magazine = weapon.magazine
        for i in range(math.floor(weapon.fireRate * (60 * MINUTES))):
            if magazine == 0:
                magazine = weapon.magazine
                #convert time to reload, into shots fired
                missedShots = math.ceil(weapon.reload * weapon.fireRate)
                i += missedShots
                continue
            hits = 0
            multishot = weapon.multishot
            while multishot >= 1:
                hits += 1
                multishot -= 1
            if random.random() < multishot:
                hits += 1

            for j in range(hits):
                criticalHits = 0
                critChance = weapon.critChance
                while critChance >= 1:
                    criticalHits += 1
                    critChance -= 1
                if random.random() < critChance:
                    criticalHits += 1
                
                critMulti = weapon.critMultiplier
                if criticalHits > 0:
                    critMulti *= criticalHits
                else:
                    critMulti = 1

                totalDamage = 0
                
                damageProfile = copy.deepcopy(weapon.damageTypes)
                resProfile = random.choice(RES)
                #Apply Armor
                if resProfile.appliesAsArmor:
                    damageProfile = resProfile.applyAsArmor(damageProfile, TARGET_ARMOR)

                #Apply Resistances
                damageProfile = resProfile.applyRes(damageProfile)
                
                for key in damageProfile:
                    totalDamage += damageProfile[key]
                
                totalDamage *= critMulti
                damage += totalDamage

            magazine -= 1

        damage /= (60 * MINUTES) #damage per second
        damage = round(damage, 2)
        damages.append(damage)
        ModLists.append(build)
    
    
    i = 0
    while i <= len(MODS): #single slot, incremental
        damages = []
        modLists = []

        threads = []
        for j in range(MAX_THREADS):
            if i + j >= len(MODS):
                break
            if CheckForConflicts(MODS[i + j], []):
                continue
            thread = threading.Thread(target=TestBuild, args=([MODS[i + j]], damages, modLists))
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        for j in range(len(damages)):
            damage = damages[j]
            build = modLists[j] 
            if len(Top10) < 10:
                Top10[damage] = build
            else:
                if damage > min(Top10):
                    Top10.pop(min(Top10))
                    Top10[damage] = build
            
            if len(SavedBuilds) < SAVED_BUILDS:
                SavedBuilds[damage] = build
            else:
                if damage > min(SavedBuilds):
                    SavedBuilds.pop(min(SavedBuilds))
                    SavedBuilds[damage] = build
        
        i+=MAX_THREADS

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Single Slot, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1
        

    #2 Slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds: #Slot 1, only use saved builds for optimization
            j = 0
            while j <= len(MODS): #Slot 2, incremental
                damages = []
                modLists = []

                threads = []
                for k in range(MAX_THREADS):
                    if j + k >= len(MODS):
                        break
                    if CheckForConflicts(MODS[j + k], previousSavedBuilds[key]):
                        continue
                    mods = previousSavedBuilds[key] + [MODS[j + k]]
                    thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                    threads.append(thread)
            
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                for k in range(len(damages)):
                    damage = damages[k]
                    build = modLists[k] 
                    if len(Top10) < 10:
                        Top10[damage] = build
                    else:
                        if damage > min(Top10):
                            Top10.pop(min(Top10))
                            Top10[damage] = build

                    if len(SavedBuilds) < SAVED_BUILDS:
                        SavedBuilds[damage] = build
                    else:
                        if damage > min(SavedBuilds):
                            SavedBuilds.pop(min(SavedBuilds))
                            SavedBuilds[damage] = build
                
                j+=MAX_THREADS
            pbar.update(1)
        
    
    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Two Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    #3 Slots
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            k = 0
            while k <= len(MODS): #Slot 3, incremental
                damages = []
                modLists = []

                threads = []
                for l in range(MAX_THREADS):
                    if k + l >= len(MODS):
                        break
                    if CheckForConflicts(MODS[k + l], previousSavedBuilds[key]):
                        continue
                    mods = previousSavedBuilds[key] + [MODS[k + l]]
                    thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                    threads.append(thread)
        
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                for l in range(len(damages)):
                    damage = damages[l]
                    build = modLists[l] 
                    if len(Top10) < 10:
                        Top10[damage] = build
                    else:
                        if damage > min(Top10):
                            Top10.pop(min(Top10))
                            Top10[damage] = build
                    
                    if len(SavedBuilds) < SAVED_BUILDS:
                        SavedBuilds[damage] = build
                    else:
                        if damage > min(SavedBuilds):
                            SavedBuilds.pop(min(SavedBuilds))
                            SavedBuilds[damage] = build
                k+=MAX_THREADS
            pbar.update(1)

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Three Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

    #4 Slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            l = 0
            while l <= len(MODS): #Slot 4, incremental
                damages = []
                modLists = []

                threads = []
                for m in range(MAX_THREADS):
                    if l + m >= len(MODS):
                        break
                    if CheckForConflicts(MODS[l + m], previousSavedBuilds[key]):
                        continue
                    mods = previousSavedBuilds[key] + [MODS[l + m]]
                    thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                    threads.append(thread)
        
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                for m in range(len(damages)):
                    damage = damages[m]
                    build = modLists[m] 
                    if len(Top10) < 10:
                        Top10[damage] = build
                    else:
                        if damage > min(Top10):
                            Top10.pop(min(Top10))
                            Top10[damage] = build

                    if len(SavedBuilds) < SAVED_BUILDS:
                        SavedBuilds[damage] = build
                    else:
                        if damage > min(SavedBuilds):
                            SavedBuilds.pop(min(SavedBuilds))
                            SavedBuilds[damage] = build
                
                l+=MAX_THREADS
            pbar.update(1)
    
    
    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Four Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

    #5 Slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            m = 0
            while m <= len(MODS): #Slot 5, incremental
                damages = []
                modLists = []

                threads = []
                for n in range(MAX_THREADS):
                    if m + n >= len(MODS):
                        break
                    if CheckForConflicts(MODS[m + n], previousSavedBuilds[key]):
                        continue
                    mods = previousSavedBuilds[key] + [MODS[m + n]]
                    thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                    threads.append(thread)
        
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                for n in range(len(damages)):
                    damage = damages[n]
                    build = modLists[n] 
                    if len(Top10) < 10:
                        Top10[damage] = build
                    else:
                        if damage > min(Top10):
                            Top10.pop(min(Top10))
                            Top10[damage] = build

                    if len(SavedBuilds) < SAVED_BUILDS:
                        SavedBuilds[damage] = build
                    else:
                        if damage > min(SavedBuilds):
                            SavedBuilds.pop(min(SavedBuilds))
                            SavedBuilds[damage] = build
                
                m+=MAX_THREADS
            pbar.update(1)
    
    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Five Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1
    
    #6 Slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            m = 0
            while m <= len(MODS): #Slot 5, incremental
                damages = []
                modLists = []

                threads = []
                for n in range(MAX_THREADS):
                    if m + n >= len(MODS):
                        break
                    if CheckForConflicts(MODS[m + n], previousSavedBuilds[key]):
                        continue
                    mods = previousSavedBuilds[key] + [MODS[m + n]]
                    thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                    threads.append(thread)
        
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                for n in range(len(damages)):
                    damage = damages[n]
                    build = modLists[n] 
                    if len(Top10) < 10:
                        Top10[damage] = build
                    else:
                        if damage > min(Top10):
                            Top10.pop(min(Top10))
                            Top10[damage] = build

                    if len(SavedBuilds) < SAVED_BUILDS:
                        SavedBuilds[damage] = build
                    else:
                        if damage > min(SavedBuilds):
                            SavedBuilds.pop(min(SavedBuilds))
                            SavedBuilds[damage] = build
                
                m+=MAX_THREADS
            pbar.update(1)

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Six Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

    #7 Slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            m = 0
            while m <= len(MODS):
                damages = []
                modLists = []

                threads = []
                for n in range(MAX_THREADS):
                    if m + n >= len(MODS):
                        break
                    if CheckForConflicts(MODS[m + n], previousSavedBuilds[key]):
                        continue
                    mods = previousSavedBuilds[key] + [MODS[m + n]]
                    thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                    threads.append(thread)
        
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                for n in range(len(damages)):
                    damage = damages[n]
                    build = modLists[n] 
                    if len(Top10) < 10:
                        Top10[damage] = build
                    else:
                        if damage > min(Top10):
                            Top10.pop(min(Top10))
                            Top10[damage] = build

                    if len(SavedBuilds) < SAVED_BUILDS:
                        SavedBuilds[damage] = build
                    else:
                        if damage > min(SavedBuilds):
                            SavedBuilds.pop(min(SavedBuilds))
                            SavedBuilds[damage] = build
                
                m+=MAX_THREADS
            pbar.update(1)

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Seven Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

    #8 Slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            m = 0
            while m <= len(MODS):
                damages = []
                modLists = []

                threads = []
                for n in range(MAX_THREADS):
                    if m + n >= len(MODS):
                        break
                    if CheckForConflicts(MODS[m + n], previousSavedBuilds[key]):
                        continue
                    mods = previousSavedBuilds[key] + [MODS[m + n]]
                    thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                    threads.append(thread)
        
                for thread in threads:
                    thread.start()
                
                for thread in threads:
                    thread.join()
                
                for n in range(len(damages)):
                    damage = damages[n]
                    build = modLists[n] 
                    if len(Top10) < 10:
                        Top10[damage] = build
                    else:
                        if damage > min(Top10):
                            Top10.pop(min(Top10))
                            Top10[damage] = build

                    if len(SavedBuilds) < SAVED_BUILDS:
                        SavedBuilds[damage] = build
                    else:
                        if damage > min(SavedBuilds):
                            SavedBuilds.pop(min(SavedBuilds))
                            SavedBuilds[damage] = build
                
                m+=MAX_THREADS
            pbar.update(1)

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Eight Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

#Sequential, but does 2 mods at a time, takes a while, but may provide better results with combos
def twoByeSequencialTest():
     #Test Single Slot
    from mods import MODS
    from resistances import RESISTANCES
    #RES = [RESISTANCES["Infested|Fossilized"], RESISTANCES["Infested|Infested Flesh"], RESISTANCES["Infested|Infested"], RESISTANCES["Infested|Infested Sinew"], RESISTANCES["Grineer|Ferrite Armor"]]
    #RES = [RESISTANCES["Grineer|Ferrite Armor"], RESISTANCES["Grineer|Cloned Flesh"], RESISTANCES["Grineer|Alloy Armor"], RESISTANCES["Grineer|Machinery"]]
    #RES = [RESISTANCES["Corpus|Flesh"], RESISTANCES["Corpus|Robotic"], RESISTANCES["Corpus|Shield"], RESISTANCES["Corpus|Proto Shield"]]
    RES = [RESISTANCES["Corpus|Proto Shield"]]
    MAX_THREADS = 25
    SAVED_BUILDS = 30
    MAX_COST = 30
    TARGET_ARMOR = 1000
    Top10 = {}
    SavedBuilds = {}
    #Returns True if there is a conflict
    def CheckForConflicts(mod, build):
        modNames = [mod.nameForConflicts for mod in build]
        if mod.nameForConflicts in modNames and not mod.canBeDuplicated:
            return True
        if mod.conflicts != []:
            for conflict in mod.conflicts:
                if conflict in modNames:
                    return True
        cost = math.ceil(mod.cost / 2)
        for mod in build:
            cost += math.ceil(mod.cost / 2)
        if cost > MAX_COST:
            return True
        return False
    
    def CheckForConflictsInBuild(build):
        modNames = [mod.nameForConflicts for mod in build]
        for i in range(len(modNames)):
            for conflict in build[i].conflicts:
                if conflict in modNames:
                    return True
            if not build[i].canBeDuplicated:
                for j in range(i + 1, len(modNames)):
                    if modNames[i] == modNames[j]:
                        return True
        cost = 0
        for mod in build:
            cost += math.ceil(mod.cost / 2)
        if cost > MAX_COST:
            return True
        return False

    def TestBuild(build, damages, ModLists):
        #apply mods
        modProfile = ModProfile()
        for mod in build:
            mod.apply(modProfile)
        modProfile.AdjustForDamageCombinations()
        #use the mod profile to mod the weapon
        weapon = Dera()
        weapon.apply(modProfile)
        weapon.AdjustForDamageCombinations()
        MINUTES = 1

        #calculate damage over a minute
        damage = 0
        magazine = weapon.magazine
        for i in range(math.floor(weapon.fireRate * (60 * MINUTES))):
            if magazine == 0:
                magazine = weapon.magazine
                #convert time to reload, into shots fired
                missedShots = math.ceil(weapon.reload * weapon.fireRate)
                i += missedShots
                continue
            hits = 0
            multishot = weapon.multishot
            while multishot >= 1:
                hits += 1
                multishot -= 1
            if random.random() < multishot:
                hits += 1

            for j in range(hits):
                criticalHits = 0
                critChance = weapon.critChance
                while critChance >= 1:
                    criticalHits += 1
                    critChance -= 1
                if random.random() < critChance:
                    criticalHits += 1
                
                critMulti = weapon.critMultiplier
                if criticalHits > 0:
                    critMulti *= criticalHits
                else:
                    critMulti = 1

                totalDamage = 0
                
                damageProfile = copy.deepcopy(weapon.damageTypes)
                resProfile = random.choice(RES)
                #Apply Armor
                if resProfile.appliesAsArmor:
                    damageProfile = resProfile.applyAsArmor(damageProfile, TARGET_ARMOR)

                #Apply Resistances
                damageProfile = resProfile.applyRes(damageProfile)
                
                for key in damageProfile:
                    totalDamage += damageProfile[key]
                
                totalDamage *= critMulti
                damage += totalDamage

            magazine -= 1

        damage /= (60 * MINUTES) #damage per second
        damage = round(damage, 2)
        damages.append(damage)
        ModLists.append(build)
    
    
    #First 2 slots
    i = 0
    with tqdm(total=len(MODS)) as pbar:
        while i < len(MODS):
            with tqdm(total=len(MODS), leave=False) as pbartwo:
                j = 0
                while j < len(MODS):
                    damages = []
                    modLists = []
                    skips = 0
                    threads = []
                    for k in range(MAX_THREADS):
                        if j + k >= len(MODS):
                            break
                        if CheckForConflicts(MODS[i], [MODS[j + k]]):
                            skips += 1
                            continue
                        thread = threading.Thread(target=TestBuild, args=([MODS[j + k], MODS[i]], damages, modLists))
                        threads.append(thread)
                    
                    for thread in threads:
                        thread.start()
                    
                    for thread in threads:
                        thread.join()
                    
                    for k in range(len(damages)):
                        damage = damages[k]
                        build = modLists[k] 
                        if len(Top10) < 10:
                            Top10[damage] = build
                        else:
                            if damage > min(Top10):
                                Top10.pop(min(Top10))
                                Top10[damage] = build
                        
                        if len(SavedBuilds) < SAVED_BUILDS:
                            SavedBuilds[damage] = build
                        else:
                            if damage > min(SavedBuilds):
                                SavedBuilds.pop(min(SavedBuilds))
                                SavedBuilds[damage] = build
                    pbartwo.update(MAX_THREADS + skips)
                    j+=MAX_THREADS + skips
            i+=1
            pbar.update(1)

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Two Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1
        

    #Second 2 slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            i = 0
            while i < len(MODS):
                while k < len(MODS):
                    damages = []
                    modLists = []
                    skips = 0
                    threads = []
                    for j in range(MAX_THREADS):
                        if k + j >= len(MODS):
                            break
                        if CheckForConflictsInBuild(previousSavedBuilds[key] + [MODS[i], MODS[k + j]]):
                            skips += 1
                            continue
                        mods = previousSavedBuilds[key] + [MODS[i], MODS[j + k]]
                        thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                        threads.append(thread)
                
                    for thread in threads:
                        thread.start()
                    
                    for thread in threads:
                        thread.join()
                    
                    for j in range(len(damages)):
                        damage = damages[j]
                        build = modLists[j] 
                        if len(Top10) < 10:
                            Top10[damage] = build
                        else:
                            if damage > min(Top10):
                                Top10.pop(min(Top10))
                                Top10[damage] = build

                        if len(SavedBuilds) < SAVED_BUILDS:
                            SavedBuilds[damage] = build
                        else:
                            if damage > min(SavedBuilds):
                                SavedBuilds.pop(min(SavedBuilds))
                                SavedBuilds[damage] = build
                    k += MAX_THREADS + skips
                i += 1
            pbar.update(1)
        
    
    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Four Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

    #3rd 2 slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            i = 0
            while i < len(MODS):
                while k < len(MODS):
                    damages = []
                    modLists = []
                    skips = 0
                    threads = []
                    for j in range(MAX_THREADS):
                        if k + j >= len(MODS):
                            break
                        if CheckForConflictsInBuild(previousSavedBuilds[key] + [MODS[i], MODS[k + j]]):
                            skips += 1
                            continue
                        mods = previousSavedBuilds[key] + [MODS[i], MODS[j + k]]
                        thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                        threads.append(thread)
                
                    for thread in threads:
                        thread.start()
                    
                    for thread in threads:
                        thread.join()
                    
                    for j in range(len(damages)):
                        damage = damages[j]
                        build = modLists[j] 
                        if len(Top10) < 10:
                            Top10[damage] = build
                        else:
                            if damage > min(Top10):
                                Top10.pop(min(Top10))
                                Top10[damage] = build

                        if len(SavedBuilds) < SAVED_BUILDS:
                            SavedBuilds[damage] = build
                        else:
                            if damage > min(SavedBuilds):
                                SavedBuilds.pop(min(SavedBuilds))
                                SavedBuilds[damage] = build
                    k += MAX_THREADS + skips
                i += 1
            pbar.update(1)

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Six Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

    #4th two Slots
    previousSavedBuilds = SavedBuilds
    SavedBuilds = {}
    with tqdm(total=len(previousSavedBuilds)) as pbar:
        for key in previousSavedBuilds:
            i = 0
            with tqdm(total=len(MODS), leave=False) as pbartwo:
                while i < len(MODS):
                    with tqdm(total=len(MODS), leave=False) as pbarthree:
                        while k < len(MODS):
                            damages = []
                            modLists = []
                            skips = 0
                            threads = []
                            for j in range(MAX_THREADS):
                                if k + j >= len(MODS):
                                    break
                                if CheckForConflictsInBuild(previousSavedBuilds[key] + [MODS[i], MODS[k + j]]):
                                    skips += 1
                                    continue
                                mods = previousSavedBuilds[key] + [MODS[i], MODS[j + k]]
                                thread = threading.Thread(target=TestBuild, args=(mods, damages, modLists))
                                threads.append(thread)
                        
                            for thread in threads:
                                thread.start()
                            
                            for thread in threads:
                                thread.join()
                            
                            for j in range(len(damages)):
                                damage = damages[j]
                                build = modLists[j] 
                                if len(Top10) < 10:
                                    Top10[damage] = build
                                else:
                                    if damage > min(Top10):
                                        Top10.pop(min(Top10))
                                        Top10[damage] = build

                                if len(SavedBuilds) < SAVED_BUILDS:
                                    SavedBuilds[damage] = build
                                else:
                                    if damage > min(SavedBuilds):
                                        SavedBuilds.pop(min(SavedBuilds))
                                        SavedBuilds[damage] = build
                            pbarthree.update(MAX_THREADS + skips)
                            k += MAX_THREADS + skips
                pbartwo.update(1)
                i += 1
            pbar.update(1)
    
    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Eight Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

#PURE Incremental, takes a freaking long time
def incrementalTest():
    #Test Single Slot
    from mods import MODS
    from resistances import RESISTANCES
    #RES = [RESISTANCES["Infested|Fossilized"], RESISTANCES["Infested|Infested Flesh"], RESISTANCES["Infested|Infested"], RESISTANCES["Infested|Infested Sinew"], RESISTANCES["Grineer|Ferrite Armor"]]
    RES = [RESISTANCES["Grineer|Ferrite Armor"], RESISTANCES["Grineer|Cloned Flesh"], RESISTANCES["Grineer|Alloy Armor"], RESISTANCES["Grineer|Machinery"]]
    MAX_THREADS = 15
    MAX_COST = 57
    TARGET_ARMOR = 300
    Top10 = {}
    #Returns True if there is a conflict
    def CheckForConflicts(mod, build):
        modNames = [mod.nameForConflicts for mod in build]
        if mod.nameForConflicts in modNames and not mod.canBeDuplicated:
            return True
        if mod.conflicts != []:
            for conflict in mod.conflicts:
                if conflict in modNames:
                    return True
        cost = math.ceil(mod.cost / 2)
        for mod in build:
            cost += math.ceil(mod.cost / 2)
        if cost > MAX_COST:
            return True
        return False
    
    def CheckForConflicts(build):
        modNames = [mod.nameForConflicts for mod in build]
        for i in range(len(modNames)):
            for conflict in build[i].conflicts:
                if conflict in modNames:
                    return True
            if not build[i].canBeDuplicated:
                for j in range(i + 1, len(modNames)):
                    if modNames[i] == modNames[j]:
                        return True
        cost = 0
        for mod in build:
            cost += math.ceil(mod.cost / 2)
        if cost > MAX_COST:
            return True
        return False

    def TestBuild(build, damages, ModLists):
        #apply mods
        modProfile = ModProfile()
        for mod in build:
            mod.apply(modProfile)
        modProfile.AdjustForDamageCombinations()
        #use the mod profile to mod the weapon
        amprex = Amprex()
        amprex.apply(modProfile)
        amprex.AdjustForDamageCombinations()
        MINUTES = 5

        #calculate damage over a minute
        damage = 0
        magazine = amprex.magazine
        for i in range(math.floor(amprex.fireRate * (60 * MINUTES))):
            if magazine == 0:
                magazine = amprex.magazine
                #convert time to reload, into shots fired
                missedShots = math.ceil(amprex.reload * amprex.fireRate)
                i += missedShots
                continue
            hits = 0
            multishot = amprex.multishot
            while multishot >= 1:
                hits += 1
                multishot -= 1
            if random.random() < multishot:
                hits += 1

            for j in range(hits):
                criticalHits = 0
                critChance = amprex.critChance
                while critChance >= 1:
                    criticalHits += 1
                    critChance -= 1
                if random.random() < critChance:
                    criticalHits += 1
                
                critMulti = amprex.critMultiplier
                if criticalHits > 0:
                    critMulti *= criticalHits
                else:
                    critMulti = 1

                totalDamage = 0
                
                damageProfile = copy.deepcopy(amprex.damageTypes)
                resProfile = random.choice(RES)
                #Apply Armor
                if resProfile.appliesAsArmor:
                    damageProfile = resProfile.applyAsArmor(damageProfile, TARGET_ARMOR)

                #Apply Resistances
                damageProfile = resProfile.applyRes(damageProfile)
                
                for key in damageProfile:
                    totalDamage += damageProfile[key]
                
                totalDamage *= critMulti
                damage += totalDamage

            magazine -= 1

        damage /= (60 * MINUTES) #damage per second
        damage = round(damage, 2)
        damages.append(damage)
        ModLists.append(build)
    
    
    totalCombos = len(MODS)**8

    def GenerateAllCombos():
        print("Generating all combos...")
        combos = []
        indexes = [0, 0, 0, 0, 0, 0, 0, 0]
        with tqdm(total=totalCombos) as pbar:
            while indexes[0] < len(MODS):
                while indexes[1] < len(MODS):
                    while indexes[2] < len(MODS):
                        while indexes[3] < len(MODS):
                            while indexes[4] < len(MODS):
                                while indexes[5] < len(MODS):
                                    while indexes[6] < len(MODS):
                                        while indexes[7] < len(MODS):
                                            #check for only unique combinations
                                            indexList = copy.deepcopy(indexes)
                                            indexList.sort()
                                            if indexList in combos:
                                                indexes[7] += 1
                                                pbar.update(1)
                                                continue
                                            build = []
                                            for index in indexes:
                                                build.append(MODS[index])
                                            if CheckForConflicts(build):
                                                indexes[7] += 1
                                                pbar.update(1)
                                                continue
                                            combos.append(indexList)
                                            pbar.update(1)
                                            indexes[7] += 1
                                        indexes[7] = 0
                                        indexes[6] += 1
                                    indexes[6] = 0
                                    indexes[5] += 1
                                indexes[5] = 0
                                indexes[4] += 1
                            indexes[4] = 0
                            indexes[3] += 1
                        indexes[3] = 0
                        indexes[2] += 1
                    indexes[2] = 0
                    indexes[1] += 1
                indexes[1] = 0
                indexes[0] += 1
        
        return combos

    builds = GenerateAllCombos()

    print("Testing all combos...")
    with tqdm(total=len(builds)) as pbar:
        i = 0
        while i < len(builds):
            damages = []
            modLists = []
            threads = []
            for j in range(MAX_THREADS):
                if i + j >= len(builds):
                    break
                thread = threading.Thread(target=TestBuild, args=(builds[i + j], damages, modLists))
                threads.append(thread)
                i += 1
            
            for thread in threads:
                thread.start()
            
            for thread in threads:
                thread.join()
            
            for j in range(len(damages)):
                damage = damages[j]
                build = modLists[j]
                if len(Top10) < 10:
                    Top10[damage] = build
                else:
                    if damage > min(Top10):
                        Top10.pop(min(Top10))
                        Top10[damage] = build

    #sort the top 10
    Top10 = dict(sorted(Top10.items(), reverse=True))
    print("Two Slots, Top Ten")
    num = 1
    for key in Top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in Top10[key]])))
        print("Mods: ")
        for mod in Top10[key]:
            print(mod.name)
        num += 1

#Use this with breakpoints to test a single build, to check math
def TestZone():
    def TestBuild(build, damages, ModLists):
        from resistances import RESISTANCES
        import guns
        #apply mods
        modProfile = ModProfile()
        for mod in build:
            mod.apply(modProfile)

        #use the mod profile to mod the weapon
        weapon = guns.Regulators()
        modProfile.AdjustForDamageCombinations()
        weapon.apply(modProfile)
        weapon.AdjustForDamageCombinations()
        weapon.damageTypes = RESISTANCES["Grineer|Cloned Flesh"].applyRes(weapon.damageTypes)

        # damageProfile = copy.deepcopy(weapon.damageTypes)
        # damageProfile = RESISTANCES["Grineer|Alloy Armor"].applyRes(damageProfile)

        #calculate damage over a minute
        damage = 0
        magazine = weapon.magazine
        for i in range(math.floor(weapon.fireRate * 60)):
            if magazine == 0:
                magazine = weapon.magazine
                #convert time to reload, into shots fired
                missedShots = math.ceil(weapon.reload * weapon.fireRate)
                i += missedShots
                continue
            hits = 0
            multishot = weapon.multishot
            while multishot >= 1:
                hits += 1
                multishot -= 1
            if random.random() < multishot:
                hits += 1

            for j in range(hits):
                criticalHits = 0
                critChance = weapon.critChance
                while critChance >= 1:
                    criticalHits += 1
                    critChance -= 1
                if random.random() < critChance:
                    criticalHits += 1
                
                critMulti = weapon.critMultiplier
                if criticalHits > 0:
                    critMulti *= criticalHits
                else:
                    critMulti = 1

                totalDamage = 0
                # for key in damageProfile:
                #     totalDamage += damageProfile[key]
                for key in weapon.damageTypes:
                    totalDamage += weapon.damageTypes[key]
                
                totalDamage *= critMulti
                damage += totalDamage

            magazine -= 1

        damage /= 60 #damage per second
        damage = round(damage, 2)
        damages.append(damage)
        ModLists.append(build)

    from mods import MODS
    build = []
    for mod in MODS:
        if mod.name == "PistolGambit5":
            build.append(mod)
        if mod.name == "SawtoothClip5":
            build.append(mod)

    TestBuild(build, [], [])

if __name__ == '__main__':
    #TestZone()
    sequencialTest()
    #incrementalTest()
    #twoByeSequencialTest()
            

                


            