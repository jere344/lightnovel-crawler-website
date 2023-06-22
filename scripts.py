
# region test json

# from pathlib import Path
# import shutil

# folder = Path("Lightnovels")

# for novel in folder.iterdir():
#     if novel.is_dir():
#         for source in novel.iterdir():
#             has_json_folder = False
#             if source.is_dir() :
#                 for content in source.iterdir():
#                     if content.is_dir() and content.name == "json":
#                         has_json_folder = True
#                         break
#                 if not has_json_folder:
#                     print("Deleting " + str(source))
#                     shutil.rmtree(source)

# for novel in folder.iterdir():
#     if novel.is_dir():
#         has_sources = False
#         for source in novel.iterdir():
#             if source.is_dir():
#                 has_sources = True
#                 break
#         if not has_sources:
#             print("Deleting " + str(novel))
#             shutil.rmtree(novel)
        
# endregion


# region count sources

# sources = {}
# for novel in Path("Lightnovels").iterdir():
#     if novel.is_dir():
#         for source in novel.iterdir():
#             if source.is_dir():
#                 if source.name not in sources:
#                     sources[source.name] = 0
#                 sources[source.name] += 1

# for source in sorted(sources, key=sources.get, reverse=True):
#     print(source + ": " + str(sources[source]))

# endregion

# region test proxy

# from fp.fp import FreeProxy
# import threading
# import time
# proxy = []
 
# def fetch_proxy():
#     print("Fetching proxy")
#     proxy.append(FreeProxy(rand=True, timeout=1, https=True).get())
#     print("Fetched proxy")

# for i in range(100):
#     threading.Thread(target=fetch_proxy).start()

# with open("proxy.txt", "a") as f:
#     while True:
#         if len(proxy) != 0:
#             f.write(proxy[0] + "\n")
#             proxy.pop(0)
#             print("Wrote proxy")
#         else :
#             time.sleep(1)
#             print("Waiting for proxy")

# with open("proxy.txt", "r") as f:
#     proxy_list = set(f.read().splitlines())

# with open("proxy.txt", "w") as f:
#     for proxy in proxy_list:
#         f.write(proxy + "\n")

# endregion

# region largest source

from pathlib import Path
import os

sources = {}

for novel in Path("Lightnovels").iterdir():
    if novel.is_dir():
        for source in novel.iterdir():
            if source.is_dir():
                # sources[novel.name + "/" + source.name] = shutil.disk_usage(str(source)).total
                sources[novel.name + "/" + source.name] = sum(os.path.getsize(f) for f in source.glob('**/*') if os.path.isfile(f))
        
for source in sorted(sources, key=sources.get, reverse=True):
    print(source + ": " + str(sources[source]))
    
