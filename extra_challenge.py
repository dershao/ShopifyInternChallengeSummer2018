import json, requests

#This file is the exact same as the original 'menu_validation.py' file but with a different URL. 

URL = 'https://backend-challenge-summer-2018.herokuapp.com/challenges.json?id=2&page='

#root menus - contains no parent menus
root_menus = []

#leaf menus - contains no child menus
leaf_menus = []

#cycle menus -  contains a child menu that is a root menu
cycle_menus = []

#dictionary of all menus accessible by their respective ids
all_menus = {}

#list of all valid menus with their root ids and child ids
valid_menus = []

#list of all invalid menus with their root ids and child ids
invalid_menus = []
    
def requestApiEndpoint(page):
    """Make request for JSON response with specified page number.

    page -- the page number desired
    """
    res = requests.get(URL + str(page))
    res.raise_for_status()
    return res

def getNumberOfPages(jsonRes):
    """Calculate the total number of pages of the JSON response.
    
    jsonRes -- the API endpoint response
    """
    totalPages = jsonRes['pagination']['total']
    per_page = jsonRes['pagination']['per_page']
    return (totalPages // per_page) + int(totalPages % per_page != 0)

def classifyMenus(menus):
    """Classify each menu as a root, leaf or cycle menu.

    menus -- list of all menus available
    """
    for key, value in menus.items():
        if 'parent_id' not in value:
            root_menus.append(value['id'])
        elif ( len(value['child_ids']) is 0):
            leaf_menus.append(value)
        else:
            for child_id in value['child_ids']:
                if (child_id in root_menus):
                    cycle_menus.append(value)

def menuValidation():

    #converts the first challegen API JSON response into string
    jsonResponse = requestApiEndpoint(1).text

    #converts the JSON response string into Python dictionary
    jsonResponseDict = json.loads(jsonResponse)

    #get number of page
    numberOfPages = getNumberOfPages(jsonResponseDict)
    print("Response contains " + str(numberOfPages) + " pages.")


    #put all menus into dictionary with key as their id and value as the menu
    for i in range(1, numberOfPages + 1):
        for menu in jsonResponseDict['menus']:
                all_menus[menu['id']] = menu
    
        #loads next page of menus
        jsonResponseDict = json.loads(requestApiEndpoint(i+1).text)

    classifyMenus(all_menus)
       
    for leaf_menu in leaf_menus:

        parent_id = 0
        current_menu = leaf_menu
        path = []

        #from each last menu, record the path taken until the root menu is reached
        while (parent_id not in root_menus):
            
            #find the parent id of the current menu
            parent_id = current_menu['parent_id']

            #record the current menu to the path
            path.append(current_menu['id'])

            #parent menu is now the current menu
            current_menu = all_menus[parent_id]

        #since we're going from last menu to root menu: need to reverse the path    
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
    