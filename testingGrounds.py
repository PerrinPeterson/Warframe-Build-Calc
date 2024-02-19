import random
import math
import threading
from tqdm import tqdm
import copy
import os

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
        self.BonusToGrineer = 0
        self.BonusToCorpus = 0
        self.BonusToInfested = 0
        self.BonusToCorrupted = 0

        self.mods = []

    def AdjustForDamageCombinations(self, mods):
        ComboDict = {}
        for mod in mods:
            if "BonusElectricity" in mod.modDict:
                if "BonusElectricity" not in ComboDict:
                    ComboDict["BonusElectricity"] = mod.modDict["BonusElectricity"]
                else:
                    ComboDict["BonusElectricity"] += mod.modDict["BonusElectricity"]
            if "BonusHeat" in mod.modDict:
                if "BonusHeat" not in ComboDict:
                    ComboDict["BonusHeat"] = mod.modDict["BonusHeat"]
                else:
                    ComboDict["BonusHeat"] += mod.modDict["BonusHeat"]
            if "BonusCold" in mod.modDict:
                if "BonusCold" not in ComboDict:
                    ComboDict["BonusCold"] = mod.modDict["BonusCold"]
                else:
                    ComboDict["BonusCold"] += mod.modDict["BonusCold"]
            if "BonusToxin" in mod.modDict:
                if "BonusToxin" not in ComboDict:
                    ComboDict["BonusToxin"] = mod.modDict["BonusToxin"]
                else:
                    ComboDict["BonusToxin"] += mod.modDict["BonusToxin"]
        for key in ComboDict:
            if ComboDict[key] > 0:
                for keyTwo in ComboDict:
                    if keyTwo != key and ComboDict[keyTwo] > 0 and ComboDict[key] > 0:
                        if key == "BonusHeat" and keyTwo == "BonusCold":
                            self.BonusBlast = ComboDict[key] + ComboDict[keyTwo]
                            ComboDict[key] = 0
                            ComboDict[keyTwo] = 0
                            self.BonusHeat = 0
                            self.BonusCold = 0
                        if key == "BonusElectricity" and keyTwo == "BonusToxin":
                            self.BonusCorrosive = ComboDict[key] + ComboDict[keyTwo]
                            ComboDict[key] = 0
                            ComboDict[keyTwo] = 0
                            self.BonusElectricity = 0
                            self.BonusToxin = 0
                        if key == "BonusHeat" and keyTwo == "BonusToxin":
                            self.BonusGas = ComboDict[key] + ComboDict[keyTwo]
                            ComboDict[key] = 0
                            ComboDict[keyTwo] = 0
                            self.BonusHeat = 0
                            self.BonusToxin = 0
                        if key == "BonusCold" and keyTwo == "BonusElectricity":
                            self.BonusMagnetic = ComboDict[key] + ComboDict[keyTwo]
                            ComboDict[key] = 0
                            ComboDict[keyTwo] = 0
                            self.BonusCold = 0
                            self.BonusElectricity = 0
                        if key == "BonusHeat" and keyTwo == "BonusElectricity":
                            self.BonusRadiation = ComboDict[key] + ComboDict[keyTwo]
                            ComboDict[key] = 0
                            ComboDict[keyTwo] = 0
                            self.BonusHeat = 0
                            self.BonusElectricity = 0
                        if key == "BonusCold" and keyTwo == "BonusToxin":
                            self.BonusViral = ComboDict[key] + ComboDict[keyTwo]
                            ComboDict[key] = 0
                            ComboDict[keyTwo] = 0
                            self.BonusCold = 0
                            self.BonusToxin = 0





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
            elif key == "BonusToGrineer":
                modProfile.BonusToGrineer += (1 - self.modDict[key])
            elif key == "BonusToCorpus":
                modProfile.BonusToCorpus += (1 - self.modDict[key])
            elif key == "BonusToInfested":
                modProfile.BonusToInfested += (1 - self.modDict[key])
            elif key == "BonusToCorrupted":
                modProfile.BonusToCorrupted += (1 - self.modDict[key])


   
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
    MAX_THREADS = 200
    SAVED_BUILDS = 60
    MAX_COST = 60
    USING_FORMA = True
    TARGET_ARMOR = 300
    WEAPON_CLASS = guns.Boar
    MINUTES = 0.5
    Top10 = {}
    SavedBuilds = {}
    #Returns True if there is a conflict
    def CheckForConflicts(mod, build):
        weapon = WEAPON_CLASS()
        weaponTags = weapon.tags
        modNames = [mod.nameForConflicts for mod in build]
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
        if USING_FORMA:
            cost = math.ceil(mod.cost / 2)
            for mod in build:
                cost += math.ceil(mod.cost / 2)
        else:
            cost = mod.cost
            for mod in build:
                cost += mod.cost
        if cost > MAX_COST:
            return True
        return False

    def TestBuild(build, damages, ModLists):
        #apply mods
        modProfile = ModProfile()
        for mod in build:
            mod.apply(modProfile)
        modProfile.AdjustForDamageCombinations(build)
        #use the mod profile to mod the weapon
        weapon = WEAPON_CLASS()
        weapon.apply(modProfile)
        weapon.AdjustForDamageCombinations(build)

        # if len(build) == 2:
        #     if (build[0].name == "PrimedChargedShell7" and build[1].name == "ContagiousSpread5") or (build[1].name == "PrimedChargedShell7" and build[0].name == "ContagiousSpread5"):
        #         print(weapon.damageTypes)
        
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


