import os.path
import json
import re
from os import path
IMAGE_PATTERN = '!\\[[^\\]]*\\]\\((.*?)\\s*("(?:.*[^"])")?\\s*\\)'

def build(site):
    print("started building config for "+ site)

    site_path = path.join(path.realpath('sites'), site)
    ## check if the site exists if not interrupt the program
    if not path.isdir(site_path):
        print("please make sure that there is a directory name", site, "under sites folder")
        raise FileNotFoundError
    ## iterate the file and create a deploy file: Good place to inject JSON SCHEMA checks for catalog builder
    ## load camera json into an object
    print("DEBUG: config_template")

    with open(path.join(site_path, "config_template.json")) as json_file:
        site_config = json.load(json_file)

    print("DEBUG: sub_modules")
    catalog_groups = []
    ## iterate the modules and load the groups 
    sub_modules = [f for f in os.scandir(site_path) if f.is_dir()]
    for sub_module in sub_modules:
        print("DEBUG: sub_module", sub_module)
        try:
            catalog_groups.append(load_sub_module(site, sub_module.path, sub_module.name))
        except FileNotFoundError:
            print("No valid config found. Skipping: ", sub_module)
    print("DEBUG: sub_modules loaded")

    catalog_groups = sorted(catalog_groups, key=lambda k: k['order']) 
    print("DEBUG: sub_modules sorted")

    site_config["catalog"] = catalog_groups
    ## if config exists delete is 

    print("DEBUG: write config")
    config_prod_mini=json.dumps(site_config, separators=(',', ':'))

    if path.isfile(path.join(site_path,'config.json')):
        os.remove(path.join(site_path,'config.json'))
    with open(path.join(site_path,'config.json'), 'w') as json_file:
        json_file.write(config_prod_mini)
    print("finished building config for "+ site)

def load_sub_module(site, sub_module_path, sub_module_name):


    with open(path.join(sub_module_path, "catalog_group.json")) as json_file:
        catalog_group = json.load(json_file)
    group_description = catalog_group["description"]
    if path.isfile(path.join(sub_module_path, group_description)):
        catalog_group["description"] = process_markdown_file(site ,sub_module_path, group_description, sub_module_name)  
    new_catalog_group_items=visit_items_in_catalog(site, sub_module_name, sub_module_path, catalog_group['items'])
    catalog_group['items'] = new_catalog_group_items
    
    return catalog_group
 

def visit_items_in_catalog(site, sub_module_name, sub_module_path, catalog_group_items):
    new_catalog_group_items = []
    for catalog_item in catalog_group_items:
        if catalog_item['type'] == 'group':
            visit_items_in_catalog(site, sub_module_name, sub_module_path ,catalog_item['items'])
        #otherwise the item is not a group
        #if all items are not groups the load the items 
        data = process_catalog_group(site, sub_module_path, catalog_item, sub_module_name)
        new_catalog_group_items.append(data)
    return new_catalog_group_items

def process_markdown_file(site_name, sub_module_path, group_description, sub_module_name):
    markdown_file_path = path.join(sub_module_path, group_description)
    string = """{}""".format(open(markdown_file_path).read())
    new_strings_array = []
    for line in string.splitlines():
        is_image = re.match(IMAGE_PATTERN, line)
        if is_image and path.isfile(path.join(sub_module_path, is_image.group(1))):
            new = path.join('https://data.apps.fao.org/static/sites', site_name, sub_module_name, is_image.group(1))
            line = line.replace(is_image.group(1), new)
            new_strings_array.append(line)
        else:
            new_strings_array.append(line)
    string = '\n'.join(new_strings_array)
    return string

def process_catalog_group(site_name ,sub_module_path, catalog_item, sub_module_name):
    if catalog_item["type"] == "csw" and "getRecordsTemplate" in catalog_item:
        catalog_item = get_csw_filter(sub_module_path, catalog_item)
    for _key in catalog_item:
        if isinstance(catalog_item[_key], str) and path.isfile(path.join(sub_module_path, catalog_item[_key])):
            catalog_item[_key] = path.join('https://data.apps.fao.org/static/sites',site_name, sub_module_name , catalog_item[_key])
    return catalog_item
            
def get_csw_filter(sub_module_path, catalog_item):
    xml_file_path = path.join(sub_module_path, catalog_item["getRecordsTemplate"])
    if path.isfile(xml_file_path):
        ##take the entries and return gther catalog item
        contents = open(xml_file_path).read()
        catalog_item["getRecordsTemplate"]=str(contents)
    return catalog_item
