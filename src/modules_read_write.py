from path import path
import json
PATH_current = path('seed.txt').abspath()
PATH_Package = "/".join(PATH_current.split('/')[:-2])

def load_index():
    text_file = open("seed.txt", "r")
    seed_links = text_file.readlines()
    return seed_links

def write_stories_txt(data_store):
    print "writing stories to files.."
    count = 1
    for key in data_store:
        with open(PATH_Package + "/data/Stories/UVCS_stories/" + str(count) + "_" + data_store[key]['title'] + ".txt", 'wt') as fp:
            fp.write(data_store[key]['story'].encode("utf-8"))
            fp.close()
            count+=1
    print count, "files written properly.."

def write_to_file_json(data):
    print "dumping info to JSON files.."
    with open(PATH_Package+"/data/Files_JSON/" + "DeKO_UVCS.json", 'wt') as fp:
        json.dump(data, fp, indent=2, encoding = "utf-8")
    print "dumped successfully.."



