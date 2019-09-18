from tempfile import mkstemp
from shutil import move
from os import fdopen, remove, path, stat, mkdir
import shutil, urllib, json, re

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def get_current_version(file_path):
    with open(file_path) as file:
        for line in file:
            version = re.search(r'(\*\s*version:\s*)([\d\.*]+)', line, re.IGNORECASE)
            if version is not None:
                return version.groups()[1]
    return False

def create_product_file( **options ):
    dir_name = options.get('dir_name')
    plugin_config = options.get('plugin_config')
    current_app_id = options.get('current_app_id')
    new_app_id = options.get('new_app_id')
    sites = options.get('sites')
    type = options.get('type')
    current_version = options.get('version')
    print '%s-%s' % (current_version, type)

    replace(plugin_config, current_app_id, new_app_id)
    plugin_name = "%s_%s_%s(%s)" % (path.basename(dir_name), current_version, sites, type)
    shutil.make_archive('%s/%s/%s' % (type, sites, plugin_name), 'zip', dir_name)

def load_json_by_url( url ):
    response = urllib.urlopen(url)
    return json.loads(response.read())

def make_zip_sites( config_url, plugin_detail, project_dir ):
    config_obj = load_json_by_url( config_url )
    plugin_detail_obj = load_json_by_url( plugin_detail )
    version = plugin_detail_obj['version']
    plugin_config = path.join( project_dir, config_obj["file_config"])
    current_pid = config_obj['current_pid']
    types = config_obj['types']

    for val in config_obj["products"]:
        type = types[val['type']]['slug']
        create_product_file( 
            dir_name = project_dir, 
            plugin_config = plugin_config,
            current_app_id = current_pid,
            new_app_id = val['pid'],
            sites = val['slug'],
            version = version,
            type = type
        )
        current_pid = val['pid']