def evolutionTest():
    import guns
    from resistances import RESISTANCES
    from mods import MODS
    MAX_ITERATIONS = 10000
    MIN_PERCENT_INCREASE = 0.001
    BUILD_SIZE = 8
    #RES = [RESISTANCES["Infested|Fossilized"], RESISTANCES["Infested|Infested Flesh"], RESISTANCES["Infested|Infested"], RESISTANCES["Infested|Infested Sinew"], RESISTANCES["Grineer|Ferrite Armor"]]
    #RES = [RESISTANCES["Grineer|Ferrite Armor"], RESISTANCES["Grineer|Cloned Flesh"], RESISTANCES["Grineer|Alloy Armor"], RESISTANCES["Grineer|Machinery"]]
    #RES = [RESISTANCES["Corpus|Flesh"], RESISTANCES["Corpus|Robotic"], RESISTANCES["Corpus|Shield"], RESISTANCES["Corpus|Proto Shield"], RESISTANCES["Corpus|Alloy Armor"], RESISTANCES["Corpus|Ferrite Armor"]]
    #RES = [RESISTANCES["Corpus|Proto Shield"]]
    RES = []
    for resistance in RESISTANCES:
        RES.append(RESISTANCES[resistance])
    MAX_COST = 60
    USING_FORMA = True
    TARGET_ARMOR = 300
    WEAPON_CLASS = guns.Amprex
    MINUTES = 5

    weightedModChances = [1/len(MODS) for i in range(len(MODS))]
    weightedModSlots = [1/BUILD_SIZE for i in range(BUILD_SIZE)]
    def mutateBuild(numMutations, build):
        changedIndexes = []

        def changeMod():
            if i == 6:
                bp = 1
            ModToMutate = random.choices(range(BUILD_SIZE), weightedModSlots)[0]
            changedIndexes.append(ModToMutate)
            while True:
                newMod = random.choices(MODS, weightedModChances)[0]
                build[ModToMutate] = newMod
                if not CheckForConflicts(build):
                    weightedModChances[MODS.index(newMod)] *= 1.01
                    break
                weightedModChances[MODS.index(newMod)] *= 0.99
        
        #Tries to upgrade a mod, if it fails, it tries again, up to 10 times
        def upgradeMod():
            MAX_ATTEMPTS = 10
            for i in range(MAX_ATTEMPTS):
                ModToMutate = random.choices(range(BUILD_SIZE), weightedModSlots)[0]
                changedIndexes.append(ModToMutate)
                upgradedModIndex = MODS.index(build[ModToMutate]) + 1
                if upgradedModIndex >= len(MODS):
                    weightedModSlots[ModToMutate] *= 0.99
                    continue
                if MODS[upgradedModIndex].nameForConflicts != build[ModToMutate].nameForConflicts:
                    weightedModSlots[ModToMutate] *= 0.99
                    continue #If the mods are different types, don't upgrade
                build[ModToMutate] = MODS[upgradedModIndex]
                if not CheckForConflicts(build):
                    weightedModChances[upgradedModIndex] *= 1.01
                    weightedModSlots[ModToMutate] *= 1.01
                    changedIndexes.append(ModToMutate)
                    break

        def downgradeMod():
            MAX_ATTEMPTS = 10
            for i in range(MAX_ATTEMPTS):
                ModToMutate = random.choices(range(BUILD_SIZE), weightedModSlots)[0]
                changedIndexes.append(ModToMutate)
                downgradedModIndex = MODS.index(build[ModToMutate]) - 1
                if downgradedModIndex < 0:
                    weightedModSlots[ModToMutate] *= 0.99
                    continue
                if MODS[downgradedModIndex].nameForConflicts != build[ModToMutate].nameForConflicts:
                    weightedModSlots[ModToMutate] *= 0.99
                    continue
                build[ModToMutate] = MODS[downgradedModIndex]
                if not CheckForConflicts(build):
                    weightedModChances[downgradedModIndex] *= 1.01
                    weightedModSlots[ModToMutate] *= 1.01
                    changedIndexes.append(ModToMutate)
                    break

        def removeMod():
            ModToMutate = random.choices(range(BUILD_SIZE), weightedModSlots)[0]
            changedIndexes.append(ModToMutate)
            build[ModToMutate] = MODS[0]
            weightedModChances[0] *= 1.01
            weightedModSlots[ModToMutate] *= 1.01

        def DoNothing():
            pass

        funcs = [changeMod, upgradeMod, downgradeMod, removeMod, DoNothing]

        for i in range(numMutations):
            funcs[random.randint(0, 3)]()
        return build, changedIndexes

    def CheckForConflicts(build):
        weapon = WEAPON_CLASS()
        weaponTags = weapon.tags
        modNames = [mod.nameForConflicts for mod in build]
        modTags = [mod.tags for mod in build]
        if weaponTags != []:
            for tagList in modTags:
                for tag in tagList:
                    if tag == []:
                        continue
                    if tag not in weapon.tags:
                        return True
        for i in range(len(build)):
            j = 1
            while i + j < len(build):
                if build[i].nameForConflicts == build[i + j].nameForConflicts and not build[i].canBeDuplicated:
                    return True
                if build[i].nameForConflicts in build[i + j].conflicts:
                    return True
                if build[i + j].nameForConflicts in build[i].conflicts:
                    return True
                j += 1
        if USING_FORMA:
            cost = sum([math.ceil(mod.cost / 2) for mod in build])
        else:
            cost = sum([mod.cost for mod in build])
        if cost > MAX_COST:
            return True
        return False

    def TestBuild(build, damages, ModLists):
        #apply mods
        modProfile = ModProfile()
        for mod in build:
            mod.apply(modProfile)
        modProfile.AdjustForDamageCombinations(build)
        #use the mod profile to mod the weapon
        weapon = WEAPON_CLASS()
        weapon.apply(modProfile)
        weapon.AdjustForDamageCombinations(build)

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

                #Apply Faction Bonuses
                if modProfile.BonusToGrineer > 0 and resProfile.factionTag == "Grineer":
                    for key in damageProfile:
                        damageProfile[key] *= (1 + modProfile.BonusToGrineer)
                if modProfile.BonusToCorpus > 0 and resProfile.factionTag == "Corpus":
                    for key in damageProfile:
                        damageProfile[key] *= (1 + modProfile.BonusToCorpus)
                if modProfile.BonusToInfested > 0 and resProfile.factionTag == "Infested":
                    for key in damageProfile:
                        damageProfile[key] *= (1 + modProfile.BonusToInfested)
                if modProfile.BonusToCorrupted > 0 and resProfile.factionTag == "Corrupted":
                    for key in damageProfile:
                        damageProfile[key] *= (1 + modProfile.BonusToCorrupted)

                #Apply Resistances
                damageProfile = resProfile.applyRes(damageProfile)

                #Apply Armor
                if resProfile.appliesAsArmor:
                    damageProfile = resProfile.applyAsArmor(damageProfile, TARGET_ARMOR)
                
                for key in damageProfile:
                    totalDamage += damageProfile[key]
                
                totalDamage *= critMulti
                damage += totalDamage

            magazine -= 1

        damage /= (60 * MINUTES) #damage per second
        damage = round(damage, 2)
        damages.append(damage)
        ModLists.append(build)

    i = BUILD_SIZE
    build = [MODS[0] for i in range(BUILD_SIZE)]
    previousBuild = []
    top10 = {}
    #with tqdm(total=len(previousSavedBuilds)) as pbar:
    with tqdm(total=BUILD_SIZE) as pbar:
        while i > 0:
            j = 0
            with tqdm(total=MAX_ITERATIONS / i, leave=False) as pbar2:
                while j < MAX_ITERATIONS / i:
                    damages = []
                    modLists = []
                    indexes = []
                    if build != previousBuild:
                        previousBuild = copy.copy(build)
                    build, indexes = mutateBuild(i, build)

                    TestBuild(build, damages, modLists)

                    for k in range(len(damages)):
                        damage = damages[k]
                        build = modLists[k]
                        if len(top10) < 10:
                            top10[damage] = build
                            pbar2.n = 0
                            pbar2.refresh()
                            j = 0
                            continue
                        else:
                            if damage - (damage * MIN_PERCENT_INCREASE) > max(top10): #So we're not getting random slight increases repeatedly
                                for mod in build:
                                    weightedModChances[MODS.index(mod)] *= 1.01
                                for index in indexes:
                                    weightedModSlots[index] *= 1.01
                                top10.pop(min(top10))
                                top10[damage] = build
                                j = 0
                                os.system('cls' if os.name == 'nt' else 'clear')
                                key = max(top10)
                                print("DPS: " + str(key))
                                print("Cost: " + str(sum([mod.cost for mod in top10[key]])))
                                print("Mods: ")
                                for mod in top10[key]:
                                    print(mod.name)
                                continue
                            elif damage >= max(top10) and sum([mod.cost for mod in build]) < sum([mod.cost for mod in top10[max(top10)]]):
                                for mod in build:
                                    weightedModChances[MODS.index(mod)] *= 1.01
                                for index in indexes:
                                    weightedModSlots[index] *= 1.01
                                top10.pop(max(top10))
                                top10[damage] = build
                                j = 0
                                os.system('cls' if os.name == 'nt' else 'clear')
                                key = max(top10)
                                print("DPS: " + str(key))
                                print("Cost: " + str(sum([mod.cost for mod in top10[key]])))
                                print("Mods: ")
                                for mod in top10[key]:
                                    print(mod.name)
                                continue
                            else:
                                for mod in build:
                                    weightedModChances[MODS.index(mod)] *= 0.99
                                for index in indexes:
                                    weightedModSlots[index] *= 0.99
                                build = copy.copy(previousBuild)
                    j+=1
                    if pbar2.n < j:
                        pbar2.update(1)
            pbar.update(1)
            i-=1

    #sort the top 10
    top10 = dict(sorted(top10.items(), reverse=True))
    print("Evolution, Top Ten")
    num = 1
    for key in top10:
        print("-----------------" + str(num) + "-----------------")
        print("DPS: " + str(key))
        print("Cost: " + str(sum([mod.cost for mod in top10[key]])))
        print("Mods: ")
        for mod in top10[key]:
            print(mod.name)
        num += 1

