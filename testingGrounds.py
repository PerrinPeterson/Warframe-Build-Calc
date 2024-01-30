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
            

                


            