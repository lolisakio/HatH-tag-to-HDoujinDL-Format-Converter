import os 
import json
filename='HaH/galleryinfo1.txt'
with open(filename) as f:
    raw_txt = f.read().splitlines() # Delete /n character


mod_txt = []
for i in range(0,len(raw_txt)): #Scan First Element to End
    if raw_txt[i] != '' : # Remove Blank Line
        mod_txt.append(raw_txt[i])

Comment_str_raw = [] # Will Be Description
Tags_list_raw = [] # Will Be Tags Bulk
Title_str = "" # Will Be Title
for i in range(0,len(raw_txt)): #Scan First Element to End
    
    if   raw_txt[i][0:5] =='Title': # Title Extract [str]
        Title_str = raw_txt[i][5+8:]
    elif raw_txt[i][0:4] =='Tags' : # Tags(Includs group, parody, language, artist, other) Bulk Extract [list]
        Tags_list_raw  = raw_txt[i][4+9:].split(', ')
    elif raw_txt[i][0:20]=="Uploader's Comments:" : #Comment Extract [str]
        Comment_str_raw = raw_txt[i+1:]
        
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
file_path = "blank.json" # 수정하기
with open(file_path + '', encoding='utf-8') as blankjsonfile:
    blankjson = json.load(blankjsonfile)
    print(blankjson)

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
#characters   = 
#series       = 
parody       = parody_Tag_list
#url          =

#manga_info  =blankjson['manga_info'] # 망가정보 전체 
blankjson['manga_info']['original_title'] = title      # 망가 정보 
blankjson['manga_info']['artist'] = artist             # artist
blankjson['manga_info']['circle'] = circle             # group -> circle
blankjson['manga_info']['description'] = description
#pages       =blankjson['manga_info']['pages'] # 저자
#tags_all    =blankjson['manga_info']['tags'] #태그전체
blankjson['manga_info']['tags']['female'] = tag_female # female 태그
blankjson['manga_info']['tags']['male'] = tag_male     # male  태그 
blankjson['manga_info']['tags']['misc'] = tag_misc       # other -> misc
blankjson['manga_info']['language'] = language
blankjson['manga_info']['parody'] = parody

#tag_type    =blankjson['manga_info']['type'] # parody? 
#tag_url     =blankjson['manga_info']['url'] #
with open("info.json", 'w') as outfile:
    json.dump(blankjson, outfile, indent=4)
