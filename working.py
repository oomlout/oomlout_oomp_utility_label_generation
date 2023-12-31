import os
import yaml
import glob
import copy
import jinja2    


folder_configuration = "configuration"
#add this files current loaction to the folder
folder_configuration = os.path.join(os.path.dirname(__file__), folder_configuration)
file_configuration = os.path.join(folder_configuration, "configuration.yaml")
#import templates
with open(file_configuration, 'r') as stream:
    try:
        configuration = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:   
        print(exc)

    


for item_details in configuration:
    item = item_details["file_template"]
    item_details["file_template_absolute"] = os.path.join(os.path.dirname(__file__), item)
    




def main(**kwargs):
    
    
    folder = kwargs.get("folder", f"os.path.dirname(__file__)/parts")
    folder = folder.replace("\\","/")
    
    kwargs["file_template_list"] = configuration
    print(f"oomlout_oomp_utility_label_generation for folder: {folder}")
    create_recursive(**kwargs)
    
def create_recursive(**kwargs):
    folder = kwargs.get("folder", os.path.dirname(__file__))
    kwargs["folder"] = folder
    folder_template_absolute = kwargs.get("folder_template_absolute", "")
    kwargs["folder_template_absolute"] = folder_template_absolute
    filter = kwargs.get("filter", "")
    count = 0
    for item in os.listdir(folder):
        if filter in item:
            item_absolute = os.path.join(folder, item)
            if os.path.isdir(item_absolute):
                #if working.yaml exists in the folder
                if os.path.exists(os.path.join(item_absolute, "working.yaml")):
                    kwargs["directory"] = item_absolute
                    create(**kwargs)
                    count += 1
                    if count % 100 == 0:
                        print(f"count: {count}")

def create(**kwargs):
    directory = kwargs.get("directory", os.getcwd())    
    kwargs["directory"] = directory
    file_template_list = kwargs.get("file_template_list", configuration)
    kwargs["file_template_list"] = file_template_list
    generate_label_generic(**kwargs)
    

def generate_label_generic(**kwargs):
    import os
    directory = kwargs.get("directory",os.getcwd())    
    file_template_list = kwargs.get("file_template_list", configuration)
    
    


    for file_template_details in file_template_list:
        file_template = file_template_details["file_template_absolute"]
        file_output = f"{file_template_details['file_output']}.svg"
        file_output = os.path.join(directory, file_output)
        #      yaml part
        file_yaml = f"{directory}/working.yaml"
        details = {}
        if os.path.exists(file_yaml):
            with open(file_yaml, 'r') as stream:
                try:
                    details = yaml.load(stream, Loader=yaml.FullLoader)
                except yaml.YAMLError as exc:   
                    print(exc)
        test_attribute = file_template_details.get("test_attribute", "")
        if details != None:
            if test_attribute == "" or test_attribute in details:
                    
                #      file part
                files = []    
                #get a list of recursive files
                files = glob.glob(f"{directory}/**/*.*", recursive=True)
                #replace all \\ with /
                for i in range(len(files)):
                    files[i] = files[i].replace("\\","/")
                #remove the directory from the file name
                directory = directory.replace("\\","/")
                for i in range(len(files)):
                    files[i] = files[i].replace(f"{directory}/","")    
                files2 = copy.deepcopy(files)
                details["files"] = files2

                file_template = file_template
                file_output = file_output
                dict_data = details
                get_jinja2_template(file_template=file_template,file_output=file_output,dict_data=dict_data)

def get_jinja2_template(**kwargs):
    file_template = kwargs.get("file_template","")
    file_output = kwargs.get("file_output","")
    dict_data = kwargs.get("dict_data",{})

    markdown_string = ""
    #if running in windows
    if os.name == "nt":
        file_template = file_template.replace("/", "\\")
    else:
        file_template = file_template.replace("\\", "/")
    with open(file_template, "r") as infile:
        markdown_string = infile.read()
    data2 = copy.deepcopy(dict_data)


    try:
        markdown_string = jinja2.Template(markdown_string).render(p=data2)
    except Exception as e:
        print(f"error in jinja2 template: {file_template}")        
        print(f".")
        print(f".")
        print(f".")
        print(f".")
        print(e)
        markdown_string = f"markdown_string_error\n{e}"
    #make directory if it doesn't exist
    directory = os.path.dirname(file_output)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(file_output, "w", encoding="utf-8") as outfile:
        outfile.write(markdown_string)
        #print(f"jinja2 template file written: {file_output}")
        #delete pdf version if it exists
        file_output_pdf = file_output.replace(".svg",".pdf")
        if os.path.exists(file_output_pdf):
            os.remove(file_output_pdf)
            #print(f"pdf file deleted: {file_output_pdf}")

if __name__ == '__main__':
    #folder is the path it was launched from
    
    kwargs = {}
    folder = os.path.dirname(__file__)
    #folder = "C:/gh/oomlout_oomp_builder/parts"
    #folder = "C:/gh/oomlout_oomp_part_generation_version_1/parts"
    kwargs["folder"] = folder
    main(**kwargs)