from glob import glob
from tqdm import tqdm
from re import findall, DOTALL

fils = glob(".\\Randland_ORG\\*.md")

exclude_tags = ["Aes Sedai factions",
"Aes Sedai positions",
"Articles to be expanded",
"Chapter disambiguations",
"Chapter summaries crown of swords",
"Character not mentioned in books",
"Characters named after fans",
"Characters only mentioned in the Companion",
"Characters only mentioned in the RPG",
"Characters original to the video game",
"Characters with customized ewot links",
"Characters with default ewot links",
"Unknown Ajah",
"Unknown clan",
"Unknown gender",
"Unknown nationality",
"Unknown occupation",
"Unknown sept",
"Unknown society",
"Unknown status",
"Updates needed",
"Other Media",
"Other animals",
"Other features",
"Other non-humans",
"Other notable buildings",
"Pages using ISBN magic links",
"Pages with reference errors",
"featured","POV chara","Notes needed",
"Shortpages","Stubs","Unknownnationality","Characterswithcustomizedewotlinks","Characterswithdefaultewotlinks",
"Citationneeded","Unknownsept",]

tag_dic = {}

for each_file in tqdm(fils):

    # Read file
    with open(each_file, "r", encoding="utf-8") as f:
        cont = f.read()

    # Find tag matches
    mac = findall(r"---\ntags:.*?---", cont, DOTALL)

    # If there are tags
    if mac != []:

        # Get tags
        old_tags = findall(r"\[.*?\]", mac[0])[0].replace("[","").replace("]","")

        # Split to list
        tagss = old_tags.split(", ")

        # Filter, convert to Obsidian format and join
        new_tags = []
        for each_tag in tagss:
            if each_tag not in exclude_tags:
                new_tags.append(each_tag.replace(" ","").replace("(","_").replace(")","").replace("'",""))
        new_tags = "[" + ", ".join(new_tags) + "]"

        # Replace old tags with new tags
        cont = cont.replace("[" + old_tags + "]", new_tags)

        # Add to dictionary
        for i in [x.replace(" ","").replace("(","_").replace(")","").replace("'","") if x not in exclude_tags else "" for x in tagss]:
            try:
                tag_dic[i] += 1
            except:
                tag_dic[i] = 1

    # Write file
    with open(each_file.replace("\\Randland_ORG","\\Randland"), "w+", encoding="utf-8") as f:
        f.write(cont)

    # Write tag list
    with open("tags.txt", "w", encoding="utf-8") as tags_file:

        # Convert dic to descending list
        tag_list = sorted(tag_dic.items(), key=lambda x: x[1], reverse=True)

        # Write tags to file
        for i in tag_list:
            tags_file.write(i[0] + "\t" + str(i[1]) + "\n")