# One Piece/beautymanga-com: 5172581478
# Isekai Maou To Shoukan Shoujo Dorei Majutsu/beautymanga-com: 1696360032
# Solo Leveling/isekaiscan-com: 1451358004
# Solo Leveling/www-mangaread-org: 1444927966
# Welcome To Demon School Iruma Kun/anime-sama-fr: 1402681774
# Sweet Home/freemanga-me: 1298964270
# Chainsaw Man/beautymanga-com: 1172974488
# Magika No Kenshi To Shoukan Maou/beautymanga-com: 945686075
# Jujutsu Kaisen/beautymanga-com: 920049914
# Nidome No Jinsei Wo Isekai De/beautymanga-com: 908453329
# Return Of The Female Knight/beautymanga-com: 881872670
# Beyond The Clouds/mangatoto-net: 813910284
# Youjo Senki/beautymanga-com: 796065583
# The Legendary Mechanic/beautymanga-com: 686253012
# Tensei Shite Inaka De Slowlife Wo Okuritai/beautymanga-com: 556101368
# Trigun Maximum/beautymanga-com: 514347910
# Danganronpa Gaiden Killer Killer/mangatoto-net: 464500707
# Goshujin Sama To Yuku Isekai Survival/beautymanga-com: 405129474
# Touhou Suzunaan Forbidden Scrollery/beautymanga-com: 404850939
# The World Of Otome Games Is Tough For Mobs/freemanga-me: 395212838
# Touhou Suzunaan Forbidden Scrollery/freemanga-me: 394244139
# Asadora/mangabuddy-com: 384776346
# Blame/beautymanga-com: 384356920
# Otome Game No Heroine De Saikyou Survival/beautymanga-com: 373310240
# Made In Abyss/freemanga-me: 362609806
# Lumine/freemanga-me: 350068105
# IM The Evil Lord Of An Intergalactic Empire/beautymanga-com: 343006662
# Akira/myreadingmanga-fit: 332584079
# AcademyS Undercover Professor/aquamanga-com: 331116759
# Little Girl X Scoop X Evil Eye/mangabuddy-com: 330926602
# Sono Mono Nochi Ni Nariie Shinichirou/batotwo-com: 303872020
# Touhou Suichouka Lotus Eater Tachi No Suisei/freemanga-me: 298404166
# Hellsing/freemanga-me: 294277531
# AcademyS Undercover Professor/freemanga-me: 287102548
# Reincarnation Of The Strongest Sword God/beautymanga-com: 281855928
# Otome Game No Heroine De Saikyou Survival/hto-to: 259700338
# Neko No Massajiya San Official/mangatoto-net: 248398201
# Game Loading/comiko-net: 201473898
# Reborn Girl Starting A New Life In Another World A/freemanga-me: 193219114
# Damn Reincarnation/coffeemanga-com: 176118289
# Mairimashita Iruma Kun/comiko-net: 144169312
# Touhou Sangetsusei Visionary Fairies In Shrine/bato-to: 135028433
# Stellar Transformations/batotwo-com: 130631459
# The Frontier Alchemist I CanT Go Back To That Job/isekaiscan-com: 121692221
# Swallowed Star/comiko-net: 117290963
# Botsuraku Youtei Nanode Kajishokunin Wo Mezasu/hto-to: 106000510
# I Got A Cheat Ability In A Different World And In/www-novelupdates-com: 78873470
# Reincarnated As The Mastermind Of The Story/beautymanga-com: 68872362
# Battle Through The Heavens/bestlightnovel-com: 67635349
# The Mech Touch/morenovel-net: 65521648
# The Mech Touch/bestlightnovel-com: 64830438
# Martial Peak/bestlightnovel-com: 64278278
# Hachinan Tte Sore Wa Nai Deshou/comiko-net: 64074182
# Elden Ring Ougonju E No Michi/mangatoto-net: 61461028
# War Sovereign Soaring The Heavens/bestlightnovel-com: 52542780
# Martial God Asura/novelhard-com: 49857083
# Invincible/novelfullplus-com: 47013117
# Versatile Mage/daonovel-com: 46891942
# Chaotic Sword God/bestlightnovel-com: 46690782
# Ancient Strengthening Technique/librarynovel-com: 45278091
# Reverend Insanity/mixednovel-net: 43770247
# Dragon Marked War God/novelfull-com: 43762927
# Spirit Sword Sovereign/www-novelhall-com: 42508847
# Omiai Shitakunakattanode Muri Nandai Na Jouken Wo/bato-to: 41496413
# EmperorS Domination/novelsala-com: 40782307
# A Record Of A MortalS Journey To Immortality/allnovel-org: 40664577
# endregion


# region set all admin to 4


# import pathlib
# import json

# for novel in pathlib.Path("Lightnovels").iterdir():
#     if novel.is_dir():
#         file = novel / "stats.json"
#         if file.exists():
#             try :
#                 with open(file, "r") as f:
#                     stats = json.load(f)
#                     if stats["ratings"] and stats["ratings"]["-6455068401711230225"]:
#                         del stats["ratings"]["-6455068401711230225"]
#                         stats["ratings"]["admin"] = 4
#                 with open(file, "w") as f:
#                     json.dump(stats, f, indent=4)
#                 print("Set " + str(novel) + " to 4")
#             except KeyError:
#                 print("KeyError: " + str(novel))

                    

# endregion


# failed chapters detector / repairer

# import pathlib
# import json
# import random
# with open("success.txt", "r") as f:
#     success = f.read().splitlines()

# for novel in pathlib.Path("Lightnovels").iterdir():
#     if novel.name in success:
#         continue

#     failed = False
#     for source in novel.iterdir():
#         if not source.is_dir():
#             continue
        
#         if not (source / "json").is_dir():
#             print("glitched source: " + str(novel.name + "/" + source.name))
#             failed = True
#             break

#         for chapter in (source / "json").iterdir():
#                 with open(chapter, "r") as f:
#                     if "Failed to download chapter body" in f.read():
#                         # print("Failed: " + str(novel.name + "/" + source.name + "\t" + chapter.name))
                        
#                         if not (source / "meta.json").exists():
#                             print("glitched source: " + str(novel.name + "/" + source.name))
                        
#                         else :
#                             with open(source / "meta.json", "r") as f:
#                                 meta = json.load(f)
#                                 url = meta["novel"]["url"]

#                             print("https://api.lncrawler.monster/addnovel/update?job_id=" + str(random.randrange(1, 10000)) + "&&url=" + url)

#                         failed = True
#                         break
    
#     if not failed:
#         with open("success.txt", "a") as f:
#             f.write(novel.name + "\n")