#Sequential, but does 2 mods at a time, takes a while, but may provide better results with combos
def twoByeSequencialTest():
     #Test Single Slot
    from mods import MODS
    from resistances import RESISTANCES
    import guns
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
        weapon = guns.Dera()
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
    import guns
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
        amprex = guns.Amprex()
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
        weapon = guns.Boar()
        modProfile.AdjustForDamageCombinations(build)
        weapon.apply(modProfile)
        weapon.AdjustForDamageCombinations(build)
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
        if mod.name == "ContagiousSpread5":
            build.append(mod)
    for mod in MODS:
        if mod.name == "IncendiaryCoat5":
            build.append(mod)
    for mod in MODS:
        if mod.name == "ChillingGrasp3":
            build.append(mod)
    for mod in MODS:
        if mod.name == "ToxicBarrage3":
            build.append(mod)
    for mod in MODS:
        if mod.name == "PrimedChargedShell10":
            build.append(mod)

    TestBuild(build, [], [])

def openUI():
    import tkinter as tk
    import guns

    window = tk.Tk()
    window.title("Warframe DPS Calculator")
    window.geometry("1280x720")

    leftFrame = tk.Frame(window)
    leftFrame.grid(row=0, column=0, padx=10, pady=10)


    #gunList
    gunChoiceFrame = tk.Frame(leftFrame, bg="lightgrey")
    gunChoiceFrame.grid(row=0, column=0, padx=10, pady=10)
    gunLabel = tk.Label(gunChoiceFrame, text="Choose a weapon", font=("Arial", 12), bg="lightgrey")
    gunLabel.grid(row=0, column=0, padx=10, pady=10)
    gunList = tk.Listbox(gunChoiceFrame, height=10, width=20)
    gunList.grid(row=1, column=0, padx=10, pady=10)
    weapons = guns.getWeaponList()
    for weapon in weapons:
        gunList.insert(tk.END, weapon.name)
    gunList.selection_set(0)
    #grabbing the index of selected gun
    selectedGun = weapons[0]

    #sliders
    sliderFrame = tk.Frame(leftFrame, bg="lightgrey")
    sliderFrame.grid(row=1, column=0, padx=10, pady=10)
    #threads
    threadLabel = tk.Label(sliderFrame, text="Threads", font=("Arial", 12), bg="lightgrey")
    threadLabel.grid(row=0, column=0, padx=10, pady=10)
    threadSlider = tk.Scale(sliderFrame, from_=1, to=50, orient="horizontal", bg="lightgrey")
    threadSlider.grid(row=1, column=0, padx=10, pady=10)
    threadSlider.set(10)
    #maxCost
    maxCostLabel = tk.Label(sliderFrame, text="Max Cost", font=("Arial", 12), bg="lightgrey")
    maxCostLabel.grid(row=2, column=0, padx=10, pady=10)
    maxCostSlider = tk.Scale(sliderFrame, from_=1, to=60, orient="horizontal", bg="lightgrey")
    maxCostSlider.grid(row=3, column=0, padx=10, pady=10)
    maxCostSlider.set(30)
    #MaxSavedBuilds
    maxSavedLabel = tk.Label(sliderFrame, text="Max Saved Builds", font=("Arial", 12), bg="lightgrey")
    maxSavedLabel.grid(row=4, column=0, padx=10, pady=10)
    maxSavedSlider = tk.Scale(sliderFrame, from_=10, to=120, orient="horizontal", bg="lightgrey")
    maxSavedSlider.grid(row=5, column=0, padx=10, pady=10)
    maxSavedSlider.set(120)

    #Mods Selection window
    import mods
    modFrame = tk.Frame(window, bg="lightgrey")
    modFrame.grid(row=0, column=1, padx=10, pady=10)
    modLabel = tk.Label(modFrame, text="Mod Inventory", font=("Arial", 12), bg="lightgrey")
    modLabel.grid(row=0, column=0, padx=10, pady=10)
    modList = tk.Listbox(modFrame, height=30, width=30)
    modList.grid(row=1, column=0, padx=10, pady=10)
    #To track dissabled mods
    modDict = {} 
    for mod in mods.MODS:
        if mod.name != "EmptyMod":
            if mod.nameForConflicts not in modList.get(0, tk.END):
                modList.insert(tk.END, mod.nameForConflicts)
    
    
    #grey out mods that the user clicked
    def onselect(evt):
        #if the selection isn't in the modList, return
        if len(evt.widget.curselection()) == 0:
            return
        w = evt.widget
        index = int(w.curselection()[0])
        if w.itemcget(index, "fg") == "#464646":
            w.itemconfig(index, fg="#dedede")
        else:
            w.itemconfig(index, fg="#464646")
        #deselect
        w.selection_clear(index)

    modList.bind('<<ListboxSelect>>', onselect)
    
    def selectAll(list, trackingDict):
        for i in range(list.size()):
            list.itemconfig(i, fg="#464646")
            trackingDict[modList.get(i)] = True
    
    def deselectAll(list, trackingDict):
        for i in range(list.size()):
            list.itemconfig(i, fg="#dedede")
            trackingDict[modList.get(i)] = False
    selectAll(modList, modDict)
    
    #buttons
    buttonFrame = tk.Frame(modFrame, bg="lightgrey")
    buttonFrame.grid(row=2, column=0, padx=10, pady=10)
    selectAllButton = tk.Button(buttonFrame, text="Select All", command= lambda: selectAll(modList, modDict))
    selectAllButton.grid(row=0, column=0, padx=10, pady=10)
    deselectAllButton = tk.Button(buttonFrame, text="Deselect All", command= lambda: deselectAll(modList, modDict))
    deselectAllButton.grid(row=0, column=1, padx=10, pady=10)

    #Armors Column
    import resistances
    armorFrame = tk.Frame(window, bg="lightgrey")
    armorFrame.grid(row=0, column=2, padx=10, pady=10)
    armorLabel = tk.Label(armorFrame, text="Choose Armor", font=("Arial", 12), bg="lightgrey")
    armorLabel.grid(row=0, column=0, padx=10, pady=10)
    armorList = tk.Listbox(armorFrame, height=30, width=30)
    armorList.grid(row=1, column=0, padx=10, pady=10)
    #To track dissabled mods
    armorDict = {}
    for armor in resistances.RESISTANCES:
        armorList.insert(tk.END, armor)

    #buttons
    armorButtonFrame = tk.Frame(armorFrame, bg="lightgrey")
    armorButtonFrame.grid(row=2, column=0, padx=10, pady=10)
    armorSelectAllButton = tk.Button(armorButtonFrame, text="Select All", command= lambda: selectAll(armorList, armorDict))
    armorSelectAllButton.grid(row=0, column=0, padx=10, pady=10)
    armorDeselectAllButton = tk.Button(armorButtonFrame, text="Deselect All", command= lambda: deselectAll(armorList, armorDict))
    armorDeselectAllButton.grid(row=0, column=1, padx=10, pady=10)

    selectAll(armorList, armorDict)
    armorList.bind('<<ListboxSelect>>', onselect)

    #armorEntryBox
    armorEntryFrame = tk.Frame(armorFrame, bg="lightgrey")
    armorEntryFrame.grid(row=3, column=0, padx=10, pady=10)
    armorEntryLabel = tk.Label(armorEntryFrame, text="Target Armor", font=("Arial", 12), bg="lightgrey")
    armorEntryLabel.grid(row=0, column=0, padx=10, pady=10)
    vcmd = (window.register(lambda P: P.isdigit() or P == ""), '%P')
    armorEntry = tk.Entry(armorEntryFrame, width=10, bg="lightgrey", validate="all", validatecommand=(vcmd))
    armorEntry.grid(row=1, column=0, padx=10, pady=10)
    armorEntry.insert(0, "300")

    #Gun Stats Column
    from PIL import Image, ImageTk
    gunStatsFrame = tk.Frame(window, bg="lightgrey")
    gunStatsFrame.grid(row=0, column=3, padx=10, pady=10)
    gunCanvas = tk.Canvas(gunStatsFrame, bg="lightgrey", width=200, height=200)
    gunCanvas.grid(row=0, column=0, padx=10, pady=10)
    img = Image.open(selectedGun.imageName)
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    #img = tk.PhotoImage(file="gunImages/Amprex.png")
    gunCanvas.create_image(0, 0, anchor="nw", image=img)
    gunCanvas.image = img


    #Weapon Stats
    weaponStatsFrame = tk.Frame(gunStatsFrame, bg="lightgrey")
    weaponStatsFrame.grid(row=1, column=0, padx=10, pady=10)
    weaponStatsLabel = tk.Label(weaponStatsFrame, text="Weapon Stats", font=("Arial", 12), bg="lightgrey")
    weaponStatsLabel.grid(row=0, column=0, padx=10, pady=10)
    weaponStatsLabel.config(text=selectedGun.GetStats())

    def UpdateGunStats():
        weaponStatsLabel.config(text=selectedGun.GetStats())

    def onGunSelect(evt):
        nonlocal selectedGun
        nonlocal img
        selectedGun = weapons[gunList.curselection()[0]]
        img = Image.open(selectedGun.imageName)
        img = img.resize((200, 200), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        gunCanvas.create_image(0, 0, anchor="nw", image=img)
        gunCanvas.image = img
        UpdateGunStats()
    
    gunList.bind('<<ListboxSelect>>', onGunSelect)
    
    window.mainloop()


if __name__ == '__main__':

    #TestZone()
    #openUI()
    #sequencialTest()
    evolutionTest()
            

                


            