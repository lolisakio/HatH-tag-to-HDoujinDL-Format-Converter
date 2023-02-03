import os 
import json


## 기본경로, 수정해주기! 
baseDir = 'WORK/download/'


targetDir_List = os.listdir(baseDir) # ALl Folders name to list 
for targetDirectory_index in range(0,len(targetDir_List)): # Loop For ALl SubDir
    targetDirectory = targetDir_List[targetDirectory_index] # Indexnumber To Dir Name
    converted_Obj_Json = HatHConvHDoujinDL_JSON(baseDir, targetDirectory) # Covert Tag ANd Export json
    
    exportFilename = baseDir + targetDirectory + '/info.json' #Set Export info.json Directory
    with open(exportFilename, 'w', encoding='utf-8') as exportConverted: # Open json with utf-8 
        json.dump(converted_Obj_Json, exportConverted, indent=4, ensure_ascii=False) #Prevent Char Crash With ensure_ascii=false

## 함수의 정의
## IN :  baseDir , targetDir 
## OUT : json 구조체
## 함수화 시작할곳? 
def HatHConvHDoujinDL_JSON(baseDir, targetDir):

    filename =  baseDir + targetDir + '/galleryinfo.txt'

    gallery_num = filedir.split(' ')[-1][1:-1] # Split FileDir to list
    url_str = 'https://hitomi.la/galleries/' + gallery_num + '.html' # Extract gallerynum and convert to hitomi.la address 

    ## txt 파일 태그 열기 
    with open(filename) as f:
        raw_txt = f.read().splitlines() # Delete /n character
    mod_txt = []
    for i in range(0,len(raw_txt)): #Scan First Element to End
        if raw_txt[i] != '' : # Remove Blank Line
            mod_txt.append(raw_txt[i])

    Comment_str_raw = [] # Will Be Description
    Tags_list_raw = [] # Will Be Tags Bulk
    Title_str = "" # Will Be Title
    Upload_time_str = "" # Will Be released

    for i in range(0,len(raw_txt)): #Scan First Element to End

        if   raw_txt[i][0:5] =='Title': # Title Extract [str]
            Title_str = raw_txt[i][5+8:]
        elif raw_txt[i][0:4] =='Tags' : # Tags(Includs group, parody, language, artist, other) Bulk Extract [list]
            Tags_list_raw  = raw_txt[i][4+9:].split(', ')
        elif raw_txt[i][0:20]=="Uploader's Comments:" : #Comment Extract [str]
            Comment_str_raw = raw_txt[i+1:]
        elif raw_txt[i][0:12]=="Upload Time:": # Upload Time Extract
            Upload_time_str = raw_txt[i][13:]
    #Comment 비어있을시 처리
    if Comment_str_raw == []:
        Comment_str_strip = raw_txt[-1]
    else:     
        Comment_str_strip = '' # Comment(@json -> Description) Extract [str]
        for i in range(0,len(Comment_str_raw)): #Scan First Element to End
            if Comment_str_raw[i] != '':
                Comment_str_strip = Comment_str_strip + Comment_str_raw[i] + ' \n '

    # comment 쌍따옴표 제거 -> 홑따옴표로 변환
    Comment_str_strip = Comment_str_strip.replace('"',"'")

    language_Tag_list = [] # Will Be language
    parody_Tag_list = [] # Will Be Parody
    group_Tag_list = [] # Will be Circle
    artist_Tag_list = [] # Will Be Artist 
    male_Tag_list = [] # Will Be tag_male 
    female_Tag_list = [] # Will Be tag_female
    other_Tag_list = [] # Will Be tag_misc

    for i in range(0,len(Tags_list_raw)):
        if   Tags_list_raw[i][0:9] =='language:':
            if language_Tag_list == []:
                language_Tag_list.append(Tags_list_raw[i][9:])
        elif Tags_list_raw[i][0:7] =='parody:': 
                parody_Tag_list.append(Tags_list_raw[i][7:])
        elif Tags_list_raw[i][0:6] =='group:':
                group_Tag_list.append(Tags_list_raw[i][6:])
        elif Tags_list_raw[i][0:7] =='artist:': 
                artist_Tag_list.append(Tags_list_raw[i][7:])  
        elif Tags_list_raw[i][0:5] =='male:': 
                male_Tag_list.append(Tags_list_raw[i][5:])
        elif Tags_list_raw[i][0:7] =='female:': 
                female_Tag_list.append(Tags_list_raw[i][7:])
        elif Tags_list_raw[i][0:6] =='other:': 
                other_Tag_list.append(Tags_list_raw[i][6:])

    ## JSON 파일 작업 시작

        # Replaced By Below Mod
        #file_path = "blank.json" # Import From File
        #with open(file_path + '', encoding='utf-8') as blankjsonfile:
        #    blankjson = json.load(blankjsonfile)
        #    print(blankjson)

    # import blank info.json structure
    info_blank_str = '''{
      "manga_info": {
        "title": "",
        "original_title": "",
        "author": [],
        "artist": [],
        "circle": [],
        "scanlator": [],
        "translator": [],
        "publisher": "",
        "description": "",
        "status": "",
        "chapters": null,
        "pages": "",
        "tags": {
          "female": [],
          "male": [],
          "misc": []
        },
        "type": "",
        "language": [],
        "released": "",
        "characters": [],
        "series": "",
        "parody": [],
        "url": ""
      }
    }'''

    info_blank_obj = json.loads(info_blank_str)
    blankjson = info_blank_obj
    title        = Title_str
    artist       = artist_Tag_list
    circle       = group_Tag_list
    description  = Comment_str_strip
    #pages        = 
    #tags_all     = 
    tag_female   = female_Tag_list
    tag_male     = male_Tag_list
    tag_misc     = other_Tag_list
    #tag_type     = 
    #tag_url      = 
    language     = language_Tag_list
    released     = Upload_time_str
    #characters   = 
    #series       = 
    parody       = parody_Tag_list
    url          = url_str 

    #manga_info  =blankjson['manga_info'] # 망가정보 전체 
    blankjson['manga_info']['title'] = title      # 망가 정보 
    blankjson['manga_info']['artist'] = artist             # artist
    blankjson['manga_info']['circle'] = circle             # group -> circle
    blankjson['manga_info']['description'] = description
    #pages       =blankjson['manga_info']['pages'] # 저자
    #tags_all    =blankjson['manga_info']['tags'] #태그전체
    blankjson['manga_info']['tags']['female'] = tag_female # female 태그
    blankjson['manga_info']['tags']['male'] = tag_male     # male  태그 
    blankjson['manga_info']['tags']['misc'] = tag_misc       # other -> misc
    blankjson['manga_info']['language'] = language
    blankjson['manga_info']['released'] = released
    blankjson['manga_info']['parody'] = parody

    #tag_type    =blankjson['manga_info']['type'] # parody? 
    blankjson['manga_info']['url'] = url  # Gallery Number From Filedir to hitomi.la  url            
    return blankjson
    ## 함수끝 json 내보내줌 

blank1= HatHConvHDoujinDL_JSON(baseDir,targetDir)
