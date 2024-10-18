import json
import os

# records = [
#     { "date" : "2024-08-20-12-23", "item_name" : "Pizza", "category" : "Food", "price" : 600 },
#     { "date" : "2024-08-21-13-54", "item_name" : "PS5", "category" : "Entertainment", "price" : 17580 },
#     { "date" : "2024-08-22-19-07", "item_name" : "T-shirt", "category" : "Clothing", "price" : 300 }
# ]

# categories = [ 'Food', 'Clothing', 'Home', 'Entertainment', 'Tax' ]

# data = {
#     "records": records,
#     "categories": categories
# }

# 文件路徑
FILE_PATH = "./record/data.json"

# 讀取紀錄
def load_records() :
    try :
        if os.stat( FILE_PATH ).st_size == 0 :
            return { "records" : [], "categories" : [] }  # 如果文件是空的，初始化为一个空字典
        else :
            with open( FILE_PATH, 'r' ) as json_file :
                data = json.load( json_file )
                return data[ "records" ]
    except :
        print( "load records error" )
        return [ "load records error" ]
        
# 保存紀錄
def add_record( record ):
    try :
        if os.stat( FILE_PATH ).st_size == 0 :
            data = { "records" : [], "categories" : [] }  # 如果文件是空的，初始化为一个空字典
        else :
            with open( FILE_PATH, 'r' ) as json_file :
                data = json.load( json_file )

        data[ "records" ].append( record )
        data[ "records" ].sort( key = lambda x : x["date"], reverse = True )

        with open( FILE_PATH, 'w' ) as json_file :
            json.dump( data, json_file, indent = 4 )
    except :
        print( "add record error" )
        return [ "add records error" ]

# 刪除一個紀錄
def delete_record( index ):
    try :
        with open( FILE_PATH, 'r' ) as json_file :
            data = json.load( json_file )
        
        del data[ "records" ][ index ]

        with open( FILE_PATH, 'w' ) as json_file :
            json.dump( data, json_file, indent = 4 )
    except :
        print( "delete records error" )
        return [ "delete records error" ]

def edit_record( index, record ) :
    try :
        with open( FILE_PATH, 'r' ) as json_file :
            data = json.load( json_file )
        
        data[ "records" ][ index ] = record

        with open( FILE_PATH, 'w' ) as json_file :
            json.dump( data, json_file, indent = 4 )
    except :
        print( "delete records error" )
        return [ "delete records error" ]

# 讀取分類
def load_categories() :
    try :
        if os.stat( FILE_PATH ).st_size == 0 :
            data = { "records" : [], "categories" : [] }  # 如果文件是空的，初始化为一个空字典
        else :
            with open( FILE_PATH, 'r' ) as json_file :
                data = json.load( json_file )
                return data[ "categories" ]
    except :
        print( "load categories error" )
        return [ "load categories error" ]

# 保存分類
def save_categories( categories ):
    try :
        if os.stat( FILE_PATH ).st_size == 0 :
            data = { "records" : [], "categories" : [] }  # 如果文件是空的，初始化为一个空字典
        else :
            with open( FILE_PATH, 'r' ) as json_file :
                data = json.load( json_file )
            
            data[ "categories" ] = categories
            data[ "categories" ].sort()

            with open( FILE_PATH, 'w' ) as json_file :
                json.dump( data, json_file, indent = 4 )
    except :
        print( "save categories error" )
        return [ "save categories error" ]