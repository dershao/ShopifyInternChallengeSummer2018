# ShopifyInternChallengeSummer2018

## EDIT
I didn't make it.

## Introduction

Shopify Backend challenge using Python. 

Modules used: 

- json: used to convert between JSON and Python dictionaries
- requests: used to retrieve API response

## Original Thought

The original solution was a naive approach. The steps were to find all root menus (i.e., menus without a parent menu) and recursively record the path by traveling from a root menu to their children menus. If the path reaches a menu without a child menu, it is a valid menu. If the path returns to a root menu, the menu is invalid.

## Better Solution

The issue with the original solution was there were too many method calls due to recursion which makes it very inefficient. 
Also, a menu could have multiple children menus and it is unpredictable when that would occur. 

The current solution has the same principle of finding root menus and identifying whether a menu is valid or invalid.
However, instead of travelling from a root menu, this solution would travel from the last menu back to the root menu. In this method, it is no longer required to choose which path to take since each menu can only have one parent menu. 

## Sample Program output
```
>>>python3 menu_validation.py
Response contains 3 pages.
{
    "invalid_menus": [
        {
            "root_id": 1,
            "children": [
                3,
                7,
                15
            ]
        }
    ],
    "valid_menus": [
        {
            "root_id": 2,
            "children": [
                4
            ]
        },
        {
            "root_id": 2,
            "children": [
                5,
                6
            ]
        },
        {
            "root_id": 2,
            "children": [
                8
            ]
        },
        {
            "root_id": 9,
            "children": [
                10
            ]
        },
        {
            "root_id": 9,
            "children": [
                11
            ]
        },
        {
            "root_id": 9,
            "children": [
                12,
                13
            ]
        },
        {
            "root_id": 9,
            "children": [
                12,
                14
            ]
        }
    ]
}
```

## Conclusion

It was a fun and fulfilling problem to solve. Thank you for reading!
