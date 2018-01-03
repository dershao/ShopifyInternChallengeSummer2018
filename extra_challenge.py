import json, requests

URL = 'https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=2&page='

#root menus - contains no parent nodes
root_menus = []

#leaf menus - contains no child nodes
leaf_menus = []

#cycle menus -  contains a child node that refers to a root node
cycle_menus = []

#dictionary of all menus accessible by id
all_menus = {}

#list of all valid menus with their root ids and child ids
valid_menus = []

#list of all invalid menus with their root ids and child ids
invalid_menus = []

    
def requestApiEndpoint(page):
    res = requests.get(URL + str(page))
    res.raise_for_status()
    return res

def getNumberOfPages(jsonRes):
    totalPages = jsonRes['pagination']['total']
    per_page = jsonRes['pagination']['per_page']
    return (totalPages // per_page) + int(totalPages % per_page != 0)

def findAllRootIds(menus):
    for key, value in menus.items():
        #if the menu does not contain a parent_id key, it is a root menu
        if 'parent_id' not in value:
            root_menus.append(value['id'])        

def findAllLeafMenus(menus):
    for key, value in menus.items():
        #if the menu does not have child menus, it is a 'leaf' menu
        if (len (value['child_ids']) is 0 ):
            leaf_menus.append(value)

def findAllChildAsRootMenus(menus):
    for key, value in menus.items():
        for child_id in value['child_ids']:
            if (child_id in root_menus):
                cycle_menus.append(value)

def menuValidation():

    #converts the first challegen API JSON response into string
    challenge1 = requestApiEndpoint(1).text

    #converts the JSON response string into Python dictionary
    challenge1Dict = json.loads(challenge1)

    #get number of page
    numberOfPages = getNumberOfPages(challenge1Dict)
    print("Response contains " + str(numberOfPages) + " number of pages.")


    #put all menus into dictionary with key as their id and value as the menu
    for i in range(1, numberOfPages + 1):
        for menu in challenge1Dict['menus']:
                all_menus[menu['id']] = menu
    
        #loads next page of menus
        challenge1Dict = json.loads(requestApiEndpoint(i+1).text)

    findAllRootIds(all_menus)
    findAllLeafMenus(all_menus)
    findAllChildAsRootMenus(all_menus)
        
    for leaf_menu in leaf_menus:
        parent_id = 0
        current_menu = leaf_menu
        path = []
        while (parent_id not in root_menus):
            parent_id = current_menu['parent_id']
            path.append(current_menu['id'])
            current_menu = all_menus[parent_id]
            
        path.reverse()
        valid_menus.append( {"root_id": parent_id, "children": path} )

    for cycle_menu in cycle_menus:
        parent_id = 0
        current_menu = cycle_menu
        path = []
        while (parent_id not in root_menus):
            parent_id = current_menu['parent_id']
            path.append(current_menu['id'])
            current_menu = all_menus[parent_id]
            
        path.reverse()
        invalid_menus.append( {"root_id": parent_id, "children": path} )

    return {"valid_menus" : valid_menus, "invalid_menus"  : invalid_menus}
    
def main():
    output = json.dumps(menuValidation(), indent=4)
    print(output)


if __name__ == "__main__":
    main()
    
